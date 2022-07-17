# https://learn.adafruit.com/circuitpython-display-support-using-displayio/tilegrid-and-group
# https://circuitpython-jake.readthedocs.io/en/latest/shared-bindings/displayio/TileGrid.html#displayio.TileGrid
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/sprite-sheet
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/multiple-tilegrids

import adafruit_imageload
import displayio

TRANSPARENT_COLOR = 0xFF00FF


def import_tile_grid(
    image_path,
    tile_pixel_width,
    tile_pixel_height,
    width=1,
    height=1,
    default_tile=0,
    transparent_color=TRANSPARENT_COLOR,
):
    """
    Import a sprite sheet into a tile grid.
    This import can make specific colors transparent.
    For a better understanding of how tile grids work, please see the links at the top of the file

    Args:
        image_path: The path to the sprite sheet image (.bmp) to load
        tile_pixel_width: The width of a tile in pixel
        tile_pixel_heigh: The height of a tile in pixel
        width: The number of tiles the created tile grid will have in the x direction
        height: The number of tiles the created tile grid will have in the y direction
        default_tile: Default tile index to show in the created tile grid
        transparent_color: Make a specific color in your sprite sheet transparent. Usefull for characters and props. Set to None to not make any colors transparent
    """
    # Loads the image
    bitmap, palette = adafruit_imageload.load(image_path)

    # Marks colors which are 'transparent_color' actually transparent
    for i in range(len(palette)):
        if palette[i] == transparent_color:
            palette.make_transparent(i)

    # Makes the tile grid
    return displayio.TileGrid(
        bitmap=bitmap,
        pixel_shader=palette,
        width=width,
        height=height,
        tile_width=tile_pixel_width,
        tile_height=tile_pixel_height,
        default_tile=default_tile,
    )
