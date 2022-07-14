print("Hello World!")
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# https://github.com/todbot/circuitpython-tricks/blob/main/README.md#read-an-digital-input-as-a-button
# https://docs.circuitpython.org/en/latest/shared-bindings/displayio/#displayio.Bitmap 

# Todo
# - Analog
# - Design game
#   - Player movement
#   - Player sprite
#   - Player actions (Melee (with charge), Shoot(with charge), dash (with charge))
#   - Effects
#   - Enemies
#   - Game world (Hardcoded, Perlin noise, Wave function collaps)


"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import board
import terminalio
import displayio
import digitalio
from digitalio import DigitalInOut, Pull
from analogio import AnalogIn
import pwmio
from adafruit_display_text import label
from adafruit_st7735r import ST7735R
import time


from adafruit_slideshow import PlayBackOrder, SlideShow

# Release any resources currently in use for the displays
displayio.release_displays()


spi = board.SPI()
tft_cs = board.CS
tft_dc = board.D1

display_bus = displayio.FourWire(
	spi, command=tft_dc, chip_select=tft_cs, reset=board.D0
)

display = ST7735R(display_bus, width=128, height=160, rotation=0, bgr=True, colstart=2, rowstart=1)

# bl = digitalio.DigitalInOut(board.PWM0)
# bl.direction = digitalio.Direction.OUTPUT
# bl.value = True
bl = pwmio.PWMOut(board.PWM0, frequency=5000, duty_cycle=0)
bl.duty_cycle = 60000


# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Pin Map Script"""
import microcontroller
import board


print(help(microcontroller.pin))

# board_pins = []
# for pin in dir(microcontroller.pin):
#     if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
#         pins = []
#         for alias in dir(board):
#             if getattr(board, alias) is getattr(microcontroller.pin, pin):
#                 pins.append("board.{}".format(alias))
#         if len(pins) > 0:
#             board_pins.append(" ".join(pins))
# for pins in sorted(board_pins):
#     print(pins)


# Setup buttons
buttonA = DigitalInOut(board.G0)
buttonA.pull = Pull.UP
buttonB = DigitalInOut(board.G1) 
buttonB.pull = Pull.UP
buttonX = DigitalInOut(board.G2)
buttonX.pull = Pull.UP
buttonY = DigitalInOut(board.G3)
buttonY.pull = Pull.UP

# Setup analog
print(dir(board))
print(str(board.board_id))
print(board.A1)
analogX = AnalogIn(board.G9)
analogY = AnalogIn(board.BATT_VIN3)
analog_dead_zone_size=0.025


def get_analog_value(analog):
	# Normalizes the anlog value to -1 - 0 - 1 
	value = (analog.value - 32768.0) / 32768.0
	
	# Handles deadzone
	if -analog_dead_zone_size < value and value < analog_dead_zone_size:
		return 0
	
	return value

# Setup the display
splash = displayio.Group()
display.show(splash)

# Show JWolf badge
text_group1 = displayio.Group(scale=3, x=20, y=50)
text_area1 = label.Label(terminalio.FONT, text="JWolf", color=0xFF00FF)
text_group1.append(text_area1)  # Subgroup for text scaling

text_group2 = displayio.Group(scale=1, x=15, y=100)
text_area2 = label.Label(terminalio.FONT, text="Press A to start", color=0xFFFFFF)
text_group2.append(text_area2)  # Subgroup for text scaling

splash.append(text_group1)
splash.append(text_group2)
display.show(splash)

while buttonA.value:
    time.sleep(0.05)


xPos = 50.0
yPos = 50.0

count = 1

splash = displayio.Group()

# Text
text_group = displayio.Group(scale=2, x=5, y=10)
text = str(count)
text_area = label.Label(terminalio.FONT, text=text, color=0xFF0000)
text_group.append(text_area)  # Subgroup for text scaling

# Player
color_bitmap = displayio.Bitmap(10, 10, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=int(xPos), y=int(yPos))
	
# Show on screen
splash.append(text_group)
splash.append(bg_sprite)
display.show(splash)


while True:
	
	count = count + 1
	if buttonA.value:
		yPos += 5
	if buttonB.value:
		yPos -= 5
	if buttonX.value:
		xPos += 5
	if buttonY.value:
		xPos -= 5
	xPos += get_analog_value(analogX) * 5
	yPos += get_analog_value(analogY) * -5
	
	# now I do the big OwO
	bg_sprite.x = int(xPos)
	bg_sprite.y = int(yPos)
	#if count % 100 == 0:
	
	text_area.text = str(count)
	#display.show(splash)

	print(
	 	"A: " + str(buttonA.value) + ", " + 
	 	"B: " + str(buttonB.value) + ", " + 
	 	"X: " + str(buttonX.value) + ", " + 
	 	"Y: " + str(buttonY.value) + ", " +
		"Analog_X: " + str(analogX.value) + ", " 
		"Analog_Y: " + str(analogY.value) + ", " 
		)

	time.sleep(0.01)



while True:
	pass

