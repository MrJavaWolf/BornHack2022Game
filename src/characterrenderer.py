import displayio
from imagemanager import ImageManager
from tileanimation import TileAnimation

class CharacterRenderer:
    character_sprite: displayio.TileGrid
    sprite: displayio.Group

    def __init__(self, 
        image_manager:ImageManager, 
        sprite_sheet:str,
        tile_width:int,
        tile_height:int,
        offset_x:int,
        offset_y:int,
        idle_animation,
        run_animation,
        ):
        self.sprite = displayio.Group(scale=1)
        self.sprite.x = int(self.position_x)
        self.sprite.y = int(self.position_y)
        self.bitmap, self.palette = image_manager.get_image(sprite_sheet)
        self.character_sprite = displayio.TileGrid(
            bitmap=self.bitmap,
            pixel_shader=self.palette,
            tile_width=tile_width,
            tile_height=tile_height,
        )

        self.character_sprite.x = offset_x
        self.character_sprite.y = offset_y
        self.idle_animation = TileAnimation(
            self.character_sprite,
            idle_animation["frames"],
            idle_animation["fps"],
        )
        self.run_animation = TileAnimation(
            self.character_sprite,
            run_animation["frames"],
            run_animation["fps"],
        )
        self.sprite.append(self.character_sprite)
