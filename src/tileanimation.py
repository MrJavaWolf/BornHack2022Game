from gametime import GameTime
from displayio import TileGrid


class TileAnimation:
    """Animates a single tile on a tile grid"""

    tile_grid: TileGrid
    """The tile grid to animate"""

    tile_grid_index: int = 0
    """Which tile in the tile grid to animate"""

    frames = []
    """A list of tile indexs which will be looped through. Looping through this list is the animation"""

    speed: float = 0.5
    """The animation speed in seconds. How long each frame in the animation will be shown"""

    __current_frame = -1
    __last_frame_change = 0

    def __init__(
        self,
        tile_grid: TileGrid,
        frames,
        speed: float,
        tile_grid_index=0,
    ):
        """
        Creates a animation for a single tile in the tile grid 
        Args:
            tile_grid: The tile grid to animate
            frames: A list of tile indexs which will be looped through. Looping through this list is the animation
            speed: The speed in seconds of how fast the frames should change
            tile_grid_index: Which tile in the tile grid to animate
        """
        self.tile_grid = tile_grid
        self.frames = frames
        self.speed = speed
        self.tile_grid_index = tile_grid_index

    def reset(self):
        """Restart the animation"""
        self.__current_frame = -1
        self.__last_frame_change = 0

    def loop(self, game_time: GameTime):
        # The very start of the animation
        if self.__current_frame == -1: 
            self.__current_frame = 0
            self.__animate_tile_grid(game_time)
        
        # Checks if it is time to change the frame
        if self.__last_frame_change + self.speed < game_time.total_time:
            self.__current_frame += 1
            if self.__current_frame >= len(self.frames):
                self.__current_frame = 0
            self.__animate_tile_grid(game_time)

    def __animate_tile_grid(self, game_time: GameTime):
        """Changes the tile on the tile grid"""    
        self.tile_grid[self.tile_grid_index] = self.frames[self.__current_frame]
        self.__last_frame_change = game_time.total_time
