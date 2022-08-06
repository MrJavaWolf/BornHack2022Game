from characterrenderer import CharacterRenderer
import displayio
from adafruit_display_shapes.roundrect import RoundRect

from gamepad import Gamepad
from gamestate import GameState
from gametime import GameTime
from gameworld import GameWorld
# from player import Player
from tileanimation import TileAnimation
from imagemanager import ImageManager
from uispeechbox import UISpeechBox

DEBUG_SHOW_NPC_POSITION = False  # Shows the npc's exact position with a small dot

# Visuals


class InteractableNpc:

    position_x: float
    """The NPC's x position"""

    position_y: float
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
    idle_animation: TileAnimation = None
    run_animation: TileAnimation = None
    characer_renderer: CharacterRenderer = None

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
        self.sprite = displayio.Group()
        self.sprite.x = int(self.position_x)
        self.sprite.y = int(self.position_y)
        if npc_data["sprite_sheet"] is not None:
            self.characer_renderer = CharacterRenderer(
                image_manager,
                npc_data["sprite_sheet"],
                npc_data["sprite_sheet_tile_size"]["width"],
                npc_data["sprite_sheet_tile_size"]["height"],
                npc_data["sprite_offset"]["x"],
                npc_data["sprite_offset"]["y"],
                npc_data["animations"],
            )
            if npc_data["default_animation"] is not None:
                self.characer_renderer.play_animation(
                    npc_data["default_animation"])
            self.sprite.append(self.characer_renderer.sprite)
            self.characer_renderer.flip_x(npc_data["default_flip_x"])
            self.characer_renderer.flip_y(npc_data["default_flip_y"])

        # Debug show enemy center dot
        if DEBUG_SHOW_NPC_POSITION:
            color_bitmap = displayio.Bitmap(1, 1, 1)
            color_palette = displayio.Palette(1)
            color_palette[0] = 0xFF0000
            self.character_position = displayio.TileGrid(
                color_bitmap, pixel_shader=color_palette
            )
            self.sprite.append(self.character_position)

    def loop(self, game_state: GameState):

        if self.characer_renderer is not None:
            self.characer_renderer.loop(game_state.game_time)

        if self.is_interacted_with:
            self.interaction_loop(game_state)

    def interact(self, game_time: GameTime):
        self.is_interacted_with = True
        self.__current_action_index = -1

    def interaction_loop(
        self, game_state: GameState
    ):
        if not self.is_interacted_with:
            return

        if self.__current_action_index == -1:
            self.go_to_next_interaction(
                game_state.game_time, game_state.game_world)
            return

        if self.current_action_type == "wait":
            if (
                game_state.game_time.total_time - self.__current_action_start_time
                >= self.current_action["time"]
            ):
                self.go_to_next_interaction(
                    game_state.game_time, game_state.game_world)

        elif self.current_action_type == "change_world_tile":
            game_state.game_world.change_tile(
                self.current_action["tile_x"],
                self.current_action["tile_y"],
                self.current_action["to_tile_type"],
            )
            self.go_to_next_interaction(
                game_state.game_time, game_state.game_world)

        elif self.current_action_type == "camera_shake":
            time_eclipsed = game_state.game_time.total_time - self.__current_action_start_time
            if time_eclipsed < self.current_action["time"]:
                dampening = 1 - time_eclipsed / (
                    self.current_action["time"] *
                    self.current_action["decrease_factor"]
                )
                game_state.game_world.shake(
                    self.current_action["amount"] * dampening)
            else:
                game_state.game_world.shake(0)
                self.go_to_next_interaction(
                    game_state.game_time, game_state.game_world)

        elif self.current_action_type == "talk":
            if game_state.gamepad.button_X.on_press:
                self.ui_speech_box.hide()
                self.go_to_next_interaction(
                    game_state.game_time, game_state.game_world)

        elif self.current_action_type == "flip_sprite_x":
            if self.characer_renderer is not None:
                self.characer_renderer.flip_x(self.current_action["value"])

            self.go_to_next_interaction(
                game_state.game_time, game_state.game_world)

        elif self.current_action_type == "flip_sprite_y":
            if self.characer_renderer is not None:
                self.characer_renderer.flip_y(self.current_action["value"])
            self.go_to_next_interaction(
                game_state.game_time, game_state.game_world)

        elif self.current_action_type == "play_animation":
            if self.characer_renderer is not None:
                self.characer_renderer.play_animation(
                    self.current_action["animation"])
            self.go_to_next_interaction(
                game_state.game_time, game_state.game_world)
        elif self.current_action_type == "change_skin":
            game_state.player.set_player_sprite(self.current_action["skin"])
            self.go_to_next_interaction(
                game_state.game_time, game_state.game_world)
        else:
            self.go_to_next_interaction(
                game_state.game_time, game_state.game_world)

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
