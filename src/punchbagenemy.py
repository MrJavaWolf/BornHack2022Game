import displayio
from gametime import GameTime
from gameworld import GameWorld
from imagemanager import ImageManager, TRANSPARENT_COLOR
from characterrenderer import CharacterRenderer

ENEMY_MAX_SPEED = 50.0
ENEMY_MAX_HEALTH = 100.0
DEBUG_SHOW_ENEMY_POSITION = False  # Shows the enemies exact position with a small dot

# Visuals
ENEMY_SPRITE = "/game_data/big_npc_2.bmp"
ENEMY_SPRITE_OFFSET = {"x": -16, "y": -26}
ENEMY_SPRITE_TILE_SIZE = {"width": 32, "height": 36}
ENEMY_IDLE_ANIMATION = {"name": "idle", "fps": 0.45, "frames": [1, 2]}
ENEMY_RUN_ANIMATION = {"name": "run", "fps": 0.15, "frames": [4, 7]}

# Take damange
TAKE_DAMAGE_WHITE_TIME = 0.2


class PunchBagEnemy:

    despawn: bool = False
    take_damanage_time: float = 0

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
            [ENEMY_IDLE_ANIMATION, ENEMY_RUN_ANIMATION]
        )
        self.characer_renderer.flip_x(True)
        self.characer_renderer.play_animation("idle")

        self.sprite = displayio.Group()
        self.sprite.append(self.characer_renderer.sprite)
        self.sprite.x = int(self.position_x)
        self.sprite.y = int(self.position_y)

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
    ):
        self.characer_renderer.loop(game_time)

    def take_damage(self, amount: float, game_time: GameTime):
        self.health -= amount
        if self.health <= 0:
            self.despawn = True
        else:
            self.take_damanage_time = game_time.total_time
            self.characer_renderer.play_white_out(game_time)
