import displayio
import displayio
from gametime import GameTime
from tileanimation import TileAnimation
from tilegridloader import import_tile_grid

TILE_WIDTH = 16
TILE_HEIGHT = 16
SPRITE_MAP_FILE = "/"
TRANSPARENT_COLOR = 0xFF00FF


class GameWorld:

    count = 0
    last_change = 0

    world = [
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [7, 8, 8, 8, 8, 8, 8, 8, 8, 9],
        [7, 8, 8, 8, 8, 8, 8, 8, 8, 9],
        [7, 8, 8, 8, 8, 8, 8, 8, 8, 9],
        [7, 8, 8, 8, 8, 8, 8, 8, 8, 9],
        [7, 8, 8, 8, 8, 8, 8, 8, 8, 9],
        [7, 8, 8, 8, 8, 8, 8, 8, 8, 9],
        [7, 8, 8, 8, 8, 8, 8, 8, 8, 9],
        [7, 8, 8, 8, 8, 8, 8, 8, 8, 9],
        [13, 14, 14, 14, 14, 14, 14, 14, 14, 9],
    ]

    def __init__(self):
        self.world_sprite = import_tile_grid(
            image_path="images/mystic-woods.bmp",
            tile_pixel_width=16,
            tile_pixel_height=16,
            height=len(self.world),
            width=len(self.world[0]),
        )

        self.sprite = displayio.Group()
        self.sprite.append(self.world_sprite)
        self.sprite.x = 0
        self.sprite.y = 0
        self.world_sprite[20] = 15
        for y, row in enumerate(self.world):
            for x, value in enumerate(row):
                print("lookup: " + str(x) + ", " + str(y) + ": " + str(value))
                self.world_sprite[y * len(row) + x] = value

    def loop(self, game_time: GameTime):
        # if game_time.total_time > self.last_change + 0.02:
        #     self.palette.make_opaque(self.count)
        #     self.count += 1
        #     if self.count > 100:
        #         self.count = 0
        #     print(str(self.palette[self.count]))
        #     self.palette.make_transparent(self.count)

        #     self.last_change = game_time.total_time
        pass
