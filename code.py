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

game_pad = GamePad()

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

while not game_pad.button_A.on_press:
    time.sleep(0.05)
    game_pad.loop()

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
	game_pad.loop()
	game_pad.print_state_detailed()
	count = count + 1
	#if buttonA.value:
	#	yPos += 5
	#if buttonB.value:
#		yPos -= 5#
#	if buttonX.value:
#		xPos += 5
#	if buttonY.value:
#		xPos -= 5
	xPos += game_pad.analog_X * 5
	yPos += game_pad.analog_Y * -5
	
	# now I do the big OwO
	bg_sprite.x = int(xPos)
	bg_sprite.y = int(yPos)
	#if count % 100 == 0:
	
	text_area.text = str(count)
	#display.show(splash)

	time.sleep(0.01)



while True:
	pass

