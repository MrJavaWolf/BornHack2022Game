from gamepad import Gamepad
from enemy import Enemy
from gametime import GameTime
from gameworld import GameWorld
from interactable_npc import InteractableNpc
from imagemanager import ImageManager
import displayio
import interactable_npc_data
from uispeechbox import UISpeechBox
from gamestate import GameState


class NpcManager:
    def __init__(self, image_manager: ImageManager, ui_speech_box: UISpeechBox):
        self.sprite = displayio.Group(scale=1)

        # Enemies
        self.enemies = []
        self.enemies.append(Enemy(image_manager, 594, 64, self))
        self.enemies.append(Enemy(image_manager, 544, 64, self))
        self.enemies.append(Enemy(image_manager, 200, 32, self))

        for enemy in self.enemies:
            self.sprite.append(enemy.sprite)

        # Initialize interactable npcs
        self.interactable_npcs = []
        for npc in interactable_npc_data.interactable_npcs:
            new_npc = InteractableNpc(image_manager, ui_speech_box, npc)
            self.interactable_npcs.append(new_npc)
            self.sprite.append(new_npc.sprite)

    def loop(
        self,
        game_state: GameState,
    ):
        for enemy in self.enemies:
            enemy.loop(game_state)

        for interactable_npc in self.interactable_npcs:
            interactable_npc.loop(game_state)

    def get_damageable_npcs(self):
        return self.enemies

    def get_interactable_npcs(self):
        return self.interactable_npcs

    def is_walkable(self, world_x: float, world_y: float):
        for npc in self.interactable_npcs:
            if self.is_within_npc(
                npc.position_x,
                npc.position_y,
                npc.collision_size_width,
                npc.collision_size_height,
                world_x,
                world_y,
            ):
                return False
        return True

    def is_walkable_enemy(self, world_x: float, world_y: float, ignore: Enemy):
        for npc in self.enemies:
            if npc == ignore:
                continue
            if self.is_within_npc(
                npc.position_x,
                npc.position_y,
                npc.collision_size_width,
                npc.collision_size_height,
                world_x,
                world_y,
            ):
                return False
        return True

    def is_within_npc(
        self,
        npc_x: float,
        npc_y: float,
        collision_size_width: float,
        collision_size_height: float,
        player_x: float,
        player_y: float,
    ):
        return npc_x - collision_size_width / 2 <= player_x <= npc_x + collision_size_width and \
            npc_y - collision_size_height / 2 <= player_y <= npc_y + collision_size_height
