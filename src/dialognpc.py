import displayio
from adafruit_display_text import label
from adafruit_display_text import wrap_text_to_pixels
import terminalio
from adafruit_display_shapes.roundrect import RoundRect

from gamepad import Gamepad
from gametime import GameTime
from gameworld import GameWorld
from tileanimation import TileAnimation
from tilegridloader import import_tile_grid, TRANSPARENT_COLOR

ENEMY_MAX_SPEED = 50.0
ENEMY_MAX_HEALTH = 100.0
DEBUG_SHOW_NPC_POSITION = False  # Shows the enemies exact position with a small dot

# Visuals
NPC_SPRITE = "/game_data/big-enemies.bmp"
NPC_SPRITE_TYPE = 0
NPC_SPRITE_OFFSET = {"x": -16, "y": -26}
NPC_SPRITE_TILE_SIZE = {"width": 32, "height": 36}
NPC_IDLE_ANIMATION = {
    "fps": 0.45,
    "frames": [1 + NPC_SPRITE_TYPE * 8, 2 + NPC_SPRITE_TYPE * 8],
}
NPC_RUN_ANIMATION = {"fps": 0.15, "frames": [4, 7]}

INTERACTION_ACTIONS = [
    {
        "action_type": "talk",
        "text": "Hello greate adventur-y",
    },
    {
        "action_type": "talk",
        "text": "I am happy to see you",
    },
    {
        "action_type": "talk",
        "text": "I need you to write-y me some dialog",
    },
    {"action_type": "camera_shake", "time": 1, "amount": 10, "decrease_factor": 1},
    {"action_type": "wait", "time": 1},
    {
        "action_type": "change_world_tile",
        "tile_x": 1,
        "tile_y": 1,
        "to_tile_type": 1,
    },
    {
        "action_type": "talk",
        "text": "Ohh-y~ I think the world just changed",
    },
]


class DialogNpc:

    is_interacted_with: bool = False
    __current_interact_index: int = -1

    # Wait time state
    __current_action_start_time: float = 0

    def __init__(self, position_x: float, position_y: float):

        # Setup
        self.position_x = position_x
        self.position_y = position_y
        self.actions = INTERACTION_ACTIONS
        # Visuals
        self.character_sprite = import_tile_grid(
            image_path=NPC_SPRITE,
            tile_pixel_width=NPC_SPRITE_TILE_SIZE["width"],
            tile_pixel_height=NPC_SPRITE_TILE_SIZE["height"],
        )
        self.character_sprite.x = NPC_SPRITE_OFFSET["x"]
        self.character_sprite.y = NPC_SPRITE_OFFSET["y"]
        self.idle_animation = TileAnimation(
            self.character_sprite,
            NPC_IDLE_ANIMATION["frames"],
            NPC_IDLE_ANIMATION["fps"],
        )
        self.run_animation = TileAnimation(
            self.character_sprite, NPC_RUN_ANIMATION["frames"], NPC_RUN_ANIMATION["fps"]
        )
        self.sprite = displayio.Group(scale=1)
        self.sprite.append(self.character_sprite)
        self.sprite.x = int(self.position_x)
        self.sprite.y = int(self.position_y)
        
        # UI speech box
        self.sprite_ui = displayio.Group()
        self.speech_box_ui = displayio.Group()
        screen_width = 128
        screen_height = 160
        border_size = 4
        speech_box_height = 56
        roundiness = 2
        line_height = 12
        self.max_line_width = screen_width - border_size * 4
        roundrect = RoundRect(
            border_size, 
            screen_height - border_size - speech_box_height, 
            screen_width - border_size * 2, 
            speech_box_height, 
            roundiness,
            fill=0xDDDDDD, 
            outline=0x111111, 
            stroke=2)
        self.speech_box_ui.append(roundrect)
        label_group = displayio.Group(scale=1, x=border_size + 4 , y=screen_height - speech_box_height + border_size)
        self.text_line_1 = label.Label(terminalio.FONT, text="", color=0x111111)
        self.text_line_2 = label.Label(terminalio.FONT, text="", color=0x111111, y = line_height * 1)
        self.text_line_3 = label.Label(terminalio.FONT, text="", color=0x111111, y = line_height * 2)
        self.text_line_4 = label.Label(terminalio.FONT, text="", color=0x111111, y = line_height * 3)
        label_group.append(self.text_line_1)
        label_group.append(self.text_line_2)
        label_group.append(self.text_line_3)
        label_group.append(self.text_line_4)
        self.speech_box_ui.append(label_group)

        # Debug show enemy center dot
        if DEBUG_SHOW_NPC_POSITION:
            color_bitmap = displayio.Bitmap(1, 1, 1)
            color_palette = displayio.Palette(1)
            color_palette[0] = 0xFF0000
            self.character_position = displayio.TileGrid(
                color_bitmap, pixel_shader=color_palette
            )
            self.sprite.append(self.character_position)

    def loop(self, game_time: GameTime, game_world: GameWorld, gamepad: Gamepad):
        self.idle_animation.loop(game_time)
        if self.is_interacted_with:
            self.interaction_loop(game_time, game_world, gamepad)

    def interact(self, game_time: GameTime):
        self.is_interacted_with = True
        self.__current_interact_index = -1

    def interaction_loop(self, game_time: GameTime, game_world: GameWorld, gamepad: Gamepad):
        if not self.is_interacted_with:
            return

        if self.__current_interact_index == -1:
            self.go_to_next_interaction(game_time, game_world)
            return

        if self.current_action_type == "wait":
            if (
                game_time.total_time - self.__current_action_start_time
                >= self.current_action["time"]
            ):
                self.go_to_next_interaction(game_time, game_world)

        elif self.current_action_type == "change_world_tile":
            game_world.change_tile(
                self.current_action["tile_x"],
                self.current_action["tile_y"],
                self.current_action["to_tile_type"],
            )
            self.go_to_next_interaction(game_time, game_world)

        elif self.current_action_type == "camera_shake":
            time_eclipsed = game_time.total_time - self.__current_action_start_time
            if time_eclipsed < self.current_action["time"]:
                dampening = 1 - time_eclipsed / (
                    self.current_action["time"] * self.current_action["decrease_factor"]
                )
                game_world.shake(self.current_action["amount"] * dampening)
            else:
                game_world.shake(0)
                self.go_to_next_interaction(game_time, game_world)

        elif self.current_action_type == "talk":
            if gamepad.button_X.on_press:
                self.text_line_1.text = "" 
                self.text_line_2.text = "" 
                self.text_line_3.text = "" 
                self.text_line_4.text = "" 
                self.sprite_ui.remove(self.speech_box_ui)
                self.go_to_next_interaction(game_time, game_world)

        else:
            self.go_to_next_interaction(game_time, game_world)

    def go_to_next_interaction(self, game_time: GameTime, game_world: GameWorld):
        self.__current_interact_index += 1
        if self.__current_interact_index >= len(self.actions):
            self.is_interacted_with = False
            return
        self.__current_action_start_time = game_time.total_time
        self.current_action = self.actions[self.__current_interact_index]
        self.current_action_type = self.current_action["action_type"]

        if self.current_action_type == "talk":
            texts = wrap_text_to_pixels(self.current_action["text"], self.max_line_width, terminalio.FONT)
            if len(texts) > 0:
                self.text_line_1.text = texts[0]
            if len(texts) > 1:
                self.text_line_2.text = texts[1]
            if len(texts) > 2:
                self.text_line_3.text = texts[2]
            if len(texts) > 3:
                self.text_line_4.text = texts[3]
            self.sprite_ui.append(self.speech_box_ui)

