"""Eight separately staged editorial shorts. Their miniature events are fictional."""

from drawing import *


def kernels(c, x, y, scale, opened, angle=0):
    with c.transform(x, y, scale, angle):
        if opened:
            c.path(
                "M -20 9 Q -35 -2 -23 -14 Q -24 -30 -8 -25 Q 5 -36 13 -20 Q 32 -23 30 -5 Q 42 9 23 15 Q 18 30 4 23 Q -11 33 -20 9 Z",
                "ead9a7",
                "775134",
                1.6,
            )
            for dx, dy, r in [(-12, -10, 9), (6, -15, 8), (16, 3, 9), (-5, 11, 7)]:
                c.ellipse(dx, dy, r, r * 0.72, "fff4ca")
            c.path("M -10 2 Q -4 -7 4 -1 L 12 6 L 3 12 Z", "b07536")
        else:
            c.path(
                "M -13 4 Q -24 -11 -7 -18 Q 9 -24 15 -7 Q 20 6 3 15 L -3 23 Z",
                "d39639",
                "805031",
                1.8,
            )
            c.path("M -12 -6 Q -10 -15 1 -15", None, "f9d888", 3)


def caption_news(c, t):
    cut = int(t // 3)
    u = t % 3
    c.gradient("3c3028", "171b21")
    c.path(
        "M 225 250 Q 242 377 388 401 Q 552 442 707 387 Q 791 358 822 266 Z", "59514c"
    )
    for band, col in [(0, "72665a"), (1, "8b7967"), (2, "635952")]:
        c.path(
            f"M 235 {279 + band * 7} Q 520 {443 + band * 6} 813 {279 + band * 6}",
            None,
            col,
            3,
        )
    c.ellipse(530, 270, 310, 92, "aa8e72")
    c.ellipse(530, 260, 306, 86, "393135")
    c.ellipse(530, 252, 278, 70, "53403b", "b8a48f", 2)
    for i in range(18):
        x = 323 + (i * 59) % 390
        y = 233 + (i * 39) % 65
        hop = clamp((t - 2.6 - i * 0.17) * 3)
        lift = 95 * sin(pi * hop)
        kernels(
            c,
            x + 7 * sin(i + hop * 2),
            y - lift,
            0.35 + 0.1 * (i % 3),
            hop > 0.48,
            i * 0.7 + hop,
        )
    phase = smooth((t - 3.1) / 2.1)
    for j in range(3):
        xx = 424 + j * 86 + 6 * sin(t * 1.1 + j)
        yy = 204 - j % 2 * 21
        c.path(
            f"M {xx} {yy} Q {xx - 14} {yy - 17} {xx + 1} {yy - 31} Q {xx + 13} {yy - 44} {xx + 4} {yy - 57}",
            None,
            "e7d6b6",
            1.4,
            0.17 + 0.08 * sin(t + j),
        )
    with c.transform(
        528 + 28 * phase, 241 - 91 * sin(phase * pi), 1.12 if cut != 1 else 1.49
    ):
        kernels(
            c, 0, 2 * sin(t * 10) * (1 - phase), 1.2, phase > 0.37, -0.3 + phase * 0.8
        )
    c.rect(0, 0, 250, 432, "20292c", a=0.94)
    c.rect(28, 38, 35, 5, "f2bd56")
    c.txt("한 알의 관찰", 26, 54, 18, "e7e3d9", True)
    a, b = [("옥수수", "한 알"), ("껍질이", "열린 순간"), ("한 줌이", "피었다")][cut]
    c.txt(a, 23, 139, 47, "fff9ed", True)
    c.txt(b, 23, 196, 43, "ffd16b", True)
    c.line([(29, 332), (217, 332)], "757b78")
    c.txt(["가열 전", "팽창", "가열 후"][cut], 27, 350, 18, "e7e3d9")
    for i in range(3):
        c.rect(29 + i * 63, 391, 52, 3, "ffd16b" if i <= cut else "505554")


def carriage(c, x, y, k=1):
    with c.transform(x, y, k):
        c.line([(-5, -46), (1, -56), (8, -42), (0, -20)], "252727", 3)
        c.path(
            "M -36 -18 Q -34 -24 -23 -24 L 24 -24 Q 34 -22 35 -17 L 32 15 Q 28 21 17 21 L -20 21 Q -33 17 -36 -18 Z",
            "ded8c7",
            "262827",
            3,
        )
        for dx in [-26, -8, 10]:
            c.rect(dx, -15, 13, 16, "464643")
        for dx in [-21, -4, 15]:
            c.circle(dx, -7, 2.5, "b2b0a1")
            c.ellipse(dx, -1.7, 4.1, 3, "9d9c8f")
        c.line([(-31, 8), (33, 8)], "54514d", 4)
        c.line([(-8, -19), (-8, 17), (9, 17), (9, -18)], "716f63", 0.8)
        for dx in [-26, -18, 16, 25]:
            c.circle(dx, 14, 0.8, "69695e")
        c.line([(-4, -51), (3, -58), (9, -55)], "323730", 1.5)
        c.circle(2, -57, 2.1, "242923")


def newsreel(c, t):
    c.bg("202020")
    if t < 2.5:
        with c.transform(
            384, 216, 0.38 + 0.66 * smooth(t / 2), -0.63 * (1 - smooth(t / 1.8))
        ):
            c.rect(-300, -180, 600, 360, "ded9c9")
            c.txt("산마을 신보", 0, -160, 47, "282823", True, True, True)
            c.line([(-270, -96), (270, -96)], "383833", 4)
            c.txt("오늘, 첫 운행", -260, -68, 46, "30312c", True, True)
            c.rect(45, 9, 207, 126, "8e8e80")
            carriage(c, 149, 79, 1.22)
            for j in range(9):
                c.rect(-260, 21 + j * 13, 257 - (j % 3) * 15, 3, "56564e")
    else:
        c.gradient("aaa99f", "ece9db")
        for k in range(3):
            points = [
                (x, 183 + k * 70 + 32 * sin(x / (79 - 9 * k) + k * 2))
                for x in range(-9, 790, 8)
            ]
            c.poly(points + [(800, 432), (-10, 432)], ["9b9c92", "777a73", "515550"][k])
        for j in range(92):
            xx = (j * 67) % 811 - 24
            yy = 307 + (j * 41) % 130
            ht = 9 + (yy - 300) * 0.16 + (j % 4)
            c.poly(
                [
                    (xx - ht * 0.28, yy),
                    (xx - ht * 0.11, yy - ht * 0.53),
                    (xx - ht * 0.18, yy - ht * 0.48),
                    (xx, yy - ht),
                    (xx + ht * 0.21, yy - ht * 0.43),
                    (xx + ht * 0.13, yy - ht * 0.46),
                    (xx + ht * 0.30, yy),
                ],
                "474c46",
            )
        c.path(
            "M -9 322 Q 145 291 238 313 Q 296 326 235 338 Q 170 354 65 371",
            None,
            "aaab98",
            2.2,
        )
        c.line([(-10, 160), (780, 60)], "2d302e", 3)
        c.line([(-10, 171), (780, 71)], "50544d", 2)
        x = 96 + (t - 2.5) * 84
        carriage(c, x, 231 - x * 0.127, 1.26)
        for xx in [40, 585]:
            c.poly(
                [
                    (xx, 432),
                    (xx + 11, 142 - xx * 0.127),
                    (xx + 21, 142 - xx * 0.127),
                    (xx + 35, 432),
                ],
                "353934",
            )
            c.rect(xx - 7, 136 - xx * 0.127, 51, 8, "30342f")
        if t > 6.4:
            c.rect(196, 335, 376, 55, "252723")
            c.rect(202, 340, 364, 44, None, "c8c5b6")
            c.txt(
                "고개 너머로 첫 손님을 싣고", 384, 349, 21, "e8e3d1", False, True, True
            )
    for j in range(4):
        x = (j * 237 + int(t * 9) * 73) % 770
        c.line([(x, 20 + j * 39), (x + 0.4, 40 + j * 42)], "ebe8d9", 0.65, 0.45)
    c.rect(6, 6, 756, 420, None, "2b2b29", 9)


def countdown(c, t):
    c.bg("11191c")

    # Continuous marble run. The ball meets the hanging bell at second seven.
    def ball(s):
        if s < 4:
            return (68 + 83 * s, 78 + 22 * s + 3 * sin(s * 2))
        if s < 6:
            return (400 + 55 * (s - 4), 168 + 30 * (s - 4) ** 2)
        return (510 + 54 * min(s - 6, 1.45), 288 - 31 * sin(clamp((s - 6) / 1.45) * pi))

    bx, by = ball(t)

    def bench():
        c.gradient("394849", "81715c")
        for j in range(12):
            c.line([(j * 80 - 60, 0), (j * 80 + 25, 432)], "a28b6c", 2, 0.19)
        c.line([(25, 74), (400, 179), (449, 209), (510, 302), (600, 302)], "393632", 10)
        c.line([(25, 71), (400, 176), (449, 206), (510, 299), (600, 299)], "d2b894", 4)
        for x, y in [(90, 91), (270, 138), (444, 206), (540, 300)]:
            c.rect(x, y, 9, 330 - y, "52493b")
        with c.transform(
            612,
            207,
            1,
            0.17 * sin((t - 7.32) * 23) * math.exp(-2 * max(0, t - 7.32))
            if t > 7.32
            else 0,
        ):
            c.line([(0, -65), (0, 5)], "d4c3a8", 3)
            c.path(
                "M -4 2 Q -22 6 -23 36 Q -26 52 -40 64 Q 0 76 40 64 Q 25 47 23 32 Q 20 6 4 2 Z",
                "c99850",
                "443c30",
                3,
            )
            c.circle(0, 71, 7, "463f33")
        c.circle(bx, by, 10, "a6c6bd", "2b413c", 2)
        c.circle(bx - 3, by - 4, 3, "f2f5e4")

    for i, (x, y, w, h, zoom, cx, cy) in enumerate(
        [
            (12, 14, 487, 307, 0.78, 286, 175),
            (509, 14, 246, 145, 1.15, bx, by),
            (509, 170, 246, 151, 0.92, 608, 250),
        ]
    ):
        with (
            c.window(x, y, w, h),
            c.transform(x + w / 2 - cx * zoom, y + h / 2 - cy * zoom, zoom),
        ):
            c.rect(-800, -800, 2500, 2200, "574f45")
            bench()
        c.rect(x + 8, y + 8, 66, 21, "202629")
        c.txt(["전체", "구슬", "종"][i], x + 16, y + 12, 12, "e5e6da")
    c.txt("구슬이 종에 닿기까지", 18, 352, 24, "e6e6dc", True)
    c.txt(f"{max(0, 7.32 - t):05.2f}", 640, 336, 52, "ffd497", True, center=True)
    c.rect(20, 404, 728, 4, "374247")
    c.rect(20, 404, 728 * clamp(t / 7.32), 4, "dc9b50")


def city_symphony(c, t):
    cut = 0 if t < 3.2 else 1 if t < 5.9 else 2
    if cut == 0:
        c.gradient("829aa7", "ffcf9f")
        c.circle(551, 135 - t * 8, 45, "ffdfaa")
        for j in range(30):
            x = j * 31 - 42 - t * 4
            h = 35 + (j * 71) % 135
            c.rect(x, 289 - h, 24 + j % 11, h, "788588")
            for a in range(int(h / 13)):
                c.rect(x + 4, 295 - h + a * 13, 13, 3, "bbad98")
        c.rect(0, 297, 768, 24, "36484c")
        for i in range(8):
            c.rect(i * 117 - 30, 320, 14, 130, "435356")
        x = -160 + t * 150
        for i in range(4):
            c.rect(x - i * 95, 260, 92, 33, "efc287")
            c.rect(x - i * 95 + 3, 266, 85, 12, "334b57")
            for j in range(6):
                c.rect(x - i * 95 + j * 14, 264, 2, 17, "b09a73")
        c.rect(0, 406, 768, 26, "243e44")
    elif cut == 1:
        c.bg("56646a")
        with c.transform(384, 216, 1, 0.24):
            for j in range(-5, 6):
                c.rect(j * 49 - 14, -110, 25, 221, "d7d2bd")
            for j in range(37):
                x = -310 + (j * 79) % 625
                y = ((j * 47 + t * (34 if j % 2 else -39)) % 510) - 255
                c.ellipse(x + 4, y + 6, 8, 14, "3d4a50")
                c.ellipse(x, y, 7, 11, ["d2895c", "343b42", "9fa99a", "dbbf7c"][j % 4])
                c.circle(x - 1, y - 4, 4, "333f40")
    else:
        c.gradient("182c44", "b47564")
        for j in range(30):
            x = j * 30 - 35
            h = 48 + (j * 29) % 130
            c.rect(x, 272 - h, 25, h, "2c3e4c")
            for k in range(int(h / 12)):
                c.rect(x + 6, 279 - h + k * 12, 7, 2, "cead89", a=(j % 4 + 1) / 5)
        c.rect(0, 276, 768, 156, "273d4d")
        for j in range(110):
            x = (j * 107) % 820
            y = 281 + (j * 43) % 149
            c.line(
                [(x + 5 * sin(t + j), y), (x + 8 + (j % 9) * 4, y)],
                ["98766c", "375260", "af8c71"][j % 3],
                1.2,
            )
        c.path(
            "M -20 249 Q 131 262 204 110 Q 362 354 558 98 Q 664 247 790 218",
            None,
            "27343d",
            4,
        )
        for j in range(2):
            c.rect(201 + j * 354, 106 - j * 12, 9, 215, "283741")
        for j in range(27):
            x = j * 30
            y = (
                243
                - 109 * max(0, 1 - abs(x - 204) / 153) ** 2
                - 130 * max(0, 1 - abs(x - 558) / 174) ** 2
            )
            c.line([(x, y), (x, 253)], "384652", 1.5)
        c.rect(0, 251, 768, 12, "283742")
        for j in range(18):
            x = (j * 101 + t * 127) % 850 - 50
            c.line([(x - 25, 247), (x, 247)], "ffbb80", 2.5)


def visual_investigation(c, t):
    c.bg("16242a")
    c.txt("어느 풍경이 울렸을까", 25, 20, 26, "e6e6da", True)
    c.txt("모의 관측", 645, 30, 15, "a4b7b6")
    for j in range(3):
        x = 27 + j * 244
        y = 73
        c.rect(x, y, 226, 183, "263a40", "596b6b")
        c.line([(x + 26, y + 24), (x + 198, y + 24)], "93a2a0", 3)
        for k in range(5):
            phase = max(0, t - 3.25)
            angle = (
                0.28 * math.exp(-0.42 * phase) * sin(phase * 8 + k * 0.15)
                if j == 1 and t > 3.25
                else 0.01 * sin(t + k)
            )
            with c.transform(x + 54 + 30 * k, y + 24, 1, angle):
                c.line([(0, 0), (0, 18)], "ccd4bf")
                c.rect(-5, 18, 10, 52 + (k * 11) % 41, "a2afab")
                c.rect(-4, 18, 2, 50 + (k * 11) % 41, "d1d3bc")
        c.txt(["서쪽", "가운데", "동쪽"][j], x + 12, 223, 17, "d4dbcc")
        if j == 1 and t > 4.05:
            c.arc(
                x + 114,
                y + 82,
                70,
                -pi / 2,
                -pi / 2 + TAU * clamp(t - 4.05),
                "eeb66f",
                3,
            )
    c.rect(27, 278, 714, 125, "203139")
    for j in range(4):
        c.line([(54, 303 + j * 23), (718, 303 + j * 23)], "3c4c51")
    pts = []
    for x in range(54, 718, 2):
        s = (x - 54) / 664 * 9
        v = max(0, s - 3.25)
        amp = 0 if s < 3.25 else 39 * math.exp(-v * 0.83) * sin(v * 57) * cos(v * 3)
        pts.append((x, 347 + amp + 1.5 * sin(x)))
    c.line(pts, "9cbdb6", 1.6)
    xx = 54 + 664 * t / 9
    c.line([(xx, 287), (xx, 392)], "f0ba72", 2)
    if t > 6.25:
        c.txt("가운데 관이 먼저 흔들렸다", 46, 288, 16, "f1d3a0", True)


def gear(c, x, y, r, a, col, hole):
    pts = []
    for i in range(64):
        theta = i * TAU / 64 + a
        rad = r * (1 if i % 4 in (1, 2) else 0.85)
        pts.append((x + rad * cos(theta), y + rad * sin(theta)))
    c.poly(pts, col)
    c.circle(x, y, r * 0.46, hole)
    for j in range(6):
        c.circle(
            x + r * 0.64 * cos(a + j * TAU / 6),
            y + r * 0.64 * sin(a + j * TAU / 6),
            r * 0.085,
            hole,
        )


def kino_montage(c, t):
    paper = "e4d8b9"
    ink = "272c2a"
    red = "bc4232"
    cut = int(t // 3)
    u = t % 3
    c.bg(paper)
    if cut == 0:
        c.poly([(0, 0), (490, 0), (219, 432), (0, 432)], ink)
        gear(c, 135, 236, 153, t * 0.8, paper, ink)
        gear(c, 316, 55, 99, -t * 1.1, red, ink)
        with c.transform(543, 214, 1, -0.22):
            c.txt("회전", 0, -32, 78, ink, True, center=True)
    elif cut == 1:
        with c.transform(395, 204, 1, -0.20):
            for i in range(7):
                c.rect(-560 + i * 135, -300, 55, 600, ink if i % 3 else red)
            c.rect(-315, -61 + 22 * cos(t * 8), 630, 85, paper, ink, 7)
            for j in range(8):
                c.rect(-287 + j * 76, -36 + 22 * cos(t * 8), 44, 29, ink)
        c.rect(28, 311, 202, 82, red)
        c.txt("압착", 43, 321, 57, paper, True)
    else:
        for j in range(5):
            x = 25 + j * 131
            y = 124 - j * 14 + 5 * sin(u * 3 + j)
            with c.transform(x, y, 0.77, -0.2):
                c.rect(-11, -15, 276, 310, paper, ink, 3)
                c.poly([(0, 244), (159, 23), (179, 23), (50, 244)], red)
                c.circle(180, 86, 37, ink)
                for k in range(4):
                    c.rect(122, 174 + k * 13, 95 - k * 8, 4, ink)
        c.poly([(0, 340), (370, 302), (330, 432), (0, 432)], ink)
        c.txt("인쇄", 25, 342, 62, paper, True)


def stone(c, x, y, s, col):
    c.ellipse(x + 3, y + 5, s * 1.08, s * 0.67, "9daba7")
    c.ellipse(x, y, s, s * 0.67, "65716f", "505c59", 1.2)
    c.ellipse(x, y - s * 0.15, s * 0.93, s * 0.55, "9da8a0")
    c.ellipse(x, y - s * 0.19, s * 0.66, s * 0.38, col)
    c.line(
        [
            (x - s * 0.38, y - s * 0.26),
            (x - s * 0.28, y - s * 0.44),
            (x + s * 0.31, y - s * 0.44),
        ],
        "e4d8b1",
        max(2, s * 0.09),
    )


def telestrator(c, t):
    ice = "d3ded8"
    c.bg(ice)
    with c.transform(503, 250, 1, -0.16, 0.66):
        for r, col in [
            (164, "537c9a"),
            (115, "e6e9de"),
            (62, "b65b50"),
            (24, "e7e6d8"),
        ]:
            c.circle(0, 0, r, col)
    for j in range(52):
        x = (j * 101) % 790 - 20
        y = (j * 69) % 431
        c.line([(x, y), (x + 95, y - 17)], "f6f5e9", 0.8, 0.38)
    for j in range(2):
        c.line([(-20, 345 + j * 13), (790, 201 + j * 13)], "9eaaa5", 1)
    # Full speed, rewind, freeze to draw, then repeat the decisive run.
    s = (
        t / 2.8
        if t < 2.8
        else 1 - (t - 2.8) / 1.3 * 0.60
        if t < 4.1
        else 0.40
        if t < 6.7
        else 0.40 + 0.60 * clamp((t - 6.7) / 1.8)
    )
    px = 95 + 425 * s
    py = 295 - 88 * s + 34 * sin(s * pi)
    for x, y in [(411, 216), (555, 271), (473, 292)]:
        stone(c, x, y, 18, "c9a64e")
    stone(c, px, py, 20, "bd5e4c")
    c.rect(584, 22, 160, 38, "efc959")
    c.txt("빙판 해설", 663, 29, 23, "213036", True, center=True)
    c.rect(22, 24, 103, 28, "273539")
    c.txt(
        "재연"
        if t < 2.8
        else "되감기"
        if t < 4.1
        else "정지 분석"
        if t < 6.7
        else "다시 보기",
        72,
        29,
        15,
        "f3edda",
        True,
        center=True,
    )
    if 4.1 <= t < 7.6:
        c.arc(px, py, 32, -pi / 2, -pi / 2 + TAU * clamp((t - 4.1) * 2), "eaa92e", 4)
        track = [
            (95 + 425 * f, 295 - 88 * f + 34 * sin(f * pi) - 12)
            for f in np.linspace(0.48, 1, 60)
        ]
        c.line(progress(track, (t - 4.7) * 1.2), "2e8c96", 4)
        if t > 5.6:
            c.poly([(522, 187), (503, 190), (516, 205)], "2e8c96")
        c.rect(43, 352, 282, 44, "293739")
        c.txt("두 스톤 사이로 휘어 들어간다", 54, 362, 19, "fff3d1", True)


def pear(c, x, y, s, col):
    with c.transform(x, y, s):
        c.path(
            "M -7 -20 Q -5 -38 2 -38 Q 9 -37 11 -20 C 15 -9 31 -3 27 15 Q 24 31 0 31 Q -29 30 -28 10 Q -28 -1 -17 -11 Z",
            col,
        )
        c.path("M 1 -36 Q -1 -46 6 -51", None, "594634", 3)
        c.path("M 3 -40 Q 10 -53 25 -48 Q 20 -37 3 -40 Z", "61754b")


def news_package(c, t):
    c.bg("132e3b")
    u = t % 3
    for j in range(15):
        c.line([(j * 72, 0), (j * 72 - 270, 432)], "224452", 1)
    c.poly([(0, 0), (268, 0), (240, 51), (0, 51)], "e9e6d4")
    c.txt("과수원 소식", 25, 11, 24, "183844", True)
    if t < 3:
        c.poly([(44, 104), (358, 104), (326, 328), (44, 328)], "215163")
        for j in range(3):
            pear(
                c,
                137 + j * 57,
                198 + 26 * sin(j * 2 + t),
                1.15,
                ["dfab59", "ddb963", "cda362"][j],
            )
        c.txt("배 수확", 388, 141, 54, "f6ead3", True)
        c.txt("첫 바구니가 찼다", 394, 216, 25, "b3c9c4")
    elif t < 6:
        c.rect(39, 76, 458, 259, "d4d2ae")
        for j in range(6):
            for k in range(5):
                x = 69 + j * 68 + k * 5
                y = 103 + k * 43
                c.circle(x, y, 14, "73865c")
                c.circle(x - 6, y - 3, 7, "8b9b68")
        c.line(
            progress(
                [(77, 302), (201, 302), (282, 236), (386, 234), (436, 154)], u * 0.54
            ),
            "b46637",
            5,
        )
        c.txt("수확 구역", 521, 117, 32, "f4e7cc", True)
        c.txt("남쪽 밭", 523, 170, 21, "e8b46b")
    else:
        for j in range(3):
            x = 100 + j * 211
            c.rect(x - 35, 230, 161, 70, "966a43")
            c.rect(x - 42, 237, 174, 12, "bd9061")
            for k in range(3):
                f = smooth((u - 0.18 * j - 0.17 * k) * 1.5)
                pear(c, x + k * 36, 216 - (1 - f) * 139, 0.68, "dfb667")
            c.line([(x - 32, 274), (x + 124, 274)], "704e37", 4)
        c.txt("세 상자 출발", 389, 86, 42, "f2ead4", True, center=True)
    c.poly([(0, 353), (768, 353), (768, 410), (0, 410)], "eae7d8")
    c.rect(0, 353, 14, 57, "d4914e")
    c.txt(
        ["오늘의 과수원", "운반 수레의 길", "선별을 마친 배"][int(t // 3)],
        33,
        368,
        24,
        "193c49",
        True,
    )
