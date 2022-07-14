# Used by GamePad.py


class GamePadButton:
    """Keeps track of a game pads button's state"""

    is_pressed: bool = False
    """Is true if the button is currently pressed down, otherwise false"""

    on_press: bool = False
    """Is true if the button was pressed down this frame(/update/loop), otherwise false.
    Use this if you want to trigger an event when the button was pressed"""

    on_release: bool = False
    """Is true if the button was released this frame(/update/loop), otherwise false.
    Use this if you want to trigger an event when the button was released"""

    def loop(self, isPressedDown: bool):
        """Update the buttons state"""

        # Was not pressed down before, is pressed down now
        if not self.is_pressed and isPressedDown:
            self.on_press = True
            self.on_release = False

        # Is keeping it pressed down
        elif self.is_pressed and isPressedDown:
            self.on_press = False
            self.on_release = False

        # Releases the button
        elif self.is_pressed and not isPressedDown:
            self.on_press = False
            self.on_release = True

        # Was not pressed and is still not pressed
        elif not self.is_pressed and not isPressedDown:
            self.on_press = False
            self.on_release = False

        self.is_pressed = isPressedDown
