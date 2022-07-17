import displayio
from gamepad import GamePad
from gametime import GameTime
from tileanimation import TileAnimation
from tilegridloader import import_tile_grid

DEFAULT_TILE = 52
DEFAULT_TILE_MAP = "/map/bornhack.csv"
DEFAULT_SPRITE_SHEET = "/images/mystic-woods.bmp"
DEFAULT_TILE_PIXEL_WIDTH = 16
DEFAULT_TILE_PIXEL_HEIGHT = 16
DEFAULT_WALKABLE_TILES = [-1, 8, 52, 53, 54, 55, 18, 22, 23, 24, 38, 128, 129, 130]

class GameWorld:
    """Contains the world.
    The world is build from tiles"""

    walkable_tiles = []
    tile_pixel_width: int  
    tile_pixel_height: int

    def __init__(self,
        sprite_sheet_file:str = DEFAULT_SPRITE_SHEET,
        tile_map_file:str = DEFAULT_TILE_MAP,
        default_tile:int = DEFAULT_TILE,
        tile_pixel_width:int = DEFAULT_TILE_PIXEL_WIDTH,
        tile_pixel_height:int = DEFAULT_TILE_PIXEL_HEIGHT,
        walkable_tiles = DEFAULT_WALKABLE_TILES):

        self.sprite_sheet_file = sprite_sheet_file
        self.tile_map_file = tile_map_file
        self.default_tile = default_tile
        self.tile_pixel_width = tile_pixel_width
        self.tile_pixel_height = tile_pixel_height
        self.walkable_tiles = walkable_tiles

        # Reads the size of the tile map
        self.map_width, self.map_height = self.__get_map_size()

        # Sets up the world tile map
        self.world_map = import_tile_grid(
            image_path=self.sprite_sheet_file,
            tile_pixel_width=self.tile_pixel_width,
            tile_pixel_height=self.tile_pixel_height,
            width=self.map_width,
            height=self.map_height,
            default_tile=self.default_tile
        )
        self.__paint_world_map()

        # Saves it to a group to be easily moved around
        self.sprite = displayio.Group()
        self.sprite.append(self.world_map)
        self.sprite.x = 0
        self.sprite.y = 0

    def __get_map_size(self):
        height = 0
        width = 0
        with open(self.tile_map_file, mode="r") as file:
            for line in file:
                height += 1
                values = line.split(",")
                width = len(values) if len(values) > width else width
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


    def loop(self, game_time: GameTime, gamepad: GamePad):


        pass

