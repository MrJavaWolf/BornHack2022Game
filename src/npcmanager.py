from gamepad import Gamepad
from punchbagenemy import PunchBagEnemy
from gametime import GameTime
from gameworld import GameWorld
from dialognpc import DialogNpc
import displayio
import player


class NpcManager:

    def __init__(self):
        self.punch_bag_enemy = PunchBagEnemy(86, 64)
        self.dialog_npc = DialogNpc(35, 64)
        self.sprite = displayio.Group(scale=1)
        self.sprite.append(self.punch_bag_enemy.sprite)
        self.sprite.append(self.dialog_npc.sprite)
        self.sprite_ui = displayio.Group(scale=1)
        self.sprite_ui.append(self.dialog_npc.sprite_ui)

    def loop(self, game_time: GameTime, game_world: GameWorld, player: player.Player, gamepad: Gamepad):
        if self.punch_bag_enemy: 
            self.punch_bag_enemy.loop(game_time, game_world)

            if self.punch_bag_enemy.despawn: 
                self.sprite.remove(self.punch_bag_enemy.sprite)
                self.punch_bag_enemy = None
        
        self.dialog_npc.loop(game_time, game_world, gamepad)

    def get_damageable_npcs(self):
        damageable_npcs = []
        if self.punch_bag_enemy: 
            damageable_npcs.append(self.punch_bag_enemy)
        return damageable_npcs 
    
    
    def get_interactable_npcs(self):
        interactable_npcs = []
        interactable_npcs.append(self.dialog_npc)
        return interactable_npcs 
    
