"""Small Cairo drawing vocabulary, with original path coordinates in the scene modules."""

import ctypes as ct
import ctypes.util
from functools import lru_cache
from contextlib import contextmanager
import math
import re
import os
import numpy as np
from PIL import Image, ImageFont, ImageDraw

W, H = 768, 432
TAU = 2 * math.pi
sin, cos, pi = math.sin, math.cos, math.pi
lib = ct.CDLL(ctypes.util.find_library("cairo") or "/opt/homebrew/lib/libcairo.dylib")
P, D, I = ct.c_void_p, ct.c_double, ct.c_int


def bind(name, result, *args):
    fn = getattr(lib, "cairo_" + name)
    fn.restype = result
    fn.argtypes = args
    return fn


make = bind("image_surface_create_for_data", P, P, I, I, I, I)
context = bind("create", P, P)
destroy = bind("destroy", None, P)
free = bind("surface_destroy", None, P)
api = {}
for name, args in {
    "save": "",
    "restore": "",
    "move_to": "dd",
    "line_to": "dd",
    "curve_to": "dddddd",
    "arc": "ddddd",
    "close_path": "",
    "new_path": "",
    "fill": "",
    "fill_preserve": "",
    "clip": "",
    "stroke": "",
    "rectangle": "dddd",
    "set_source_rgba": "dddd",
    "set_line_width": "d",
    "paint": "",
    "translate": "dd",
    "rotate": "d",
    "scale": "dd",
    "set_line_join": "i",
    "set_line_cap": "i",
    "set_fill_rule": "i",
    "set_source_surface": "pdd",
}.items():
    api[name] = bind(name, None, P, *[{"d": D, "i": I, "p": P}[k] for k in args])


def clamp(x):
    return max(0, min(1, x))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def mix(a, b, t):
    return a + (b - a) * t


@lru_cache(maxsize=16000)
def color(s):
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(i * 2 for i in s)
    return tuple(int(s[i : i + 2], 16) / 255 for i in (0, 2, 4))


def blend(a, b, t):
    return "".join(
        f"{round(255 * mix(i, j, clamp(t))):02x}" for i, j in zip(color(a), color(b))
    )


@lru_cache(maxsize=160)
def font(size, bold, serif):
    path = os.environ.get("ASTRA_FONT") or (
        "/System/Library/Fonts/Supplemental/AppleMyungjo.ttf"
        if serif
        else "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    )
    return ImageFont.truetype(
        path,
        size,
        index=0 if serif or os.environ.get("ASTRA_FONT") else (6 if bold else 0),
    )


@lru_cache(maxsize=600)
def lettering(s, size, ink, bold, serif):
    f = font(size, bold, serif)
    x0, y0, x1, y1 = f.getbbox(s)
    w, h = max(1, x1 - x0 + 4), max(1, y1 - y0 + 4)
    mask = Image.new("L", (w, h))
    ImageDraw.Draw(mask).text((2 - x0, 2 - y0), s, font=f, fill=255)
    a = np.array(mask)
    buf = np.zeros((h, w, 4), np.uint8)
    for i, c in enumerate(reversed(color(ink))):
        buf[:, :, i] = a * c
    buf[:, :, 3] = a
    return buf


@lru_cache(maxsize=4096)
def parse(s):
    return re.findall(r"[MLQCZ]|-?\d*\.?\d+", s)


class Canvas:
    def __init__(self):
        self.buf = np.zeros((H, W, 4), np.uint8)
        self.surface = make(self.buf.ctypes.data, 0, W, H, W * 4)
        self.c = context(self.surface)
        api["set_line_join"](self.c, 1)
        api["set_line_cap"](self.c, 1)
        api["set_fill_rule"](self.c, 1)

    def close(self):
        destroy(self.c)
        free(self.surface)

    def call(self, k, *v):
        api[k](self.c, *v)

    @contextmanager
    def transform(self, x=0, y=0, scale=1, rot=0, sy=None):
        self.call("save")
        self.call("translate", x, y)
        self.call("rotate", rot)
        self.call("scale", scale, scale if sy is None else sy)
        try:
            yield
        finally:
            self.call("restore")

    @contextmanager
    def window(self, x, y, w, h):
        self.call("save")
        self.call("rectangle", x, y, w, h)
        self.call("clip")
        try:
            yield
        finally:
            self.call("restore")

    def ink(self, col, alpha=1):
        self.call("set_source_rgba", *color(col), alpha)

    def finish(self, fill, stroke, width, alpha):
        if fill:
            self.ink(fill, alpha)
            self.call("fill_preserve" if stroke else "fill")
        if stroke:
            self.ink(stroke, alpha)
            self.call("set_line_width", width)
            self.call("stroke")

    def rect(self, x, y, w, h, col, stroke=None, width=1, a=1):
        self.call("rectangle", x, y, w, h)
        self.finish(col, stroke, width, a)

    def bg(self, col):
        self.rect(0, 0, W, H, col)

    def path(self, s, fill=None, stroke=None, width=1, a=1):
        seq = iter(parse(s))
        x = y = 0
        for v in seq:
            if v == "Z":
                self.call("close_path")
                continue
            n = {"M": 2, "L": 2, "Q": 4, "C": 6}[v]
            p = [float(next(seq)) for _ in range(n)]
            if v == "Q":
                q, r, e, f = p
                self.call(
                    "curve_to",
                    (x + 2 * q) / 3,
                    (y + 2 * r) / 3,
                    (e + 2 * q) / 3,
                    (f + 2 * r) / 3,
                    e,
                    f,
                )
            else:
                self.call({"M": "move_to", "L": "line_to", "C": "curve_to"}[v], *p)
            x, y = p[-2:]
        self.finish(fill, stroke, width, a)

    def poly(self, points, fill=None, stroke=None, width=1, a=1, closed=True):
        for i, (x, y) in enumerate(points):
            self.call("move_to" if i == 0 else "line_to", x, y)
        if closed:
            self.call("close_path")
        self.finish(fill, stroke, width, a)

    def line(self, points, col, w=1, a=1):
        self.poly(points, None, col, w, a, False)

    def ellipse(self, x, y, rx, ry, fill=None, stroke=None, width=1, a=1):
        if rx <= 0 or ry <= 0:
            return
        self.call("save")
        self.call("translate", x, y)
        self.call("scale", rx, ry)
        self.call("arc", 0, 0, 1, 0, TAU)
        self.call("restore")
        self.finish(fill, stroke, width, a)

    def circle(self, x, y, r, fill=None, stroke=None, width=1, a=1):
        self.ellipse(x, y, r, r, fill, stroke, width, a)

    def txt(self, s, x, y, size, col, bold=False, serif=False, center=False):
        buf = lettering(str(s), int(size), col, bold, serif)
        h, w = buf.shape[:2]
        surf = make(buf.ctypes.data, 0, w, h, w * 4)
        self.call("save")
        self.call("set_source_surface", surf, x - w / 2 if center else x, y)
        self.call("paint")
        self.call("restore")
        free(surf)

    def gradient(self, top, bottom, y=0, h=432):
        for i in range(48):
            self.rect(0, y + h * i / 48, W, h / 48 + 1, blend(top, bottom, i / 47))

    def arc(self, x, y, r, start, end, col, w=1):
        if end <= start:
            return
        self.call("arc", x, y, r, start, end)
        self.finish(None, col, w, 1)


def progress(points, f):
    if not points:
        return []
    pos = clamp(f) * (len(points) - 1)
    i = int(pos)
    if i == len(points) - 1:
        return points
    return points[: i + 1] + [
        (
            mix(points[i][0], points[i + 1][0], pos - i),
            mix(points[i][1], points[i + 1][1], pos - i),
        )
    ]


def rose(x, y, r, n, phase=0):
    return [
        (
            x + cos(a) * r * (0.74 + 0.26 * cos(n * a)),
            y + sin(a) * r * (0.74 + 0.26 * cos(n * a)),
        )
        for a in np.linspace(phase, TAU + phase, 120)
    ]


def spool(x, y, r, n=80):
    return [(x + r * cos(TAU * i / n), y + r * sin(TAU * i / n)) for i in range(n + 1)]


def rnd(seed):
    return np.random.default_rng(seed)
