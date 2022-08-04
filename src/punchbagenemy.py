import displayio
from gametime import GameTime
from gameworld import GameWorld
from imagemanager import ImageManager, TRANSPARENT_COLOR
from characterrenderer import CharacterRenderer
import player
import math
ENEMY_MAX_SPEED = 20.0
ENEMY_MAX_HEALTH = 50.0
DEBUG_SHOW_ENEMY_POSITION = True  # Shows the enemies exact position with a small dot

# Visuals
ENEMY_SPRITE = "/game_data/big_npc_2.bmp"
ENEMY_SPRITE_OFFSET = {"x": -16, "y": -18}
ENEMY_SPRITE_TILE_SIZE = {"width": 32, "height": 36}
ENEMY_IDLE_ANIMATION = {"name": "idle", "fps": 0.45, "frames": [0, 1]}
ENEMY_RUN_ANIMATION = {"name": "run", "fps": 0.15, "frames": [0, 4]}
ENEMY_ATTACK_ANIMATION = {"name": "attack", "fps": 0.3, "frames": [3, 5, 6, 7], "loop_animation": False}

# Take damange
TAKE_DAMAGE_WHITE_TIME = 0.2

# Attack
MAX_DISTANCE_TO_PLAYER = 100
START_ATTACK_DISTANCE_TO_PLAYER = 15
ATTACK_DISTANCE_TO_PLAYER = 18

ENEMY_ATTACK_TOTAL_TIME = 1.2
ENEMY_ATTACK_DAMAGE_TIME = 1
ENEMY_ATTACK_DAMAGE = 10


class PunchBagEnemy:

    is_dead: bool = False
    player_death_time: float = 0
    despawn: bool = False
    take_damanage_time: float = 0
    attack_start_time: float = 0
    is_attacking: bool = False
    have_dealt_damage: bool = False

    def __init__(
        self, image_manager: ImageManager, position_x: float, position_y: float
    ):
        # Setup
        self.health = ENEMY_MAX_HEALTH
        self.position_x = position_x
        self.position_y = position_y

        # Visuals
        self.characer_renderer = CharacterRenderer(
            image_manager,
            ENEMY_SPRITE,
            ENEMY_SPRITE_TILE_SIZE["width"],
            ENEMY_SPRITE_TILE_SIZE["height"],
            ENEMY_SPRITE_OFFSET["x"],
            ENEMY_SPRITE_OFFSET["y"],
            [ENEMY_IDLE_ANIMATION, ENEMY_RUN_ANIMATION, ENEMY_ATTACK_ANIMATION]
        )
        self.characer_renderer.flip_x(True)
        self.characer_renderer.play_animation("idle")

        self.sprite = displayio.Group()
        self.sprite.append(self.characer_renderer.sprite)
        self.sprite.x = int(self.position_x)
        self.sprite.y = int(self.position_y)
        
        self.bitmap_skull, self.palette_skull = image_manager.get_image("/game_data/items.bmp")
        self.skull_sprite = displayio.TileGrid(
            bitmap=self.bitmap_skull,
            pixel_shader=self.palette_skull,
            tile_width=16,
            tile_height=16,
            x=-8,
            y=-10,
        )
        self.skull_sprite[0] = 24

        # Debug show enemy center dot
        if DEBUG_SHOW_ENEMY_POSITION:
            color_bitmap = displayio.Bitmap(1, 1, 1)
            color_palette = displayio.Palette(1)
            color_palette[0] = 0xFF0000
            self.character_position = displayio.TileGrid(
                color_bitmap, pixel_shader=color_palette
            )
            self.sprite.append(self.character_position)

    def loop(
        self,
        game_time: GameTime,
        game_world: GameWorld,
        player: player.Player
    ):
        self.characer_renderer.loop(game_time)
        if self.is_dead:
            return
        if self.is_attacking: 
            self.attacking_loop(game_time, player)
        elif self.is_within_radius(START_ATTACK_DISTANCE_TO_PLAYER, player.position_x, player.position_y):
          self.start_attacking(game_time)
        elif self.is_within_radius(MAX_DISTANCE_TO_PLAYER, player.position_x, player.position_y):
           self.move_towards_player(game_time, player, game_world)
        else:
            if self.characer_renderer.get_current_animation_name() != "idle":
                self.characer_renderer.play_animation("idle")

    def move_towards_player(self, game_time: GameTime, player: player.Player, game_world: GameWorld):
        if self.characer_renderer.get_current_animation_name() != "run":
            self.characer_renderer.play_animation("run")
         
        direction_to_player_x = player.position_x - self.position_x
        direction_to_player_y = player.position_y - self.position_y 
        distance_to_player = math.sqrt((direction_to_player_x) ** 2 + (direction_to_player_y) ** 2)
        self.characer_renderer.flip_x(True if direction_to_player_x < 0 else False)
        
        # Normalizes the direction
        direction_to_player_x /= distance_to_player
        direction_to_player_y /= distance_to_player

        new_position_x = self.position_x + direction_to_player_x * ENEMY_MAX_SPEED *  game_time.delta_time
        new_position_y = self.position_y + direction_to_player_y * ENEMY_MAX_SPEED *  game_time.delta_time
        self.move_to_position(new_position_x, new_position_y, game_world)

    def start_attacking(self, game_time: GameTime):
        self.characer_renderer.play_animation("attack")
        self.is_attacking = True
        self.have_dealt_damage = False
        self.attack_start_time = game_time.total_time

    def attacking_loop(
        self,
        game_time: GameTime,
        player: player.Player):
        if game_time.total_time - self.attack_start_time > ENEMY_ATTACK_TOTAL_TIME:
            self.is_attacking = False
        
        if not self.have_dealt_damage and game_time.total_time - self.attack_start_time > ENEMY_ATTACK_DAMAGE_TIME:
            self.have_dealt_damage = True
            if self.is_within_radius(ATTACK_DISTANCE_TO_PLAYER, player.position_x, player.position_y):
                player.take_damage(ENEMY_ATTACK_DAMAGE, game_time)

    def is_within_radius(self, radius:float, position_x: float, position_y: float):
        square_dist = (self.position_x - position_x) ** 2 + (
            self.position_y - position_y
        ) ** 2
        return square_dist <= radius**2

    def take_damage(self, amount: float, game_time: GameTime):
        self.health -= amount
        if self.health <= 0:
            #self.despawn = True
            # change to item 55 on item map 3
            if not self.is_dead:
                self.sprite.append(self.skull_sprite)
                self.sprite.remove(self.characer_renderer.sprite)
                self.sprite.scale = 2
            self.is_dead = True
        else:
            self.take_damanage_time = game_time.total_time
            self.characer_renderer.play_white_out(game_time)


     ### Utility
    def move_to_position(
        self,
        x_position: float,
        y_position: float,
        game_world: GameWorld):
        
        if y_position < 0:
            y_position = 0
        if x_position < 0:
            x_position = 0
            self.position_x = x_position
            self.position_y = y_position
        if game_world.is_walkable(x_position, y_position):
            self.position_x = x_position
            self.position_y = y_position
        elif game_world.is_walkable(self.position_x, y_position): 
            self.position_y = y_position
        elif game_world.is_walkable(x_position, self.position_y):
            self.position_x = x_position
        self.sprite.x = int(self.position_x)
        self.sprite.y = int(self.position_y)