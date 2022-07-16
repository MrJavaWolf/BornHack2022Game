import displayio
import adafruit_imageload
from adafruit_imageload.tilegrid_inflator import inflate_tilegrid
from gametime import GameTime

TILE_WIDTH = 16
TILE_HEIGHT = 16
SPRITE_MAP_FILE = "/"
TRANSPARENT_COLOR = 0xFF00FF
class GameWorld:

    count = 0
    last_change = 0

    def __init__(self):
        pass

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

