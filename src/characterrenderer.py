import displayio
from imagemanager import TRANSPARENT_COLOR, ImageManager
from tileanimation import TileAnimation
from gametime import GameTime

DEFAULT_WHITE_OUT_TIME = 0.2


class CharacterRenderer:
    character_sprite: displayio.TileGrid
    sprite: displayio.Group
    bitmap = None
    palette = None
    animations = None
    current_animation: TileAnimation = None
    white_out_palette: displayio.Palette = None
    white_out_end_time = 0

    def __init__(
        self,
        image_manager: ImageManager,
        sprite_sheet: str,
        tile_width: int,
        tile_height: int,
        offset_x: int,
        offset_y: int,
        animations,
    ):
        self.sprite = displayio.Group()
        # Load the sprite
        self.bitmap, self.palette = image_manager.get_image(sprite_sheet)
        self.character_sprite = displayio.TileGrid(
            bitmap=self.bitmap,
            pixel_shader=self.palette,
            tile_width=tile_width,
            tile_height=tile_height,
        )
        self.sprite.append(self.character_sprite)

        # Set offsets
        self.character_sprite.x = offset_x
        self.character_sprite.y = offset_y

        # Setup animations
        self.animations = {}
        for animation in animations:
            loop_animation = True
            if "loop_animation" in animation:
                loop_animation = animation["loop_animation"]
            self.animations[animation["name"]] = TileAnimation(
                name=animation["name"],
                tile_grid=self.character_sprite,
                frames=animation["frames"],
                speed=animation["fps"],
                loop_animation=loop_animation,
            )

        self.white_out_palette = displayio.Palette(
            len(self.character_sprite.pixel_shader)
        )
        for i, color in enumerate(self.character_sprite.pixel_shader):
            if color != TRANSPARENT_COLOR:
                self.white_out_palette[i] = 0xFFFFFF
            else:
                self.white_out_palette.make_transparent(i)


    def flip_x(self, flip: bool):
        self.character_sprite.flip_x = flip


    def is_x_flipped(self):
        return self.character_sprite.flip_x


    def flip_y(self, flip: bool):
        self.character_sprite.flip_y = flip


    def is_y_flipped(self):
        return self.character_sprite.flip_y


    def set_offset(self, x: int, y: int):
        self.character_sprite.x = x
        self.character_sprite.y = y


    def get_current_animation_name(self):
        if self.current_animation is not None:
            return self.current_animation.name
        return None


    def play_animation(self, animation_name: str):
        self.current_animation = self.animations[animation_name]
        self.current_animation.reset()

    def loop(self, game_time: GameTime):
        if self.current_animation is not None:
            self.current_animation.loop(game_time)

        if (
            self.character_sprite.pixel_shader == self.white_out_palette
            and game_time.total_time > self.white_out_end_time
        ):
            self.character_sprite.pixel_shader = self.palette


    def set_frame(self, frame_index: int):
        self.current_animation = None
        self.character_sprite[0] = frame_index


    def play_white_out(self, game_time: GameTime, time: float = DEFAULT_WHITE_OUT_TIME):
        self.white_out_end_time = game_time.total_time + time
        self.character_sprite.pixel_shader = self.white_out_palette
