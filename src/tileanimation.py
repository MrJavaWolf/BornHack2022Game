import displayio
from gametime import GameTime
from displayio import TileGrid


class TileAnimation:

    frames = []
    speed: float = 0.1

    __current_frame = -1
    __last_frame_change = 0

    def __init__(
        self,
        tile_grid: TileGrid,
        frames,
        speed: float,
        tile_grid_index=0,
    ):
        self.frames = frames
        self.tile_grid = tile_grid
        self.speed = speed
        self.tile_grid_index = tile_grid_index

    def reset(self):
        self.__current_frame = -1
        self.__last_frame_change = 0

    def loop(self, game_time: GameTime):
        if self.__current_frame == -1:
            self.__current_frame = 0
            self.__update_frame(game_time)
        
        if self.__last_frame_change + self.speed < game_time.total_time:
            self.__current_frame += 1
            if self.__current_frame >= len(self.frames):
                self.__current_frame = 0
            self.__update_frame(game_time)

    def __update_frame(self, game_time: GameTime):        
        self.tile_grid[self.tile_grid_index] = self.frames[self.__current_frame]
        self.__last_frame_change = game_time.total_time
