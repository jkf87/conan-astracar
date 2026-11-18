"""Small RGB drawing primitives; scene layout and motion live in the four film reels."""

from functools import lru_cache
from math import sin, cos, pi, exp, sqrt, floor, atan2
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

cv2.setNumThreads(1)
W, H = 768, 432
ROOT = Path(__file__).resolve().parent
PLATES = ROOT / "plates"
Y, X = np.mgrid[:H, :W].astype(np.float32)
TAU = 2 * pi
AA = cv2.LINE_AA


@lru_cache(None)
def rgb(code):
    if isinstance(code, tuple):
        return code
    return tuple(bytes.fromhex(code.lstrip("#")))


def col(c):
    return rgb(c) if isinstance(c, str) else tuple(int(x) for x in c)


def mix(a, b, u):
    a, b = col(a), col(b)
    return tuple(round(v + (w - v) * u) for v, w in zip(a, b))


def shade(c, f):
    return tuple(min(255, max(0, int(k * f))) for k in col(c))


def pt(p):
    return tuple(int(round(v)) for v in p)


def pts(ps):
    return np.rint(ps).astype(np.int32).reshape(-1, 1, 2)


def sat(v):
    return min(1, max(0, v))


def step(t, a, b):
    v = sat((t - a) / (b - a))
    return v * v * (3 - 2 * v)


def ease(t):
    return step(t, 0, 1)


def lerp(a, b, u):
    return a + (b - a) * u


def blank(c):
    return np.full((H, W, 3), col(c), np.uint8)


def line(im, a, b, c, w=1):
    cv2.line(im, pt(a), pt(b), col(c), int(w), AA)


def path(im, p, c, w=1, closed=False):
    if len(p) > 1:
        cv2.polylines(im, [pts(p)], closed, col(c), int(w), AA)


def poly(im, p, c, stroke=None, w=1):
    cv2.fillPoly(im, [pts(p)], col(c), AA)
    if stroke:
        path(im, p, stroke, w, True)


def rect(im, x, y, w, h, c, edge=None):
    cv2.rectangle(im, pt((x, y)), pt((x + w, y + h)), col(c), -1)
    if edge:
        cv2.rectangle(im, pt((x, y)), pt((x + w, y + h)), col(edge), 1, AA)


def ell(im, x, y, rx, ry, c, w=-1, rot=0):
    cv2.ellipse(
        im,
        pt((x, y)),
        (max(1, round(rx)), max(1, round(ry))),
        rot,
        0,
        360,
        col(c),
        w,
        AA,
    )


def dot(im, x, y, r, c):
    cv2.circle(im, pt((x, y)), max(1, round(r)), col(c), -1, AA)


def arc(im, x, y, rx, ry, a, b, c, w=1, rot=0):
    cv2.ellipse(
        im, pt((x, y)), (max(1, round(rx)), max(1, round(ry))), rot, a, b, col(c), w, AA
    )


def rr(im, x, y, w, h, r, c):
    r = min(r, w / 2, h / 2)
    rect(im, x + r, y, w - 2 * r, h, c)
    rect(im, x, y + r, w, h - 2 * r, c)
    for a in [x + r, x + w - r]:
        for b in [y + r, y + h - r]:
            dot(im, a, b, r, c)


@lru_cache(None)
def ground(a, b, grain=0, seed=0, light=False):
    u = (
        np.clip(np.hypot((X - W * 0.46) / (W * 0.75), (Y - H * 0.2) / (H * 1.2)), 0, 1)
        if light
        else Y / (H - 1)
    )
    out = np.array(col(a)) + (np.array(col(b)) - np.array(col(a))) * u[:, :, None]
    if grain:
        out += np.random.default_rng(seed).normal(0, grain, (H, W, 1))
    return np.uint8(np.clip(out, 0, 255))


@lru_cache(None)
def font(size, weight):
    path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    if not Path(path).exists():
        path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    return ImageFont.truetype(
        path, size, index=(6 if weight == "bold" and "AppleSD" in path else 0)
    )


@lru_cache(maxsize=1800)
def lettering(text, size, weight):
    f = font(size, weight)
    x, y, r, b = f.getbbox(text)
    mask = Image.new("L", (max(1, r - x + 2), max(1, b - y + 2)), 0)
    ImageDraw.Draw(mask).text((1 - x, 1 - y), text, font=f, fill=255)
    return np.asarray(mask)


def label(im, x, y, s, size, c, weight="normal", anchor="left"):
    mask = lettering(str(s), size, weight)
    h, w = mask.shape
    x = int(x - (w / 2 if anchor == "center" else w if anchor == "right" else 0))
    y = int(y)
    l, r = max(0, x), min(W, x + w)
    top, b = max(0, y), min(H, y + h)
    if r > l and b > top:
        alpha = mask[top - y : b - y, l - x : r - x, None] / 255
        im[top:b, l:r] = im[top:b, l:r] * (1 - alpha) + np.array(col(c)) * alpha


def glow(im, layer, power=0.75, r=7):
    cv2.addWeighted(im, 1, cv2.GaussianBlur(layer, (0, 0), r), power, 0, dst=im)
    cv2.add(im, layer, dst=im)


def grid(im, s, c, offset=(0, 0), dots=False):
    x, y = offset
    for xx in range(round(x) % s, W, s):
        if dots:
            for yy in range(round(y) % s, H, s):
                im[yy, xx] = col(c)
        else:
            line(im, (xx, 0), (xx, H), c)
    if not dots:
        for yy in range(round(y) % s, H, s):
            line(im, (0, yy), (W, yy), c)


def onpath(p, u):
    a = np.asarray(p, float)
    ds = np.linalg.norm(np.diff(a, axis=0), axis=1)
    v = sat(u) * ds.sum()
    i = min(len(ds) - 1, np.searchsorted(np.cumsum(ds), v))
    prev = sum(ds[:i])
    return a[i] + (a[i + 1] - a[i]) * ((v - prev) / max(0.00001, ds[i]))


def reveal(im, p, u, c, w=2):
    a = np.asarray(p, float)
    ds = np.linalg.norm(np.diff(a, axis=0), axis=1)
    v = sat(u) * ds.sum()
    i = min(len(ds) - 1, np.searchsorted(np.cumsum(ds), v))
    path(im, [*a[: i + 1], onpath(p, u)], c, w)


def view(im, z=1, cx=384, cy=216, angle=0):
    m = cv2.getRotationMatrix2D((cx, cy), angle, z)
    m[:, 2] += [384 - cx, 216 - cy]
    return cv2.warpAffine(
        im, m, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE
    )


def plate(name):
    return cv2.cvtColor(cv2.imread(str(PLATES / name)), cv2.COLOR_BGR2RGB)


def patch(im, src, x, y, w, h):
    x, y, w, h = map(round, (x, y, w, h))
    if min(w, h) < 1:
        return
    img = cv2.resize(
        src,
        (w, h),
        interpolation=cv2.INTER_AREA if w < src.shape[1] else cv2.INTER_LINEAR,
    )
    l, r = max(0, x), min(W, x + w)
    a, b = max(0, y), min(H, y + h)
    if r > l and b > a:
        im[a:b, l:r] = img[a - y : b - y, l - x : r - x]


def box(im, x, y, a, b, h, c, ink=None):
    """Oblique block, anchored at its back top corner."""
    u = (x + a, y + a * 0.44)
    v = (x - b, y + b * 0.44)
    front = (x + a - b, y + (a + b) * 0.44)
    poly(
        im, [u, front, (front[0], front[1] + h), (u[0], u[1] + h)], shade(c, 0.67), ink
    )
    poly(
        im, [v, front, (front[0], front[1] + h), (v[0], v[1] + h)], shade(c, 0.82), ink
    )
    poly(im, [(x, y), u, front, v], c, ink)


def bracket(im, x, y, w, h, c, k=13):
    for xx, sx in [(x, 1), (x + w, -1)]:
        for yy, sy in [(y, 1), (y + h, -1)]:
            path(im, [(xx + sx * k, yy), (xx, yy), (xx, yy + sy * k)], c, 2)
