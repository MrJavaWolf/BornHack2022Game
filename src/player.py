from math import fabs
from gamepad import GamePad
import displayio
from gametime import GameTime
from gameworld import GameWorld
from tileanimation import TileAnimation
from tilegridloader import import_tile_grid

PLAYER_MAX_SPEED = 50.0
PLAYER_MAX_HEALTH = 100.0


class Player:

    health: float
    """The amount of health the player currently has"""

    position_x: float
    """The players X position"""

    position_y: float
    """The players Y position"""

    def __init__(self, position_x: float, position_y: float):
        self.player_sprite = import_tile_grid(
            image_path="images/lizard.bmp", tile_pixel_width=16, tile_pixel_height=22
        )
        self.player_sprite.x = -8
        self.player_sprite.y = -15
        self.sprite = displayio.Group(scale=1)
        self.sprite.append(self.player_sprite)
        self.idle_animation = TileAnimation(self.player_sprite, [0, 1], 0.5)
        self.run_animation = TileAnimation(self.player_sprite, [4, 7], 0.15)
        self.health = PLAYER_MAX_HEALTH
        self.position_x = position_x
        self.position_y = position_y
        self.sprite.x = int(self.position_x)
        self.sprite.y = int(self.position_y)

        ## Debug player center dot
        #color_bitmap = displayio.Bitmap(1, 1, 1)
        #color_palette = displayio.Palette(1)
        #color_palette[0] = 0xFF0000
        #self.player_pos = displayio.TileGrid(color_bitmap, pixel_shader=color_palette)
        #self.sprite.append(self.player_pos)

    def loop(self, gamepad: GamePad, game_time: GameTime, game_world: GameWorld):

        if gamepad.analog_X == 0 and gamepad.analog_Y == 0:
            self.idle_animation.loop(game_time)
        else:
            new_x_position = (
                self.position_x
                + gamepad.analog_X * PLAYER_MAX_SPEED * game_time.delta_time
            )
            new_y_position = (
                self.position_y
                + gamepad.analog_Y * PLAYER_MAX_SPEED * game_time.delta_time
            )
            if new_y_position < 0:
                new_y_position = 0
            if new_x_position < 0:
                new_x_position = 0
            if game_world.is_walkable(new_x_position, new_y_position):
                self.position_x = new_x_position
                self.position_y = new_y_position
            elif game_world.is_walkable(self.position_x, new_y_position):
                self.position_y = new_y_position
            elif game_world.is_walkable(new_x_position, self.position_y):
                self.position_x = new_x_position
            
            self.sprite.x = int(self.position_x)
            self.sprite.y = int(self.position_y)
            

            self.run_animation.loop(game_time)

            self.player_sprite.flip_x = True if gamepad.analog_X < 0 else False
