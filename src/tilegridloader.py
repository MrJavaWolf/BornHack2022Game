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
    height=1,
    width=1,
    default_tile=0,
    transparent_color=TRANSPARENT_COLOR,
):
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
