"""Small immediate-mode drawing desk. Coordinates are in a 768 × 432 film gate."""

import math, re, os, random
from ctypes.util import find_library
from functools import lru_cache
from contextlib import contextmanager
from cffi import FFI
import numpy as np
from PIL import Image, ImageFont, ImageDraw

ffi = FFI()
ffi.cdef("""
typedef void cairo_t; typedef void cairo_surface_t; typedef void cairo_pattern_t;
cairo_surface_t *cairo_image_surface_create(int,int,int);
unsigned char *cairo_image_surface_get_data(cairo_surface_t *);
void cairo_surface_flush(cairo_surface_t *); void cairo_surface_mark_dirty(cairo_surface_t *);
void cairo_surface_destroy(cairo_surface_t *); cairo_t *cairo_create(cairo_surface_t *);
void cairo_destroy(cairo_t *); void cairo_save(cairo_t *); void cairo_restore(cairo_t *);
void cairo_translate(cairo_t *,double,double); void cairo_scale(cairo_t *,double,double); void cairo_rotate(cairo_t *,double);
void cairo_new_path(cairo_t *); void cairo_close_path(cairo_t *); void cairo_move_to(cairo_t *,double,double);
void cairo_line_to(cairo_t *,double,double); void cairo_curve_to(cairo_t *,double,double,double,double,double,double);
void cairo_arc(cairo_t *,double,double,double,double,double); void cairo_rectangle(cairo_t *,double,double,double,double);
void cairo_set_line_width(cairo_t *,double); void cairo_set_line_cap(cairo_t *,int); void cairo_set_line_join(cairo_t *,int);
void cairo_stroke(cairo_t *); void cairo_fill(cairo_t *); void cairo_fill_preserve(cairo_t *); void cairo_clip(cairo_t *);
void cairo_set_source_rgba(cairo_t *,double,double,double,double); void cairo_set_source(cairo_t *,cairo_pattern_t *);
cairo_pattern_t *cairo_pattern_create_linear(double,double,double,double);
cairo_pattern_t *cairo_pattern_create_radial(double,double,double,double,double,double);
void cairo_pattern_add_color_stop_rgba(cairo_pattern_t *,double,double,double,double,double);
void cairo_pattern_destroy(cairo_pattern_t *); void cairo_paint(cairo_t *);
void cairo_set_source_surface(cairo_t *,cairo_surface_t *,double,double);
cairo_surface_t *cairo_image_surface_create_for_data(unsigned char *,int,int,int,int);
""")
C = ffi.dlopen(find_library("cairo") or "/opt/homebrew/lib/libcairo.dylib")
tau = math.tau
sin, cos, pi, sqrt = math.sin, math.cos, math.pi, math.sqrt


def clamp(x, a=0, b=1):
    return max(a, min(x, b))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def mix(a, b, u):
    return a + (b - a) * u


def span(t, a, b):
    return ease((t - a) / (b - a))


def ramp(t, a, b):
    return clamp((t - a) / (b - a))


def phase(t):
    return min(2, int(t // 3)), t % 3 / 3


def pts(cx, cy, rx, ry, n=60, angle=0):
    return [
        (cx + rx * cos(angle + tau * i / n), cy + ry * sin(angle + tau * i / n))
        for i in range(n)
    ]


@lru_cache(2048)
def rgba(s):
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(k * 2 for k in s)
    if len(s) == 6:
        s += "ff"
    return tuple(int(s[i : i + 2], 16) / 255 for i in range(0, 8, 2))


@lru_cache(4096)
def commands(path):
    toks = re.findall(r"[MLCQZ]|-?(?:\d*\.\d+|\d+)", path)
    out = []
    i = 0
    while i < len(toks):
        cmd = toks[i]
        n = {"M": 2, "L": 2, "Q": 4, "C": 6, "Z": 0}[cmd]
        out.append((cmd, tuple(map(float, toks[i + 1 : i + 1 + n]))))
        i += n + 1
    return out


@lru_cache(256)
def stamp_text(text, size, color, face):
    file = os.environ.get(
        "ASTRA_KOREAN_FONT", "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    )
    if face == "serif" and os.path.exists(
        "/System/Library/Fonts/Supplemental/AppleMyungjo.ttf"
    ):
        file = "/System/Library/Fonts/Supplemental/AppleMyungjo.ttf"
    if face == "mono" and text.isascii():
        file = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
    try:
        font = ImageFont.truetype(
            file, size, index=6 if face == "bold" and file.endswith("ttc") else 0
        )
    except OSError:
        font = ImageFont.truetype(file, size)
    bb = font.getbbox(text)
    w = max(1, bb[2] - bb[0] + 4)
    h = max(1, bb[3] - bb[1] + 4)
    img = Image.new("L", (w, h))
    ImageDraw.Draw(img).text((2 - bb[0], 2 - bb[1]), text, font=font, fill=255)
    a = np.asarray(img).astype(float) * rgba(color)[3]
    pix = np.empty((h, w, 4), np.uint8)
    for i, ch in enumerate(rgba(color)[2::-1]):
        pix[:, :, i] = a * ch
    pix[:, :, 3] = a
    surf = ffi.gc(
        C.cairo_image_surface_create_for_data(ffi.from_buffer(pix), 0, w, h, w * 4),
        C.cairo_surface_destroy,
    )
    return surf, pix, w, h


class Desk:
    def __init__(self, w=768, h=432):
        self.w = w
        self.h = h
        self.s = ffi.gc(C.cairo_image_surface_create(0, w, h), C.cairo_surface_destroy)
        self.c = ffi.gc(C.cairo_create(self.s), C.cairo_destroy)
        C.cairo_set_line_join(self.c, 1)
        C.cairo_set_line_cap(self.c, 1)

    def color(self, s):
        C.cairo_set_source_rgba(self.c, *rgba(s))

    def bg(self, s):
        self.color(s)
        C.cairo_paint(self.c)

    @contextmanager
    def at(self, x=0, y=0, s=1, rot=0, sy=None):
        c = self.c
        C.cairo_save(c)
        C.cairo_translate(c, x, y)
        C.cairo_rotate(c, rot)
        C.cairo_scale(c, s, sy if sy is not None else s)
        try:
            yield
        finally:
            C.cairo_restore(c)

    @contextmanager
    def clip(self, shape):
        C.cairo_save(self.c)
        self.trace(shape)
        C.cairo_clip(self.c)
        try:
            yield
        finally:
            C.cairo_restore(self.c)

    def end(self, f, o=None, w=1):
        if f:
            self.color(f)
            (C.cairo_fill_preserve if o else C.cairo_fill)(self.c)
        if o:
            self.color(o)
            C.cairo_set_line_width(self.c, w)
            C.cairo_stroke(self.c)

    def rect(self, x, y, w, h, f, o=None, lw=1):
        C.cairo_rectangle(self.c, x, y, w, h)
        self.end(f, o, lw)

    def ell(self, x, y, rx, ry, f, o=None, w=1):
        if min(rx, ry) <= 0:
            return
        with self.at(x, y, rx, sy=ry):
            C.cairo_arc(self.c, 0, 0, 1, 0, tau)
            C.cairo_close_path(self.c)
        self.end(f, o, w)

    def circ(self, x, y, r, f, o=None, w=1):
        self.ell(x, y, r, r, f, o, w)

    def arc(self, x, y, r, a, b, o, w=1):
        if r <= 0:
            return
        C.cairo_new_path(self.c)
        C.cairo_arc(self.c, x, y, r, a, b)
        self.end(None, o, w)

    def poly(self, p, f=None, o=None, w=1, close=True):
        if not p:
            return
        C.cairo_move_to(self.c, *p[0])
        for q in p[1:]:
            C.cairo_line_to(self.c, *q)
        if close:
            C.cairo_close_path(self.c)
        self.end(f, o, w)

    def line(self, p, o, w=1):
        self.poly(p, None, o, w, False)

    def trace(self, p):
        c = self.c
        x = y = 0
        for k, v in commands(p):
            if k == "M":
                C.cairo_move_to(c, *v)
            if k == "L":
                C.cairo_line_to(c, *v)
            if k == "C":
                C.cairo_curve_to(c, *v)
            if k == "Q":
                C.cairo_curve_to(
                    c,
                    (x + 2 * v[0]) / 3,
                    (y + 2 * v[1]) / 3,
                    (v[2] + 2 * v[0]) / 3,
                    (v[3] + 2 * v[1]) / 3,
                    v[2],
                    v[3],
                )
            if k == "Z":
                C.cairo_close_path(c)
            else:
                x, y = v[-2:]

    def path(self, p, f=None, o=None, w=1):
        self.trace(p)
        self.end(f, o, w)

    def grad(self, x, y, w, h, stops, radial=False):
        p = (
            C.cairo_pattern_create_radial(
                x + w / 2, y + h / 2, 0, x + w / 2, y + h / 2, max(w, h) / 2
            )
            if radial
            else C.cairo_pattern_create_linear(x, y, x, y + h)
        )
        for n, col in stops:
            C.cairo_pattern_add_color_stop_rgba(p, n, *rgba(col))
        C.cairo_set_source(self.c, p)
        C.cairo_rectangle(self.c, x, y, w, h)
        C.cairo_fill(self.c)
        C.cairo_pattern_destroy(p)

    def txt(self, x, y, text, size, col, face="bold", align="left"):
        surf, img, w, h = stamp_text(str(text), int(size), col, face)
        x -= w * ({"left": 0, "center": 0.5, "right": 1}[align])
        C.cairo_save(self.c)
        C.cairo_set_source_surface(self.c, surf, x, y)
        C.cairo_paint(self.c)
        C.cairo_restore(self.c)

    def image(self):
        C.cairo_surface_flush(self.s)
        return np.frombuffer(
            ffi.buffer(C.cairo_image_surface_get_data(self.s), self.w * self.h * 4),
            np.uint8,
        ).reshape(self.h, self.w, 4)


def star(d, x, y, r, n, col, small=0.42, rot=-pi / 2):
    d.poly(
        [
            (
                x + cos(rot + i * pi / n) * r * (1 if i % 2 == 0 else small),
                y + sin(rot + i * pi / n) * r * (1 if i % 2 == 0 else small),
            )
            for i in range(n * 2)
        ],
        col,
    )


def dots(d, x, y, w, h, gap, r, col):
    for j in range(int(h / gap) + 1):
        for i in range(int(w / gap) + 1):
            d.circ(x + i * gap + (j % 2) * gap / 2, y + j * gap, r, col)


def seed(n):
    return random.Random(n)


def hatch(d, x, y, w, h, step, col):
    for z in range(-int(h), int(w), step):
        a = max(0, -z)
        b = min(h, w - z)
        if b > a:
            d.line([(x + z + a, y + a), (x + z + b, y + b)], col, 1)
