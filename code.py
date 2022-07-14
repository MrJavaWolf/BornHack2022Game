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
from gamepad import GamePad
from player import Player

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


#import microcontroller
#print(help(microcontroller.pin))
#print(dir(board))
#print(str(board.board_id))
#print(board.A1)

gamepad = GamePad()

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

while not gamepad.button_A.on_press:
    time.sleep(0.05)
    gamepad.loop()

player = Player(50,50)

count = 1
splash = displayio.Group()

# Text
text_group = displayio.Group(scale=2, x=5, y=10)
text = str(count)
text_area = label.Label(terminalio.FONT, text=text, color=0xFF0000)
text_group.append(text_area)  # Subgroup for text scaling

# Show on screen
splash.append(player.sprite)
splash.append(text_group)
display.show(splash)


while True:
	gamepad.loop()
	gamepad.print_state_detailed()
	count = count + 1
	player.loop(gamepad)
	
	text_area.text = str(count)
	#display.show(splash)

	time.sleep(0.01)



while True:
	pass

