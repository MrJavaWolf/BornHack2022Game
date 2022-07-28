import math
from gamepad import Gamepad
import displayio
from gametime import GameTime
from gameworld import GameWorld
from tileanimation import TileAnimation
from tilegridloader import import_tile_grid
import Tween.Tween
import npcmanager

# Visuals
PLAYER_SPRITE_TYPE = 3
NUMBER_OF_SPRITES = 9
SPRITE_INDEX_OFFSET = PLAYER_SPRITE_TYPE * NUMBER_OF_SPRITES
PLAYER_SPRITE = "/game_data/characters.bmp"
PLAYER_SPRITE_OFFSET = {"x": -8, "y": -29}
PLAYER_SPRITE_TILE_SIZE = {"width": 16, "height": 32}
PLAYER_IDLE_ANIMATION = {"fps": 0.5, "frames": [0 + SPRITE_INDEX_OFFSET, 1 + SPRITE_INDEX_OFFSET]}
PLAYER_RUN_ANIMATION = {"fps": 0.15, "frames": [4 + SPRITE_INDEX_OFFSET, 7 + SPRITE_INDEX_OFFSET]}

# Generel 
PLAYER_MAX_SPEED = 50.0
PLAYER_MAX_HEALTH = 100.0
DEBUG_SHOW_PLAYER_POSITION = False # Shows the players exact position with a small dot

# Dash
PLAYER_DASH_SPEED = 275
PLAYER_DASH_DURATION = 0.15
PLAYER_DASH_RECOVERY_TIME = 0.2

# Attack
PLAYER_ATTACK_DURATION = 0.1
PLAYER_ATTACK_RECOVERY_TIME = 0.1
PLAYER_ATTACK_COOLDOWN = 0.2
PLAYER_ATTACK_DAMAGE = 5
PLAYER_ATTACK_RANGE = 25

class Player:

    health: float = 50
    """The amount of health the player currently has"""

    position_x: float = 0
    """The players X position"""

    position_y: float = 0
    """The players Y position"""

    __buffered_action: str = None

    # Dashing
    __is_dashing: bool = False
    __dash_start_time: float = 0
    __dash_direction_x: float = 1
    __dash_direction_y: float = 0
    
    # Attacking
    __is_attacking: bool = False
    __attack_start_time: float = 0

    def __init__(self, position_x: float, position_y: float):
        self.health = PLAYER_MAX_HEALTH
        self.position_x = position_x
        self.position_y = position_y
        self.interacting_with_npc = None
        # Visuals
        self.character_sprite = import_tile_grid(
            image_path = PLAYER_SPRITE, 
            tile_pixel_width = PLAYER_SPRITE_TILE_SIZE["width"], 
            tile_pixel_height = PLAYER_SPRITE_TILE_SIZE["height"]
        )
        self.character_sprite.x = PLAYER_SPRITE_OFFSET["x"]
        self.character_sprite.y = PLAYER_SPRITE_OFFSET["y"]
        self.idle_animation = TileAnimation(self.character_sprite, PLAYER_IDLE_ANIMATION["frames"], PLAYER_IDLE_ANIMATION["fps"])
        self.run_animation = TileAnimation(self.character_sprite, PLAYER_RUN_ANIMATION["frames"], PLAYER_RUN_ANIMATION["fps"])
        self.sprite = displayio.Group(scale=1)
        self.sprite.append(self.character_sprite)
        self.sprite.x = int(self.position_x)
        self.sprite.y = int(self.position_y)

        # Visuals - Attack
        self.player_attack_sprite = import_tile_grid("/game_data/attack-slash.bmp", 36, 16)

        # Debug show player center dot
        if DEBUG_SHOW_PLAYER_POSITION:
            color_bitmap = displayio.Bitmap(1, 1, 1)
            color_palette = displayio.Palette(1)
            color_palette[0] = 0xFF0000
            self.character_position = displayio.TileGrid(color_bitmap, pixel_shader=color_palette)
            self.sprite.append(self.character_position)


    def loop(self, gamepad: Gamepad, game_time: GameTime, game_world: GameWorld, npc_manager: npcmanager.NpcManager):
        # Is interacting with an NPC (like talking)
        if self.interacting_with_npc is not None:
            if self.interacting_with_npc.is_interacted_with:
                return
            else:
                self.interacting_with_npc = None

        # Dash
        if (gamepad.button_B.on_press or self.__buffered_action == "dash") and not self.__is_dashing and not self.__is_attacking:
            self.start_dash(gamepad, game_time)
        elif self.__is_dashing:
            self.dash_loop(game_world, game_time)
            if gamepad.button_B.on_press:
                self.__buffered_action = "dash"
            elif gamepad.button_X.on_press:
                self.__buffered_action = "attack"

        # Attack
        elif self.can_attack(gamepad, game_time):
            self.start_attack(gamepad, game_time, npc_manager)
        elif (gamepad.button_X.on_press) and not self.__is_attacking:
            self.__buffered_action = "attack"
        elif self.__is_attacking:
            self.attack_loop(game_world, game_time)
            if gamepad.button_B.on_press:
                self.__buffered_action = "dash"
            elif gamepad.button_X.on_press:
                self.__buffered_action = "attack"

        # Run
        elif gamepad.analog_X != 0 or gamepad.analog_Y != 0:
            self.run(gamepad, game_time, game_world)

        # Idle
        else:
            self.idle_animation.loop(game_time)
            

    ### Attacking
    def can_attack(self, gamepad: Gamepad, game_time: GameTime):
        return \
            (gamepad.button_X.on_press or self.__buffered_action == "attack") and \
            not self.__is_attacking and \
            not self.__is_dashing and \
            game_time.total_time - self.__attack_start_time > PLAYER_ATTACK_DURATION + PLAYER_ATTACK_RECOVERY_TIME + PLAYER_ATTACK_COOLDOWN

    def start_attack(self, gamepad: Gamepad, game_time: GameTime, npc_manager: npcmanager.NpcManager):
        """Called on the first frame of the attack"""

        # Deal damange to enemies
        damageable_npcs = npc_manager.get_damageable_npcs()
        for damageable_npc in damageable_npcs:
            if self.can_hit(gamepad, damageable_npc.position_x,damageable_npc.position_y):
                damageable_npc.take_damage(PLAYER_ATTACK_DAMAGE, game_time)
        
        # Interactable NPC's
        interactable_npcs = npc_manager.get_interactable_npcs()
        for interactable_npc in interactable_npcs:
            if self.can_hit(gamepad, interactable_npc.position_x,interactable_npc.position_y):
                interactable_npc.interact(game_time)
                self.interacting_with_npc = interactable_npc
                self.character_sprite[0] = 0 + SPRITE_INDEX_OFFSET
                self.__buffered_action = None
                return

        # state
        self.__buffered_action = None
        self.__is_attacking = True
        self.__attack_start_time = game_time.total_time
        
        # Attack sprite
        if gamepad.analog_X != 0:
            self.character_sprite.flip_x = True if gamepad.analog_X < 0 else False
        self.character_sprite[0] = 7 + SPRITE_INDEX_OFFSET
        self.player_attack_sprite[0] = 0
        self.player_attack_sprite.flip_x = self.character_sprite.flip_x
        self.player_attack_sprite.flip_y = True if gamepad.analog_Y < 0 else False 
        self.player_attack_sprite.y = -15 if gamepad.analog_Y < 0 else -10
        if self.player_attack_sprite.flip_x:
            self.player_attack_sprite.x = -20
        else:
            self.player_attack_sprite.x = -15
        self.sprite.append(self.player_attack_sprite)

    def attack_loop(self, gamepad: Gamepad, game_time: GameTime):
        """Called continuesly untill the attack is done"""

        if game_time.total_time - self.__attack_start_time > PLAYER_ATTACK_DURATION + PLAYER_ATTACK_RECOVERY_TIME:
            self.sprite.remove(self.player_attack_sprite)
            self.__is_attacking = False
            return

        if game_time.total_time - self.__attack_start_time > PLAYER_ATTACK_DURATION:
            self.player_attack_sprite[0] = 2
            return

        elif game_time.total_time - self.__attack_start_time > 0.05:
            self.player_attack_sprite[0] = 1
            return

    def can_hit(self, gamepad: Gamepad, position_x: float, position_y: float):
        square_dist = (self.position_x - position_x) ** 2 + (self.position_y - position_y) ** 2
        return square_dist <= PLAYER_ATTACK_RANGE ** 2

### Dashing
    def start_dash(self, gamepad: Gamepad, game_time: GameTime):
        """Called on the first frame of the dash"""

        self.__buffered_action = None
        self.__dash_start_time = game_time.total_time
        self.__is_dashing = True
        self.character_sprite[0] = 5 + SPRITE_INDEX_OFFSET
        if gamepad.analog_X == 0 and gamepad.analog_Y == 0:
            self.__dash_direction_x = -1 if self.character_sprite.flip_x else 1
            self.__dash_direction_y = 0
        else:
            length = math.sqrt(gamepad.analog_X * gamepad.analog_X + gamepad.analog_Y * gamepad.analog_Y)
            self.__dash_direction_x = gamepad.analog_X / length
            self.__dash_direction_y = gamepad.analog_Y / length

    def dash_loop(self, game_world: GameWorld, game_time: GameTime):
        """Called continuesly untill the dash is done"""
        if game_time.total_time - self.__dash_start_time > PLAYER_DASH_DURATION + PLAYER_DASH_RECOVERY_TIME:
            self.__is_dashing = False
            return
        
        if game_time.total_time - self.__dash_start_time < PLAYER_DASH_DURATION:
            progress = (game_time.total_time - self.__dash_start_time) / PLAYER_DASH_DURATION
            tween_value = Tween.Tween.sineout(progress)
            speed = tween_value * PLAYER_DASH_SPEED
            new_x_position = self.position_x + self.__dash_direction_x * speed * game_time.delta_time        
            new_y_position = self.position_y + self.__dash_direction_y * speed * game_time.delta_time
            self.move_to_position(new_x_position, new_y_position, game_world)
        elif game_time.total_time - self.__dash_start_time < PLAYER_DASH_DURATION + 0.1:
            self.character_sprite[0] = 2 + SPRITE_INDEX_OFFSET
        else:
            self.character_sprite[0] = 3 + SPRITE_INDEX_OFFSET

### Running
    def run(self, gamepad: Gamepad, game_time: GameTime, game_world: GameWorld):
        new_x_position = (
            self.position_x
            + gamepad.analog_X * PLAYER_MAX_SPEED * game_time.delta_time
        )
        new_y_position = (
            self.position_y
            + gamepad.analog_Y * PLAYER_MAX_SPEED * game_time.delta_time
        )
        self.move_to_position(new_x_position, new_y_position, game_world)
        self.character_sprite.flip_x = True if gamepad.analog_X < 0 else False
        self.run_animation.loop(game_time)

### Utility
    def move_to_position(self, x_position: float, y_position: float, game_world: GameWorld):
        if y_position < 0:
            y_position = 0
        if x_position < 0:
            x_position = 0
        if game_world.is_walkable(x_position, y_position):
            self.position_x = x_position
            self.position_y = y_position
        elif game_world.is_walkable(self.position_x, y_position):
            self.position_y = y_position
        elif game_world.is_walkable(x_position, self.position_y):
            self.position_x = x_position

        self.sprite.x = int(self.position_x)
        self.sprite.y = int(self.position_y)