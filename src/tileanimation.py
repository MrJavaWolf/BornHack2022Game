from math import fabs
from gametime import GameTime
from displayio import TileGrid


class TileAnimation:
    """Animates a single tile on a tile grid"""

    name:str = None
    """The name of the animation"""
    
    tile_grid: TileGrid
    """The tile grid to animate"""

    tile_grid_index: int = 0
    """Which tile in the tile grid to animate"""

    frames = []
    """A list of tile indexs which will be looped through. Looping through this list is the animation"""

    speed: float = 0.5
    """The animation speed in seconds. How long each frame in the animation will be shown"""

    loop_animation = True
    """If true loops the animation, otherwise stays on the last frame of the animation"""

    is_animation_done = False
    """Whether the animation is done, is only true if loop_animation is set to false, and the animation have played untill the last frame"""

    __current_frame = -1
    __last_frame_change = 0

    def __init__(
        self,
        name: str,
        tile_grid: TileGrid,
        frames,
        speed: float,
        tile_grid_index=0,
        loop_animation=True
    ):
        """
        Creates a animation for a single tile in the tile grid 
        Args:
            name: The name of the animation
            tile_grid: The tile grid to animate
            frames: A list of tile indexs which will be looped through. Looping through this list is the animation
            speed: The speed in seconds of how fast the frames should change
            tile_grid_index: Which tile in the tile grid to animate
            loop_animation: If true loops the animation, otherwise stays on the last frame of the animation
        """
        self.name = name
        self.tile_grid = tile_grid
        self.frames = frames
        self.speed = speed
        self.tile_grid_index = tile_grid_index
        self.loop_animation = loop_animation

    def reset(self):
        """Restart the animation"""
        self.__current_frame = -1
        self.__last_frame_change = 0
        self.is_animation_done = False

    def loop(self, game_time: GameTime):
        # Check if the animation is done
        if self.is_animation_done:
            return

        # The very start of the animation
        if self.__current_frame == -1: 
            self.__current_frame = 0
            self.__animate_tile_grid(game_time)

        # Checks if it is time to change the frame
        if self.__last_frame_change + self.speed >= game_time.total_time:
            return
            
        self.__current_frame += 1

        if self.__current_frame >= len(self.frames):
            if self.loop_animation:
                # Loop animation
                self.__current_frame = 0
            else:
                # Animatino done, do not loop the animation
                self.is_animation_done = True
                self.__current_frame -= 1
        self.__animate_tile_grid(game_time)
            

    def __animate_tile_grid(self, game_time: GameTime):
        """Changes the tile on the tile grid"""
        self.tile_grid[self.tile_grid_index] = self.frames[self.__current_frame]
        self.__last_frame_change = game_time.total_time
