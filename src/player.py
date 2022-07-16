from gamepad import GamePad
import displayio
from gametime import GameTime
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
        self.sprite = displayio.Group(scale = 2)
        self.sprite.append(self.player_sprite)
        self.idle_animation = TileAnimation(self.player_sprite, [0, 1], 0.5)
        self.run_animation = TileAnimation(self.player_sprite, [4, 7], 0.15)
        self.health = PLAYER_MAX_HEALTH
        self.position_x = position_x
        self.position_y = position_y
        self.sprite.x = int(self.position_x)
        self.sprite.y = int(self.position_y)

    def loop(self, gamepad: GamePad, game_time: GameTime):

        if gamepad.analog_X == 0 and gamepad.analog_Y == 0:
            self.idle_animation.loop(game_time)
        else:
            self.position_x += gamepad.analog_X * PLAYER_MAX_SPEED * game_time.delta_time
            self.position_y += gamepad.analog_Y * PLAYER_MAX_SPEED * game_time.delta_time

            self.sprite.x = int(self.position_x)
            self.sprite.y = int(self.position_y)
            self.run_animation.loop(game_time)
            
            self.player_sprite.flip_x = True if gamepad.analog_X < 0 else False
            
