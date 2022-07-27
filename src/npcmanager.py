from punchbagenemy import PunchBagEnemy
from gametime import GameTime
from gameworld import GameWorld
import displayio

class NpcManager:


    def __init__(self):
        self.punch_bag_enemy = PunchBagEnemy(86, 64)
        self.sprite = displayio.Group(scale=1)
        self.sprite.append(self.punch_bag_enemy.sprite)

    def loop(self, game_time: GameTime, game_world: GameWorld):
        self.punch_bag_enemy.loop(game_time, game_world)
