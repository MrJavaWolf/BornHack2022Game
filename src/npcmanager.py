from punchbagenemy import PunchBagEnemy
from gametime import GameTime
from gameworld import GameWorld
import displayio
import player

class NpcManager:

    def __init__(self):
        self.punch_bag_enemy = PunchBagEnemy(86, 64)
        self.sprite = displayio.Group(scale=1)
        self.sprite.append(self.punch_bag_enemy.sprite)

    def loop(self, game_time: GameTime, game_world: GameWorld, player: player.Player):
        if self.punch_bag_enemy: 
            self.punch_bag_enemy.loop(game_time, game_world)

            if self.punch_bag_enemy.despawn: 
                self.sprite.remove(self.punch_bag_enemy.sprite)
                self.punch_bag_enemy = None

    def get_damageable_npcs(self):
        damageable_npcs = []
        if self.punch_bag_enemy: 
            damageable_npcs.append(self.punch_bag_enemy)
        return damageable_npcs 
    
