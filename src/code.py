import gc
import board
import terminalio
import displayio
import pwmio
from adafruit_display_text import label
from adafruit_st7735r import ST7735R
import time
from gamepad import Gamepad
from gametime import GameTime
from gameworld import GameWorld
from player import Player
from framecounter import FrameCounter
from npcmanager import NpcManager 
from imagemanager import ImageManager
import adafruit_imageload
from uispeechbox import UISpeechBox
from splashscreen import SplashScreen

SHOW_FPS = True
SHOW_SPLASHSCREEN = True

SCREEN_WIDTH = 128
SCREEN_HEIGHT = 160

# Usefull board and pin debugging
# import microcontroller
# print(help(microcontroller.pin))
# print(dir(board))
# print(str(board.board_id))

# Setup the display IO
displayio.release_displays()
spi = board.SPI()
tft_cs = board.CS
tft_dc = board.D1
display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=board.D0
)
display = ST7735R(
    display_bus, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, rotation=0, bgr=True, colstart=2, rowstart=1
)
bl = pwmio.PWMOut(board.PWM0, frequency=5000, duty_cycle=0)
bl.duty_cycle = 60000

# Setup the display
screen = displayio.Group()
display.show(screen)
gamepad = Gamepad()
splash_screen = SplashScreen()
display.show(splash_screen.sprite)

if not SHOW_SPLASHSCREEN:
    gamepad.button_X.on_press = True
while not splash_screen.go_to_next_screen:
    splash_screen.loop(gamepad)
    time.sleep(0.05)
    gamepad.loop()

display.refresh()
display.auto_refresh = False

def initialize(init):
    gc.collect() # Free memory due to unoptimized initialization code
    memory_before = gc.mem_free()
    created_object = init()
    gc.collect() # Free memory due to unoptimized initialization code
    memory_after = gc.mem_free()
    print("{} Used: {} bytes, Memory left: {} bytes".format(type(created_object).__name__, memory_before - memory_after, memory_after))
    return created_object

image_manager = initialize(lambda: ImageManager())
frame_counter = initialize(lambda: FrameCounter())
ui_speech_box = initialize(lambda: UISpeechBox())
game_world = initialize(lambda: GameWorld(image_manager))
player = initialize(lambda: Player(image_manager, 64, 64))
game_time = initialize(lambda: GameTime())
npc_manager = initialize(lambda: NpcManager(image_manager, ui_speech_box))
screen = displayio.Group()

# What to show on screen - World
world_sprite = displayio.Group()
world_sprite.append(game_world.sprite)
world_sprite.append(npc_manager.sprite)
world_sprite.append(player.sprite)
screen.append(world_sprite)

# What to show on screen - UI
ui_sprite = displayio.Group()
ui_sprite.append(ui_speech_box.sprite_ui)
screen.append(ui_sprite)
if SHOW_FPS:
    screen.append(frame_counter.sprite)


display.show(screen)
gc.collect()
start_mem = gc.mem_free()
print("Available memory: {} bytes".format(start_mem))

while True:
    game_time.loop()
    # game_time.print_state()
    frame_counter.loop()
    # frame_counter.print_state()
    gamepad.loop()
    # gamepad.print_state()
    player.loop(gamepad, game_time, game_world, npc_manager)
    npc_manager.loop(game_time, game_world, player, gamepad)
    game_world.loop(game_time)
    #time.sleep(0.01)

    world_sprite.x = int(-SCREEN_WIDTH * int(player.position_x / SCREEN_WIDTH))
    world_sprite.y = int(-SCREEN_HEIGHT * int(player.position_y / SCREEN_HEIGHT))
    #world_sprite.x = int(-player.position_x + SCREEN_WIDTH / 2)
    #world_sprite.y = int(-player.position_y + SCREEN_HEIGHT / 2)
    display.refresh()

