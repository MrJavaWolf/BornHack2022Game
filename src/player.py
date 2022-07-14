from gamepad import GamePad
import displayio
from gametime import GameTime

PLAYER_MAX_SPEED = 150.0
PLAYER_MAX_HEALTH = 100.0


class Player:

    health: float
    """The amount of health the player currently has"""

    position_x: float
    """The players X position"""

    position_y: float
    """The players Y position"""

    def __init__(self, position_x: float, position_y: float):
        self.health = PLAYER_MAX_HEALTH
        self.position_x = position_x
        self.position_y = position_y

        # Setup sprite
        color_bitmap = displayio.Bitmap(10, 10, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0x00FF00
        self.sprite = displayio.TileGrid(
            color_bitmap,
            pixel_shader=color_palette,
            x=int(self.position_x),
            y=int(self.position_y),
        )

    def loop(self, gamepad: GamePad, game_time: GameTime):
        self.position_x += gamepad.analog_X * PLAYER_MAX_SPEED * game_time.delta_time
        self.position_y += gamepad.analog_Y * PLAYER_MAX_SPEED * game_time.delta_time

        self.sprite.x = int(self.position_x)
        self.sprite.y = int(self.position_y)
