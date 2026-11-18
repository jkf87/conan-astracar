"""Original character sheets in executable form. All faces, props and sprites are self-drawn."""

from draw import *


def rubber_hose(d, t):
    q = int(t * 12) / 12
    swing = sin(q * tau / 0.66)
    ink = "262527"
    p = "eee5cd"
    b, u = phase(t)
    d.grad(0, 0, 768, 432, [(0, "8f877b"), (0.6, "ded6bd"), (1, "ada393")])
    for j in range(21):
        d.poly(
            [
                (j * 42 - 90, 0),
                (j * 42 - 45, 0),
                (j * 42 - 95, 264),
                (j * 42 - 113, 264),
            ],
            "46444024",
        )
    d.ell(389, 333, 210, 20, "514e4955")
    for j in range(15):
        x = j * 63 - 55
        d.poly([(x, 351), (x + 60, 351), (x + 83, 430), (x + 17, 430)], p, ink, 2)
        if j % 7 not in [2, 6]:
            d.poly([(x + 44, 350), (x + 62, 350), (x + 70, 391), (x + 48, 391)], ink)
    with d.at(320 + 14 * swing, 260 - abs(swing) * 12, 1, swing * 0.07):
        for s in [-1, 1]:
            d.path(
                f"M {s * 28} 35 Q {s * (53 + 15 * swing)} 56 {s * (36 - 12 * swing)} 75",
                None,
                ink,
                8,
            )
            d.ell(s * (48 - 12 * swing), 76, 22, 8, ink)
        d.path("M 47 -48 Q 102 -77 104 -38 Q 104 -6 53 3", None, ink, 14)
        d.path("M 47 -48 Q 102 -77 104 -38 Q 104 -6 53 3", None, p, 7)
        d.path(
            "M -57 -40 Q -89 -32 -108 -76 Q -114 -84 -121 -72 Q -111 -16 -75 1 L -56 18 Z",
            p,
            ink,
            4,
        )
        d.path(
            "M -46 -57 Q 2 -69 43 -56 C 62 -41 81 -7 60 22 Q 39 54 -18 49 Q -75 46 -72 7 Q -72 -23 -46 -57 Z",
            p,
            ink,
            4,
        )
        d.ell(-9, -54, 48, 10, ink)
        d.ell(-8, -58 - 15 * abs(swing), 45, 9, p, ink, 3)
        d.circ(-8, -72 - 15 * abs(swing), 8, ink)
        for x in [-23, 1]:
            d.ell(x, -17, 8, 14, ink)
            d.poly([(x - 1, -22), (x + 8, -24), (x + 3, -17)], p)
        d.path("M -25 9 Q -8 18 17 3 Q 12 33 -6 29 Q -20 26 -25 9 Z", ink)
        d.ell(0, 23, 9, 4, p)
    # Listening cup receives sugar cubes in a parabolic cascade.
    with d.at(533, 293 + 4 * swing, 1, -0.08 * swing):
        d.ell(35, -6, 20, 17, None, ink, 5)
        d.path("M -40 -23 L 39 -23 Q 40 29 7 32 Q -36 33 -40 -23 Z", p, ink, 4)
        d.ell(-1, -24, 40, 9, ink)
        d.arc(-3, -2, 11, 0, pi, ink, 2)
    if t > 1.1:
        for j in range(3):
            z = clamp((t - (1.1 + j * 1.9)) / 1.55)
            if 0 < z < 1:
                with d.at(
                    mix(310, 531, z), mix(173, 263, z) - 115 * sin(pi * z), 1, z * 3
                ):
                    d.rect(-10, -10, 20, 20, p, ink, 2)
                    dots(d, -7, 1, 12, 7, 4, 0.8, ink)
    if b == 2:
        for j in range(4):
            v = (u + j * 0.25) % 1
            x = 508 + v * 115
            y = 248 - v * 148
            d.ell(x, y, 8, 5, ink)
            d.line([(x + 6, y), (x + 6, y - 23), (x + 17, y - 19)], ink, 3)


def skyline(d, t):
    d.grad(
        0,
        0,
        768,
        432,
        [(0, "25274f"), (0.39, "5e5687"), (0.7, "c487a0"), (1, "f4bd9b")],
    )
    rng = seed(913)
    d.ell(578, 99, 44, 43, "f2b997")
    d.path(
        "M 0 224 Q 102 188 218 204 Q 329 157 445 170 Q 545 124 644 155 Q 707 143 768 157 L 768 272 L 0 272 Z",
        "74678a",
    )
    for j in range(2):
        for i in range(19):
            w = 34 + (i * 19) % 45
            x = i * 56 - (t * (4 + j * 4)) % 56 - 40
            h = rng.randrange(25, 82) + j * 21
            y = 269 - h + j * 31
            d.rect(x, y, w, h, ["706780", "454763"][j])
            d.rect(x, y, w, 3, ["a18b9b", "787288"][j])
            for a in range(int(w) // 10):
                for b in range(int(h) // 15):
                    if rng.random() > 0.47:
                        d.rect(
                            x + 4 + a * 10,
                            y + 7 + b * 15,
                            3,
                            4,
                            ["e7b995", "9b93ad"][j],
                        )
    for i in range(3):
        d.path(
            f"M 0 {43 + i * 13} Q 405 {150 + i * 13} 768 {51 + i * 13}",
            None,
            "464462",
            1.2,
        )


def commuter(d, x, y, s, wind):
    with d.at(x, y, s):
        line = "292b44"
        skin = "f4bf9f"
        # Three large cel flats and a single cool shadow plane.
        d.path(
            "M -100 210 Q -94 116 -51 98 L -30 82 L 13 77 Q 73 81 100 129 L 118 210 Z",
            "587e91",
            line,
            2.5,
        )
        d.path("M 11 79 Q 36 102 75 114 L 89 206 L 51 208 Q 48 151 11 121 Z", "3c536c")
        d.path("M -33 45 L 10 43 L 16 86 L -8 104 L -37 81 Z", skin, line, 2)
        d.path("M -37 55 Q -15 74 12 58 L 13 74 Q -15 92 -36 75 Z", "bc7980")
        d.path(
            "M -61 -63 Q -10 -111 42 -78 Q 78 -61 60 -9 L 69 12 L 56 16 Q 51 53 23 65 Q -16 78 -46 52 Q -78 21 -61 -63 Z",
            skin,
            line,
            2.5,
        )
        d.path(
            "M -62 -17 C -99 -85 -44 -119 7 -110 Q 69 -118 81 -64 L 58 -45 L 49 -66 Q 34 -51 3 -39 L 20 -65 Q -15 -34 -25 -9 L -35 20 Q -49 11 -43 37 L -24 66 Q -53 64 -68 48 Q -57 65 -69 77 Q -101 63 -99 32 Q -91 13 -85 -2 Z",
            "363951",
            line,
            3,
        )
        d.path(
            "M -77 -62 Q -57 -99 -4 -97 Q 22 -100 53 -83 Q 3 -89 -21 -73 L -7 -83 Q -37 -79 -62 -54 Z",
            "62617c",
        )
        d.path("M 17 -19 Q 31 -30 48 -21 Q 38 -3 19 -12 Z", "fae6d0", line, 2)
        d.ell(34, -17, 6, 8, "5e626e")
        d.circ(36, -20, 2, "fff1d3")
        d.line([(16, -28), (36, -32), (48, -28)], line, 2)
        d.path("M 34 32 Q 44 34 50 29", None, "965e67", 1.7)
        d.path("M -52 79 Q -14 95 17 76 L 31 93 Q 2 115 -53 102 Z", "cb685f", line, 2)
        d.path(
            f"M -46 91 Q -85 {103 + wind} -131 {74 + wind} L -150 {87 + wind} Q -93 132 -39 105 Z",
            "db8072",
            line,
            2,
        )


def tram(d, x, y, s):
    with d.at(x, y, s):
        d.path(
            "M -201 -64 Q -193 -85 -155 -86 L 158 -86 Q 189 -84 197 -58 L 207 56 L -210 56 Z",
            "d0c1ad",
            "353954",
            3,
        )
        d.rect(-205, 7, 408, 37, "b56870")
        d.rect(-203, 19, 406, 4, "f4bc91")
        for i in range(8):
            xx = -182 + i * 47
            d.rect(xx, -62, 37, 54, "474d68", "68647a", 2)
            d.rect(xx + 3, -58, 31, 7, "e3be9e")
            d.poly(
                [(xx + 4, -16), (xx + 21, -54), (xx + 30, -54), (xx + 12, -15)],
                "747a8a",
            )
        for a in [-150, 151]:
            d.circ(a, 55, 15, "343549")
            d.ell(a, 56, 8, 7, "666579")


def cel_anime_80s(d, t):
    b, u = phase(t)
    q = int(t * 12) / 12
    skyline(d, t)
    if b == 0:
        d.rect(0, 299, 768, 133, "47475a")
        d.poly([(0, 322), (768, 296), (768, 305), (0, 340)], "d2a398")
        d.rect(0, 344, 768, 7, "84758b")
        d.rect(104, 82, 9, 217, "41425b")
        d.rect(75, 85, 87, 44, "e5b397", "4c4961", 3)
        d.txt(118, 97, "종점", 15, "4a4861", align="center")
        commuter(d, 437, 261, 0.68, 6 * sin(q * 2))
    elif b == 1:
        commuter(d, 365, 239, 1.38, 9 * sin(q * 3))
        d.poly([(0, 0), (166, 0), (105, 11), (0, 39)], "484d65")
    else:
        d.rect(0, 318, 768, 114, "444457")
        d.line([(0, 349), (768, 329)], "b69094", 4)
        tram(d, 824 - 485 * span(t, 6, 8.4), 282, 1.07)
        commuter(d, 139 + 34 * span(t, 6.8, 8.8), 297, 0.47, 5 * sin(q * 4))
    for y in range(0, 432, 4):
        d.rect(0, y, 768, 0.5, "25243c18")


def alien(d, x, y, s, kind, pose):
    with d.at(x, y, s):
        k = "252638"
        body = ["8bdcaa", "f1ad6c"][kind]
        if kind == 0:
            d.path(
                "M -55 50 Q -69 3 -43 -19 Q -53 -55 -32 -72 Q -12 -82 2 -68 Q 26 -92 44 -73 Q 66 -56 51 -24 Q 77 5 61 49 Q 2 75 -55 50 Z",
                body,
                k,
                4,
            )
            for xx in [-23, 20]:
                d.ell(xx, -36, 15, 19, "fff4da", k, 3)
                d.circ(xx + pose * 4, -32, 5, k)
            d.path("M -44 8 Q -4 31 47 7 L 49 51 Q -2 69 -41 51 Z", "5e83a3", k, 3)
            d.line([(-14, -5), (0, 0), (12, -6)], k, 3)
            for j in [-1, 1]:
                d.line([(j * 48, 19), (j * (70 + pose * 4), -1 - j * pose * 4)], k, 8)
                d.circ(j * 72, -3 - j * pose * 4, 8, body, k, 2)
        else:
            d.path(
                "M -62 29 Q -66 -8 -46 -23 Q -36 -55 -4 -68 Q 33 -52 51 -17 Q 72 17 53 38 Q 0 61 -62 29 Z",
                body,
                k,
                4,
            )
            for i in range(5):
                d.path(
                    f"M -4 -58 Q {i * 14 - 35} -27 {i * 17 - 36} -16", None, "ad6e57", 2
                )
            for xx in [-18, 17]:
                d.ell(xx, 0, 8, 11, "fff4da", k, 2)
                d.circ(xx - 2, 2, 3.5, k)
            d.ell(1, 21, 8, 4 + abs(pose) * 4, k)
        for xx in [-26, 27]:
            d.line([(xx, 47), (xx - 5, 63), (xx - 14, 63)], k, 5)


def scifi_toon(d, t):
    b, u = phase(t)
    q = int(t * 12) / 12
    bg = ["b9e5c3", "c8a5e0", "ffc773"][b]
    floor = ["6fa88e", "806fbb", "df8b65"][b]
    k = "28283b"
    d.bg(bg)
    if b == 0:
        for i in range(6):
            d.rect(i * 145 - 20, 29, 119, 62, "e9e2ad", k, 3)
            d.circ(i * 145 + 78, 72, 5, k)
    elif b == 1:
        for i in range(9):
            d.poly(
                [
                    (i * 110 - 70, 293),
                    (i * 110 + 5, 85 + 32 * sin(i)),
                    (i * 110 + 70, 293),
                ],
                "956ebc",
                k,
                2,
            )
    else:
        for i in range(7):
            d.ell(i * 124 - 10, 80 + 25 * sin(i), 48, 15, "ef9f76", k, 2)
    d.rect(0, 304, 768, 128, floor)
    d.line([(0, 305), (768, 305)], k, 3)
    d.ell(400, 200, 70 + 8 * sin(t * 4), 107, "4b476f", k, 4)
    for j, c in enumerate(["f5eb9c", "8ad9c3", "6878a7"]):
        d.ell(400, 200, 61 - j * 11 + 3 * cos(t * 3 + j), 98 - j * 15, None, c, 4)
    alien(d, 182 + 20 * sin(q * 1.7), 263, 1.08, 0, sin(q * 3))
    alien(d, 563 + 19 * sin(q * 2.2), 276 - abs(sin(q * 3)) * 12, 0.89, 1, cos(q * 3))
    with d.at(
        374 + 37 * sin(t * 2),
        190 + 20 * cos(t * 2),
        [0.52, 1.25, 0.72][b],
        -0.5 + t * 0.4,
    ):
        d.line([(0, 61), (0, -20)], k, 10)
        d.line([(0, 61), (0, -20)], "e8ddd9", 5)
        d.ell(0, -40, 18, 29, "d9eaf0", k, 4)
        d.ell(-5, -44, 6, 15, "a9c3d2")


def midcentury_toon(d, t):
    d.bg("f2dfb8")
    k = "463e3b"
    q = int(t * 12) / 12
    b, u = phase(t)
    d.poly([(0, 0), (302, 0), (245, 433), (0, 433)], "c5cbb4")
    d.poly([(0, 371), (768, 318), (768, 432), (0, 432)], "dbaf8b")
    for i in range(8):
        d.line([(20 + i * 31, 21), (14 + i * 31, 296)], "a2ad9988", 1)
    # A mobile, hung from one point; the final ornament alters the tilt.
    d.line([(484, 12), (484, 96)], k, 1.7)
    with d.at(484, 96, 1, mix(-0.17, 0.04, span(t, 3.2, 7.8)) + 0.025 * sin(t * 2)):
        d.line([(-121, 28), (122, -8)], k, 3)
        for x, y, h, c, n in [
            (-100, 25, 84, "be6753", 0),
            (0, 10, 117, "d79c44", 1),
            (92, -2, 54, "608f86", 2),
        ]:
            d.line([(x, y), (x, y + h)], k, 1)
            with d.at(x, y + h + 15):
                if n == 0:
                    d.ell(2, 3, 30, 14, c)
                    d.ell(0, 0, 30, 14, None, k, 1.6)
                if n == 1:
                    d.poly([(-24, 0), (1, -20), (26, 0), (-2, 22)], c)
                    d.line([(-23, 0), (1, -20), (25, 0)], k, 1.2)
                if n == 2 and t > 2.8:
                    with d.at(0, 27 * (1 - span(t, 2.8, 5.8))):
                        star(d, 0, 0, 22, 4, c, 0.38)
                        d.line([(-19, 0), (0, -22), (3, -5)], k, 1.4)
    # A paper-cut art teacher with held torso and independently changing fingertips.
    with d.at(210, 275):
        d.path("M -68 110 L -49 -13 L -19 -32 L 16 -21 L 56 105 Z", "63988e")
        d.path(
            "M -14 -38 L -18 -58 Q -41 -68 -40 -99 Q -37 -134 -3 -135 Q 24 -136 35 -116 L 32 -91 L 51 -79 L 34 -73 Q 31 -46 4 -49 L 10 -29 Z",
            "deb18d",
            k,
            1.4,
        )
        d.path(
            "M -45 -82 Q -70 -94 -52 -131 Q -40 -154 -7 -150 Q 28 -159 40 -123 L 17 -108 L -5 -121 L -20 -98 L -26 -79 Z",
            k,
        )
        d.line([(1, -93), (37, -94)], k, 1.7)
        d.ell(23, -89, 13, 10, None, k, 2)
        d.circ(23, -90, 2, k)
        ex = 69 + 8 * sin(q * 2)
        ey = -41 - 20 * span(t, 2.7, 5.5)
        d.line([(19, 2), (62, 26), (ex + 37, ey)], k, 3)
        d.ell(ex + 38, ey - 3, 9, 6, "deb18d", k, 1)
        d.line([(ex + 37, ey - 3), (ex + 54, ey - 13)], k, 2)
    d.txt(43, 35, "모빌 수업", 24, k)


def paper_pal(d, x, y, col, flip, action):
    from illustration import sprite

    with d.at(x, y - 8 - abs(action) * 0.65, 1, action * 0.006):
        sprite(d, "comic-history", "left" if flip > 0 else "right", 107)


def comic_history(d, t):
    d.bg("ddcaa5")
    ink = "52483b"
    d.rect(28, 21, 712, 390, "f6eace", ink, 2)
    d.rect(40, 33, 686, 326, "b6c7b6", ink, 1.5)
    for i in range(16):
        d.rect(52 + 45 * i, 34, 0.7, 323, "8eaa9f")
    for i in range(9):
        d.rect(40, 50 + 37 * i, 685, 0.7, "8eaa9f")
    islands = [(195, 201, 138, 85, "c5ae81"), (567, 183, 115, 91, "ceb694")]
    for cx, cy, rx, ry, col in islands:
        for j in [3, 2, 1, 0]:
            p = []
            for a in range(81):
                v = a * tau / 80
                r = 1 + 0.15 * cos(v * 3 + cx) + 0.10 * sin(v * 5)
                p.append(
                    (cx + (rx + j * 5) * r * cos(v), cy + (ry + j * 4) * r * sin(v))
                )
            d.poly(
                p,
                col if not j else None,
                ink if not j else "91a89c",
                1.6 if not j else 1,
            )
        for j in range(5):
            x = cx - 56 + j * 23
            y = cy + 36 + 9 * sin(j * 2)
            d.line([(x - 6, y + 7), (x, y - 3), (x + 6, y + 7)], "998363", 1)
    q = int(t * 12) / 12
    paper_pal(d, 220, 186, "6d91ab", 1, 7 * sin(q * 4))
    paper_pal(d, 557, 170, "bc7766", -1, 7 * cos(q * 4))
    d.txt(189, 265, "솔섬", 19, ink, "serif")
    d.txt(546, 257, "달섬", 19, ink, "serif")
    for j in range(int(span(t, 0.6, 5.1) * 22)):
        x = 256 + j * 12
        y = 207 - 31 * sin(j / 22 * pi)
        d.line([(x, y), (x + 5, y - 1)], ink, 1.4)
    x = mix(252, 512, span(q, 1.4, 6.6))
    y = 215 - 32 * sin(pi * span(q, 1.4, 6.6))
    d.poly(
        [(x - 19, y), (x + 21, y), (x + 11, y + 11), (x - 11, y + 11)],
        "faf0d8",
        ink,
        1.8,
    )
    d.line([(x, y), (x, y - 29)], ink, 1.5)
    d.poly([(x + 2, y - 27), (x + 18, y - 4), (x + 2, y - 4)], "cd9560", ink, 1)
    if t > 5.9:
        for i in range(6):
            x = 422 + i * 36
            y = 111 + 14 * sin(i + q * 3)
            d.ell(x, y, 5, 3, ink)
            d.line([(x + 4, y), (x + 4, y - 14), (x + 11, y - 12)], ink, 2)
    d.txt(
        383,
        373,
        ["두 섬의 악보", "배에 실린 멜로디", "달섬의 첫 합주"][phase(t)[0]],
        19,
        ink,
        "serif",
        "center",
    )


def kingfisher(d, x, y, s, angle):
    from illustration import sprite

    with d.at(x, y, s, angle):
        sprite(d, "manga-panels", "all", 192)


def manga_panels(d, t):
    p = "f3eee1"
    k = "21211f"
    spot = "cd4d3e"
    d.bg(p)
    b, u = phase(t)
    # A page opens in reading order. Every drawing is clipped to its own inked gutter.
    left = "M 18 18 L 323 18 L 276 414 L 18 414 Z"
    top = "M 337 18 L 750 18 L 750 194 L 313 218 Z"
    bot = "M 311 231 L 750 207 L 750 414 L 289 414 Z"
    with d.clip(left):
        d.rect(0, 0, 340, 432, "c8c4b8")
        dots(d, 0, 0, 336, 432, 7, 1.15, "89877d")
        with d.at(149, 239, 1.15, -0.19):
            d.path(
                "M -115 -59 L -59 -61 L -43 -81 L 22 -82 L 40 -62 L 101 -59 Q 113 -55 114 -41 L 114 58 L -113 59 Z",
                p,
                k,
                4,
            )
            d.rect(-100, -40, 43, 14, k)
            d.circ(7, 0, 55, k)
            d.circ(7, 0, 44, p)
            d.circ(7, 0, 38, k)
            d.circ(7, 0, 26, "aaa79c")
            d.circ(7, 0, 16, k)
            d.circ(0, -9, 6, p)
            d.path(
                "M -124 99 Q -102 37 -82 26 Q -75 22 -74 30 L -78 47 Q -54 31 -44 44 L -65 82 L -83 108 Z",
                p,
                k,
                2,
            )
        d.txt(41, 41, "기다림", 27, k, "serif")
    if t > 1.15:
        with d.clip(top):
            d.rect(306, 16, 445, 218, p)
            dots(d, 310, 18, 448, 210, 8, 1.05, "9c978850")
            d.path("M 323 202 Q 503 112 743 164", None, k, 8)
            kingfisher(d, 565 + 15 * sin(t * 2), 108, 0.87, 0.08 * sin(t * 3))
    d.path(left, None, k, 3.4)
    d.path(top, None, k, 3.4)
    if t > 3.55:
        with d.clip(bot):
            d.rect(283, 205, 480, 216, p)
            for i in range(59):
                a = i * tau / 59
                v = 98 + 17 * sin(i * 5 + int(t * 8))
                d.line(
                    [
                        (558 + v * cos(a), 314 + v * 0.68 * sin(a)),
                        (558 + 340 * cos(a), 314 + 183 * sin(a)),
                    ],
                    k,
                    1 if i % 3 else 2.2,
                )
            x = 514 + 80 * span(t, 3.6, 6.3)
            y = 263 + 62 * span(t, 3.6, 6.3) - 55 * span(t, 6.6, 8.7)
            kingfisher(d, x, y, 0.63, 0.76 - 0.97 * span(t, 6.3, 8.7))
            d.path(
                "M 349 387 Q 430 365 492 383 Q 526 395 561 371 L 551 341 L 586 362 L 609 333 L 607 367 Q 665 350 740 362",
                None,
                k,
                2.2,
            )
        if t > 6.1:
            d.txt(322, 251, "찰칵", 32, spot, "serif")
    d.path(bot, None, k, 3.4)


def pixel_sprite(d, x, y, s, frame):
    grid = [
        "   kkk   ",
        "  krrrk  ",
        " krrrrrk ",
        "  kssks  ",
        "  ksssk  ",
        "   bbb   ",
        "  bcccb  ",
        " sbcccs  ",
        "  kbbbk  ",
        "  kk kk  ",
        "  ll ll  ",
    ]
    colors = {
        "k": "26283a",
        "r": "bc6d59",
        "s": "efd0a3",
        "b": "476588",
        "c": "81a69f",
        "l": "c9a77f",
    }
    for j, row in enumerate(grid):
        for i, ch in enumerate(row):
            if ch != " ":
                d.rect(
                    x + i * s + (s if frame % 2 and j > 8 and i < 4 else 0),
                    y + j * s,
                    s,
                    s,
                    colors[ch],
                )


def pixel_rpg(d, t):
    # Pixel positions snap to a 256 by 144 working lattice.
    k = "252d46"
    s = 3
    d.bg("344b50")
    r = seed(119)
    with d.at(0, 0, 3):
        for j in range(700):
            x, y = r.randrange(256), r.randrange(144)
            d.rect(
                x, y, r.choice([1, 2, 3]), 1, r.choice(["3d5757", "47645d", "2a4249"])
            )
        for j in range(26):
            y = j * 6
            x = 133 + round(sin(j * 0.32) * 6)
            d.rect(x, y, 38, 6, "375777")
            d.rect(x, y, 2, 6, "73928b")
            for i in range(3):
                d.rect(x + 2 + (int(t * 5) + i * 13 + j) % 32, y + i, 4, 1, "618393")
        d.rect(1, 73, 256, 12, "998972")
        for i in range(12):
            d.rect(127 + i * 4, 70, 3, 20, "a98266")
            d.rect(127 + i * 4, 71, 3, 2, "c1ac83")
        for x in [126, 174]:
            d.rect(x, 68, 3, 25, k)
            d.rect(x - 2, 63, 7, 6, "e8c772" if t > 5.8 else "76756a")
        for i in range(29):
            x = i * 29 % 266 - 5
            y = (i * 23 % 53) - 5
            if 125 < x < 174:
                continue
            d.rect(x + 6, y + 9, 3, 12, "675f51")
            for j in range(5):
                d.rect(x + 7 - j * 2, y + j * 2, 2 + j * 4, 3, "263e44")
                d.rect(x + 7 - j * 2, y + j * 2, 1 + j * 2, 2, "587565")
        for i in range(46):
            x = (i * 31 + 11) % 256
            y = 96 + (i * 23) % 43
            if 124 < x < 181:
                continue
            d.rect(x, y, 2, 6, "789181")
            d.rect(x - 2, y + 2, 2, 2, "789181")
            if i % 4 == 1:
                d.rect(x, y, 2, 2, "d4b879")
        for i in range(12):
            x = 136 + i * 5 % 29
            y = 26 + (i * 59) % 107
            if y < 69 or y > 92:
                d.rect(x, y, 5, 1, "7ca09b")
        xx = 32 + 161 * span(t, 0.2, 8.25)
        d.rect(int(xx) + 2, 80, 12, 2, "4f5954")
        pixel_sprite(d, int(xx) - 2, 62, 1.65, int(t * 7))
        for glint in [66, 98, 125]:
            v = clamp((xx - glint + 1) / 14)
            if 0 < v < 1:
                for j in range(6):
                    a = j * tau / 6
                    d.rect(
                        int(glint + cos(a) * 10 * v),
                        int(65 + sin(a) * 10 * v),
                        2,
                        2,
                        "f2d387",
                    )
        for i, x in enumerate([66, 98, 125]):
            if xx < x + 1:
                y = 66 + round(3 * sin(t * 4 + i))
                d.rect(x - 2, y + 1, 5, 1, "f5d783")
                d.rect(x, y - 1, 1, 5, "ffe8a0")
    d.rect(34, 326, 696, 76, k, "e7d6a7", 3)
    d.rect(41, 333, 682, 62, None, "8496a6", 1)
    # The three inventory lamps echo the three disappearing fireflies.
    for i, threshold in enumerate([66, 98, 125]):
        xx = 613 + i * 31
        d.rect(xx, 346, 19, 24, "566b70", "a1b8a3", 2)
        d.rect(xx + 3, 341, 13, 4, "b1ad92")
        if 32 + 161 * span(t, 0.2, 8.25) > threshold:
            d.rect(xx + 7, 353, 6, 8, "f1d77f")
            d.rect(xx + 4, 356, 12, 2, "f1d77f")
    d.txt(
        57,
        348,
        ["반딧불을 따라가자.", "다리에 불이 켜졌다.", "건너편 숲에 닿았다."][
            0 if t < 5.8 else 1 if t < 7.8 else 2
        ],
        20,
        "efe3ba",
    )
