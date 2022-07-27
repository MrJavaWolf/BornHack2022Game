# Used by GamePad.py


class GamepadButton:
    """Keeps track of a button's state"""

    is_pressed: bool = False
    """Is true if the button is currently pressed down, otherwise false"""

    on_press: bool = False
    """Is true if the button is pressed down this frame(/update/loop), otherwise false.
    Use this if you want to trigger an event when the button is pressed down"""

    on_release: bool = False
    """Is true if the button is released this frame(/update/loop), otherwise false.
    Use this if you want to trigger an event when the button is released"""

    def loop(self, is_pressed_down: bool):
        """Update the buttons state"""

        # The button is pressed down
        if not self.is_pressed and is_pressed_down:
            self.on_press = True
            self.on_release = False

        # The button is kept pressed down
        elif self.is_pressed and is_pressed_down:
            self.on_press = False
            self.on_release = False

        # The button is released
        elif self.is_pressed and not is_pressed_down:
            self.on_press = False
            self.on_release = True

        # The button is not pressed down
        elif not self.is_pressed and not is_pressed_down:
            self.on_press = False
            self.on_release = False

        self.is_pressed = is_pressed_down
