import displayio
import displayio
from gamepad import GamePad
from gametime import GameTime
from tileanimation import TileAnimation
from tilegridloader import import_tile_grid


class GameWorld:

    count = 0
    last_change = 0
    walkable_tiles = [-1, 8, 22]
    world = [
        [22, 22, 22, 22, 22, 22, 22, 22, 18, 3],
        [22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
        [22, 22, 1, 2, 3, 22, 22, 22, 22, 22],
        [22, 22, 7, 8, 10, 2, 3, 22, 22, 22],
        [2, 2, 11, 8, 18, 8, 9, 22, 22, 22],
        [8, 8, 18, 8, 8, 8, 9, 22, 0, 18],
        [8, 8, 4, 14, 14, 14, 15, 22, 20, 9],
        [14, 14, 15, 22, 22, 22, 22, 22, 12, 15],
        [22, 22, 22, 22, 22, 0, 19, 20, 21, 4],
        [19, 20, 20, 21, 22, 6, 22, 22, 4, 15],
    ]
    tile_pixel_width: int
    tile_pixel_height: int

    def __init__(self):
        self.tile_pixel_width = 16
        self.tile_pixel_height = 16
        self.world_sprite = import_tile_grid(
            image_path="images/mystic-woods.bmp",
            tile_pixel_width=self.tile_pixel_width,
            tile_pixel_height=self.tile_pixel_height,
            height=len(self.world),
            width=len(self.world[0]),
        )

        self.sprite = displayio.Group()
        self.sprite.append(self.world_sprite)
        self.sprite.x = 0
        self.sprite.y = 0
        for y, row in enumerate(self.world):
            for x, value in enumerate(row):
                self.world_sprite[y * len(row) + x] = value

    def is_walkable(self, pixel_x, pixel_y):
        tile_type = self.get_tile_type_at(pixel_x, pixel_y)
        return tile_type in self.walkable_tiles

    def get_tile_type_at(self, pixel_x, pixel_y):
        tile_x = int(pixel_x / self.tile_pixel_width)
        tile_y = int(pixel_y / self.tile_pixel_height)
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
