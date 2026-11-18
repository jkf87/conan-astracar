"""Paint the generated character art into a clipped part of a film frame."""

from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image
from draw import C, ffi

ASSETS = Path(__file__).resolve().parent / "art"


@lru_cache(maxsize=8)
def load_plate(slug, region=None):
    with Image.open(ASSETS / f"{slug}.png") as im:
        im = im.convert("RGBA")
        if region in ("left", "right"):
            x = 0 if region == "left" else im.width // 2
            im = im.crop((x, 0, x + im.width // 2, im.height))
        if region is not None:
            bounds = im.getchannel("A").point(lambda x: 255 if x > 20 else 0).getbbox()
            if bounds:
                im = im.crop(bounds)
        rgba = np.asarray(im)
    pixels = np.ascontiguousarray(rgba[:, :, [2, 1, 0, 3]])
    pixels[:, :, :3] = np.rint(pixels[:, :, :3] * (pixels[:, :, 3:4] / 255)).astype(
        np.uint8
    )
    height, width = pixels.shape[:2]
    surface = ffi.gc(
        C.cairo_image_surface_create_for_data(
            ffi.from_buffer(pixels), 0, width, height, width * 4
        ),
        C.cairo_surface_destroy,
    )
    return surface, pixels, width, height


def plate(d, slug, box, zoom=1, focus=(0.5, 0.5)):
    surface, buffer, width, height = load_plate(slug)
    x, y, w, h = box
    factor = max(w / width, h / height) * zoom
    left, top = (
        x - (width * factor - w) * focus[0],
        y - (height * factor - h) * focus[1],
    )
    C.cairo_save(d.c)
    C.cairo_rectangle(d.c, x, y, w, h)
    C.cairo_clip(d.c)
    with d.at(left, top, factor):
        C.cairo_set_source_surface(d.c, surface, 0, 0)
        C.cairo_paint(d.c)
    C.cairo_restore(d.c)


def sprite(d, slug, region, width):
    """Draw an alpha-trimmed character centered around the current origin."""
    surface, buffer, w, h = load_plate(slug, region)
    factor = width / w
    with d.at(-width / 2, -h * factor / 2, factor):
        C.cairo_set_source_surface(d.c, surface, 0, 0)
        C.cairo_paint(d.c)
