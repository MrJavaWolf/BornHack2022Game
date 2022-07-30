from gamepad import Gamepad
from punchbagenemy import PunchBagEnemy
from gametime import GameTime
from gameworld import GameWorld
from interactable_npc import InteractableNpc
from imagemanager import ImageManager
import displayio
import player
import interactable_npc_data
from uispeechbox import UISpeechBox


class NpcManager:
    def __init__(self, image_manager: ImageManager, ui_speech_box: UISpeechBox):
        self.punch_bag_enemy = PunchBagEnemy(image_manager, 86, 64)
        self.sprite = displayio.Group(scale=1)
        self.sprite.append(self.punch_bag_enemy.sprite)

        # Initialize interactable npcs
        self.interactable_npcs = []
        for npc in interactable_npc_data.interactable_npcs:
            new_npc = InteractableNpc(image_manager, ui_speech_box, npc)
            self.interactable_npcs.append(new_npc)
            self.sprite.append(new_npc.sprite)

    def loop(
        self,
        game_time: GameTime,
        game_world: GameWorld,
        player: player.Player,
        gamepad: Gamepad,
    ):
        if self.punch_bag_enemy:
            self.punch_bag_enemy.loop(game_time, game_world)

            if self.punch_bag_enemy.despawn:
                self.sprite.remove(self.punch_bag_enemy.sprite)
                self.punch_bag_enemy = None

        for interactable_npc in self.interactable_npcs:
            interactable_npc.loop(game_time, game_world, gamepad)

    def get_damageable_npcs(self):
        damageable_npcs = []
        if self.punch_bag_enemy:
            damageable_npcs.append(self.punch_bag_enemy)
        return damageable_npcs

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
