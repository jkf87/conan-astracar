"""Original cut silhouettes, ink brushwork, print blocks and multiplane scenery."""

from drawing import *
from functools import lru_cache


@lru_cache(maxsize=48)
def scatter(seed, n):
    return rnd(seed).random((n, 5)).tolist()


def bamboo(c, x, y, s, ang, ink):
    with c.transform(x, y, s, ang):
        for j in range(6):
            yy = -j * 54
            c.path(
                f"M -3 {yy} Q -1 {yy - 23} 0 {yy - 51} L 4 {yy - 51} Q 3 {yy - 20} 4 {yy} Z",
                ink,
                a=0.68,
            )
            c.line([(-2, yy - 50), (5, yy - 51)], ink, 1.7)
            if j in [2, 3, 5]:
                direction = 1 if j % 2 else -1
                with c.transform(1, yy, 1, 0, sy=1):
                    c.line(
                        [(0, 0), (18 * direction, -12), (42 * direction, -25)], ink, 1.4
                    )
                    for k in range(4):
                        with c.transform(
                            (14 + k * 7) * direction,
                            -10 - k * 4,
                            1,
                            (-0.25 if k % 2 else 0.7) * direction,
                        ):
                            c.path(
                                f"M 0 0 Q {direction * 10} -14 {direction * 25} -19 Q {direction * 14} -3 0 0 Z",
                                ink,
                            )


def ink_wash(c, t):
    c.bg("f2ecdb")
    for j in range(4):
        pts = [
            (
                x,
                194
                + j * 11
                - 48 * math.exp(-(((x - 110 - j * 17) / 96) ** 2))
                - 53 * math.exp(-(((x - 269 + j * 13) / 78) ** 2))
                + 4 * sin(x * 0.031 + j * 0.7),
            )
            for x in range(-10, 790, 8)
        ]
        c.poly(pts + [(780, 230 + j * 6), (-10, 230 + j * 6)], "7f8a80", a=0.11)
    for j in range(13):
        x = 27 + j * 63
        y = 287 + (j * 37) % 73
        c.path(
            f"M {x} {y} Q {x + 36} {y - 3} {x + 73 + 5 * sin(t + j)} {y}",
            None,
            "89958b",
            1.2,
            0.52,
        )
    for x, y, s, a in [
        (697, 425, 1.42, 0.25),
        (720, 419, 1.14, -0.2),
        (644, 419, 0.83, 0.10),
    ]:
        bamboo(c, x, y, s, a + 0.018 * sin(t * 1.4 + x), "4c5b50")
    x = 406 + 14 * sin(t * 0.65)
    y = 252
    with c.transform(x, y, 1):
        for j in [0, 1]:
            d = 12 * sin(t * 2 + j * 2)
            c.line(
                [
                    (-15 + j * 16, 3),
                    (-12 + j * 14 + d, 44),
                    (-20 + j * 16 + d, 77),
                    (-32 + j * 16 + d, 80),
                ],
                "5b6257",
                1.9,
            )
        c.path(
            "M -60 -19 Q -25 -41 9 -30 Q 30 -30 27 -11 Q 10 14 -17 12 Q -33 8 -60 -19 Z",
            "dde0cd",
            "6b7267",
            1.5,
        )
        for j in range(8):
            c.path(
                f"M {9 - j} {-24 + j} Q {-13 - j * 1.4} {-12 + j} {-52 - j * 2} {-15 + j * 0.9}",
                None,
                "839085",
                1.4,
                0.7,
            )
        dip = sin(pi * smooth((t - 2.2) / 3.7))
        with c.transform(17, -17, 1, 1.46 * dip):
            c.path(
                "M 0 9 C 32 -11 4 -32 13 -54 Q 19 -74 43 -69 L 41 -61 Q 23 -65 22 -48 C 22 -25 47 -11 8 12 Z",
                "dfdfce",
                "6c7669",
                1.5,
            )
            c.path("M 38 -67 L 85 -61 L 41 -60 Z", "514f42")
            c.circle(36, -66, 2, "39493f")
    for j in range(3):
        p = (t - 3.8 - j * 0.48) / 2.5
        if 0 < p < 1:
            c.ellipse(500, 311, 6 + p * 42, 2 + p * 5, None, "657c70", 1, 1 - p)
    c.rect(53, 325, 22, 31, "a56150")
    c.line(
        [(58, 332), (67, 330), (62, 344), (69, 343), (70, 349), (58, 350)],
        "ebddc4",
        1.4,
    )


def deer(c, x, y, scale, t, reach):
    dark = "593f34"
    saff = "c78342"
    rub = "ad5543"
    with c.transform(x, y, scale):
        for j, (bx, by) in enumerate([(-44, 0), (29, 1), (-37, 5), (37, 3)]):
            a = 0.24 * sin(t * 5 + j * 2.1) * (1 - reach)
            with c.transform(bx, by, 1, a):
                c.path(
                    "M -6 0 Q 2 -5 7 3 L 5 40 L 0 53 L -4 47 Z",
                    rub if j < 2 else saff,
                    dark,
                    1.5,
                )
                with c.transform(1, 43, 1, -a * 0.8):
                    c.path("M -3 -2 L 4 -2 L 3 38 L 10 42 L -7 42 Z", saff, dark, 1.5)
                c.circle(1, 42, 2.6, "f4cc8d", dark, 1)
        c.path(
            "M -65 -26 Q -55 -59 -20 -47 Q 16 -49 36 -48 L 56 -81 L 69 -71 Q 66 -34 45 -8 Q 34 11 7 7 Q -24 3 -39 12 Q -57 8 -65 -26 Z",
            rub,
            dark,
            2,
        )
        for j in range(20):
            px = -43 + (j % 7) * 12
            py = -30 + (j // 7) * 9
            c.poly([(px - 3, py), (px, py - 4), (px + 4, py), (px, py + 3)], "f3c98b")
        c.path("M -58 -24 Q -85 -43 -77 -56 Q -54 -48 -52 -34 Z", saff, dark, 1.7)
        with c.transform(60, -69, 1, -0.24 * reach + 0.08 * sin(t * 2)):
            c.path(
                "M -12 8 Q -15 -8 -2 -17 L -9 -35 Q 5 -36 10 -19 L 24 -16 L 44 -7 Q 47 -2 41 1 L 16 3 L 5 12 Z",
                saff,
                dark,
                2,
            )
            c.circle(16, -12, 3, dark)
            c.circle(17, -13, 0.9, "f7dd98")
            for j in range(2):
                dx = -2 + j * 8
                c.line(
                    [(dx, -17), (dx - 4, -42), (dx - 16, -54), (dx - 15, -65)],
                    dark,
                    2.8,
                )
                c.line([(dx - 6, -44), (dx + 1, -55)], dark, 2)
        for xx, yy in [(-27, -17), (39, -13), (61, -63)]:
            c.circle(xx, yy, 3, "f3c98b", dark, 1)
            c.line([(xx, yy), (xx - 85, 183)], "826e58", 1, 0.62)


def shadow_puppet(c, t):
    c.gradient("d2ad73", "f4d99d")
    for j in range(6):
        c.ellipse(397, 225, 319 - j * 34, 180 - j * 17, "fff0bd", a=0.065)
    for j in range(0, 432, 4):
        c.line([(0, j), (768, j)], "8e7756", 0.5, 0.22)
    c.rect(0, 0, 768, 23, "55362e")
    c.rect(0, 405, 768, 27, "55362e")
    for j in range(2):
        x = 21 if j == 0 else 748
        c.rect(x - 9, 18, 18, 389, "704133")
        for k in range(13):
            c.poly(
                [
                    (x - 7, 29 + k * 29),
                    (x, 21 + k * 29),
                    (x + 7, 29 + k * 29),
                    (x, 37 + k * 29),
                ],
                "cf9455",
            )
    c.path(
        "M 766 118 Q 666 123 603 67 Q 540 30 473 51 Q 540 14 622 53 Q 709 94 766 80 Z",
        "79513a",
        "594333",
        2,
    )
    for j in range(16):
        x = 494 + j * 15
        y = 48 + max(0, x - 550) * 0.28
        with c.transform(x, y, 1, 0.31 * sin(j)):
            c.path("M 0 0 Q -20 6 -28 25 Q -7 22 0 0 Z", "77804b", "685a3b", 1.4)
    fall = smooth((t - 4.2) / 1.6)
    fy = mix(100, 350, fall) - 14 * sin(fall * 2 * pi)
    c.line([(566, 56), (565, 89)], "665437", 2)
    c.circle(565, fy, 13, "b66543", "6c4537", 1.6)
    for j in range(3):
        c.circle(561 + j * 4, fy - 3, 1.7, "efd294")
    reach = smooth((t - 3) / 1.5)
    deer(
        c,
        mix(181, 466, smooth(t / 5.2)),
        266 + 2 * sin(t * 5) * (1 - reach),
        1.16,
        t,
        reach,
    )
    c.line([(27, 364), (742, 364)], "9c7149", 3)


def ukiyoe(c, t):
    paper = "e6d3af"
    key = "344344"
    c.bg(paper)
    with c.window(24, 19, 720, 390):
        c.gradient("6b99a2", "e0d2af", 19, 204)
        c.circle(541 - t * 0.6, 95, 38, "dfaa77")
        for j in range(2):
            pts = [
                (
                    x,
                    188
                    + j * 33
                    + 13 * sin(x * 0.013 + j)
                    - 44 * math.exp(-(((x - 267 - 90 * j) / 96) ** 2)),
                )
                for x in range(5, 768, 8)
            ]
            c.poly(pts + [(770, 255), (0, 255)], ["9baea1", "77988d"][j], key, 0.85)
        c.rect(0, 239, 768, 178, "83a9a4")
        for j in range(85):
            x = (j * 89) % 795 - 12 + t * (0.8 if j % 2 else -0.65)
            y = 241 + (j * 17) % 164
            c.path(
                f"M {x} {y} Q {x + 16} {y - 3} {x + 38} {y - 1}",
                None,
                "e4d5b5" if j % 3 else "537b7e",
                1.25,
            )
        # Large cropped bridge anchors the boat's crossing.
        c.path(
            "M -32 170 Q 232 18 466 206 L 465 224 Q 243 65 -33 193 Z", "b69a75", key, 2
        )
        for j in range(12):
            x = j * 42 - 16
            y = 114 + ((x - 180) / 215) ** 2 * 60
            c.line([(x, y - 20), (x + 1, y + 1)], key, 3)
        c.path("M -20 146 Q 227 -3 467 184", None, key, 4)
        for x, y in [(85, 128), (302, 134)]:
            c.rect(x, y, 9, 120, "847d68", key, 1.2)
        bx = 133 + t * 47
        by = 287 + 1.5 * sin(t * 2)
        with c.transform(bx, by):
            c.path(
                "M -89 -6 Q -8 6 91 -13 Q 72 13 45 17 Q -30 25 -68 12 Z",
                "9d7959",
                key,
                2,
            )
            c.path("M -71 -4 Q -4 4 72 -9", None, "e7c695", 2)
            for j in range(3):
                xx = -26 + j * 24
                c.circle(xx, -21, 4.2, "b28e68", key, 1)
                c.poly(
                    [(xx - 3, -17), (xx + 6, -18), (xx + 11, -3), (xx - 8, -2)],
                    ["a66551", "667b78", "b39e75"][j],
                    key,
                    1,
                )
            c.line([(36, -17), (60, 22 + 8 * sin(t * 2))], key, 2)
        with c.transform(788 - t * 1.8, -12):
            c.path(
                "M 0 0 L -18 83 Q -79 122 -164 122 Q -98 110 -54 76 L -17 -10 Z",
                "575c4b",
                key,
                2,
            )
            for j in range(18):
                x = -34 - (j * 19) % 135
                y = 98 + (j * 13) % 33
                c.path(
                    f"M {x} {y} Q {x - 14} {y - 21} {x - 31} {y - 13} Q {x - 47} {y - 15} {x - 52} {y - 7} Z",
                    "687d66",
                    key,
                    0.9,
                )
    c.rect(24, 19, 720, 390, None, key, 3)
    c.rect(29, 24, 710, 380, None, key, 0.8)
    c.rect(52, 43, 35, 76, "e9d9ba", key, 1.4)
    c.txt("나", 69, 50, 22, key, False, True, True)
    c.txt("루", 69, 83, 22, key, False, True, True)
    c.rect(57, 127, 23, 20, "a15a47")
    c.rect(61, 131, 15, 12, None, "e9cfaa", 1)


def hare(c, x, y, scale, ang, jump, red, paper):
    with c.transform(x, y, scale, ang):
        c.path(
            "M -53 9 Q -72 -21 -44 -46 Q -18 -66 14 -43 L 35 -58 Q 26 -105 39 -106 Q 54 -95 56 -64 Q 65 -116 74 -108 Q 82 -86 68 -54 Q 96 -44 85 -32 Q 77 -24 55 -24 L 40 -3 Q 31 17 3 17 L -18 24 Q -41 33 -59 22 Z",
            red,
        )
        c.circle(-61, -13, 13, red)
        for xx, yy, direction in [(-30, 13, -1), (25, 2, 1)]:
            with c.transform(xx, yy, 1, jump * 0.44 * direction):
                c.path(
                    "M -6 -9 Q 7 -15 9 0 Q 8 9 -1 16 L 22 20 Q 35 26 24 29 L -11 25 Q -16 19 -6 -9 Z",
                    red,
                )
        c.circle(68, -40, 3, paper)
        c.path(
            "M 40 -98 Q 47 -87 46 -70 Q 39 -84 40 -98 Z M 71 -97 Q 73 -83 64 -68 Q 65 -84 71 -97 Z",
            paper,
        )
        for j in range(9):
            xx = -35 + j % 3 * 20
            yy = -35 + j // 3 * 13
            c.path(
                f"M {xx} {yy} Q {xx + 11} {yy - 7} {xx + 14} {yy + 1} Q {xx + 5} {yy + 5} {xx} {yy} Z",
                paper,
            )


def papercut_red(c, t):
    paper = "ecdfc6"
    red = "ba3d38"
    c.bg(paper)
    for x in range(0, 769, 28):
        for y in (14, 418):
            c.poly([(x - 15, y), (x, y - 12), (x + 15, y), (x, y + 12)], red)
            c.poly([(x - 6, y), (x, y - 5), (x + 6, y), (x, y + 5)], paper)
    grow = smooth((t - 2) / 4.8)
    with c.transform(384, 219, 0.55 + 0.45 * grow, t * 0.11):
        c.poly(rose(0, 0, 109, 8), red)
        c.poly(rose(0, 0, 91, 8), paper)
        c.circle(0, 0, 55, red)
        c.poly(rose(0, 0, 46, 6), paper)
        c.circle(0, 0, 18, red)
        for j in range(8):
            a = j * pi / 4
            c.circle(79 * cos(a), 79 * sin(a), 4, red)
    for j in range(2):
        k = smooth((t - 0.35 * j) / 4.9)
        x = mix(100, 232, k) if j == 0 else mix(674, 537, k)
        jump = abs(sin(t * 1.45 + j * 0.3)) * (1 - 0.5 * grow)
        with c.transform(x, 286 - 42 * jump, 1 if j == 0 else -1, 0, sy=1):
            hare(c, 0, 0, 0.94, -0.12 * jump, jump, red, paper)
    for j in range(13):
        x = 47 + 56 * j
        y = 337 + 8 * sin(j * 0.7)
        c.path(
            f"M {x - 20} {y} Q {x - 5} {y - 13} {x + 2} {y - 1} Q {x + 8} {y - 21} {x + 25} {y - 18} Q {x + 15} {y - 3} {x} {y + 5} Z",
            "a6463e",
        )


def paper_lantern(c, t):
    c.bg("372d2b")
    c.rect(15, 13, 738, 406, "8e7356")
    c.rect(24, 21, 720, 390, "4b4944")
    with c.window(31, 28, 706, 376):
        c.gradient("8aa9aa", "f2cc8c", 28, 376)
        sunx = 492 - 4 * t
        c.circle(sunx, 133, 48, "f8d99c")
        c.circle(sunx, 133, 41, "f9dfac")
        colors = ["a5b2a4", "889c94", "758a83", "617675", "495f5d", "344b49"]
        for j, col in enumerate(colors):
            dx = t * (j + 1) * 2.0
            pts = [
                (
                    x,
                    214
                    + j * 23
                    + 17 * sin((x + dx) * 0.012 + j * 1.7)
                    + 12 * cos((x + dx) * 0.017 + j * 0.6),
                )
                for x in range(20, 759, 5)
            ]
            c.poly(
                [(x + 1, y + 4) for x, y in pts] + [(760, 425), (21, 425)],
                "4f524e",
                a=0.35,
            )
            c.poly(pts + [(760, 425), (21, 425)], col)
            c.line(pts, "e3c792", 1.4, 0.58)
            if j == 3:
                with c.transform(437 - dx, 257, 0.9):
                    c.path("M -40 0 L -40 -39 L 0 -68 L 43 -39 L 43 1 Z", "586963")
                    c.poly(
                        [
                            (-50, -37),
                            (0, -77),
                            (53, -40),
                            (43, -36),
                            (-1, -64),
                            (-40, -32),
                        ],
                        "465a57",
                    )
                    glow = smooth((t - 4.5) / 1.8)
                    for k in range(3):
                        c.rect(
                            -27 + k * 18, -33, 10, 18, blend("99a48a", "ffdb89", glow)
                        )
        for side in [-1, 1]:
            with c.transform(56 if side == 1 else 709, 398, side, 0, sy=1):
                c.path(
                    "M -35 0 Q 5 -106 0 -201 Q -1 -290 28 -382 L 48 -382 Q 14 -290 20 -248 Q 40 -283 90 -298 Q 40 -266 23 -210 Q 23 -92 47 4 Z",
                    "344744",
                )
                for j in range(19):
                    xx = 23 + j * 6
                    yy = -289 - 11 * sin(j * 0.7)
                    c.path(
                        f"M {xx} {yy} Q {xx + 1} {yy - 18} {xx + 20} {yy - 28} Q {xx + 23} {yy - 11} {xx} {yy} Z",
                        "3f5550",
                    )
        for j in range(12):
            u = smooth((t - j * 0.14) / 7.1)
            x = mix(87 + j * 13, 390 + 9 * sin(j), u)
            y = mix(309 + 14 * cos(j), 225 + 3 * j, u) - 34 * sin(u * TAU + j)
            c.circle(x, y, 5, "fbd591", a=0.23)
            c.circle(x, y, 1.4 + 0.8 * sin(t * 3 + j) ** 2, "ffe2a4")
    c.rect(29, 26, 710, 380, None, "cbb18a", 2)


def archpath(c, x, y, w, h):
    c.call("move_to", x - w / 2, y + h)
    c.call("line_to", x - w / 2, y + 91)
    c.call("curve_to", x - w / 2, y + 53, x - w * 0.32, y + 19, x, y)
    c.call("curve_to", x + w * 0.32, y + 19, x + w / 2, y + 53, x + w / 2, y + 91)
    c.call("line_to", x + w / 2, y + h)
    c.call("close_path")


def stained_glass(c, t):
    c.gradient("202327", "393731")
    lead = "333433"
    for j in range(7):
        c.line([(0, 49 + j * 45), (768, 49 + j * 45)], "454340", 2)
    for j, x in enumerate([181, 384, 587]):
        y = 36 if j == 1 else 58
        w = 175
        h = 282 if j == 1 else 259
        archpath(c, x, y - 6, w + 16, h + 10)
        c.finish("55514a", "24282a", 4, 1)
        archpath(c, x, y, w, h)
        c.call("save")
        c.call("clip")
        pos = 105 + t * 67
        light = 0.24 + 0.76 * math.exp(-(((x - pos) / 160) ** 2))

        def glass(col):
            return blend("303940", col, light)

        c.rect(x - 90, 20, 181, 307, glass("405e98"))
        # Uneven mosaic cells are shared vertices. The lead stays dark as light moves.
        grid = [
            [
                (
                    x - 106 + q * 43 + 7 * sin(q * 6 + r * 8),
                    y - 20 + r * 51 + 7 * cos(q * 3 + r * 1.2),
                )
                for q in range(6)
            ]
            for r in range(8)
        ]
        colors = ["327f8c", "5874a4", "42679a", "53979a", "726997"]
        for r in range(7):
            for q in range(5):
                c.poly(
                    [grid[r][q], grid[r][q + 1], grid[r + 1][q + 1], grid[r + 1][q]],
                    glass(colors[(q + 3 * r) % 5]),
                    lead,
                    3,
                )
        cy = 190 if j != 1 else 167
        c.circle(x, cy, 63, glass("bd9250"), lead, 4)
        c.circle(x, cy, 55, glass("e1b35b"), lead, 2)
        with c.transform(x, cy):
            if j == 0:
                for k in range(6):
                    a = k * pi / 3
                    with c.transform(0, 0, 1, a):
                        c.path(
                            "M 0 -4 Q -33 -17 -20 -38 Q 0 -55 16 -30 Q 18 -17 0 -4 Z",
                            glass("b56477"),
                            lead,
                            2.5,
                        )
                c.circle(0, 0, 13, glass("e3bd77"), lead, 2)
            elif j == 1:
                with c.transform(0, 1, 1, -0.4):
                    for yy in [-1, 1]:
                        with c.transform(-5, yy * 6, 1, yy * 0.65):
                            c.ellipse(0, -yy * 12, 22, 10, glass("acc6b7"), lead, 2)
                    c.ellipse(0, 0, 29, 13, glass("dc9e47"), lead, 3)
                    for xx in [-12, 0, 12]:
                        c.line([(xx - 2, -10), (xx + 1, 11)], lead, 3)
                    c.circle(27, 0, 9, glass("7b6244"), lead, 2)
                    c.line([(30, -4), (37, -14), (42, -12)], lead, 1.5)
            else:
                for k, (xx, yy) in enumerate(
                    [(-17, -17), (15, -17), (0, 11), (-29, 12), (29, 12), (0, -39)]
                ):
                    c.poly(
                        [
                            (
                                xx + 16 * cos(pi / 6 + n * pi / 3),
                                yy + 16 * sin(pi / 6 + n * pi / 3),
                            )
                            for n in range(6)
                        ],
                        glass(["d28e44", "edbd60", "b97442"][k % 3]),
                        lead,
                        2.4,
                    )
        for a, b, d, e, f in scatter(140 + j, 33):
            xx = x - 79 + a * 159
            yy = y + 18 + b * (h - 20)
            c.line([(xx, yy), (xx + 2 + d * 7, yy - 2)], "e9e7cc", 1, 0.11 * light)
        c.call("restore")
        archpath(c, x, y, w, h)
        c.finish(None, "23272a", 6, 1)
        for k in range(4):
            xx = x - 60 + k * 31
            off = 38 + (pos - x) * 0.12
            c.poly(
                [(xx, 332), (xx + 23, 332), (xx + off + 22, 413), (xx + off - 5, 413)],
                glass(["8c5b61", "a8844e", "54767e", "5f6593"][k]),
                a=0.34 * light,
            )
    for j in range(4):
        c.line([(0, 340 + j * 28), (768, 340 + j * 28)], "292c2c", 2)


def gilded_illumination(c, t):
    ink = "473d37"
    c.bg("d9c8a5")
    c.rect(13, 12, 742, 408, "8c4f46", ink, 3)
    c.rect(24, 22, 720, 388, "c9a35c", ink, 2)
    c.rect(39, 36, 690, 360, "314e68", ink, 3)
    for j in range(34):
        x = 32 + j * 21
        for y in [28, 402]:
            c.poly([(x - 7, y), (x, y - 5), (x + 7, y), (x, y + 5)], "7e423d", ink, 0.6)
    for j in range(12):
        y = 46 + j * 29
        for x in [31, 737]:
            c.circle(x, y, 4, "e3c27b", ink, 1)
    # A gilded disk is assembled from individually reflecting leaf squares.
    xx, yy = 383, 184
    r = 139
    lightpos = 110 + t * 67
    c.call("save")
    c.call("arc", xx, yy, r, 0, TAU)
    c.call("clip")
    for row in range(9):
        for col in range(10):
            x = 232 + col * 32
            y = 40 + row * 32
            f = (
                0.18
                + 0.73 * math.exp(-(((x - lightpos + row * 7) / 58) ** 2))
                + 0.08 * cos(col + row * 3)
            )
            c.rect(x, y, 33, 33, blend("9d7544", "f5d783", f), "ba965a", 0.6)
            for q in range(3):
                c.circle(x + 4 + q * 9, y + 4, 1.5, "957449", a=0.65)
    c.call("restore")
    c.circle(xx, yy, r, None, "d7b367", 3)
    for j in range(2):
        with c.transform(50 if j == 0 else 718, 370, 1 if j == 0 else -1, 0, sy=1):
            c.path(
                "M 0 0 Q 58 -41 36 -120 Q 14 -186 60 -245 Q 36 -176 53 -130 Q 82 -37 15 0 Z",
                "a08853",
                ink,
                2,
            )
            for k in range(13):
                px = 38 + 9 * sin(k * 0.8)
                py = -19 - k * 17
                with c.transform(px, py, 1, -0.57 if k % 2 else 1.6):
                    c.path("M 0 0 Q 9 -28 33 -29 Q 30 -5 0 0 Z", "729384", ink, 1.8)
                    c.line([(3, -3), (25, -22)], "d4c99b", 1.2)
    opening = 0.32 + 0.68 * smooth((t - 0.5) / 4.7)
    with c.transform(390, 310):
        for j in range(17):
            angle = (j - 8) * 0.141 * opening
            with c.transform(0, 0, 1, angle):
                reach = 185 + (8 - abs(j - 8)) * 3.8
                c.path(
                    f"M -2 0 Q -14 {-reach * 0.55} -15 {-reach + 20} Q -21 {-reach} 0 {-reach - 14} Q 24 {-reach + 2} 15 {-reach + 21} Q 9 {-reach * 0.48} 2 0 Z",
                    "608b84" if j % 2 else "427875",
                    ink,
                    1.6,
                )
                c.line([(0, -12), (0, -reach + 18)], "bea660", 1.1)
                c.ellipse(0, -reach + 7, 10, 15, "c6a45f", ink, 1)
                c.ellipse(0, -reach + 7, 5.5, 8, "3b566c")
                c.ellipse(-2, -reach + 4, 2.3, 3, "dedac1")
        c.path(
            "M -43 -2 Q -29 -28 -3 -22 Q 23 -18 19 -50 Q 11 -68 26 -74 Q 47 -80 49 -60 L 43 -53 Q 50 -17 22 5 Q 1 25 -43 -2 Z",
            "365c79",
            ink,
            2.6,
        )
        c.path("M 47 -65 L 65 -61 L 46 -57 Z", "c5a464", ink, 1.6)
        c.circle(40, -66, 2.8, "e9dcb9")
        c.circle(40, -66, 1.2, ink)
        c.path("M -31 -4 Q -6 -20 9 -10 Q -2 3 -27 1", None, "a0b6b4", 1.8)
        for j in range(3):
            c.line(
                [(27 + j * 3, -73), (22 + j * 7, -85 - 3 * sin(t * 2 + j))],
                "d9ba76",
                1.6,
            )
        for j in [-1, 1]:
            c.line([(3 + j * 7, 9), (j * 10, 28), (j * 10 + 10, 29)], "c5a464", 2)
    c.path(
        "M 102 352 Q 344 329 667 346 L 672 356 Q 333 345 104 363 Z", "a9895d", ink, 2
    )


set_operator = bind("set_operator", None, P, I)


def risograph(c, t):
    paper = "f4e7cf"
    cyan = "569caf"
    pink = "e97778"
    yellow = "e6bd65"
    c.bg(paper)
    # The press overprints the jacket, sliding record and tonearm on independent inks.
    set_operator(c.c, 14)
    sleeve = -165 * smooth((t - 0.8) / 3.3)
    with c.transform(183 + sleeve, 217, 1, -0.105):
        c.rect(-169, -148, 335, 302, pink)
        for j in range(17):
            c.rect(-167, -145 + j * 17, 330, 4, cyan, a=0.75)
        c.circle(-8, 0, 94, yellow)
        c.poly(
            [
                (-72, 71),
                (-62, -68),
                (58, -94),
                (69, 49),
                (50, 52),
                (48, -43),
                (-44, -26),
                (-44, 72),
            ],
            cyan,
        )
        c.ellipse(-66, 70, 24, 15, cyan)
        c.ellipse(46, 54, 23, 15, cyan)
    rx = 397 + 69 * smooth((t - 0.9) / 3.1)
    ry = 220
    c.circle(rx - 2, ry + 1, 154, cyan)
    for j in range(19):
        c.circle(rx + 1, ry - 1, 145 - j * 4, None, cyan, 1 + (j % 3) * 0.42)
    c.circle(rx + 2, ry - 1, 63, pink)
    c.circle(rx - 1, ry + 1, 42, yellow)
    c.circle(rx, ry, 5, cyan)
    with c.transform(rx, ry, 1, t * 1.75):
        c.poly([(-13, -47), (20, -41), (5, -23)], pink)
        c.rect(-19, 21, 32, 5, cyan)
    with c.transform(669, 84, 1, -0.12 + 0.70 * smooth((t - 3.4) / 2.25)):
        c.circle(0, 0, 40, yellow)
        c.circle(0, 0, 25, cyan)
        c.circle(0, 0, 8, pink)
        c.line([(0, 0), (12, 95), (-8, 159)], cyan, 13)
        c.poly([(-17, 151), (1, 154), (-5, 182), (-25, 176)], pink)
    for j in range(21):
        x = 56 + j * 33
        y = 382
        height = 3 + 18 * (sin(t * 5 + j * 0.83) ** 2) * smooth((t - 5.4) / 1.5)
        c.rect(x, y - height, 8, height, cyan if j % 3 else pink)
    set_operator(c.c, 2)
    for a, b, d, e, f in scatter(202, 780):
        c.circle(a * W, b * H, 0.45 + d * 0.7, paper, a=0.55)


def stamp_art(c, x, y, k, col):
    with c.transform(x, y, k, -0.11):
        c.rect(-71, -80, 142, 160, "ded2ad", "293d46", 2)
        for i in range(10):
            for xx in [-71, 71]:
                c.circle(xx, -74 + i * 16, 3.8, "f0e4c8")
        for i in range(9):
            for yy in [-80, 80]:
                c.circle(-64 + i * 16, yy, 3.8, "f0e4c8")
        c.rect(-59, -65, 118, 130, col, "293d46", 2)
        c.circle(15, -34, 19, "f6dda0")
        c.poly(
            [(-56, 34), (-25, -11), (-2, 13), (20, -10), (56, 28), (56, 44), (-56, 44)],
            "435c64",
        )
        c.poly([(-54, 39), (-15, 24), (7, 31), (55, 17), (55, 47), (-54, 47)], "e0b774")
        c.line([(-49, 53), (48, 53)], "f0e2c0", 2)


def halftone_dossier(c, t):
    ink = "233b45"
    cream = "eee2c5"
    red = "a94f43"
    c.bg(cream)
    for x in range(7, 768, 8):
        for y in range(4, 432, 8):
            if x < 137 or y > 360:
                c.circle(x + (y % 16) * 0.25, y, 1.1, "baae91")
    c.rect(19, 16, 729, 397, None, ink, 2)
    c.rect(20, 17, 727, 41, ink)
    c.txt("우편 기록실", 34, 26, 21, cream, True)
    c.txt("제  03  호", 625, 30, 14, cream, True)
    cut = int(t // 3)
    u = t % 3
    if cut == 0:
        with c.transform(360, 238, 1, -0.07 + 0.04 * sin(u)):
            c.rect(-213, -110, 426, 220, "d8c8a3", ink, 2)
            c.line([(-212, 108), (-54, -7), (0, 25), (54, -7), (213, 107)], ink, 1.4)
            c.line([(-212, -110), (0, 25), (213, -110)], ink, 2)
            c.rect(128, -90, 62, 69, None, red, 2.5)
        c.rect(46, 318, 173, 44, red)
        c.txt("빈 우표 자리", 56, 328, 23, cream, True)
    elif cut == 1:
        for j, col in enumerate(["8aa3a0", "c77a68", "a7a777"]):
            stamp_art(c, 182 + j * 198, 207 + 10 * sin(t + j), 0.81, col)
        xx = 182 + 198 * smooth(u / 1.3)
        c.arc(
            xx,
            207,
            83,
            -pi / 2,
            -pi / 2 + TAU * (0.12 + 0.88 * smooth(u / 1.7)),
            red,
            4,
        )
        c.txt("산등성이 무늬를 대조했다", 384, 334, 23, ink, True, center=True)
    else:
        stamp_art(c, 259, 223, 1.34, "c77a68")
        c.txt("산마을 소인", 433, 141, 39, ink, True)
        c.line([(433, 202), (688, 202)], ink, 2)
        c.txt("봉투와 우표가 만났다", 437, 224, 22, ink)
        if u > 0.35:
            with c.transform(
                317, 241, 1 + 0.5 * (1 - smooth((u - 0.35) / 0.45)), -0.22
            ):
                c.circle(0, 0, 52, None, red, 4)
                c.circle(0, 0, 47, None, red, 1.2)
                c.txt("산마을", 0, -14, 24, red, True, center=True)
                for j in range(3):
                    c.path(
                        f"M 44 {j * 10 - 10} Q 66 {j * 10 - 21} 84 {j * 10 - 12} Q 102 {j * 10 - 5} 122 {j * 10 - 17}",
                        None,
                        red,
                        2,
                    )
    for j in range(3):
        c.rect(627 + j * 35, 380, 26, 6, red if j <= cut else "b4a88e")


def moth(c, x, y, k, t, light, dark):
    with c.transform(x, y, k, 0.1 * sin(t * 2)):
        for side in [-1, 1]:
            wide = 0.48 + 0.52 * (0.5 + 0.5 * sin(t * 4.6))
            with c.transform(0, 0, side * wide, 0, sy=1):
                c.path(
                    "M 1 -7 Q 26 -48 72 -58 Q 66 -24 52 -7 L 21 7 Q 52 4 54 17 Q 45 40 20 34 L 0 12 Z",
                    light,
                )
                for j in range(12):
                    c.path(
                        f"M 6 {-5 + j * 0.6} Q {25 + j} {-24 + j * 0.9} {62 - j * 0.9} {-49 + j * 2.4}",
                        None,
                        dark,
                        1.1,
                    )
                c.ellipse(32, -17, 7, 4, dark)
                c.ellipse(31, -18, 2, 1.6, light)
                for j in range(5):
                    c.line([(9 + j * 4, 11), (17 + j * 5, 25)], dark, 1.4)
        c.ellipse(0, 2, 5, 20, light, dark, 1.4)
        c.circle(0, -15, 4, light)
        c.path("M -1 -16 Q -2 -27 -12 -29 M 2 -16 Q 4 -28 13 -30", None, light, 1.7)


def woodcut(c, t):
    dark = "252a29"
    light = "e6d9bc"
    c.bg(dark)
    cut = 0 if t < 3 else 1 if t < 5.7 else 2
    if cut == 0:
        for j in range(74):
            x = j * 12 - 30
            pts = [
                (x + 11 * sin(y * 0.012 + j * 0.7) + 4 * sin(y * 0.039 + j), y)
                for y in range(-9, 450, 9)
            ]
            c.line(pts, light, 1 + 1.1 * sin(j * 3) ** 2, 0.82)
        c.path(
            "M 125 467 Q 294 316 372 216 Q 426 136 584 31 Q 461 147 406 241 Q 334 377 222 441 Z",
            dark,
            light,
            3,
        )
        for j in range(15):
            c.path(
                f"M {180 + j * 3} 429 Q {291 + j * 4} 349 {383 + j} 224",
                None,
                light,
                1.5,
            )
        moth(c, 404, 208, 1.02, t, light, dark)
    elif cut == 1:
        for j in range(48):
            a = j * TAU / 48
            c.line(
                [
                    (384 + 185 * cos(a), 217 + 145 * sin(a)),
                    (384 + 373 * cos(a), 217 + 229 * sin(a)),
                ],
                light,
                1.1,
            )
        moth(c, 382 + 7 * sin(t), 215, 2.37, t * 0.79, light, dark)
    else:
        for j in range(40):
            y = 25 + j * 11
            for k in range(3):
                x = (j * 53 + k * 220) % 890 - 60
                c.path(
                    f"M {x} {y} Q {x + 25} {y - 3} {x + 74 + j % 13} {y + 1}",
                    None,
                    light,
                    1,
                )
        c.path("M 490 -12 L 503 -12 L 500 87 L 489 91 Z", light)
        c.path("M 450 115 L 494 79 L 541 112 L 548 124 L 443 124 Z", dark, light, 3)
        c.poly([(452, 126), (538, 126), (526, 227), (469, 227)], dark, light, 3)
        for j in range(11):
            c.line([(464 + j * 6, 137), (472 + j * 4, 214)], light, 1.5)
        c.path(
            "M 480 207 Q 468 188 494 158 Q 491 176 504 180 Q 518 200 501 210 Z",
            "d69159",
        )
        c.rect(467, 224, 61, 9, light)
        u = smooth((t - 5.7) / 3.1)
        moth(
            c,
            114 + 337 * u,
            296 - 111 * u - 34 * sin(u * TAU),
            0.64 + 0.11 * sin(u * pi),
            t * 1.5,
            light,
            dark,
        )
    c.rect(11, 10, 746, 411, None, light, 1)


def engraving(c, t):
    paper = "ecdfc2"
    ink = "544a3f"
    c.bg(paper)
    for j in range(0, 432, 5):
        c.line([(0, j), (768, j)], "b9ab90", 0.65, 0.29)
    c.rect(25, 18, 718, 395, None, "c6b89e", 3)
    c.rect(34, 27, 700, 377, None, ink, 1)
    c.rect(38, 31, 692, 369, None, "a99b82", 0.8)
    c.txt("앵무조개의 방", 384, 47, 25, ink, False, True, True)
    # The logarithmic shell, chamber sutures and parallel burin cuts share one surface.
    cx, cy = 316, 237

    def polar(a, r):
        return (cx + r * cos(a - 0.16), cy + r * 0.77 * sin(a - 0.16))

    def rad(a):
        return 12 * math.exp(0.186 * a)

    angles = np.linspace(0, 14.05, 440)
    outline = [polar(a, rad(a)) for a in angles]
    c.line(progress(outline, 0.15 + 0.85 * smooth(t / 3.0)), ink, 2.2)
    for j, a in enumerate(np.linspace(6.3, 14.05, 31)):
        phase = smooth((t - 1.45 - j * 0.057) / 1.55)
        if not phase:
            continue
        outer, inner = rad(a), rad(a - TAU)
        pts = [
            polar(a + 0.20 * sin(pi * f), mix(inner, outer, f))
            for f in np.linspace(0, 1, 45)
        ]
        c.line(progress(pts, phase), ink, 1.45)
        for k in range(6):
            angle = a - 0.17 + k * 0.027
            pts = [
                polar(angle + 0.20 * sin(pi * f), mix(inner, outer, f))
                for f in np.linspace(0.40 + 0.10 * sin(k), 0.98, 18)
            ]
            c.line(progress(pts, phase), "766853", 0.68)
    if t > 4.55:
        for j in range(26):
            a = 7.3 + j * 0.254
            b = a + 0.17
            f = smooth((t - 4.55 - j * 0.08) / 0.85)
            if f:
                pts = [polar(th, rad(th) * 0.97) for th in np.linspace(a, b, 9)] + [
                    polar(th, rad(th - TAU) * 1.12) for th in np.linspace(b, a, 9)
                ]
                c.poly(pts, "c5946e", a=0.32 * f)
    end = outline[-1]
    if t > 2.85:
        c.path(f"M {end[0]} {end[1]} Q 349 279 328 270", None, ink, 1.6)
    c.circle(576, 207, 72, None, ink, 1)
    c.circle(576, 207, 67, None, "9a8e77", 0.8)
    with c.transform(576, 207):
        for j in range(7):
            x = -48 + j * 13
            c.path(f"M {x} -38 Q {x + 22} -5 {x + 2} 36", None, ink, 1.5)
            for k in range(4):
                c.line([(x + 4 + k * 2, 12), (x + 1 + k * 2, 26)], ink, 0.7)
    c.line([(431, 215), (476, 206), (503, 206)], ink, 1)
    c.txt("격벽", 576, 294, 17, ink, False, True, True)
    c.txt("껍데기 단면", 312, 369, 17, ink, False, True, True)


def silkscreen_poster(c, t):
    cream = "f0dfb6"
    sun = "e6b75e"
    terra = "cf8056"
    teal = "448182"
    navy = "284b58"
    c.bg(cream)
    # Four separate screen pulls reveal the salt flats, terrace, tower and travellers.
    for j, start in enumerate([-0.8, 1.3, 3.05, 4.9]):
        f = smooth((t - start) / 1.65)
        if not f:
            continue
        with c.window(27, 22, 714, 347 * f):
            if j == 0:
                c.rect(27, 22, 714, 347, sun)
                for i in range(5):
                    c.rect(27, 117 + i * 13, 714, 3 + i, cream)
                c.circle(571, 97, 46, cream)
            elif j == 1:
                c.poly(
                    [
                        (24, 210),
                        (158, 157),
                        (229, 178),
                        (330, 140),
                        (444, 169),
                        (534, 138),
                        (636, 151),
                        (746, 104),
                        (746, 289),
                        (24, 293),
                    ],
                    terra,
                )
                for k in range(4):
                    c.rect(27, 226 + k * 14, 714, 6 + k, terra)
            elif j == 2:
                c.poly(
                    [
                        (24, 248),
                        (281, 213),
                        (374, 224),
                        (489, 204),
                        (744, 180),
                        (744, 260),
                        (25, 328),
                    ],
                    teal,
                )
                c.poly([(25, 333), (421, 256), (741, 237), (741, 256), (32, 367)], teal)
                for k in range(3):
                    c.poly(
                        [
                            (96 + k * 98, 309 - k * 16),
                            (209 + k * 95, 280 - k * 14),
                            (227 + k * 94, 280 - k * 14),
                            (112 + k * 99, 309 - k * 16),
                        ],
                        cream,
                    )
            else:
                c.poly([(129, 276), (159, 132), (174, 133), (149, 274)], navy)
                c.poly([(245, 265), (210, 130), (223, 130), (264, 261)], navy)
                c.poly([(140, 126), (225, 110), (247, 124), (144, 145)], navy)
                for k in range(6):
                    c.poly(
                        [
                            (153 + k * 10, 122 - k * 1.6),
                            (153 + k * 10, 94 - k * 1.5),
                            (157 + k * 10, 94 - k * 1.5),
                            (157 + k * 10, 122 - k * 1.6),
                        ],
                        navy,
                    )
                c.poly([(139, 94), (215, 80), (238, 90), (143, 108)], navy)
                c.poly([(460, 367), (744, 262), (744, 369)], navy)
                for k in range(2):
                    x = 495 + k * 29 + (t - 4.9) * 5
                    y = 306 - k * 8
                    c.circle(x, y - 22, 3.7, navy)
                    c.poly(
                        [
                            (x - 2, y - 18),
                            (x + 3, y - 18),
                            (x + 6, y - 3),
                            (x - 6, y - 3),
                        ],
                        navy,
                    )
                    c.line([(x, y - 6), (x - 4, y + 4), (x - 5, y + 10)], navy, 2)
                    c.line([(x, y - 6), (x + 4, y + 6)], navy, 2)
    c.txt("염전 전망대", 39, 378, 32, navy, True)
    c.txt("소금길 산책", 687, 391, 17, navy, False, True, True)


def printed_long_take(c, t):
    ink = "292e2c"
    paper = "e8dec4"
    red = "b34e3c"
    c.bg(paper)
    cam_z = 7 + t * 4.3
    cam_x = 0.36 * sin(t * 0.5)
    horizon = 161 + 4 * sin(t * 0.46)

    def project(x, y, z):
        depth = max(0.3, z - cam_z)
        return (384 + (x - cam_x) * 405 / depth, horizon + (3.25 - y) * 405 / depth)

    for j in range(24):
        y = 8 + j * 5
        for k in range(4):
            x = (j * 53 + k * 201) % 840 - 90
            c.path(f"M {x} {y} Q {x + 45} {y - 1.5} {x + 97} {y}", None, ink, 0.7, 0.65)
    for j in range(2):
        pts = [
            (x, horizon - 9 - j * 4 - 14 * sin(x * 0.012 + j) + 10 * cos(x * 0.019 + j))
            for x in range(-12, 795, 6)
        ]
        c.poly(pts + [(790, horizon + 22), (-12, horizon + 22)], ink)
        for k in range(0, 128, 2):
            x, y = pts[k]
            c.line([(x, y + 1), (x - 11, y + 11)], paper, 0.85)
    c.rect(0, horizon + 14, 768, 432 - horizon, paper)
    for i in range(215):
        z = 10 + i * 0.61
        if z < cam_z + 3:
            continue
        x = (i * 3.87) % 24 - 12
        u, v = project(x, 0, z)
        end, v2 = project(x + 0.55 + 0.7 * (i % 3), 0, z)
        if -80 < u < 805 and v < 441:
            c.line([(u, v), (end, v2 + 0.6)], ink, 0.8 + max(0, (v - 205) / 170))
    for side in [-1, 1]:
        zs = np.linspace(cam_z + 1, cam_z + 150, 90)
        border = [project(side * (6.2 + 0.6 * sin(z * 0.13)), 0.2, z) for z in zs]
        c.poly(border + [(384 + side * 490, horizon + 2), (384 + side * 490, 442)], ink)
        for z in np.arange(4, 179, 0.75):
            if z < cam_z + 2.0:
                continue
            x = side * (6.5 + 0.6 * sin(z * 0.13))
            p = project(x, 0.22, z)
            q = project(x + side * 1.4, 0.39, z + 0.17)
            c.line([p, q], paper, 1.2)

    def tree(x, z, h):
        sx, sy = project(x, 0, z)
        scale = 405 / (z - cam_z)
        if sx < -140 or sx > 908:
            return
        with c.transform(sx, sy, scale):
            c.poly([(-0.12, 0), (-0.07, -h * 0.72), (0.06, -h * 0.75), (0.16, 0)], ink)
            c.path(
                f"M 0 {-h * 0.3} Q -1.44 {-h * 0.46} -.92 {-h * 0.70} Q -.70 {-h * 0.91} 0 {-h} Q .79 {-h * 0.90} 1.0 {-h * 0.67} Q 1.27 {-h * 0.45} 0 {-h * 0.30} Z",
                ink,
            )
            for k in range(7):
                y = -h * 0.39 - k * h * 0.067
                c.line(
                    [(-0.57 + 0.04 * k, y - 0.34), (-0.04, y), (0.38, y - 0.36)],
                    paper,
                    0.042,
                )

    def boat():
        z = cam_z + 9.5 + 2 * sin(t * 0.62)
        x = 0.9 * sin(t * 0.65)
        sx, sy = project(x, 0.13, z)
        with c.transform(sx, sy, 405 / (z - cam_z)):
            c.path(
                "M -0.73 0.04 Q -0.72 -0.42 0 -0.82 Q 0.68 -0.54 0.73 0.04 Q 0.52 0.40 0 0.50 Q -0.54 0.40 -0.73 0.04 Z",
                red,
                ink,
                0.055,
            )
            c.ellipse(0, -0.19, 0.48, 0.19, ink)
            c.poly(
                [(-0.23, -0.26), (-0.16, -0.68), (0.15, -0.70), (0.26, -0.25)],
                paper,
                ink,
                0.055,
            )
            c.circle(0, -0.84, 0.15, ink)
            for side in [-1, 1]:
                k = sin(t * 3) * 0.33
                c.line([(side * 0.17, -0.49), (side * 1.55, k)], ink, 0.065)
                c.line([(side * 1.22, k - 0.09), (side * 1.54, k)], red, 0.10)
            for j in range(3):
                c.path(
                    f"M -.65 {0.4 + j * 0.26} Q 0 {0.65 + j * 0.31} .65 {0.4 + j * 0.26}",
                    None,
                    ink,
                    0.035,
                )

    def bridge(z):
        for side in [-1, 1]:
            pts = [
                project(side * x, y, z)
                for x, y in [
                    (4.3, -0.2),
                    (4.3, 3.6),
                    (5, 4.9),
                    (6.1, 5.4),
                    (6.8, 5.4),
                    (6.8, -0.2),
                ]
            ]
            c.poly(pts, ink)
        pts = [
            project(x, y, z)
            for x, y in [(-10, 5.85), (10, 5.85), (10, 5.23), (-10, 5.23)]
        ]
        c.poly(pts, ink)
        for k in range(-10, 11):
            c.line(
                [project(k, 5.86, z), project(k, 6.74, z)],
                ink,
                max(1, 22 / (z - cam_z)),
            )
        c.line(
            [project(-10, 6.74, z), project(10, 6.74, z)],
            ink,
            max(1.5, 45 / (z - cam_z)),
        )
        c.line(
            [project(-10, 5.48, z), project(10, 5.48, z)],
            paper,
            max(0.85, 12 / (z - cam_z)),
        )

    objects = [(cam_z + 9.5 + 2 * sin(t * 0.62), "boat", 0, 0), (30, "bridge", 0, 0)]
    for i in range(45):
        z = 9 + i * 2.85
        side = 1 if i % 2 else -1
        objects.append(
            (z, "tree", side * (7.6 + ((i * 7) % 8) * 0.33), 3.3 + (i % 6) * 0.56)
        )
    for z, kind, x, h in sorted(objects, reverse=True):
        if z <= cam_z + 0.85:
            continue
        if kind == "boat":
            boat()
        elif kind == "bridge":
            bridge(z)
        else:
            tree(x, z, h)
