"""Original drawing performances, each defined in its own scene coordinates."""

from drawing import *
from functools import lru_cache


@lru_cache(maxsize=32)
def marks(seed, n):
    return rnd(seed).random((n, 5)).tolist()


def crayon_book(c, t):
    paper = "f3e9cd"
    blue = "526d95"
    c.bg(paper)
    # A tide of blue wash uncovers the wax stars.
    water = smooth((t - 3.1) / 3.8)
    for i in range(4):
        y = 354 - water * 350 - i * 5
        border = [
            (x, y + 11 * sin(x * 0.017 + i * 0.6) + 4 * sin(x * 0.075))
            for x in range(-8, 790, 8)
        ]
        c.poly(border + [(794, 440), (-10, 440)], blue, a=0.20)
    for x, y, k in [
        (68, 83, 12),
        (184, 150, 9),
        (321, 72, 15),
        (437, 116, 8),
        (591, 74, 16),
        (674, 143, 11),
        (517, 192, 9),
    ]:
        if y > 353 - water * 350:
            c.poly(
                [
                    (
                        x + cos(-pi / 2 + i * pi / 5) * k * (1 if i % 2 == 0 else 0.38),
                        y + sin(-pi / 2 + i * pi / 5) * k * (1 if i % 2 == 0 else 0.38),
                    )
                    for i in range(10)
                ],
                "fff0b4",
            )
    c.path(
        "M -30 354 Q 131 257 291 310 Q 469 359 625 286 Q 708 266 805 298 L 805 440 L -30 440 Z",
        "a6ad77",
    )
    for a, b, d, e, _ in marks(91, 440):
        x = a * 800
        y = 309 + b * 123 + 11 * sin(x * 0.018)
        c.line(
            [(x, y), (x + 8 + d * 11, y - 6 - e * 5)],
            "59745a" if a > 0.5 else "e1cd87",
            1.9,
            0.76,
        )
    px = mix(375, 528, smooth((t - 2.6) / 4))
    with c.transform(px, 303 + 4 * sin(t * 3), 1, -0.12 + t * 0.14):
        c.path("M -3 -46 Q 5 -61 11 -67", None, "5a5539", 5)
        c.path("M 0 -47 Q 22 -67 36 -55 Q 20 -40 0 -47 Z", "73894e")
        c.path(
            "M -3 -45 Q -13 -39 -17 -22 Q -45 -4 -35 17 Q -22 42 4 35 Q 43 37 42 3 Q 39 -15 20 -25 Q 14 -48 -3 -45 Z",
            "dab34e",
            "8e6b45",
            3,
        )
        for a, b, *_ in marks(13, 55):
            x = -20 + a * 44
            y = -10 + b * 32
            c.line([(x, y), (x + 7, y - 8)], "eed077", 2)
    hx = mix(156, 431, smooth(t / 6.7))
    with c.transform(hx, 308 + 3 * sin(t * 5)):
        for dx in [-37, 9]:
            c.ellipse(dx, 28, 11, 6, "654a43")
        c.path(
            "M -73 15 Q -80 -42 -41 -56 Q 2 -75 35 -38 L 45 -13 L 76 1 Q 63 25 31 25 Q -17 39 -73 15 Z",
            "ae7752",
            "594a4d",
            4,
        )
        for a, b, d, e, _ in marks(12, 120):
            x = -66 + a * 91
            y = -15 - b * 35 * (1 - (x + 18) ** 2 / 3200)
            c.line(
                [(x + 6, y + 9), (x - 7 - d * 7, y - 6 - e * 4)],
                "675052" if a > 0.45 else "dbc18a",
                2.4,
            )
        c.circle(41, -7, 3, "302d39")
        c.circle(74, 1, 5, "56434a")
    c.line([(22, 18), (22, 411)], "bcad8c", 1.4, 0.55)


def petal(c, x, y, k, rot, col):
    with c.transform(x, y, k, rot):
        for j in range(3):
            with c.transform(j * 0.8, j * 0.67):
                c.path(
                    "M 0 0 C -14 -5 -32 -35 -20 -56 Q -11 -72 -3 -55 C 16 -67 29 -46 16 -26 Q 9 -11 0 0 Z",
                    col,
                    a=0.25,
                )
        c.path("M 0 -2 Q -9 -29 -8 -48", None, col, 1, 0.45)


def iris(c, x, y, k, t, opening, col):
    with c.transform(x, y, k):
        c.path("M 0 138 Q -6 71 1 0", None, "617c61", 3)
        for off, dx in [(105, -54), (127, 41), (133, -24)]:
            c.path(
                f"M 0 {off} Q {dx} {off - 35} {dx} {off - 84} Q {dx + 7} {off - 47} 0 {off} Z",
                "7b956d",
                a=0.62,
            )
        for j, (r, s) in enumerate(
            [(-1.16, 0.90), (0.92, 1), (-0.14, 0.90), (2.28, 0.64), (-2.35, 0.68)]
        ):
            petal(
                c,
                0,
                1,
                s * (0.42 + 0.58 * opening),
                r * (0.30 + 0.70 * opening) + 0.035 * sin(t + j),
                col,
            )
        c.path("M -6 2 Q 1 -12 7 -11 L 2 1 Z", "dfb14e")


def watercolor(c, t):
    c.bg("f4eedf")
    for j in range(4):
        pts = (
            [(-10, 304 + j * 16)]
            + [(x, 290 + j * 23 + 18 * sin(x * 0.011 + j)) for x in range(0, 800, 16)]
            + [(800, 432), (-10, 432)]
        )
        c.poly(pts, ["ced4bf", "b5cbba", "a4beb4", "8ea89d"][j], a=0.40)
    for j in range(15):
        x = j * 61 - 25
        iris(c, x, 276 + 17 * sin(j), 0.32 + (j % 4) * 0.038, t, 0.8, "879b9c")
    for x, y, k, offset, col in [
        (210, 239, 0.88, 0, "8995b9"),
        (381, 207, 1.43, 1.2, "746ca5"),
        (559, 256, 1.02, 2.4, "917da4"),
    ]:
        iris(c, x, y, k, t, smooth((t - offset) / 3), col)
    u = smooth((t - 3.0) / 4.6)
    x = 69 + 440 * u
    y = 125 + 90 * u - 36 * sin(u * pi * 2)
    with c.transform(x, y, 0.8, -0.16):
        for dx, dy, ang in [(0, 0, -0.8), (-2, 3, -1.12), (1, 0, 0.65), (1, 2, 0.98)]:
            with c.transform(dx, dy, 1, ang + 0.16 * sin(t * 25)):
                c.ellipse(-10, -3, 23, 3.5, None, "819e94", 1.1, 0.86)
        c.line([(-26, 0), (13, 0)], "46645e", 2)
        c.circle(13, 0, 3, "52685d")
    c.txt("붓꽃", 667, 45, 23, "727a69", False, True)
    c.line([(670, 82), (709, 80)], "aaad96", 1)


def knife(c, x, y, w, h, col, angle):
    with c.transform(x, y, 1, angle):
        c.poly(
            [
                (0, h * 0.24),
                (w * 0.19, 0),
                (w, h * 0.11),
                (w * 0.85, h * 0.86),
                (w * 0.13, h),
            ],
            col,
        )
        c.line(
            [(w * 0.15, h * 0.18), (w * 0.84, h * 0.14)],
            blend(col, "fae2ad", 0.35),
            max(0.8, h * 0.10),
        )


def impasto(c, t):
    c.bg("334d66")
    for a, b, d, e, f in marks(323, 520):
        x = a * 810 - 15
        y = b * 442 - 5
        col = (
            ["637f91", "536d80", "81959a", "475e76"]
            if y < 170
            else ["465e73", "809596", "758e94", "4c697c", "b79472"]
        )[int(d * 4)]
        knife(c, x, y, 11 + f * 45, 3 + e * 9, col, -0.08 + b * 0.11)
    for j, (x, top) in enumerate([(80, 59), (672, 89)]):
        for k in range(25):
            y = top + k * 7
            knife(
                c,
                x + 3 * sin(k),
                y,
                18 + 3 * sin(k),
                11,
                ["ac7153", "cb9368", "8a6156"][k % 3],
                -0.04,
            )
        for k in range(18):
            y = top + 178 + k * 7
            knife(
                c,
                x - 16 + 9 * sin(k + t * 2),
                y,
                20 + 15 * sin(k * 0.5) ** 2,
                3.8,
                "c29572",
                -0.03,
            )
    x = 95 + 64 * t
    y = 199 + 16 * sin(t * 0.65)
    for j in range(34):
        dx = j * 5
        knife(
            c,
            x - dx - 40,
            y + 29 + dx * 0.22 + 3 * sin(t * 3 + j),
            22,
            3,
            "b8ad92",
            0.08,
        )
    with c.transform(x, y, 1, -0.07 + 0.035 * sin(t * 3)):
        c.path("M -82 -10 Q -17 -36 88 -17 Q 55 24 -24 25 Q -56 21 -82 -10 Z", "613f39")
        c.path("M -78 -13 Q -2 -36 87 -18 Q 39 -3 -27 1 Z", "d9854e")
        for j in range(14):
            knife(
                c,
                -59 + j * 9,
                -4 + 4 * sin(j / 3),
                14,
                7,
                "c07a52" if j % 2 else "a45f45",
                -0.08,
            )
        c.poly([(-20, -21), (-13, -50), (22, -52), (38, -25)], "d9ba86")
        c.poly([(-8, -45), (16, -46), (25, -28), (-10, -27)], "5c747b")
        knife(c, -22, -51, 48, 6, "efd09b", -0.03)
    for j in range(19):
        knife(
            c,
            x - 31 + sin(j * 3 + t) * 21,
            y + 34 + j * 5,
            23 + j % 10,
            4,
            ["c98c5e", "a57f69", "967e79"][j % 3],
            -0.05,
        )


def urban_sketch(c, t):
    c.bg("f3eada")
    ink = "65584d"
    with c.transform(-3 * t, 0):
        for j, (x, y, w, roof) in enumerate(
            [
                (-28, 111, 176, 72),
                (143, 132, 163, 96),
                (302, 88, 239, 49),
                (540, 120, 146, 83),
                (684, 102, 169, 70),
            ]
        ):
            c.poly(
                [
                    (x + 3, y + 3),
                    (x + w / 2, roof + 2),
                    (x + w + 6, y + 2),
                    (x + w + 4, 312),
                    (x + 1, 317),
                ],
                ["e1c3a4", "c5c9bd", "d6b6a0", "c1c5c0", "dcc7a8"][j],
                a=0.72,
            )
            c.line(
                [
                    (x - 6, y + 2),
                    (x + w * 0.48, roof - 3),
                    (x + w + 9, y - 1),
                    (x + w - 2, y + 3),
                    (x + w * 0.50, roof + 4),
                    (x - 11, y + 9),
                ],
                ink,
                1.6,
            )
            c.line([(x + 3, y + 12), (x + 1, 311), (x + w + 5, 314)], ink, 1.7)
            for k in range(3):
                xx = x + 17 + k * (w - 32) / 3
                ww = (w - 60) / 3
                c.rect(xx + 3, y + 32, ww, 45, "9ba8a0", a=0.63)
                c.line(
                    [
                        (xx, y + 27),
                        (xx + ww + 1, y + 25),
                        (xx + ww + 2, y + 75),
                        (xx - 2, y + 78),
                        (xx, y + 25),
                    ],
                    ink,
                    1.5,
                )
                c.line([(xx + ww * 0.5, y + 28), (xx + ww * 0.51, y + 76)], ink)
            c.rect(x + 17, 236, w - 34, 73, "b7aca0", a=0.60)
            for k in range(5):
                c.line(
                    [
                        (x + 20 + k * (w - 36) / 5, 239),
                        (x + 19 + k * (w - 36) / 5, 312),
                    ],
                    ink,
                    1,
                )
            for k in range(9):
                xx = x + 3 + k * (w - 6) / 9
                ww = (w - 6) / 9
                c.poly(
                    [(xx + 3, 208), (xx + ww, 208), (xx + ww - 5, 235), (xx - 6, 238)],
                    "9b7666" if k % 2 else "e7dac3",
                    ink,
                    0.8,
                )
            for k in range(10):
                xx = x + 10 + (k * 41) % (int(w) - 20)
                yy = y + 13 + (k * 23) % 82
                c.line([(xx, yy), (xx + 7, yy - 2)], ink, 0.6, 0.54)
        # Merchants leave flower buckets and crates in the band of pavement below the awnings.
        for x, y in [(73, 307), (121, 309), (438, 308), (646, 311)]:
            c.poly(
                [(x - 9, y - 15), (x + 10, y - 15), (x + 6, y), (x - 6, y)],
                "bbb7a7",
                ink,
                1.1,
            )
            for k in range(8):
                dx = 10 * sin(k * 2.4)
                dy = 15 + (k * 19) % 22
                c.path(
                    f"M {x} {y - 15} Q {x + dx * 0.6} {y - 30} {x + dx} {y - dy - 13}",
                    None,
                    "79846f",
                    1,
                )
                c.ellipse(
                    x + dx,
                    y - dy - 13,
                    2.8,
                    2.1,
                    "b47f72" if k % 2 else "c4ac79",
                    ink,
                    0.5,
                )
        for x in [195, 230, 542]:
            c.rect(x, 287, 26, 21, "c7b292", ink, 1.3)
            for k in [5, 11, 17]:
                c.line([(x + 2, 287 + k), (x + 24, 286 + k)], ink, 0.8)
        c.path("M 340 239 L 340 311 L 373 311 L 373 238 Z", "a39b88", ink, 1.3)
        c.rect(344, 243, 25, 41, "c7c9b5", ink, 0.8)
        c.circle(367, 290, 1.6, ink)
        c.path(
            "M 12 30 Q 79 48 159 48 Q 229 70 324 54 Q 223 75 151 53 Q 77 55 2 33 Z",
            "b4b29c",
            ink,
            0.65,
        )
        for k in range(13):
            xx = 24 + k * 14
            yy = 32 + 19 * sin(k * 0.1)
            c.path(
                f"M {xx} {yy} Q {xx + 6} {yy - 11} {xx + 16} {yy - 8} Q {xx + 12} {yy} {xx} {yy} Z",
                "a7ae93",
                ink,
                0.65,
            )
        c.path(
            "M -20 327 Q 310 308 828 330 M -10 339 Q 292 323 822 343", None, ink, 1.3
        )
    x = 85 + 65 * t
    y = 336
    with c.transform(x, y):
        for dx in [-30, 30]:
            c.circle(dx, 0, 18, None, ink, 2.3)
            for j in range(6):
                a = t * 4 + j * pi / 3
                c.line([(dx, 0), (dx + 18 * cos(a), 18 * sin(a))], ink, 0.8)
        c.line(
            [(-30, 0), (-10, -23), (2, -1), (-30, 0), (18, -22), (30, 0)], "9e594b", 2.5
        )
        c.line([(-12, -25), (-18, -28)], ink, 3)
        c.circle(-1, -55, 6, "ad8972", ink, 1)
        c.path("M -6 -51 Q -20 -42 -16 -28 L -3 -29 L 4 -46 Z", "9f5e50", ink, 1.4)
        c.line([(-1, -44), (7, -31), (18, -27)], ink, 2)
        c.line([(-11, -28), (1, -18), (-5 + 6 * sin(t * 7), -6)], ink, 3)
    c.txt("장날 오후", 39, 382, 20, ink, False, True)
    c.line([(43, 412), (132, 407)], ink, 0.9)


def colored_pencil(c, t):
    c.bg("eae7d3")
    cam = 12 * smooth((t - 1.6) / 4)
    with c.transform(-cam, -cam * 0.6):
        for j in range(3):
            pts = [
                (x, 102 + j * 23 + 13 * sin(x * 0.012 + j * 0.8))
                for x in range(-8, 811, 10)
            ]
            c.poly(pts + [(810, 190), (-10, 190)], ["c9cfb7", "b9c5a4", "aabe8d"][j])
        for j, col in enumerate(["ad926e", "b7a07d", "bead92", "a49889"]):
            y = 155 + j * 72
            pts = [
                (x, y + 6 * sin(x * 0.022 + j) + 5 * cos(x * 0.047))
                for x in range(-7, 808, 8)
            ]
            c.poly(pts + [(810, 460), (-7, 460)], col, "98886f", 1.1)
        for a, b, d, e, f in marks(432, 1250):
            x = a * 806
            y = 160 + b * 302
            c.line(
                [(x, y), (x + 4 + 8 * d, y - 2 - e * 4)],
                "756b60" if f < 0.48 else "e6d1a7",
                0.9,
                0.68,
            )
        for x, y, rx in [
            (111, 262, 17),
            (210, 346, 23),
            (644, 288, 28),
            (510, 362, 18),
            (71, 385, 28),
        ]:
            c.ellipse(x, y, rx, rx * 0.53, "aa9d89", "817c73", 1.3)
            for k in range(4):
                c.line(
                    [(x - rx * 0.55 + k * 4, y + 3), (x - rx * 0.37 + k * 4, y - 3)],
                    "ded3b7",
                    1,
                )
        x = 380
        with c.transform(x, 208, 1, -0.44):
            c.ellipse(0, 0, 24, 14, "a86452", "765744", 2)
            c.path("M -15 -1 Q 0 -11 16 2", None, "d79d71", 2)
        root = [(x + 7 * sin(i * 0.095), 214 + i) for i in range(130)]
        c.line(progress(root, (t - 0.4) / 4.4), "e6d7ae", 5)
        for j in range(11):
            yy = 232 + j * 8
            pts = [
                (
                    x + 6 * sin((yy - 214) * 0.095) + (1 if j % 2 else -1) * i,
                    yy + i * 0.43 + 4 * sin(i * 0.07),
                )
                for i in range(29 + j % 4 * 5)
            ]
            c.line(progress(pts, (t - 1.1 - j * 0.20) / 2.8), "e9d9b2", 1.7)
        shoot = smooth((t - 2.8) / 3.3)
        yy = 203 - shoot * 119
        c.path(f"M 381 205 Q 363 {yy + 31} 392 {yy}", None, "678455", 4)
        for j in [-1, 1]:
            with c.transform(
                391,
                yy + 1,
                max(0.01, smooth((t - 4.1) / 3)),
                0.16 * j,
                sy=max(0.01, smooth((t - 4.1) / 3)),
            ):
                c.path(
                    f"M 0 0 Q {j * 30} -43 {j * 57} -35 Q {j * 44} -3 0 0 Z",
                    "8fa565",
                    "637c51",
                    1.4,
                )
                c.line([(0, 0), (j * 44, -28)], "728b55", 1)
    if t > 1.4:
        c.line([(240, 256), (297, 256), (355, 230)], "746f60", 1)
        c.rect(163, 242, 80, 29, "ede6ce")
        c.txt("어린 뿌리", 169, 248, 15, "676354", False, True)
    if t > 5.1:
        c.line([(539, 77), (475, 77), (430, 97)], "78755f")
        c.txt("떡잎", 546, 63, 20, "647256", False, True)


@lru_cache(maxsize=1)
def tea_line():
    # One continuously connected nib path, sampled by distance.
    segments = [
        ((30, 299), (74, 301), (100, 300)),
        ((129, 300), (135, 280), (136, 268)),
        ((84, 253), (81, 206), (109, 206)),
        ((125, 200), (130, 216), (139, 222)),
        ((148, 191), (161, 181), (179, 177)),
        ((175, 166), (200, 161), (204, 176)),
        ((220, 174), (238, 178), (249, 185)),
        ((257, 189), (254, 194), (239, 192)),
        ((253, 203), (260, 220), (262, 230)),
        ((285, 224), (299, 202), (310, 194)),
        ((317, 191), (326, 195), (325, 200)),
        ((305, 209), (309, 267), (268, 272)),
        ((254, 291), (226, 300), (192, 298)),
        ((156, 298), (143, 287), (136, 268)),
        ((154, 289), (178, 303), (221, 302)),
        ((275, 305), (290, 289), (311, 275)),
        ((337, 257), (354, 235), (367, 233)),
        ((374, 230), (381, 232), (390, 235)),
        ((421, 224), (468, 224), (489, 235)),
        ((499, 247), (411, 254), (390, 235)),
        ((391, 274), (406, 299), (444, 297)),
        ((471, 299), (489, 277), (492, 245)),
        ((530, 227), (542, 265), (486, 278)),
        ((481, 295), (464, 303), (448, 304)),
        ((499, 305), (532, 307), (534, 312)),
        ((537, 328), (377, 325), (372, 313)),
        ((379, 306), (394, 305), (414, 306)),
        ((475, 302), (510, 271), (502, 239)),
        ((490, 210), (442, 194), (458, 164)),
        ((471, 142), (512, 142), (505, 115)),
        ((498, 94), (468, 95), (472, 77)),
        ((478, 61), (510, 66), (525, 72)),
    ]
    p = (10, 300)
    arr = [p]
    for a, b, d in segments:
        for f in np.linspace(0.04, 1, 25):
            arr.append(
                tuple(
                    (1 - f) ** 3 * p[k]
                    + 3 * (1 - f) ** 2 * f * a[k]
                    + 3 * (1 - f) * f * f * b[k]
                    + f**3 * d[k]
                    for k in (0, 1)
                )
            )
        p = d
    pts = np.array(arr)
    dist = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    s = np.linspace(0, dist[-1], 900)
    return np.stack([np.interp(s, dist, pts[:, j]) for j in range(2)], axis=1).tolist()


def one_line(c, t):
    c.bg("f6f0e4")
    line = progress(tea_line(), 0.08 + 0.92 * smooth(t / 8.4))
    nx, ny = line[-1]
    zoom = 1.38 - 0.27 * smooth((t - 5.7) / 2.5)
    ox = mix(134, -23, smooth((t - 1) / 4.7)) + 54 * smooth((t - 6) / 2)
    with c.transform(ox, 8, zoom):
        for j in range(0, len(line) - 1, 9):
            c.line(line[j : j + 10], "393730", 1.5 + 0.55 * (1 + sin(j * 0.028)))
        if t < 8.42:
            c.ellipse(nx + 5, ny + 5, 8.5, 3, "524a40", a=0.11)
            c.circle(nx, ny, 1.55, "302d28")
    if t > 8:
        c.circle(674, 341, 3 * smooth(t - 8), "b67255")


def whiteboard(c, t):
    c.gradient("f3f4ec", "e7ebe4")
    c.poly([(22, 0), (72, 0), (331, 432), (273, 432)], "ffffff", a=0.39)
    c.poly([(90, 0), (108, 0), (375, 432), (352, 432)], "ffffff", a=0.33)
    for a, b, d, e, f in marks(88, 70):
        x = a * 760
        y = b * 417
        c.line([(x, y), (x + 7 + d * 49, y + 1)], "bac5bd", 0.6, 0.30)
    dx = mix(36, -14, smooth(t / 7))
    with c.transform(dx, 0):
        c.txt("길이가 다른 두 진자", 55, 39, 30, "384c4d", True)
        p = [(126 + i, 113 + 1.1 * sin(i / 43)) for i in range(512)]
        c.line(progress(p, (t + 0.22) / 1.35), "344f51", 4)
        for j, (px, length) in enumerate([(242, 186), (530, 93)]):
            start = 1.1 + j * 1.8
            s = smooth((t - start) / 1.3)
            if s == 0:
                continue
            ang = 0.56 * cos(max(0, t - 4.5) * (2 if j == 0 else 2.828))
            ex = px + length * sin(ang)
            ey = 113 + length * cos(ang)
            c.line([(px, 113), (mix(px, ex, s), mix(113, ey, s))], "354e50", 3)
            c.circle(px, 113, 6, "636f70")
            c.circle(px - 1.5, 111, 1.8, "fafff3")
            c.circle(ex, ey, 13 * s, "387e85" if j == 0 else "ca744f")
            if t > 4.5:
                tail = []
                for z in np.linspace(max(4.5, t - 0.37), t, 20):
                    theta = 0.56 * cos((z - 4.5) * (2 if j == 0 else 2.828))
                    tail.append((px + length * sin(theta), 113 + length * cos(theta)))
                c.line(tail, "649395" if j == 0 else "d28f75", 1.5)
        if t < 4.38:
            if t < 1.1:
                xx = 126 + 511 * clamp((t + 0.22) / 1.35)
                yy = 113
            else:
                j = int(t >= 2.9)
                s = smooth((t - 1.1 - j * 1.8) / 1.3)
                xx = [242, 530][j] + [186, 93][j] * sin(0.56) * s
                yy = 113 + [186, 93][j] * cos(0.56) * s
            with c.transform(xx, yy, 1, -0.71):
                c.poly([(0, 0), (1, -7), (6, -7)], "384746")
                c.rect(-1, -48, 9, 41, "c4ceca", "777f79")
                c.rect(-1, -49, 9, 8, "418384")
        if t > 5.1:
            c.txt("긴 줄", 217, 328, 20, "387e85", True)
        if t > 6.1:
            c.txt("짧은 줄", 503, 328, 20, "ab6247", True)
    c.rect(0, 402, 768, 6, "b9c4c1")
    c.rect(0, 409, 768, 23, "cdd4ce")
    c.rect(614, 396, 64, 7, "648b8c")


def chalkboard(c, t):
    c.bg("6e6958")
    c.rect(14, 11, 740, 399, "243e38", "9d9176", 6)
    for a, b, d, e, f in marks(10, 560):
        x = 19 + a * 729
        y = 17 + b * 384
        c.line([(x, y), (x + d * 3 + 0.5, y - 0.5)], "9da89a", 0.8, 0.26)
    c.txt("한 원에 같은 길이를 여섯 번", 38, 34, 24, "d6ddc9")
    x, y, r = 375, 233, 131
    circle = spool(x, y, r, 270)
    c.line(progress(circle, 0.1 + 0.9 * smooth(t / 2.2)), "d2dac5", 2.4)
    for j in range(6):
        a = -pi / 2 + j * pi / 3
        b = a + pi / 3
        pts = [(x + r * cos(a), y + r * sin(a)), (x + r * cos(b), y + r * sin(b))]
        f = smooth((t - 1.8 - j * 0.65) / 0.65)
        if f:
            c.line(progress(pts, f), "e6c981", 2.8)
            c.circle(*pts[0], 3, "f0d897")
        if t > 5.65:
            pet = [
                (
                    pts[0][0] + r * cos(a + pi - pi / 3 + k * 2 * pi / 3),
                    pts[0][1] + r * sin(a + pi - pi / 3 + k * 2 * pi / 3),
                )
                for k in np.linspace(0, 1, 80)
            ]
            c.line(progress(pet, (t - 5.65 - j * 0.17) / 1.1), "a3c7bb", 1.7)
    c.circle(x, y, 2.4, "e1dfc8")
    c.rect(18, 409, 729, 9, "a19578")
    c.rect(617, 403, 37, 6, "d6d7bd")
    if t > 6.9:
        c.txt("정육각형", 555, 209, 27, "e8d394", True)


def sketchnote(c, t):
    c.bg("f6f1de")
    for x in range(11, 770, 17):
        for y in range(10, 434, 17):
            c.circle(x, y, 0.7, "b3b1a0")
    ink = "383a36"
    yellow = "e9bd54"
    c.poly([(38, 44), (277, 40), (272, 68), (33, 74)], yellow)
    c.txt("빗소리 채집 노트", 39, 26, 31, ink, True)
    # A page develops from a cloud at the upper left to a tape at the lower right.
    with c.transform(139, 194):
        c.path(
            "M -77 4 Q -88 -17 -62 -26 Q -59 -52 -34 -49 Q -12 -78 12 -53 Q 37 -56 45 -34 Q 75 -37 76 -12 Q 85 7 58 10 L -63 11 Z",
            "d7d7c9",
            ink,
            2.6,
        )
        for j in range(11):
            dx = -49 + j * 10
            y = 19 + ((t * 31 + j * 15) % 48)
            c.line([(dx, y), (dx - 4, y + 8)], ink, 1.7)
    c.txt("빗방울", 105, 283, 20, ink, True)
    if t > 1.4:
        pts = [(220 + i * 1.5, 216 - 41 * sin(i / 69 * pi / 2)) for i in range(70)]
        c.line(progress(pts, (t - 1.4) / 1.3), ink, 2.4)
        if t > 2.6:
            c.line([(311, 171), (326, 175), (316, 183)], ink, 2.4)
    if t > 2.4:
        with c.transform(393, 155, min(1, 0.25 + smooth((t - 2.4) / 0.6))):
            c.rect(-32, -39, 63, 85, "c7c9ba", ink, 3)
            c.rect(-24, -30, 48, 31, yellow, ink, 2)
            c.line(
                [
                    (-18, -13),
                    (-13, -14),
                    (-8, -20),
                    (-3, -7),
                    (5, -23),
                    (10, -10),
                    (18, -15),
                ],
                ink,
                1.6,
            )
            c.circle(0, 23, 10, "ece9d8", ink, 2)
            for j in range(3):
                c.rect(-18 + j * 13, 3, 6, 3, ink)
        c.txt("녹음", 367, 220, 20, ink, True)
    if t > 4.3:
        p = [(435 + i * 2.2, 200 + i * 0.96 - 8 * sin(i / 12)) for i in range(49)]
        c.line(progress(p, (t - 4.3) / 1.22), ink, 2.4)
        if t > 5.4:
            c.line([(527, 247), (541, 246), (537, 234)], ink, 2)
    if t > 5.35:
        with c.transform(621, 268, smooth((t - 5.35) / 0.6) * 0.92 + 0.01, -0.08):
            c.rect(-76, -43, 152, 87, "e8c263", ink, 3)
            c.rect(-62, -31, 123, 44, "eae7d6", ink, 2)
            for j in [-1, 1]:
                c.circle(39 * j, -9, 13, None, ink, 2)
                for k in range(4):
                    a = k * pi / 2 + t * 3
                    c.line(
                        [
                            (39 * j + 8 * cos(a), -9 + 8 * sin(a)),
                            (39 * j + 12 * cos(a), -9 + 12 * sin(a)),
                        ],
                        ink,
                        2,
                    )
            c.poly([(-38, 30), (-26, 16), (30, 16), (43, 30)], None, ink, 2)
        c.txt("다시 듣기", 577, 339, 21, ink, True)
    c.line([(30, 399), (730, 394)], ink, 1.4)


def stick_explainer(c, t):
    c.bg("f2ecda")
    ink = "393b33"
    accent = "b96b3e"
    c.line([(0, 322), (768, 322)], ink, 3)
    c.txt("한 권씩 건네면", 40, 39, 31, ink, True)
    xs = [137, 300, 463, 626]
    for j, x in enumerate(xs):
        start = j * 2.05
        passage = smooth((t - start) / 1.5)
        lean = sin(pi * passage) * 9
        if j > 0:
            lean -= 7 * sin(pi * smooth((t - start + 1.2) / 1.3))
        hx = x + lean
        cy = 180 - 3 * sin(t + j)
        c.circle(hx, cy, 14, None, ink, 3.3)
        c.circle(hx + 4, cy - 1, 1.3, ink)
        c.line([(hx, cy + 15), (x, 252), (x - 18, 318), (x - 29, 319)], ink, 4)
        c.line([(x, 252), (x + 19, 313), (x + 28, 319)], ink, 4)
        c.line(
            [(hx, cy + 28), (hx - 12, 231), (x - 29 - 12 * sin(t * 1.5 + j), 219)],
            ink,
            3,
        )
        c.line(
            [(hx, cy + 28), (hx + 18, 222 - lean), (x + 38 + lean, 212 - lean)], ink, 3
        )
    step = min(2, int(t / 2.05))
    u = smooth((t - 2.05 * step - 0.35) / 1.50)
    x = mix(xs[step] + 34, xs[step + 1] + 32, u)
    y = 205 - 52 * sin(pi * u)
    if t > 6.4:
        u = smooth((t - 6.4) / 1.38)
        x = mix(658, 672, u)
        y = mix(205, 289, u)
    c.rect(650, 299, 82, 20, "c9c0a8", ink, 2)
    c.rect(656, 287, 74, 10, "ded5bc", ink, 2)
    with c.transform(x, y, 1, -0.13 - 0.29 * sin(u * pi)):
        c.rect(-18, -13, 40, 23, accent, ink, 2)
        c.rect(-16, 5, 36, 4, "e6dabf")
        c.line([(-11, -11), (-11, 5)], "ead2ac", 1.2)
    for j, x in enumerate(xs[:-1]):
        if t > j * 2.05 + 1.85:
            c.line([(x + 41, 356), (x + 79, 356), (x + 73, 351)], accent, 2)
    if t > 7.5:
        c.txt("도착", 684, 249, 18, accent, True, center=True)


def ipad_sketch(c, t):
    c.bg("f1e8d9")
    ink = "555862"
    with c.transform(385, 229, 1, -0.06):
        for j in range(4):
            c.line([(-249 + j * 3, -109), (200 + j * 2, 56 - j * 2)], "c6bdb5", 0.8)
        c.line([(-229, 119), (244, -125)], "b8b1aa", 1)
        c.line([(-166, -130), (108, 129)], "c7bfb3", 1)
        shape = [
            (-220, 32),
            (-73, -73),
            (39, -36),
            (213, -103),
            (134, 15),
            (37, 77),
            (-53, 55),
            (-119, 127),
            (-105, 38),
        ]
        shapes = [
            ([(-220, 32), (-73, -73), (-44, 13), (-105, 38)], "b6c7be"),
            ([(-73, -73), (39, -36), (-44, 13)], "d5c6b4"),
            ([(-44, 13), (39, -36), (213, -103), (37, 77)], "8ea8af"),
            ([(37, 77), (213, -103), (134, 15)], "c6a49d"),
            ([(-105, 38), (-44, 13), (37, 77), (-53, 55), (-119, 127)], "dbb6a3"),
        ]
        for j, (pts, col) in enumerate(shapes):
            f = smooth((t - 2.25 - j * 0.58) / 1.12)
            if f:
                with c.window(-240, -149, 480 * f, 320):
                    c.poly([(x + 2.5, y + 1.8) for x, y in pts], col)
            q = progress(pts + [pts[0]], (t - 0.24 * j) / 1.9)
            c.line(q, ink, 1.4)
        for a, b, d, e, f in marks(42, 115):
            x = -65 + a * 55
            y = -41 + b * 47
            if x + y > -71:
                c.line([(x, y), (x + 7, y - 5)], "9eaaa4", 0.8)
        c.line(progress(shape + [shape[0]], (t + 0.1) / 2.7), ink, 2.4)
        if t > 5.25:
            f = smooth((t - 5.25) / 1.55)
            c.line(progress([(213, -103), (181, -58), (156, -43)], f), "bd7469", 3.5)
            c.circle(126, -59, 2.8 * f, ink)
        if t > 6.8:
            for j in range(3):
                p = [
                    (-189 - i * 0.85, -17 - 12 * j - 11 * sin(i * 0.04 + j))
                    for i in range(46)
                ]
                c.line(progress(p, t - 6.8 - j * 0.2), "b2786f", 1.5)
    c.txt("종이새", 52, 49, 22, "81796e", False, True)
    for j, col in enumerate(["565960", "99b2b0", "c8998a"]):
        c.circle(656 + j * 23, 373, 7, col)


def marker_paper(c, t):
    c.bg("f8f4e8")
    ink = "303632"
    blue = "437d90"
    red = "b65849"
    c.txt("선 하나를 사이에 두고", 42, 32, 27, ink, True)
    c.line(progress([(384, 93), (384, 351)], t / 1.25), ink, 5)
    pts = [
        (140, 280),
        (165, 173),
        (227, 118),
        (285, 167),
        (311, 254),
        (244, 230),
        (212, 285),
        (140, 280),
    ]
    mirror = [(768 - x, y) for x, y in pts]
    c.line(progress(pts, (t - 0.65) / 2.9), blue, 6)
    if t > 3:
        for j in [2, 4, 6]:
            x, y = pts[j]
            f = smooth((t - 3.1 - j * 0.13) / 1.6)
            for xx in range(int(x), int(mix(x, 768 - x, f)), 16):
                c.line([(xx, y), (xx + 6, y)], "92938c", 1.7)
            c.circle(x, y, 4, blue)
    if t > 4.4:
        c.line(progress(mirror, (t - 4.4) / 2.8), red, 6)
    if t > 6.6:
        y = 329
        f = smooth((t - 6.6) / 1.3)
        for x, dir in [(384, -1), (384, 1)]:
            end = x + dir * 141 * f
            c.line([(x, y), (end, y)], ink, 2.5)
            c.line([(end - dir * 7, y - 5), (end, y), (end - dir * 7, y + 5)], ink, 2)
    if t > 7.5:
        c.txt("같은 거리", 384, 367, 23, ink, True, center=True)
