import board
from digitalio import DigitalInOut, Pull
from analogio import AnalogIn
from gamecontrollerbutton import GameControllerButton
import json
from collections import OrderedDict


# Setup the pins
BUTTON_A_PIN = board.G0
BUTTON_B_PIN = board.G1
BUTTON_X_PIN = board.G2
BUTTON_Y_PIN = board.G3
ANALOG_X_PIN = board.G9
ANALOG_Y_PIN = board.BATT_VIN3
ANALOG_DEAD_ZONE = 0.0275
INVERT_ANALOG_X = False
INVERT_ANALOG_Y = False


class GameController:
    """Keeps track of the game controller's state"""

    button_A: GameControllerButton = GameControllerButton()
    """Get the A button's state"""

    button_B: GameControllerButton = GameControllerButton()
    """Get the B button's state"""
    
    button_X: GameControllerButton = GameControllerButton()
    """Get the X button's state"""
    
    button_Y: GameControllerButton = GameControllerButton()
    """Get the Y button's state"""
    
    analog_X: float = 0
    """A value between -1 and 1. Where 0 is in the center"""

    analog_Y: float = 0
    """A value between -1 and 1. Where 0 is in the center"""

    button_A_io: DigitalInOut
    """Read the raw digital input for the button"""
    
    button_B_io: DigitalInOut
    """Read the raw digital input for the button"""

    button_X_io: DigitalInOut
    """Read the raw digital input for the button"""
    
    button_Y_io: DigitalInOut
    """Read the raw digital input for the button"""
    
    analog_X_io: AnalogIn
    """Read the raw analog input"""

    analog_Y_io: AnalogIn
    """Read the raw analog input"""

    def __init__(self):
        
        # Setup button inputs
        self.button_A_io = DigitalInOut(BUTTON_A_PIN)
        self.button_B_io = DigitalInOut(BUTTON_B_PIN)
        self.button_X_io = DigitalInOut(BUTTON_X_PIN)
        self.button_Y_io = DigitalInOut(BUTTON_Y_PIN)
        
        # Pull-up buttons
        self.button_A_io.pull = Pull.UP
        self.button_B_io.pull = Pull.UP
        self.button_X_io.pull = Pull.UP
        self.button_Y_io.pull = Pull.UP

        # Setup analog inputs
        self.analog_X_io = AnalogIn(ANALOG_X_PIN)
        self.analog_Y_io = AnalogIn(ANALOG_Y_PIN)
        self.loop()

    def read_button_value(self, button):
        """Reads the buttons value"""
        # The buttons are pulled up, meaning if they are not pushed they are set to True (High)
        # When the buttons are pressed they are set to False (Low)
        return not button.value

    def read_analog_value(self, analog, invert):
        # Normalizes the anlog value to -1 - 0 - 1 
        value = (analog.value - 32768.0) / 32768.0
        if invert: # Inverts the value
            value *= -1
        if -ANALOG_DEAD_ZONE < value and value < ANALOG_DEAD_ZONE: # Handles deadzone
            return 0
        return value

    def loop(self):
        self.button_A.loop(self.read_button_value(self.button_A_io))
        self.button_B.loop(self.read_button_value(self.button_A_io))
        self.button_X.loop(self.read_button_value(self.button_X_io))
        self.button_Y.loop(self.read_button_value(self.button_Y_io))
        self.analog_X = self.read_analog_value(self.analog_X_io, INVERT_ANALOG_X)
        self.analog_Y = self.read_analog_value(self.analog_Y_io, INVERT_ANALOG_Y)
    
    def print_state(self):
        print(json.dumps(OrderedDict({
            'analog_X': self.analog_X,
            'analog_Y': self.analog_Y,
            'A':self.button_A.is_pressed,
            'B':self.button_B.is_pressed,
            'X':self.button_X.is_pressed,
            'Y':self.button_Y.is_pressed})))

    def print_state_detailed(self):
        print(json.dumps(OrderedDict({
            'analog_X': self.analog_X,
            'analog_Y': self.analog_Y,
            'A':self.button_A.__dict__,
            'B':self.button_B.__dict__,
            'X':self.button_X.__dict__,
            'Y':self.button_Y.__dict__})))
