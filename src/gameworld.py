import displayio
import displayio
from gamepad import GamePad
from gametime import GameTime
from tileanimation import TileAnimation
from tilegridloader import import_tile_grid


class GameWorld:
    """Contains the world.
    The world is build from tiles"""

    walkable_tiles = [-1, 8, 22]
    tile_pixel_width: int
    tile_pixel_height: int

    def __init__(self):
        # The world map is a 2D array of the different tile types
        self.world = self.__read_world_map_file("world_map.csv", default_tile=22)

        # Sets up the world tile map
        self.tile_pixel_width = 16
        self.tile_pixel_height = 16
        self.world_tile_map = import_tile_grid(
            image_path="images/mystic-woods.bmp",
            tile_pixel_width=self.tile_pixel_width,
            tile_pixel_height=self.tile_pixel_height,
            height=len(self.world),
            width=len(self.world[0]),
        )

        # Inistantiates values for the world tile map
        for y, row in enumerate(self.world):
            for x, value in enumerate(row):
                self.world_tile_map[y * len(row) + x] = value

        # Saves it to a group to be easily moved around
        self.sprite = displayio.Group()
        self.sprite.append(self.world_tile_map)
        self.sprite.x = 0
        self.sprite.y = 0

    def __read_world_map_file(self, map_file, default_tile=0):
        """Reads the world map"""
        world = []
        with open(map_file, mode="r") as file:
            for line in file:
                row = []
                world.append(row)
                for value in line.split(","):
                    tile_type, is_int = self.__int_try_parse(value)
                    if is_int:
                        row.append(tile_type)
                    else:
                        row.append(default_tile)

        # Ensures all rows in the world map is exactly the same length as the first row
        target_width = len(world[0])
        for row in world:
            while len(row) > target_width:
                del row[len(row) - 1]
            while len(row) < target_width:
                row.append(default_tile)
        return world

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
        if tile_y >= len(self.world):
            return -1
        if tile_x >= len(self.world[tile_y]):
            return -1
        return self.world[tile_y][tile_x]

    def loop(self, game_time: GameTime, gamepad: GamePad):

        # if game_time.total_time > self.last_change + 0.02:
        #     self.palette.make_opaque(self.count)
        #     self.count += 1
        #     if self.count > 100:
        #         self.count = 0
        #     print(str(self.palette[self.count]))
        #     self.palette.make_transparent(self.count)

        #     self.last_change = game_time.total_time
        pass
