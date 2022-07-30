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
from imagemanager import ImageManager
from uispeechbox import UISpeechBox

DEBUG_SHOW_NPC_POSITION = False  # Shows the npc's exact position with a small dot

# Visuals
class DialogNpc:

    position_x : float
    """The NPC's x position"""

    position_y : float 
    """The NPC's y position"""
    
    collision_size_width: float
    """How big the NPC is"""
    
    collision_size_height: float
    """How big the NPC is"""

    is_interacted_with: bool = False
    __current_action_index: int = -1

    # Wait time state
    __current_action_start_time: float = 0

    bitmap = None
    palette = None
    character_sprite = None
    idle_animation:TileAnimation = None
    run_animation: TileAnimation = None

    def __init__(
        self, image_manager: ImageManager, ui_speech_box: UISpeechBox, npc_data
    ):
        self.ui_speech_box = ui_speech_box
        self.npc_data = npc_data
        self.collision_size_width = npc_data["collision_size"]["width"]
        self.collision_size_height = npc_data["collision_size"]["height"]
        
        # Setup
        self.position_x = npc_data["position"]["x"]
        self.position_y = npc_data["position"]["y"]
        self.actions = npc_data["actions"]

        # Visuals
        self.sprite = displayio.Group(scale=1)
        self.sprite.x = int(self.position_x)
        self.sprite.y = int(self.position_y)
        if npc_data["sprite_sheet"] is not None:
            self.bitmap, self.palette = image_manager.get_image(npc_data["sprite_sheet"])
            self.character_sprite = displayio.TileGrid(
                bitmap=self.bitmap,
                pixel_shader=self.palette,
                tile_width=npc_data["sprite_sheet_tile_size"]["width"],
                tile_height=npc_data["sprite_sheet_tile_size"]["height"],
            )

            self.character_sprite.x = npc_data["sprite_offset"]["x"]
            self.character_sprite.y = npc_data["sprite_offset"]["y"]
            self.idle_animation = TileAnimation(
                self.character_sprite,
                npc_data["idle_animation"]["frames"],
                npc_data["idle_animation"]["fps"],
            )
            self.run_animation = TileAnimation(
                self.character_sprite,
                npc_data["run_animation"]["frames"],
                npc_data["run_animation"]["fps"],
            )
            self.sprite.append(self.character_sprite)
        

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
        
        if self.idle_animation is not None:
            self.idle_animation.loop(game_time)
        
        if self.is_interacted_with:
            self.interaction_loop(game_time, game_world, gamepad)

    def interact(self, game_time: GameTime):
        self.is_interacted_with = True
        self.__current_action_index = -1

    def interaction_loop(
        self, game_time: GameTime, game_world: GameWorld, gamepad: Gamepad
    ):
        if not self.is_interacted_with:
            return

        if self.__current_action_index == -1:
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
                self.ui_speech_box.hide()
                self.go_to_next_interaction(game_time, game_world)

        elif self.current_action_type == "flip_sprite_x":
            if self.character_sprite is not None:
                self.character_sprite.flip_x = self.current_action["value"]
            self.go_to_next_interaction(game_time, game_world)

        elif self.current_action_type == "flip_sprite_y":
            if self.character_sprite is not None:
                self.character_sprite.flip_y = self.current_action["value"]
            self.go_to_next_interaction(game_time, game_world)

        else:
            self.go_to_next_interaction(game_time, game_world)

    def go_to_next_interaction(self, game_time: GameTime, game_world: GameWorld):
        self.__current_action_index += 1
        if self.__current_action_index >= len(self.actions):
            self.is_interacted_with = False
            return
        self.__current_action_start_time = game_time.total_time
        self.current_action = self.actions[self.__current_action_index]
        self.current_action_type = self.current_action["action_type"]

        if self.current_action_type == "talk":
            self.ui_speech_box.show(self.current_action["text"])
