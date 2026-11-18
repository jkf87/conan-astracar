"""Ten motion-graphic films. All contours and cut-paper plates drawn for this edition."""

from draw import *

K = "171724"
P = "fff1d7"
R = "ef3f47"
Y = "ffd738"
B = "2163ba"
LEMON = "M -100 0 Q -105 -13 -86 -18 C -44 -83 42 -70 83 -23 Q 105 -18 101 -3 Q 112 11 89 18 C 53 73 -50 74 -85 24 Q -109 21 -100 0 Z"


def citrus(d, x, y, s, rot=0, cut=False):
    with d.at(x, y, s, rot):
        if cut:
            d.circ(0, 0, 67, Y, K, 5)
            d.circ(0, 0, 59, P)
            for i in range(9):
                with d.at(0, 0, 1, i * tau / 9):
                    d.path(
                        "M 4 0 Q 44 -16 53 -15 Q 60 1 52 16 Q 24 10 4 0 Z",
                        "ffb51c",
                        K,
                        1.1,
                    )
        else:
            d.path(LEMON, Y, K, 5)
            with d.clip(LEMON):
                dots(d, -99, 16, 201, 50, 9, 2.3, "dd4941")
            d.path("M -63 -20 Q -43 -48 -11 -46", None, P, 6)
            d.path("M 69 -25 Q 70 -63 116 -58 Q 102 -27 69 -25 Z", B, K, 4)


def pop_art(d, t):
    b, u = phase(t)
    d.bg(P)
    if b == 0:
        with d.at(365, 213, mix(2.8, 1.44, span(t, 0, 2.5)), -0.18):
            star(d, 0, 0, 247, 16, R, 0.76)
            citrus(d, 0, 0, 1.45, cos(t * 2) * 0.08)
    elif b == 1:
        d.bg(B)
        for j in range(2):
            for i in range(3):
                x = 84 + i * 290 + (j % 2) * 65
                y = 74 + j * 246
                citrus(d, x + 12 * cos(tau * u + i), y, 0.89, u * tau / 3 + i + j, True)
        with d.at(416, 216):
            star(d, 0, 0, 101, 12, P, 0.78)
            d.txt(0, -22, "톡", 50, K, align="center")
    else:
        d.bg(Y)
        dots(d, 3, 5, 765, 430, 17, 2.3, "d79214")
        star(d, 386, 229, 237, 15, R, 0.76)
        with d.at(383, 190, 1.15, -0.05):
            d.path("M -69 -62 L 68 -62 L 50 145 L -47 145 Z", P, K, 5)
            d.path(
                "M -61 -22 Q -25 -36 6 -23 Q 36 -12 60 -27 L 45 137 L -42 137 Z",
                "ffae20",
                K,
                3,
            )
            for i in range(14):
                d.circ(
                    -39 + i * 19 % 76, 119 - (t * 54 + i * 27) % 138, 3 + i % 3, P, K, 1
                )
            d.line([(23, -43), (38, -115), (69, -129)], B, 9)
            citrus(d, -65, -64, 0.64, -0.4, True)


def samara(d, x, y, s, a):
    with d.at(x, y, s, a):
        p = "M -55 14 C -38 -1 -12 -54 70 -64 C 101 -62 64 -33 45 -23 Q 6 1 -33 17 Q -48 36 -58 28 Q -65 20 -55 14 Z"
        with d.at(4, 5):
            d.path(p, "43392e55", None)
        d.path(p, "f4e8cc", "fffaeb", 10)
        d.path(p, None, "544836", 1.5)
        for i in range(11):
            d.path(
                f"M -39 14 Q {-5 + i * 2} {-16 - i * 2} {40 + i * 3} {-29 - i * 3}",
                None,
                "796b54",
                0.9,
            )
        d.ell(-47, 19, 13, 8, "564835")
        d.ell(-49, 16, 4, 2, "c0a981")


def vintage_collage(d, t):
    b, u = phase(t)
    q = int(t * 12) / 12
    d.bg("d6c3a1")
    rng = seed(79)
    for i in range(130):
        x, y = rng.randrange(768), rng.randrange(432)
        d.line([(x, y), (x + rng.randrange(3, 21), y - 1)], "90785845", 0.7)
    edge = [(i * 15, 114 + 5 * sin(i * 3) + 3 * cos(i)) for i in range(53)]
    d.poly([(0, 432), (768, 432)] + edge[::-1], "417875")
    with d.at(386, 213, 1, -0.07):
        d.rect(-298, -149, 604, 306, "302c2444")
        d.rect(-303, -155, 604, 306, "f8edcf")
        d.rect(-288, -142, 575, 278, None, "9d503b", 1)
        # engraved relief rings on a postal survey
        for j in range(13):
            p = [
                (
                    -280 + i * 8,
                    40 + sin(i * 0.12) * 28 + cos(i * 0.17 + j * 0.16) * 26 + j * 6,
                )
                for i in range(71)
            ]
            d.line(p, "9f9c84", 0.8)
        d.txt(-270, -123, ["단풍나무", "바람 우편", "착지"][b], 24, "484536", "serif")
        for j in range(4):
            d.line([(151, -87 + j * 6), (255, -90 + j * 6)], "ad6557", 1)
        d.circ(235, -91, 35, None, "aa624d", 2)
        d.circ(235, -91, 29, None, "aa624d", 1)
        d.txt(235, -97, "11", 18, "aa624d", "mono", "center")
        if b == 0:
            d.path("M 293 -142 Q 200 -64 41 -37 Q -53 -30 -121 -7", None, "504c37", 7)
            for i in range(3):
                samara(d, -65 + i * 85, 2 - i * 21, 0.65, -0.6 + 0.09 * sin(q * 3 + i))
        elif b == 1:
            for i in range(3):
                samara(
                    d,
                    -230 + ((q * 74 + i * 167) % 470),
                    -65 + i * 45 + sin(q * 3 + i) * 24,
                    0.82,
                    q * 1.9 + i,
                )
        else:
            samara(d, 23, 45 - 75 * (1 - span(q, 6, 7.2)), 1.05, 0.15)
            with d.at(-42, 62, span(q, 7.15, 8.6) + 0.001):
                d.path(
                    "M 0 3 Q -4 -21 8 -42 M 5 -32 Q -24 -40 -25 -53 Q -2 -55 5 -32 M 8 -41 Q 17 -63 34 -63 Q 29 -46 8 -41",
                    None,
                    "4a7051",
                    4,
                )


def swiss_motion(d, t):
    b, u = phase(t)
    d.bg("f4f0e7")
    k = "1e211e"
    r = "eb3927"
    for i in range(13):
        d.rect(32 + i * 59, 29, 0.7, 372, "c9c7bf")
    d.rect(31, 50, 708, 2, k)
    d.txt(32, 27, "박자 연습", 14, k)
    d.txt(735, 25, "0" + str(b + 1) + " / 03", 14, k, "mono", "right")
    d.txt(27, 71, ["셋", "쉼", "합"][b], 103, k)
    d.txt(36, 229, ["세 번 짚고", "한 박 쉬고", "함께 짚다"][b], 18, k)
    for j in range(3):
        y = 102 + j * 87
        d.rect(268, y + 43, 470, 1, k)
        for i in range(8):
            x = 270 + i * 59
            h = (29, 49, 68)[j]
            col = k
            if (i + j) % 4 == int(t * 2) % 4:
                col = r
            if b == 1 and i in (3, 4):
                d.rect(x, y + 41, 38, 3, r)
                continue
            off = (1 - span(u, 0, 0.28)) * (j - 1) * 40 if b == 2 else 0
            d.rect(x + off, y + 42 - h, 13 + 8 * j, h, col)
    d.rect(31, 375, 708, 3, k)
    d.rect(32 + int(t * 2) % 12 * 59, 382, 58, 12, r)


def vinyl(d, x, y, r, a):
    d.circ(x, y, r, "1c2323")
    for j in [0.44, 0.56, 0.67, 0.78, 0.88, 0.94]:
        d.circ(x, y, r * j, None, "565347", 1)
    d.circ(x, y, r * 0.34, "edaa46")
    d.circ(x, y, r * 0.06, P)
    with d.at(x, y, 1, a):
        d.line([(r * 0.17, -r * 0.15), (r * 0.24, -r * 0.08)], K, 3)
        for j in range(6):
            d.arc(
                0,
                0,
                r * (0.50 + j * 0.066),
                -0.8 + j * 0.016,
                -0.31 + j * 0.012,
                "b4ae936e",
                1.6,
            )
            d.arc(
                0,
                0,
                r * (0.52 + j * 0.066),
                2.38 + j * 0.016,
                2.76 + j * 0.012,
                "c6b69452",
                1.3,
            )
        d.poly(
            [
                (r * 0.15, -r * 0.04),
                (r * 0.29, -r * 0.04),
                (r * 0.27, r * 0.06),
                (r * 0.14, r * 0.06),
            ],
            "b76139",
        )


def spy_titles(d, t):
    b, u = phase(t)
    q = int(t * 12) / 12
    cream = "f7e2b0"
    ink = "222320"
    red = "cc4935"
    d.bg([cream, red, ink][b])
    if b == 0:
        for i in range(7):
            x = i * 148 - 90 + u * 70
            d.poly([(x, -12), (x + 43, -12), (x - 74, 443), (x - 113, 443)], ink)
        with d.at(395, 212, 1, -0.15):
            d.rect(-184, -106, 368, 212, red)
            d.txt(-161, -63, "야간", 85, cream)
            d.txt(22, 22, "음반", 50, ink)
        vinyl(d, 110 + u * 82, 322, 70, q * 2)
    elif b == 1:
        with d.at(378, 224, 1.18, -0.13):
            d.rect(-189, -124, 378, 249, cream)
            d.rect(-180, -115, 360, 230, None, ink, 2)
            vinyl(d, -32, 0, 98, q * 2)
        with d.at(564, 18, 1, mix(-0.53, 0.24, span(u, 0.07, 0.82))):
            d.poly(
                [(0, -38), (32, -28), (-41, 135), (-123, 166), (-139, 156), (-63, 117)],
                ink,
            )
            d.poly([(-129, 151), (-140, 163), (-151, 156), (-141, 144)], cream, ink, 2)
        d.circ(564, 18, 30, cream, ink, 4)
    else:
        for i in range(16):
            a = pi + i * pi / 15
            d.line(
                [
                    (380 + cos(a) * 76, 295 + sin(a) * 76),
                    (
                        380 + cos(a) * (165 + 18 * sin(i + q * 4)),
                        295 + sin(a) * (165 + 18 * sin(i + q * 4)),
                    ),
                ],
                red if i % 2 else cream,
                5 + i % 4,
            )
        vinyl(d, 380, 300, 79, q * 3)
        d.txt(380, 389, "첫 곡", 19, cream, align="center")


def art_deco(d, t):
    b, u = phase(t)
    d.grad(0, 0, 768, 432, [(0, "111616"), (0.69, "163b36"), (1, "0b1717")])
    gold = "caa667"
    iv = "fff0c8"
    for side in [-1, 1]:
        with d.at(384, 0, side, sy=1):
            for j in range(4):
                d.line(
                    [
                        (360 - j * 7, 21 + j * 6),
                        (360 - j * 7, 407 - j * 6),
                        (268 - j * 7, 407 - j * 6),
                        (250 - j * 7, 390 - j * 6),
                        (0, 390 - j * 6),
                    ],
                    gold,
                    1.3,
                )
            for j in range(7):
                d.poly(
                    [
                        (180 + j * 25, 357),
                        (180 + j * 25, 323 - j * 22),
                        (203 + j * 25, 301 - j * 22),
                        (203 + j * 25, 357),
                    ],
                    "213e36",
                    gold,
                    1.5,
                )
    for j in range(19):
        a = pi + j * pi / 18
        extent = 76 + span(t, 0.3, 4.3) * 101
        d.line(
            [(384, 309), (384 + cos(a) * extent * 1.4, 309 + sin(a) * extent)],
            "a1844f",
            1,
        )
        x = 384 + cos(a) * extent * 1.4
        y = 309 + sin(a) * extent
        d.circ(x, y, 3.2, iv if t * 4 > j else "696047")
    # A gold ribbed shell fans out around its pearl
    for j in range(15):
        a = (j - 7) * (0.025 + 0.137 * span(t, 0.35, 4.7))
        with d.at(384, 315, 1, a):
            h = 119 + 32 * cos((j - 7) * 0.17)
            d.path(
                f"M 0 0 C -4 -42 -34 {-h} 0 {-h} C 33 {-h} 7 -43 0 0 Z",
                "3f7060",
                gold,
                1.6,
            )
            d.line([(0, -4), (0, -h + 6)], "d6bd86", 1)
    y = 295 - 91 * span(t, 3.3, 6.7) + 3 * sin(t * 2)
    d.grad(
        384 - 30,
        y - 30,
        60,
        60,
        [
            (0, "fff8dc"),
            (0.36, "f6e7c5"),
            (0.68, "b9ad8c"),
            (0.96, "a0927500"),
            (1, "a0927500"),
        ],
        True,
    )
    if t > 6:
        for i in range(8):
            a = i * tau / 8
            d.line(
                [
                    (384 + cos(a) * 35, y + sin(a) * 35),
                    (
                        384 + cos(a) * (35 + 12 * span(t, 6, 7)),
                        y + sin(a) * (35 + 12 * span(t, 6, 7)),
                    ),
                ],
                iv,
                1.3,
            )
    for j, w in enumerate([224, 190, 150]):
        d.rect(384 - w / 2, 351 - j * 8, w, 5, gold)
    if t >= 6:
        # The lacquer catches a moving band of light, from the shell to the wings.
        progress = span(t, 6, 8.75)
        for side in [-1, 1]:
            for j in range(7):
                x = 384 + side * (191 + j * 25)
                yy = 313 - j * 22
                shine = clamp(1 - abs(progress * 8 - j) * 0.67)
                if shine > 0:
                    c = "f5df9f" + f"{int(210 * shine):02x}"
                    d.line([(x, 350), (x, yy), (x + side * 12, yy - 11)], c, 2)
                    d.grad(
                        x - 13,
                        yy - 24,
                        26,
                        26,
                        [(0, "fff4b8" + f"{int(220 * shine):02x}"), (1, "fff4b800")],
                        True,
                    )
        d.arc(
            384,
            y,
            35 + 10 * progress,
            -pi / 2,
            -pi / 2 + tau * max(0.001, progress),
            gold,
            1.2,
        )


def pictogram_motion(d, t):
    b, u = phase(t)
    grounds = ["194f80", "057568", "ad4b27"]
    pales = ["a5d8ff", "a4ead7", "ffd8a4"]
    d.bg(grounds[b])
    light = pales[b]
    ink = "fff5da"
    for j in [0, 1, 7, 8]:
        for i in range(-2, 18):
            x = i * 48 + (1 if j % 2 else -1) * ((t * 48) % 48)
            y = j * 48
            if (i + j) % 3 == 0:
                d.circ(x + 24, y + 24, 21, light)
            elif (i + j) % 3 == 1:
                d.poly([(x, y + 46), (x + 46, y), (x + 46, y + 46)], light)
            else:
                for k in range(3):
                    d.rect(x + k * 13, y, 5, 46, light)
    d.txt(53, 143, ["걷기", "타기", "젓기"][b], 52, ink)
    with d.at(459 + sin(t * 2) * 12, 236):
        a = t * pi * 1.5
        if b == 0:
            d.circ(0, -77, 21, ink)
            d.line([(0, -42), (-7, 8)], ink, 18)
            for s in [-1, 1]:
                d.line(
                    [(-3, -39), (s * 30 * cos(a), -19), (s * 46 * cos(a) - 6, -34)],
                    ink,
                    12,
                )
                d.line(
                    [(-7, 9), (s * 27 * cos(a), 41), (s * 43 * cos(a) - 13, 67)],
                    ink,
                    14,
                )
        if b == 1:
            for x in [-66, 69]:
                d.circ(x, 41, 38, None, ink, 8)
            d.line([(-66, 41), (-24, -14), (1, 39), (53, -13), (69, 41)], ink, 8)
            d.line([(-66, 41), (1, 39)], ink, 7)
            d.circ(12, -80, 17, ink)
            d.line([(5, -53), (-21, -23), (8, 3), (12 + 10 * sin(a), 26)], ink, 12)
            d.line([(3, -51), (38, -23), (53, -23)], ink, 10)
        if b == 2:
            d.path("M -104 18 Q -30 48 103 12 Q 70 65 -48 57 Q -83 50 -104 18 Z", ink)
            d.circ(1, -61, 17, ink)
            d.line([(0, -37), (-8, 14), (38, 14)], ink, 14)
            with d.at(4, -14, 1, sin(a) * 0.5):
                d.line([(-44, -53), (53, 54)], ink, 6)
                d.line([(31, 30), (53, 54)], ink, 12)


def bauhaus_shapes(d, t):
    d.bg("eee7d6")
    blue = "254c74"
    red = "c84233"
    yellow = "e5ad3c"
    for x in range(48, 738, 56):
        d.line([(x, 40), (x, 389)], "bcb5a6", 0.7)
    for y in range(52, 394, 56):
        d.line([(45, y), (720, y)], "bcb5a6", 0.7)
    d.txt(52, 55, "원의 넓이", 21, "302e2a")
    # Two equal semicircles travel on opposite rails and join a single circular measure.
    for i, c in enumerate([blue, red]):
        x = mix([174, 592][i], 384, span(t, 2 + i * 0.35, 6.45))
        y = mix([178, 278][i], 219, span(t, 2.6, 6.55))
        a = mix([pi, 0][i] + 0.85, [pi, 0][i], span(t, 0.4, 5))
        with d.at(x, y, 1, a):
            d.poly(
                [(0, 0)]
                + [(cos(pi * j / 48) * 88, sin(pi * j / 48) * 88) for j in range(49)],
                c,
            )
    if t >= 6.5:
        a = span(t, 6.5, 8.6) * tau
        d.arc(384, 219, 105, -pi / 2, -pi / 2 + a, "363833", 1.7)
        d.circ(384 + 105 * sin(a), 219 - 105 * cos(a), 7, yellow)
    else:
        d.line([(54, 347), (714, 347)], "323736", 1.6)
        d.circ(100 + 568 * span(t, 0, 6.5), 337, 10, yellow)
    d.txt(704, 354, ["½", "½ + ½", "1"][phase(t)[0]], 31, "393a33", "mono", "right")


def flat_space_explainer(d, t):
    b, u = phase(t)
    d.bg("10213f")
    mint = "7ed6b7"
    blue = "4a9ed5"
    q = "f1c16f"
    for j in range(39):
        x = (j * 81 + 19) % 768
        y = (j * j * 27 + 19) % 432
        d.circ(x, y, 1 + (j % 3) * 0.5, "28425e")
    with d.at(380, 215, 1 + span(u, 0, 0.96) * 0.23):
        if b == 0:
            d.ell(0, 24, 239, 111, "203c55")
            d.ell(0, 8, 225, 100, blue)
            for i in range(8):
                x = -158 + i * 43
                y = 12 + sin(i * 3 + t) * 22
                d.ell(x, y, 22, 8, mint)
                d.line([(x, y), (x + 14, y - 4)], "316e71", 2)
            d.circ(38, 13, 19, None, q, 2)
        elif b == 1:
            d.circ(0, 0, 148, "1c3453")
            d.circ(0, 0, 128, "284c72")
            d.circ(0, 0, 115, blue)
            for i in range(14):
                x = sin(i * 6.72 + t * 0.3) * 78
                y = cos(i * 4.93 + t * 0.24) * 68
                with d.at(x, y, 1, i + t * 0.2):
                    d.ell(0, 0, 17, 6, mint, "316c71", 2)
                    d.line([(-11, 0), (11, 0)], "316c71", 1.5)
        else:
            with d.at(0, 0, 1, -0.28 + 0.05 * sin(t)):
                d.ell(0, 0, 184, 58, "326b75")
                d.ell(-3, -5, 174, 51, mint)
                for i in range(-13, 14):
                    x = i * 11
                    h = 41 * sqrt(max(0, 1 - (x / 160) ** 2))
                    d.line([(x, -h), (x + 8, -5)], "3a878a", 2)
                    d.line([(x + 6, 4), (x, h)], "3a878a", 2)
                d.ell(0, 0, 156, 5, q)
    d.txt(38, 357, ["연못", "물 한 방울", "규조류"][b], 25, "f7e9cc")
    d.rect(575, 371, [145, 105, 73][b], 2, q)
    d.txt(577, 381, ["1 m", "1 mm", "50 μm"][b], 15, q, "mono")


def text_flash_cuts(d, t):
    beat = int(t * 2.5)
    f = t * 2.5 % 1
    b, u = phase(t)
    red = "c72334"
    ink = "131318"
    paper = "f2e9d6"
    if beat in [3, 7, 11, 15, 19] and f < 0.55:
        d.bg(red if beat % 3 else paper)
        d.txt(384, 35, ["비", "틈", "빛"][b], 306, ink, "serif", "center")
        return
    d.bg([paper, ink, paper][b])
    if b == 0:
        for i in range(8):
            x = i * 121 - (t * 62) % 121
            d.poly([(x, -30), (x + 50, -30), (x - 78, 432), (x - 125, 432)], ink)
        for i in range(45):
            x = (i * 97 - t * 62) % 830
            y = (i * 61 + t * 160) % 455
            d.line([(x, y), (x - 12, y + 31)], red, 1.6)
    elif b == 1:
        from illustration import plate

        plate(
            d,
            "text-flash-cuts",
            (0, 0, 768, 432),
            1.04 + 0.13 * u,
            (0.51 + 0.08 * u, 0.43),
        )
    else:
        d.circ(554, 106, 64, red)
        for i in range(9):
            d.poly(
                [
                    (i * 100 - 40, 431),
                    (i * 100, 298 - i % 3 * 24),
                    (i * 100 + 80, 298 - i % 3 * 24),
                    (i * 100 + 92, 431),
                ],
                ink,
            )
    if b != 1:
        x = 307 + sin(t * 1.7) * 32
        y = 187 + (22 if b == 2 else 0)
        with d.at(x, y, 1, 0.12 * cos(t)):
            d.path(
                "M -143 18 Q -97 -82 0 -85 Q 106 -75 139 16 Q 107 -8 78 18 Q 39 -3 5 24 Q -36 -3 -73 21 Q -111 -2 -143 18 Z",
                red,
                ink,
                3,
            )
            d.path("M 0 -85 L 2 95 Q 6 123 22 106", None, ink, 5)


def heron(d, x, y, s, a, ink):
    with d.at(x, y, s):
        d.path(
            "M -55 9 Q -26 -12 13 -5 Q 25 -11 27 -31 Q 31 -56 50 -53 L 55 -48 L 83 -44 L 55 -42 Q 43 -48 40 -29 Q 39 5 22 12 Q -6 34 -55 9 Z",
            ink,
        )
        d.poly([(-39, 9), (-76, 15), (-51, 2)], ink)
        with d.at(-2, 3, 1, a):
            d.path(
                "M 0 0 Q -22 -32 -71 -58 L -66 -43 L -83 -53 L -70 -32 L -87 -41 Q -46 13 0 9 Z",
                ink,
            )
        d.line([(-28, 16), (-55, 29), (-74, 28)], ink, 2)
        d.line([(-20, 18), (-45, 35), (-68, 37)], ink, 2)


def silhouette_rhythm(d, t):
    d.grad(
        0,
        0,
        768,
        432,
        [(0, "6c397a"), (0.44, "e96c5b"), (0.74, "ffc173"), (1, "a65065")],
    )
    d.circ(523, 222, 71, "ffcf80")
    for i in range(2):
        d.poly(
            [(0, 321)]
            + [
                (j * 12, 280 + i * 17 + 14 * sin(j * 0.16 + i) + 9 * cos(j * 0.4 + i))
                for j in range(66)
            ]
            + [(768, 325)],
            ["945574", "6f4767"][i],
        )
    d.rect(0, 316, 768, 116, "b26573")
    for i in range(52):
        x = (i * 91 + t * (4 + i % 4)) % 798 - 15
        y = 319 + (i * 19) % 112
        d.line([(x, y), (x + 8 + i % 22, y)], "e99980", 1)
    for j in range(3):
        depart = span(t, 0.9 + j * 0.65, 4 + j * 0.65)
        x = 98 + j * 81 + depart * (115 + j * 21) + span(t, 5.8, 9) * 112
        y = 291 - depart * (71 + j * 30) - 21 * sin(t * 0.7 + j) * depart
        a = 0.13 if t < 1 + j * 0.65 else 0.37 + sin(int(t * 10) / 10 * 4.5 - j) * 0.66
        if 5.55 < t < 6.4:
            a = -0.45
        heron(d, x, y, 0.62 + j * 0.095, a, "201c2c")
        if y > 220:
            with d.at(x, 318 + (318 - y) * 0.25, 0.67, sy=-0.22):
                heron(d, 0, 0, 0.66, a, "794e60")
    for j in range(21):
        x = j * 13 - 30
        d.line(
            [(x, 437), (x + 7, 366 - 23 * sin(j * 2)), (x + 13, 342 - 22 * sin(j * 2))],
            "282333",
            2,
        )
