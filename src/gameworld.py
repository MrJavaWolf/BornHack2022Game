from random import random
import displayio
from imagemanager import ImageManager
from tileanimation import TileAnimation
from gametime import GameTime

DEFAULT_TILE = 52
DEFAULT_TILE_MAP = "/game_data/world_map.csv"
DEFAULT_SPRITE_SHEET = "/game_data/mystic-woods.bmp"
DEFAULT_TILE_PIXEL_WIDTH = 16
DEFAULT_TILE_PIXEL_HEIGHT = 16
ANIMATIONS_WORLD_TILES = [
    {
        "x": 33,
        "y": 1,
        "fps": 0.3,
        "frames": [61, 62, 63],
    },
    {
        "x": 33,
        "y": 2,
        "fps": 0.3,
        "frames": [77, 78, 79],
    },
    {
        "x": 34,
        "y": 1,
        "fps": 0.3,
        "frames": [62, 63, 61],
    },
    {
        "x": 34,
        "y": 2,
        "fps": 0.3,
        "frames": [78, 79, 77],
    },
    {
        "x": 35,
        "y": 1,
        "fps": 0.3,
        "frames": [63, 61, 62],
    },
    {
        "x": 35,
        "y": 2,
        "fps": 0.3,
        "frames": [79, 77, 78],
    },
    {
        "x": 38,
        "y": 1,
        "fps": 0.8,
        "frames": [29, 30, 31],
    },
    {
        "x": 38,
        "y": 2,
        "fps": 0.8,
        "frames": [45, 46, 47],
    },
]

DEFAULT_WALKABLE_TILES = [
    -1,
    8,
    9,
    52,
    53,
    54,
    55,
    18,
    22,
    23,
    24,
    25,
    38,
    128,
    129,
    130,
    75,
    92,
    90,
    74,
    76,
    91,
    106,
    107,
    124,
    123,
    122,
    13,
    14,
    15,
    10,
    11,
]


class GameWorld:
    """Contains the world.
    The world is build from tiles"""

    walkable_tiles = []
    tile_pixel_width: int
    tile_pixel_height: int
    tile_animations = []

    def __init__(
        self,
        image_manager: ImageManager,
        sprite_sheet_file: str = DEFAULT_SPRITE_SHEET,
        tile_map_file: str = DEFAULT_TILE_MAP,
        default_tile: int = DEFAULT_TILE,
        tile_pixel_width: int = DEFAULT_TILE_PIXEL_WIDTH,
        tile_pixel_height: int = DEFAULT_TILE_PIXEL_HEIGHT,
        walkable_tiles=DEFAULT_WALKABLE_TILES,
    ):

        self.sprite_sheet_file = sprite_sheet_file
        self.tile_map_file = tile_map_file
        self.default_tile = default_tile
        self.tile_pixel_width = tile_pixel_width
        self.tile_pixel_height = tile_pixel_height
        self.walkable_tiles = walkable_tiles

        # Reads the size of the tile map
        self.map_width, self.map_height = self.__get_map_size()

        # Sets up the world tile map
        self.bitmap, self.palette = image_manager.get_image(self.sprite_sheet_file)
        self.world_map = displayio.TileGrid(
            bitmap=self.bitmap,
            pixel_shader=self.palette,
            width=self.map_width,
            height=self.map_height,
            tile_width=tile_pixel_width,
            tile_height=tile_pixel_height,
            default_tile=default_tile,
        )
        self.__paint_world_map()

        # Saves it to a group to be easily moved around
        self.sprite = displayio.Group()
        self.sprite.append(self.world_map)
        self.sprite.x = 0
        self.sprite.y = 0

        # Animate world tiles
        self.animated_tiles = []
        for animation in ANIMATIONS_WORLD_TILES:
            tile_animation = TileAnimation(
                "world",
                self.world_map,
                animation["frames"],
                animation["fps"],
                animation["x"] + animation["y"] * self.map_width
            )
            self.animated_tiles.append(tile_animation)

    def __get_map_size(self):
        height = 0
        width = 0
        with open(self.tile_map_file, mode="r") as file:
            for line in file:
                height += 1
                values = line.count(",")
                width = values if values > width else width
                pass
        return width, height

    def __paint_world_map(self):
        with open(self.tile_map_file, mode="r") as file:
            for y, line in enumerate(file):
                for x, value in enumerate(line.split(",")):
                    tile_type, is_int = self.__int_try_parse(value)
                    if is_int and tile_type >= 0:
                        self.world_map[y * self.map_width + x] = tile_type

    def __int_try_parse(self, value):
        try:
            return int(value), True
        except ValueError:
            return value, False

    def is_walkable(self, world_x, world_y):
        """Returns true if the tile at world x, y is walkable, otherwise false"""
        tile_type = self.get_tile_type_at(world_x, world_y)
        return tile_type in self.walkable_tiles

    def get_tile_type_at(self, world_x, world_y):
        """Get the tile type at world x, y. If the x,y is outside of the map it returns -1"""
        tile_x = int(world_x / self.tile_pixel_width)
        tile_y = int(world_y / self.tile_pixel_height)
        lookup_index = tile_y * self.map_width + tile_x
        if lookup_index >= self.map_width * self.map_height:
            return -1
        return self.world_map[lookup_index]

    def change_tile(self, tile_x: int, tile_y: int, to_tile_type: int):
        """Change a tile in the world"""
        lookup_index = tile_y * self.map_width + tile_x
        if lookup_index >= self.map_width * self.map_height:
            return
        self.world_map[lookup_index] = to_tile_type

    def shake(self, amount: float):
        """Shakes the whole world"""
        self.sprite.x = (int)(random() * amount - amount / 2)
        self.sprite.y = (int)(random() * amount - amount / 2)

    def loop(self, game_time: GameTime):
        for animation in self.animated_tiles:
            animation.loop(game_time)

