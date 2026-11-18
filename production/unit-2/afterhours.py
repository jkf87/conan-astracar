"""Eight small night screenings, each with its own scene geometry and exposure."""

from draw import *


def hd_2d(d, t):
    # A shallow focal plane keeps the keeper and window lights sharp.
    from PIL import ImageFilter

    zoom = 1.18 + 0.30 * span(t, 1.2, 4.8) - 0.22 * span(t, 6.5, 8.8)
    x = 385 - 53 + 99 * span(t, 0.8, 8)
    with d.at((1 - zoom) * x, (1 - zoom) * 213, zoom):
        station(d, t)
    a = d.image()
    im = Image.fromarray(a[:, :, :3])
    blur = np.asarray(im.filter(ImageFilter.GaussianBlur(2.0)))
    y = np.arange(432)[:, None, None]
    blend = np.clip((abs(y - 218) - 83) / 102, 0, 1) * 0.78
    a[:, :, :3] = (a[:, :, :3] * (1 - blend) + blur * blend).astype("uint8")
    C.cairo_surface_mark_dirty(d.s)


def station(d, t):
    # World-space coordinates projected through an orthographic three-quarter camera.
    k = "393847"
    b, u = phase(t)
    d.grad(0, 0, 768, 432, [(0, "393c55"), (0.53, "687282"), (1, "98a1a6")])
    shift = 28 * span(t, 0, 8.9)
    origin = (409 - shift, 194)

    def proj(x, y, z):
        return (origin[0] + (x - y) * 0.87, origin[1] + (x + y) * 0.43 - z)

    def box(x, y, z, w, l, h, colors):
        top = [
            proj(x, y, z + h),
            proj(x + w, y, z + h),
            proj(x + w, y + l, z + h),
            proj(x, y + l, z + h),
        ]
        bottom = [
            proj(x, y, z),
            proj(x + w, y, z),
            proj(x + w, y + l, z),
            proj(x, y + l, z),
        ]
        d.poly([top[3], top[2], bottom[2], bottom[3]], colors[1])
        d.poly([top[1], top[2], bottom[2], bottom[1]], colors[2])
        d.poly(top, colors[0])

    rng = seed(88)
    for j in range(2):
        for i in range(37):
            x = i * 28 - 52 - shift * (j + 0.5)
            y = 120 + j * 42 + 13 * sin(i * 0.5)
            h = rng.randrange(29, 80)
            d.poly([(x - 12, y), (x, y - h), (x + 12, y)], ["52596e", "555e70"][j])
    box(-175, -119, -45, 350, 240, 45, ("94999b", "676975", "525767"))
    for i in range(780):
        x, y = rng.uniform(-171, 169), rng.uniform(-116, 115)
        px, py = proj(x, y, 1)
        d.rect(int(px), int(py), 3, 1, rng.choice(["a7acac", "818991", "b5b8b4"]))
    # Slate roof, tiny eaves and individual mullioned panes.
    box(-126, -99, 0, 165, 61, 70, ("88898d", "656674", "505563"))
    for j in range(7):
        box(
            -139,
            -106 + j * 11,
            72 + min(j, 6 - j) * 5,
            187,
            13,
            4,
            ("858793", "606577", "73747d"),
        )
    for i in range(12):
        for j in range(7):
            p1 = proj(
                -136 + i * 15 + (j % 2) * 6, -105 + j * 11, 75 + min(j, 6 - j) * 5
            )
            d.line([p1, (p1[0] + 9, p1[1] + 4)], "a5a6ab", 0.8)
    box(-57, -76, 84, 13, 14, 21, ("a5a09f", "686573", "595c69"))
    sx, sy = proj(-52, -71, 106)
    for j in range(6):
        u = (t * 0.32 + j / 6) % 1
        d.ell(
            sx + 13 * u + 3 * sin(t + u * 4),
            sy - u * 32,
            3 + u * 6,
            2 + u * 3,
            "c5c9c5" + f"{int((1 - u) * 70):02x}",
        )
    for i in range(4):
        for j in range(2):
            x = -111 + i * 35 + j * 12
            y = -37
            A = proj(x, y, 26)
            B = proj(x + 9, y, 26)
            D = proj(x, y, 48)
            E = proj(x + 9, y, 48)
            d.poly([A, B, E, D], ["c6a277", "f0c68d"][(i + j) % 2], k, 1)
    # Stacked platform parcels and a small station nameboard give the building scale.
    for xx, yy, h in [(-149, -23, 14), (-133, -20, 10), (-148, -21, 24)]:
        box(xx, yy, 0, 13, 12, h, ("b69b82", "947e70", "7d706b"))
        pa = proj(xx + 6, yy, h)
        pb = proj(xx + 6, yy + 12, h)
        d.line([pa, pb], "d6baa0", 1)
    for xx in [-104, -62]:
        box(xx, -36, 0, 2, 2, 30, ("bdb6a5", "675e61", "534f58"))
    for j in range(7):
        box(-177 + j * 53, 108, -1, 3, 8, 15, ("bfc0af", "737582", "686d76"))
    for z in [2, 11]:
        d.line([proj(-175, 112, z), proj(175, 112, z)], "7f8189", 2)
    lights = [(-98, 50), (12, 50), (121, 50)]
    for i, (x, y) in enumerate(lights):
        px, py = proj(x, y, 0)
        on = t >= 1.3 + i * 2.6
        if on:
            d.grad(
                px - 35,
                py - 77,
                70,
                70,
                [(0, "f8c87c75"), (0.5, "e8a76438"), (1, "e8a45c00")],
                True,
            )
            d.poly(
                [(px - 2, py), (px + 3, py), (px - 28, py + 14), (px - 36, py + 13)],
                "53526477",
            )
        d.rect(px - 3, py - 43, 5, 44, k)
        d.rect(px - 7, py - 53, 13, 15, k)
        d.rect(px - 5, py - 51, 9, 10, "f7d798" if on else "899292")
        d.poly([(px - 10, py - 53), (px, py - 61), (px + 9, py - 53)], k)
    x = -146 + span(t, 0.15, 8.8) * 292
    px, py = proj(x, 65, 0)
    d.ell(px + 4, py, 14, 4, "52536168")
    stroll = int(t * 7) % 2
    with d.at(int(px) - 11, int(py) - 34, 2):
        sprite = [
            "   vvv   ",
            "  vvwwv  ",
            "  vvvwvv ",
            "   ssks  ",
            "  sssss  ",
            "  mrrr   ",
            " mmbbmm  ",
            "  bbbbs  ",
            "  bbbbk  ",
            "   k kk  ",
            "  kk  k  ",
        ]
        col = {
            "v": "514654",
            "w": "a5a9a2",
            "s": "dfbaa2",
            "k": "404049",
            "m": "c39272",
            "r": "bd735e",
            "b": "5d687c",
        }
        for j, row in enumerate(sprite):
            for i, ch in enumerate(row):
                if ch != " ":
                    d.rect(i + (stroll if j >= 9 else 0), j * 1.44, 1.05, 1.5, col[ch])
    for i in range(48):
        x = (i * 115 - t * (7 + i % 4)) % 775
        y = (i * 83 + t * (13 + i % 7)) % 436
        d.ell(x, y, 1 + i % 3 * 0.4, 0.85, "d7dadd9a")


def microgame(d, t):
    # Garden triathlon. The first stage uses wax strokes; the next uses blue plan ink;
    # the last stage is a chunky handheld game driven by a discrete rain counter.
    b = 0 if t < 3.6 else 1 if t < 6.55 else 2
    u = ramp(t, [0, 3.6, 6.55][b], [3.6, 6.55, 9][b])
    r = seed(18)
    if b == 0:
        d.bg("f1dca5")
        for i in range(240):
            x, y = r.randrange(768), r.randrange(432)
            d.line([(x, y), (x + 12, y - 3)], "ae987950", 1.3)
        d.ell(365, 336, 117, 12, "b49a78")
        d.poly([(283, 222), (459, 222), (431, 330), (310, 330)], "bf684d", "664335", 4)
        d.rect(274, 215, 194, 23, "d68b61", "664335", 3)
        for i in range(21):
            d.line([(298 + i * 7, 245), (314 + i * 5.5, 320)], "e89e7755", 2.4)
        with d.at(
            445 - 70 * span(t, 0, 1.8),
            160 + 17 * sin(t * 2),
            1,
            -0.64 + 0.57 * span(t, 1.4, 2.3),
        ):
            d.line([(0, -87), (0, 1)], "6c503e", 10)
            d.path("M -23 -8 Q -33 19 0 49 Q 38 10 24 -9 Z", "748e90", "574f46", 3)
        for j in range(26):
            x = 371 + r.randrange(-31, 31)
            y = 186 + (j * 11 + t * 64) % 38
            if t > 0.9:
                d.circ(x, y, 2 + j % 3, "754c3a")
    elif b == 1:
        d.bg("214d72")
        for x in range(0, 769, 24):
            d.rect(x, 0, 0.7, 432, "47728c")
        for y in range(0, 433, 24):
            d.rect(0, y, 768, 0.7, "47728c")
        c = "d8eedc"
        d.path("M 231 231 L 532 231 L 493 342 L 273 342 Z", None, c, 2)
        d.line([(239, 247), (525, 247)], c, 2)
        for j in range(18):
            d.line([(269 + j * 12, 313), (281 + j * 12, 297)], "83a3af", 1)
        y = 109 + 138 * span(u, 0.13, 0.77)
        with d.at(377, y, 1, u * 0.75):
            d.path(
                "M -18 12 Q -22 -17 14 -28 Q 31 -6 7 15 Q -8 25 -18 12 Z",
                "ead19c",
                c,
                2,
            )
            d.path("M -13 12 Q 4 2 11 -17", None, "977c59", 2)
        for j in range(6):
            d.rect(378, 144 + j * 15, 1, 7, c)
    else:
        d.bg("9dbe8f")
        dark = "284d43"
        mid = "608765"
        pix = 6
        for i in range(16):
            d.rect(i * 48, 323 - (i % 3) * 6, 48, 432, mid)
        d.rect(303, 271, 156, 18, dark)
        d.rect(315, 289, 132, 48, mid, dark, 5)
        d.rect(375, 222 - 37 * u, 9, 52 + 37 * u, dark)
        for i in range(3):
            d.rect(345 - i * 6, 236 - i * 6 - 28 * u, 24, 9, dark)
            d.rect(383 + i * 7, 216 - i * 6 - 28 * u, 18, 8, dark)
        for j in range(32):
            x = 286 + j * 23 % 189
            y = 91 + (int(t * 32 + j * 7) % 29) * 6
            d.rect(x, y, 6, 12, "476f66")
        if u > 0.65:
            for j in range(5):
                a = j * tau / 5
                d.rect(369 + cos(a) * 14, 174 + sin(a) * 14, 16, 14, "e2dca3")
    col = ["684633", "e4efd6", "284d43"][b]
    d.txt(43, 38, ["담아!", "심어!", "물 줘!"][b], 40, col)
    d.rect(40, 389, 688, 8, None, col, 2)
    d.rect(43, 392, 681 * (1 - u), 3, col)


def clam(d, x, y, s, c, openamt):
    k = "30243d"
    with d.at(x, y, s):
        d.path("M -74 12 C -68 68 58 69 74 12 Q 0 -10 -74 12 Z", c, k, 5)
        d.ell(0, 11, 67, 10, k)
        with d.at(0, 7 - openamt * 21, 1, sy=0.45 + openamt * 0.55):
            d.path(
                "M -71 3 C -89 -26 -62 -43 -46 -40 Q -42 -70 -14 -58 Q 1 -83 21 -60 Q 46 -72 53 -45 Q 84 -44 73 3 Q 2 22 -71 3 Z",
                c,
                k,
                4,
            )
            for j in range(-2, 3):
                d.path(
                    f"M {j * 5} 4 Q {j * 17} -24 {j * 24} {-43 + abs(j) * 4}",
                    None,
                    k,
                    2,
                )
        for xx in [-14, 15]:
            d.circ(xx, 32, 4, k)


def game_show(d, t):
    k = "36263e"
    d.bg("f2b859")
    for i in range(20):
        a = i * tau / 20 + t * 0.055
        d.poly(
            [
                (384, 253),
                (384 + 620 * cos(a), 253 + 620 * sin(a)),
                (384 + 620 * cos(a + 0.13), 253 + 620 * sin(a + 0.13)),
            ],
            "ffd878",
        )
    d.path("M 0 329 Q 384 272 768 329 L 768 432 L 0 432 Z", "68bdb2", k, 4)
    for j in range(22):
        d.circ(18 + j * 35, 359 + 12 * cos(j * 0.3), 5, "fdf1b9", k, 1.5)
    beat = t / 0.375
    idx = int(beat)
    pulse = sin(pi * (beat % 1)) ** 2
    for i, (x, col) in enumerate([(181, "e98286"), (384, "ac99dc"), (587, "75bed7")]):
        turn = (idx // 2) % 3
        op = 0.08 + 0.88 * pulse if i == turn or t > 6.4 else 0.05
        clam(d, x, 269 - 11 * op, 1 if i != 1 else 1.16, col, op)
        if i == turn:
            star(d, x + 75, 153 - 9 * pulse, 11 + 4 * pulse, 4, "faf4c6", 0.35)
    d.ell(384, 82, 125, 39, "fdf0c5", k, 4)
    d.txt(
        384,
        62,
        "짝!" if pulse > 0.28 else ["먼저", "따라", "함께"][phase(t)[0]],
        34,
        k,
        align="center",
    )


def ascii_crt(d, t):
    d.bg("0a1511")
    green = "87e6a3"
    faint = "2b6a47"
    b, u = phase(t)
    # A beam sweeps a character matrix: the disc uses density, its rings use punctuation.
    cx = 428 - 48 * span(t, 2, 8)
    cy = 218
    radius = 42 + 77 * span(t, 1.2, 6.5)
    sweep = (t * 0.17) % 1
    for j in range(22):
        for i in range(69):
            x = 43 + i * 10
            y = 69 + j * 13
            dx = (x - cx) / radius
            dy = (y - cy) / radius
            rad = dx * dx + dy * dy
            yr = dy + 0.32 * dx
            ring = dx * dx / (1.68**2) + yr * yr / (0.42**2)
            ch = ""
            col = faint
            if (i * 443 + j * 271 + i * j * 79) % 91 == 3:
                ch = "."
                col = green
            if t > 1.05 and rad < 1:
                val = clamp(
                    0.45
                    + 0.21 * (-dx - dy)
                    + 0.22 * sin(dy * 14 + t * 0.75 + dx * 0.84)
                )
                ch = ".,:-=+*#%"[min(8, int(val * 9))]
                col = green
            if t > 2.7 and 0.79 < ring < 1.11 and (yr > 0.01 or rad > 1):
                ch = "=~-"[(i + j) % 3]
                col = "c1f2be"
            if abs(i / 69 - sweep) < 0.012 and not ch:
                ch = ":"
            if ch:
                d.txt(x, y, ch, 14, col, "mono")
    d.txt(44, 32, ["수신 대기", "고리 추적", "관측 저장"][b], 19, green)
    d.txt(723, 35, f"{int(t * 24):03d}", 14, green, "mono", "right")
    for i in range(64):
        x = 47 + i * 10
        v = 5 + 15 * (1 + sin(i * 0.23 - t * 1.8)) * (0.5 + 0.5 * sin(i * 0.14 + t))
        d.txt(x, 377 - int(v / 5) * 3, "+" if i % 3 else ":", 11, faint, "mono")
    d.rect(34, 59, 700, 1, faint)
    d.rect(34, 362, 700, 1, faint)
    for j in range(0, 432, 3):
        d.rect(0, j, 768, 0.55, "060c0948")


def porter(d, x, y, s, arms, stride):
    with d.at(x, y, s):
        k = "343333"
        c = "d5d1c3"
        for sg in [-1, 1]:
            d.line(
                [
                    (sg * 7, 3),
                    (sg * 11 + stride * sg, 29),
                    (sg * 9 + stride * sg * 1.4, 55),
                ],
                k,
                9,
            )
            d.ell(sg * 9 + stride * sg * 1.4 + 4, 55, 10, 3, k)
        d.path("M -12 -52 Q 4 -60 17 -47 L 26 1 Q 10 12 -22 3 Z", "65635f", k, 2)
        d.path("M -9 -56 L 8 -56 L 3 -32 Z", c)
        d.line([(2, -49), (5, -34)], k, 3)
        for sg in [-1, 1]:
            d.line(
                [
                    (sg * 13, -44),
                    (sg * (22 + 8 * arms), -25 - arms * 12),
                    (sg * (23 + 13 * arms), -14 - arms * 55),
                ],
                k,
                6,
            )
            d.ell(sg * (23 + 13 * arms), -14 - arms * 55, 4, 6, c, k, 1)
        d.ell(0, -76, 17, 24, c, k, 1.7)
        d.path(
            "M -17 -76 Q -22 -103 -3 -103 Q 16 -106 20 -91 L 11 -83 L 11 -93 Q -5 -87 -17 -76 Z",
            k,
        )
        d.circ(9, -77, 1.8, k)
        d.path("M 7 -62 Q 13 -60 15 -65", None, k, 1)


def hat(d, x, y, a):
    with d.at(x, y, 1, a):
        d.ell(0, 0, 28, 5, "43403f", "302e2e", 1.5)
        d.path(
            "M -17 -2 L -16 -16 Q -16 -26 1 -24 Q 18 -25 19 -15 L 19 -2 Z",
            "77726b",
            "343232",
            1.5,
        )
        d.rect(-16, -8, 34, 5, "393736")


def silent_film(d, t):
    paper = "d8d4c6"
    d.bg("241d22")
    q = int(t * 16) / 16
    for side in [-1, 1]:
        with d.at(384, 0, side, sy=1):
            for j in range(11):
                d.path(
                    f"M {273 + j * 12} 0 Q {277 + j * 10} 110 {340 + j * 6} 196 Q {319 + j * 10} 329 {322 + j * 9} 432 L {334 + j * 9} 432 Q {328 + j * 10} 321 {351 + j * 6} 196 Q {291 + j * 10} 100 {288 + j * 12} 0 Z",
                    ["503137", "3c2930"][j % 2],
                )
    with d.clip("M 97 0 L 671 0 L 671 432 L 97 432 Z"):
        with d.at(1.1 * sin(t * 49), 1.05 * cos(t * 55)):
            d.grad(94, -3, 580, 439, [(0, "a5a299"), (0.46, "e2dfd2"), (1, "777770")])
            if 2.15 < t < 3.07:
                d.rect(97, -2, 575, 437, "363533")
                d.rect(125, 44, 517, 344, None, "cdc7b5", 1)
                d.rect(132, 52, 503, 328, None, "918c80", 1)
                for yy in [104, 329]:
                    d.line([(235, yy), (533, yy)], "ada696", 1)
                    star(d, 384, yy, 10, 4, paper)
                d.txt(384, 183, "모자도 한 장이요!", 31, paper, "serif", "center")
                return
            for j in range(5):
                x = 95 + j * 129
                d.rect(x, 41, 108, 164, "767671", "585954", 2)
                d.rect(x + 6, 49, 96, 149, "b9b9ae")
                d.line([(x + 53, 49), (x + 53, 198)], "85877d", 4)
                d.line([(x + 6, 123), (x + 101, 123)], "85877d", 4)
            d.rect(93, 235, 582, 8, "64635d")
            d.poly([(94, 315), (672, 297), (672, 435), (94, 435)], "a9a79b")
            for j in range(10):
                d.line([(90 + j * 65, 433), (162 + j * 44, 308)], "8d8a80", 1)
            z = span(q, 2.94, 7.32)
            x = 240 + 232 * z
            cart = 367 + 126 * span(q, 3, 6.35)
            d.line([(cart - 62, 282), (cart + 70, 282), (cart + 79, 213)], "474641", 5)
            for xx in [-42, 44]:
                d.circ(cart + xx, 298, 13, "62615a", "41413b", 2)
                d.circ(cart + xx, 298, 5, paper)
            for i, (w, h) in enumerate([(99, 33), (70, 24)]):
                yy = 247 - i * 25
                d.rect(cart - w / 2, yy, w, h, "8d887b", "58554f", 2)
                for sx in [-1, 1]:
                    d.rect(cart + sx * w * 0.3, yy, 4, h, "625f57")
            porter(
                d,
                x,
                268,
                0.97,
                span(q, 5.7, 6.8) * (1 - span(q, 7.7, 8.7)),
                sin(q * 7) * 9 * (1 if 3 < q < 7 else 0.12),
            )
            if q < 1.3:
                hat(d, x, 170, -0.04)
            elif q < 6.2:
                v = span(q, 1.3, 4.2)
                hat(
                    d,
                    mix(240, cart, v),
                    mix(169, 219, v) - 72 * sin(v * pi),
                    v * pi * 2,
                )
            else:
                v = span(q, 6.2, 7.7)
                hat(d, mix(cart, x, v), mix(219, 169, v) - 79 * sin(v * pi), pi * 2 * v)
            rng = seed(int(t * 24) * 23)
            d.rect(95, 0, 578, 432, "f8f4df0" + str(rng.randrange(1, 9)))
            for j in range(13):
                xx, yy = rng.randrange(97, 671), rng.randrange(432)
                d.line([(xx, yy), (xx, yy + 1 + rng.randrange(5))], "48423b69", 0.7)


def backrooms(d, t):
    d.bg("161918")
    inner = "M 96 0 L 672 0 L 672 432 L 96 432 Z"
    with d.clip(inner):
        d.rect(94, -2, 581, 437, "a4a58b")
        cam = 1.1 + t * 1.11
        cx = 384 + 9 * sin(t * 1.48)
        cy = 188 + 3.3 * sin(t * 6.6)

        def point(x, y, z):
            depth = max(0.15, z - cam)
            return cx + (x + 0.08 * sin(t * 1.9)) * 320 / depth, cy - y * 320 / depth

        def plane(vertices, c, o=None, lw=1):
            d.poly([point(*p) for p in vertices], c, o, lw)

        far = 31
        d.rect(96, cy, 576, 432 - cy, "898976")
        d.rect(96, 0, 576, cy, "bcbdaa")
        plane(
            [(-3, -1.45, far), (3, -1.45, far), (3, 1.55, far), (-3, 1.55, far)],
            "989e8b",
        )
        plane(
            [
                (-1.1, -1.45, far - 0.1),
                (1.1, -1.45, far - 0.1),
                (1.1, 1, far - 0.1),
                (-1.1, 1, far - 0.1),
            ],
            "77887e",
            "596b64",
            1,
        )
        for j in reversed(range(0, 15)):
            z = 1 + j * 2.1
            z2 = z + 2.1
            if z2 <= cam + 0.22:
                continue
            near = max(z, cam + 0.22)
            for sg in [-1, 1]:
                x = sg * 3
                plane(
                    [(x, -1.45, near), (x, -1.45, z2), (x, 1.55, z2), (x, 1.55, near)],
                    ["aaa98c", "a8a990"][j % 2],
                )
                plane(
                    [
                        (x, -1.17, near),
                        (x, -1.17, z2),
                        (x, -1.37, z2),
                        (x, -1.37, near),
                    ],
                    "788274",
                )
                if j % 3 == 0 and z > cam + 0.25:
                    plane(
                        [
                            (x, -1.25, z + 0.3),
                            (x, -1.25, z + 1.34),
                            (x, 0.93, z + 1.34),
                            (x, 0.93, z + 0.3),
                        ],
                        "7b887a",
                        "657365",
                        1,
                    )
                    for g in range(4):
                        plane(
                            [
                                (x, 0.53 - g * 0.08, z + 0.5),
                                (x, 0.51 - g * 0.08, z + 1.1),
                                (x, 0.48 - g * 0.08, z + 1.1),
                                (x, 0.50 - g * 0.08, z + 0.5),
                            ],
                            "637566",
                        )
            if z > cam + 0.28:
                d.line([point(-3, 1.55, z), point(3, 1.55, z)], "9ea391", 1)
                d.line([point(-3, -1.45, z), point(3, -1.45, z)], "7e8272", 0.9)
                if j % 2 == 0:
                    lamp = (
                        "eeedcf"
                        if j > int(t / 2.8) * 2 + 2 or int(t * 12) % 13
                        else "a5ad99"
                    )
                    plane(
                        [
                            (-0.62, 1.53, z + 0.16),
                            (0.62, 1.53, z + 0.16),
                            (0.62, 1.53, z + 0.92),
                            (-0.62, 1.53, z + 0.92),
                        ],
                        lamp,
                        "8a9184",
                        1,
                    )
        for j in range(-3, 4):
            d.line([point(j, -1.45, cam + 0.25), point(j, -1.45, far)], "818471", 0.8)
        # Fixed flecks in world coordinates belong to the linoleum, not to the camera.
        r = seed(617)
        for i in range(1300):
            x = r.uniform(-3, 3)
            z = r.uniform(1, 31)
            if z > cam + 0.5:
                px, py = point(x, -1.448, z)
                if 96 < px < 670 and 185 < py < 433:
                    v = clamp(4 / (z - cam), 0.6, 3.2)
                    d.line(
                        [(px, py), (px + v, py - 0.18 * v)],
                        "575e4853" if i % 2 else "c4c3a349",
                        0.65,
                    )
        for z in [13.8, 24.3]:
            if z > cam + 0.8:
                for zz in [z, z + 1.1]:
                    plane(
                        [
                            (2.17, -1.4, zz),
                            (2.25, -1.4, zz),
                            (2.25, -0.94, zz),
                            (2.17, -0.94, zz),
                        ],
                        "606958",
                    )
                plane(
                    [
                        (2.1, -0.99, z - 0.18),
                        (2.92, -0.99, z - 0.18),
                        (2.92, -0.99, z + 1.45),
                        (2.1, -0.99, z + 1.45),
                    ],
                    "8d8970",
                    "73755f",
                    1,
                )
                plane(
                    [
                        (2.9, -0.94, z - 0.18),
                        (2.9, -0.60, z - 0.18),
                        (2.9, -0.60, z + 1.45),
                        (2.9, -0.94, z + 1.45),
                    ],
                    "8a896f",
                    "747762",
                    1,
                )
        # A striped gym ball rolls from the side into the corridor and toward a distant door.
        ballX = mix(-2.5, 0.12, span(t, 0.7, 5)) + sin(t * 1.8) * 0.09
        ballZ = cam + 5.4 + t * 0.76
        px, py = point(ballX, -1.21, ballZ)
        rr = 0.24 * 320 / (ballZ - cam)
        d.ell(px + 4, py + rr, rr * 0.94, rr * 0.25, "686c5c")
        d.circ(px, py, rr, "c6b778", "918b6d", 1)
        with d.at(px, py, 1, t * 2.8):
            d.ell(0, 0, rr * 0.32, rr * 0.91, None, "85846a", 1)
        d.txt(117, 24, "●", 10, "c6c4ab")
        d.txt(135, 24, "00:00:" + str(int(t)).zfill(2), 14, "d9d9c7", "mono")
        for y in range(0, 432, 4):
            d.rect(96, y, 576, 0.65, "4b564329")
        if 5.8 < t < 5.9:
            d.rect(96, 96, 576, 11, "d5d7bd80")


def scratch_film(d, t):
    q = int(t * 12) / 12
    r = seed(int(t * 12) * 31 + 9)
    d.bg("100e10")
    for j in range(154):
        x, y = r.randrange(768), r.randrange(432)
        d.line(
            [(x, y), (x + r.randrange(-1, 2), y + r.randrange(1, 7))], "71625359", 0.75
        )
    b, u = phase(t)
    cream = "f4e8ba"
    # One scratched spiral unwinds into antennae. The two wings are re-inscribed every exposure.
    if b == 0:
        n = int(45 + 155 * span(q, 0, 2.8))
        p = []
        for i in range(n):
            a = i * 0.088 + q * 0.2
            v = 8 + i * 0.48
            p.append(
                (
                    379 + cos(a) * v + r.uniform(-1.8, 1.8),
                    222 + sin(a) * v + r.uniform(-1.8, 1.8),
                )
            )
        d.line(p, "b5c6a4", 1.8)
        d.circ(*p[-1], 4, cream)
    else:
        x = 378 + 81 * span(t, 5.7, 8.7)
        y = 221 - 68 * span(t, 5.6, 8.6) + 6 * sin(q * 2)
        with d.at(x, y, 1, -0.12 + sin(q * 3) * 0.05):
            for sg in [-1, 1]:
                width = 0.63 + 0.32 * (1 + sin(q * (3 if b == 1 else 7))) / 2
                with d.at(0, 0, sg * width, sy=1):
                    for i in range(18):
                        p = []
                        size = 1 - i * 0.042
                        for j in range(64):
                            a = tau * j / 63
                            rx = 65 + 59 * cos(a)
                            ry = 45 * sin(a) - 20 - 34 * cos(a)
                            p.append(
                                (
                                    rx * size + r.uniform(-1.8, 1.8),
                                    ry * size + r.uniform(-1.8, 1.8),
                                )
                            )
                        d.line(
                            p,
                            ["e3af80", "d9c8a3", "a6c2b4"][i % 3],
                            0.8 if i % 3 else 1.5,
                        )
                    for i in range(9):
                        d.path(
                            f"M 4 8 Q {38 + i * 3 + r.random() * 3} {91 - i * 3} {64 - i * 5} {57 - i * 4} Q {88 - i * 4} {27 - i * 2} 4 8",
                            None,
                            "b9a6bf",
                            1,
                        )
            d.line([(0, -21), (1 + r.random(), 4), (0, 31)], cream, 4)
            for sg in [-1, 1]:
                d.path(f"M 0 -20 Q {sg * 7} -51 {sg * 26} -54", None, cream, 1.6)
    if b == 2:
        for j in range(21):
            a = j * 2.4 + q * 0.03
            v = sqrt(j) * 6.2
            d.line(
                [
                    (639 + v * cos(a), 80 + v * sin(a)),
                    (644 + v * cos(a), 71 + v * sin(a)),
                ],
                cream,
                1,
            )


def ocean(d, t):
    d.grad(
        0,
        0,
        768,
        432,
        [(0, "8c9496"), (0.40, "e2e0d6"), (0.55, "cbcfc9"), (1, "677478")],
    )
    for j in range(3):
        p = [
            (
                x,
                183
                + 7 * j
                + 11 * sin(x * 0.011 + j)
                + 7 * cos(x * 0.027 + j)
                + 2 * sin(x * 0.071),
            )
            for x in range(-4, 779, 5)
        ]
        d.poly(p + [(773, 223), (0, 223)], ["a0a7a4", "939d9c", "879290"][j])
    d.grad(
        0,
        215,
        768,
        217,
        [(0, "abb4b1"), (0.22, "c6ccc5"), (0.58, "99a5a5"), (1, "667579")],
    )
    rng = seed(981)
    for j in range(325):
        x = rng.randrange(800) - 16
        y = rng.randrange(216, 433)
        w = 2 + (y - 215) * rng.random() * 0.19
        xx = x + sin(t * 0.8 + j) * 4
        d.line(
            [(xx, y), (xx + w, y - 0.8 + sin(j + t) * 0.6)],
            "f3f0db50" if j % 3 else "55636655",
            0.55 + (y - 216) * 0.003,
        )


WHALE = "M -207 -5 C -267 -30 -273 -65 -309 -54 Q -308 -28 -282 -8 Q -278 9 -310 24 Q -280 37 -250 17 Q -226 5 -206 12 C -137 42 -63 72 39 72 Q 82 114 122 112 Q 111 90 92 71 C 155 75 242 58 257 21 C 270 -10 252 -43 212 -52 Q 138 -75 52 -63 Q 7 -58 -19 -60 Q -37 -96 -53 -93 L -53 -59 C -115 -54 -159 -29 -207 -5 Z"


def double_exposure(d, t):
    ocean(d, t)
    b, u = phase(t)
    x = 360 + 53 * span(t, 0, 8.8)
    y = 219 + 7 * sin(t * 0.68)
    s = 0.79 + 0.31 * span(t, 0.15, 6.4) - 0.04 * span(t, 6.4, 9)
    with d.at(x, y, s, -0.045 + 0.046 * sin(t * 0.56)):
        with d.clip(WHALE):
            d.grad(
                -325,
                -115,
                612,
                250,
                [
                    (0, "b5b7b2"),
                    (0.37, "818a89"),
                    (0.59, "777f7f"),
                    (0.81, "363f43"),
                    (1, "515a5d"),
                ],
            )
            # The inner harbour slides against the whale's travel. Layers have independent parallax.
            off = 30 * sin(t * 0.34) - t * 3
            for j in range(2):
                for i in range(22):
                    ax = -336 + i * 33 + off * (0.45 + j * 0.6)
                    h = 18 + (i * 37 + j * 22) % 54
                    yy = 41 + j * 13
                    d.rect(ax, yy - h, 30, h, ["616a6b", "3a4448"][j])
                    for k in range(3):
                        for m in range(2 + (i % 3)):
                            if (k + i + m) % 3:
                                d.rect(
                                    ax + 4 + k * 7,
                                    yy - h + 6 + m * 7,
                                    2.6,
                                    3.2,
                                    "d5ae75" if j and t > 2.7 else "929a99",
                                )
            for i in range(3):
                ax = -198 + i * 154 + off
                d.poly(
                    [(ax - 4, 38), (ax + 1, -37), (ax + 5, -37), (ax + 7, 38)], "333d40"
                )
                d.line(
                    [
                        (ax - 17, -33),
                        (ax + 3, -52),
                        (ax + 74, -62),
                        (ax + 63, -55),
                        (ax - 17, -33),
                    ],
                    "354044",
                    2.5,
                )
                d.line([(ax + 56, -55), (ax + 56, 3)], "41494b", 1)
                if t > 4.1:
                    d.circ(ax + 3, -52, 2, "e6be83")
            d.rect(-324, 53, 615, 68, "515d60")
            for j in range(100):
                xx = -320 + (j * 37 + sin(t + j) * 3) % 610
                yy = 54 + j * 17 % 62
                d.line(
                    [(xx, yy), (xx + 5 + j % 11, yy)],
                    "d5bc8e70" if j % 7 == 0 and t > 4 else "83909188",
                    1,
                )
        d.path(WHALE, None, "4c585976", 1)
        d.circ(213, -11, 2.5, "343c3e")
        d.path("M 194 24 Q 222 22 251 9", None, "5a6260", 1)
    if t > 6.5:
        v = span(t, 6.5, 8.55)
        for j in range(11):
            a = -(0.35 + j * 0.21)
            xx = x + s * 156 + cos(a) * 40 * v
            yy = y - s * 65 + sin(a) * 39 * v
            d.ell(xx, yy, 1.3, 2.5, "e2e4db")
