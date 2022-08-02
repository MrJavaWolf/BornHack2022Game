import terminalio
import displayio
from adafruit_display_text import label
from gamepad import Gamepad


class SplashScreen:

    go_to_next_screen = False
    __press_button_to_start = None

    def __init__(self):
        self.sprite = displayio.Group()
        self.sprite.append(
            self.create_label("Jens", x=40, y=30, scale=2, color=0xFF00FF)
        )
        self.sprite.append(
            self.create_label("JWolf", x=20, y=60, scale=3, color=0xFF00FF)
        )
        self.sprite.append(
            self.create_label("Larsen", x=30, y=90, scale=2, color=0xFF00FF)
        )
        self.__press_to_start = self.create_label("Press X to start", x=15, y=130)
        self.sprite.append(self.__press_to_start)
        self.sprite.append(
            self.create_label("<Req: Analog A2, A3>", x=5, y=145)
        )

    def create_label(self, text: str, x: int, y: int, color=0xFFFFFF, scale: int = 1):
        group = displayio.Group(scale=scale, x=x, y=y)
        text_label = label.Label(terminalio.FONT, text=text, color=color)
        group.append(text_label)
        return group

    def loop(self, gamepad: Gamepad):
        if gamepad.button_X.on_press:
            self.go_to_next_screen = True
            self.sprite.remove(self.__press_to_start)
            self.sprite.append(self.create_label("Loading...", x=40, y=130))
