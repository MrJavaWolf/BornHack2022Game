import displayio
from gametime import GameTime
from gameworld import GameWorld
from tileanimation import TileAnimation
from tilegridloader import import_tile_grid, TRANSPARENT_COLOR

ENEMY_MAX_SPEED = 50.0
ENEMY_MAX_HEALTH = 100.0
DEBUG_SHOW_ENEMY_POSITION = False # Shows the enemies exact position with a small dot

# Visuals
ENEMY_SPRITE = "/game_data/big-enemies.bmp"
ENEMY_SPRITE_TYPE = 0
ENEMY_SPRITE_OFFSET = {"x": -16, "y": -26}
ENEMY_SPRITE_TILE_SIZE = {"width": 32, "height": 36}
ENEMY_IDLE_ANIMATION = {"fps": 0.45, "frames": [1 + ENEMY_SPRITE_TYPE * 8, 2 + ENEMY_SPRITE_TYPE * 8]}
ENEMY_RUN_ANIMATION = {"fps": 0.15, "frames": [4, 7]}

# Take damange
TAKE_DAMAGE_WHITE_TIME = 0.2

class PunchBagEnemy:

    despawn: bool = False
    take_damanage_time: float = 0

    def __init__(self, position_x: float, position_y: float):
        # Setup        
        self.health = ENEMY_MAX_HEALTH
        self.position_x = position_x
        self.position_y = position_y
        
        # Visuals
        self.character_sprite = import_tile_grid(
            image_path = ENEMY_SPRITE, 
            tile_pixel_width = ENEMY_SPRITE_TILE_SIZE["width"], 
            tile_pixel_height = ENEMY_SPRITE_TILE_SIZE["height"]
        )
        self.character_sprite.x = ENEMY_SPRITE_OFFSET["x"]
        self.character_sprite.y = ENEMY_SPRITE_OFFSET["y"]
        self.idle_animation = TileAnimation(self.character_sprite, ENEMY_IDLE_ANIMATION["frames"], ENEMY_IDLE_ANIMATION["fps"])
        self.run_animation = TileAnimation(self.character_sprite, ENEMY_RUN_ANIMATION["frames"], ENEMY_RUN_ANIMATION["fps"])
        self.sprite = displayio.Group(scale=1)
        self.sprite.append(self.character_sprite)
        self.sprite.x = int(self.position_x)
        self.sprite.y = int(self.position_y)
        self.character_sprite.flip_x = True
        self.original_palette =  self.character_sprite.pixel_shader
        self.take_damange_palette = displayio.Palette(len(self.character_sprite.pixel_shader))
        for i, color in enumerate(self.character_sprite.pixel_shader):
            if color != TRANSPARENT_COLOR:
                self.take_damange_palette[i] = 0xFFFFFF
            else:
                self.take_damange_palette.make_transparent(i)

        # Debug show enemy center dot
        if DEBUG_SHOW_ENEMY_POSITION:
            color_bitmap = displayio.Bitmap(1, 1, 1)
            color_palette = displayio.Palette(1)
            color_palette[0] = 0xFF0000
            self.character_position = displayio.TileGrid(color_bitmap, pixel_shader=color_palette)
            self.sprite.append(self.character_position)
    
    def loop(self, game_time: GameTime, game_world: GameWorld):
        self.idle_animation.loop(game_time)
        if game_time.total_time - self.take_damanage_time > TAKE_DAMAGE_WHITE_TIME:
            self.character_sprite.pixel_shader = self.original_palette


    def take_damage(self, amount: float, game_time: GameTime):
        self.health -= amount
        if self.health <= 0:
            self.despawn = True
        else:
            self.take_damanage_time = game_time.total_time
            self.character_sprite.pixel_shader = self.take_damange_palette
