"""Flow engraving, phosphor, rainy glass and four tabletop stories."""

from drawing import *


@lru_cache(None)
def streamlines():
    # Potential flow past a circular cylinder, integrated in nondimensional units.
    ps = []
    for y in np.linspace(-2.5, 2.5, 129):
        if abs(y) < 0.008:
            continue
        z = complex(-5, y)
        linepts = []
        for i in range(510):
            linepts.append((372 + 87 * z.real, 220 + 87 * z.imag))

            def vel(z):
                return (1 - 1 / z**2).conjugate()

            v = vel(z)
            z += 0.027 * vel(z + 0.0135 * v)
            if z.real > 5:
                break
        ps.append(np.array(linepts))
    return ps


def flow_field(t):
    im = ground("f3e9cb", "dfcfac", 2, 3).copy()
    for j, p in enumerate(streamlines()):
        path(im, p, "9aa798" if j % 4 else "728f88", 1)
        k = int((t * (21 + 9 * step(t, 2, 5)) + j * 17) % len(p))
        path(im, p[k : k + 12], "376663" if j % 3 else "947451")
    # Two dye beads enter one above the other and follow opposite flanks of the rock.
    traces = streamlines()
    for p, c, offset in [
        (traces[len(traces) // 2 - 6], "bb684a", 0),
        (traces[len(traces) // 2 + 5], "326f72", 0.08),
    ]:
        progress = 0.08 + 0.85 * step(t, offset, 9.4 + offset)
        k = int(progress * (len(p) - 1))
        path(im, p[max(0, k - 19) : k + 1], c, 3)
        dot(im, *p[k], 3, c)
    ell(im, 372, 220, 86, 86, "c5b58d")
    for r in range(21, 86, 8):
        pts0 = [
            (372 + (r + 2 * sin(5 * a)) * cos(a), 220 + (r + 2 * sin(5 * a)) * sin(a))
            for a in np.linspace(0, TAU, 150)
        ]
        path(im, pts0, "a99571")
    label(im, 372, 214, "여", 22, "76694f", "bold", "center")
    im = view(
        im,
        1 + 0.28 * step(t, 1, 4) - 0.19 * step(t, 6, 9),
        340 + 82 * step(t, 2, 7),
        216,
    )
    rr(im, 32, 31, 168, 54, 4, "eee1bd")
    label(im, 46, 46, "여를 도는 물살", 20, "3a554c", "bold")
    return im


def oscilloscope_math(t):
    im = ground("102018", "050c09", 0, light=True).copy()
    grid(im, 24, "1f4930", dots=True)
    line(im, (55, 214), (716, 214), "295739")
    line(im, (384, 68), (384, 360), "295739")
    layer = blank("000000")
    s = np.linspace(0, TAU, 1100)
    f = 1 + step(t, 2, 4) + step(t, 5.7, 7.5)
    g = 1 + step(t, 5.7, 7.5)
    angle = 0.55 + 0.6 * sin(t * 0.62)
    p = np.column_stack((384 + 221 * np.sin(f * s + angle), 212 + 117 * np.sin(g * s)))
    path(layer, p, "51db77", 2)
    k = int(t * 0.45 * len(s)) % len(s)
    path(layer, p[max(0, k - 50) : k + 1], "bcffc5", 3)
    dot(layer, *p[k], 4, "cfffd6")
    glow(im, layer, 0.8, 5)
    label(im, 42, 32, "두 진동의 자취", 22, "90c89c")
    label(im, 730, 34, f"{f:.2f}  /  {g:.2f}", 17, "9ddaa4", anchor="right")
    # The two orthogonal projection traces share the frequencies above.
    for j, freq in enumerate([f, g]):
        x = np.linspace(0, 124, 150)
        path(
            im,
            np.column_stack(
                (78 + j * 191 + x, 375 + 10 * np.sin(x / 124 * TAU * freq + t))
            ),
            "75b780",
        )
    return im


def rabbit(x, y, pose):
    if pose == 0:
        points = [
            (-30, 9),
            (-28, -5),
            (-21, -16),
            (-5, -19),
            (5, -12),
            (9, -26),
            (6, -49),
            (12, -52),
            (20, -33),
            (26, -40),
            (30, -38),
            (26, -20),
            (36, -8),
            (29, -2),
            (16, -3),
            (9, 10),
            (-9, 10),
            (-21, 14),
            (-34, 14),
            (-32, 10),
        ]
    elif pose == 1:
        points = [
            (-46, 8),
            (-26, -3),
            (-13, -17),
            (6, -14),
            (19, -18),
            (27, -33),
            (24, -49),
            (29, -52),
            (36, -36),
            (42, -40),
            (44, -37),
            (40, -24),
            (51, -15),
            (43, -10),
            (28, -10),
            (8, 2),
            (-2, 12),
            (-24, 12),
            (-38, 19),
            (-48, 18),
        ]
    else:
        points = [
            (-40, -4),
            (-25, -8),
            (-13, -21),
            (6, -21),
            (19, -17),
            (25, -29),
            (26, -43),
            (32, -42),
            (33, -28),
            (40, -33),
            (42, -30),
            (39, -18),
            (48, -9),
            (38, -5),
            (24, -7),
            (18, 8),
            (33, 14),
            (31, 18),
            (9, 12),
            (0, 2),
            (-16, 2),
            (-38, 3),
        ]
    return [(x + i, y + j) for i, j in points]


@lru_cache(None)
def alley():
    im = ground("1e2632", "080c16", 2, 4).copy()
    for row in range(14):
        y = 65 + row * 20
        line(im, (0, y), (768, y), "30323c")
        for x in range(-55 + (row % 2) * 42, 780, 85):
            line(im, (x, y), (x, y + 20), "30323c")
    for i, (x, y) in enumerate([(46, 132), (289, 102), (532, 142)]):
        rr(im, x, y, 188, 124, 13, "0c111c")
        for xx in [x + 10, x + 178]:
            for yy in [y + 9, y + 115]:
                dot(im, xx, yy, 2, "64616b")
    return im


def neon_tubes(t):
    im = alley().copy()
    layer = blank("000000")
    hot = ["ff634c", "41bcb9", "ff8eae"]
    beat = int(t * 2.5)
    act = [0, 0, 1, 1, 2, 2, 1, 0][beat % 8]
    for j, (x, y) in enumerate([(140, 206), (383, 177), (626, 217)]):
        p = rabbit(x, y, (beat + j) % 3 if act == j else j)
        path(im, p, "373b48", 5, True)
        if act == j or t > 7.75:
            path(layer, p, hot[j], 5, True)
            path(layer, p, "ffe4cf", 1, True)
            for k in range(2):
                line(
                    layer, (x - 62, y - 8 - k * 11), (x - 45, y - 8 - k * 11), hot[j], 2
                )
    glow(im, layer, 1.3, 9)
    floor = im[80:260][::-1].copy()
    floor = cv2.resize(floor, (768, 118))
    im[314:] = np.uint8(floor * 0.50)
    for j in range(26):
        x = (j * 91) % 768
        y = 325 + j * 41 % 103
        d = 5 + int((t * 10 + j * 7) % 25)
        arc(im, x, y, d, max(1, d * 0.11), 0, 180, "535461")
    for j in range(51):
        x = (j * 101 + int(t * 45)) % 790
        y = (j * 67 + int(t * 260)) % 432
        line(im, (x, y), (x - 2, y + 9), "38414b")
    return im


def toybrick(im, x, y, a, b, h, c, n, m):
    box(im, x, y, a, b, h, c)
    for i in range(n):
        for j in range(m):
            xx = x + (i + 0.5) * a / n - (j + 0.5) * b / m
            yy = y + ((i + 0.5) * a / n + (j + 0.5) * b / m) * 0.44
            ell(im, xx, yy, 6.4, 3.4, shade(c, 0.64))
            ell(im, xx, yy - 2.2, 6.3, 3.3, shade(c, 1.10))
            arc(im, xx, yy - 2.3, 5, 2, 174, 315, shade(c, 1.4))


def brick_toy(t):
    im = ground("ddc199", "aa7959", 2, 20).copy()
    for j in range(23):
        yy = 15 + j * 19
        path(
            im, [(x, yy + 5 * sin(x * 0.012 + j)) for x in range(-2, 780, 7)], "c5a17d"
        )
    # A wind-up duck assembles on the wooden workbench and rolls to its duckling.
    u = floor(t * 12) / 12
    x = 244 + 195 * step(u, 5.1, 8.9)
    y = 222
    ell(im, x + 19, y + 51, 76, 9, "9a795d")
    for k, (a, b, level, c, n, m) in enumerate(
        [
            (83, 42, 34, "dfaa3e", 4, 2),
            (61, 39, 55, "edc84f", 3, 2),
            (39, 36, 78, "f2cf55", 2, 2),
        ]
    ):
        drop = (1 - step(u, k * 0.62, k * 0.62 + 1.3)) * 125
        toybrick(im, x + (k * 6), y - level - drop, a, b, 20, c, n, m)
    box(im, x - 3, y - 1, 71, 30, 18, "ca933d")
    for dx in [-12, 43]:
        ell(im, x + dx, y + 31, 15, 19, "424143")
        ell(im, x + dx, y + 31, 7, 9, "a98d66")
        a = u * 4
        line(
            im,
            (x + dx, y + 31),
            (x + dx + 5 * cos(a), y + 31 + 7 * sin(a)),
            "e9d8b9",
            2,
        )
    headlift = 95 * (1 - step(u, 1.6, 3))
    toybrick(im, x + 40, y - 83 - headlift, 34, 34, 33, "efd253", 2, 2)
    dot(im, x + 64, y - 57 - headlift, 3, "2f3031")
    toybrick(im, x + 72, y - 52 - headlift, 21, 15, 7, "ec803e", 1, 1)
    toybrick(im, x - 40, y - 16, 22, 17, 13, "dbaf49", 1, 1)
    # Smaller duck waits beside a shallow tray of blue plates.
    for i in range(3):
        toybrick(im, 580 + i * 33, 274 + i * 14, 35, 49, 9, "699ea9", 2, 3)
    bx = 605 + 8 * sin(u * 3) * step(u, 6, 8)
    by = 235 - 9 * abs(sin(u * 5)) * step(u, 6, 8)
    toybrick(im, bx, by, 37, 24, 15, "eac04e", 2, 1)
    toybrick(im, bx + 19, by - 16, 19, 18, 16, "f1d35f", 1, 1)
    dot(im, bx + 32, by, 2, "383323")
    box(im, bx + 38, by - 1, 11, 7, 4, "ec853c")
    return view(
        im,
        1 + 0.12 * step(t, 0.2, 2) - 0.12 * step(t, 4, 6),
        360 + 25 * step(t, 4, 8),
        218,
    )


def paper_popup(t):
    im = ground("795746", "b18b63", 2, 9, True).copy()
    poly(
        im,
        [(96, 300), (417, 275), (696, 305), (658, 377), (361, 363), (97, 379)],
        "503e45",
    )
    poly(im, [(82, 281), (375, 263), (379, 350), (99, 369)], "f6e7bd", "c6a980", 2)
    poly(im, [(375, 263), (667, 278), (668, 364), (379, 350)], "eedeb3", "c6a980", 2)
    u = 0.23 + 0.77 * step(t, 0, 2.2)
    poly(
        im,
        [(91, 286), (91, 286 - 170 * u), (377, 263 - 184 * u), (377, 263)],
        "8abcc1",
        "f8edd1",
        4,
    )
    poly(
        im,
        [(377, 263), (377, 263 - 184 * u), (661, 281 - 163 * u), (661, 281)],
        "a4cbca",
        "fbf0d6",
        4,
    )
    for i in range(8):
        x = 117 + i * 72
        base = 289 + 6 * sin(i)
        h = (55 + (i * 37) % 83) * step(t, 0.35 + i * 0.13, 2.55 + i * 0.12)
        p = [
            (x, base),
            (x - 13, base - h * 0.39),
            (x - 4, base - h * 0.60),
            (x - 9, base - h),
            (x + 6, base - h * 0.82),
            (x + 7, base - h * 0.47),
            (x + 18, base - h * 0.61),
            (x + 12, base - h * 0.27),
            (x + 10, base),
        ]
        poly(im, p, "4d9285" if i % 2 else "659c89", "fff0cc", 3)
        line(im, (x + 1, base), (x + 2, base - h * 0.65), "457b73")
    # Author-drawn seahorse silhouette with a pleated belly, white cut edge and spiral tail.
    xx = lerp(187, 526, step(t, 2.3, 8.2))
    yy = 218 - 17 * sin(t * 1.6)
    points = [
        (-10, -38),
        (-22, -47),
        (-13, -52),
        (-16, -61),
        (-2, -56),
        (10, -60),
        (25, -51),
        (24, -41),
        (45, -36),
        (44, -28),
        (25, -29),
        (12, -24),
        (18, -8),
        (10, 9),
        (-3, 19),
        (-15, 23),
        (-18, 34),
        (-10, 39),
        (1, 34),
        (4, 26),
        (9, 28),
        (7, 40),
        (-3, 49),
        (-18, 50),
        (-30, 40),
        (-31, 25),
        (-20, 8),
        (-11, -5),
        (-16, -23),
        (-30, -14),
        (-30, -30),
    ]
    poly(im, [(xx + x, yy + y) for x, y in points], "dc845e", "fff4d5", 4)
    for k in range(5):
        line(im, (xx - 9, yy - 14 + k * 6), (xx + 8 - k, yy - 13 + k * 6), "ae684f")
    dot(im, xx + 13, yy - 45, 3, "493f39")
    for i in range(6):
        xx2 = 601 + 13 * sin(i + t)
        yy2 = 270 - (i * 25 + t * 21) % 143
        ell(im, xx2, yy2, 3 + i % 4, 3 + i % 4, "e4f2d9", 1)
    return view(
        im,
        1 + 0.12 * step(t, 2, 4) - 0.12 * step(t, 7.8, 10),
        383 + 20 * sin(0.5 * t),
        216,
    )


@lru_cache(None)
def harbour():
    im = ground("74acac", "6f9b92", 2, 32).copy()
    for i in range(400):
        x = (i * 137) % 768
        y = (i * 61) % 432
        line(im, (x, y), (x + 4 + i % 13, y), "97bbb3")
    poly(
        im,
        [
            (-80, -25),
            (433, -25),
            (409, 48),
            (355, 95),
            (355, 264),
            (300, 298),
            (-30, 246),
        ],
        "d9c59c",
    )
    poly(im, [(-40, 27), (320, 97), (319, 110), (-40, 43)], "93978c")
    for j in range(10):
        x = -48 + j * 42
        y = 24 + (j % 3) * 17
        box(im, x, y, 32, 22, 18, "d6cab1")
        box(im, x, y - 3, 32, 22, 6, "a76751")
    box(im, 179, 125, 126, 48, 12, "f3d9a5")
    box(im, 171, 93, 104, 40, 34, "e1ba86")
    box(im, 171, 87, 108, 43, 8, "739991")
    for k in range(4):
        rect(im, 148 + k * 19, 133 + k * 8, 9, 13, "536f72")
    for i in range(4):
        box(im, 325, 142 + i * 43, 92, 9, 5, "ae916f")
    return im


def tilt_shift(t):
    u = floor(t * 10) / 10
    im = harbour().copy()
    for j in range(4):
        p = step(u, j * 0.2, 4.8 + j * 0.3)
        x = 262 + 29 * j + 65 * p
        y = 213 + 11 * j - 29 * p
        dot(im, x + 2, y + 3, 3, "837e6e")
        rect(im, x, y - 3, 3, 7, ["b35e47", "536f80", "bd9152", "55765b"][j])
        dot(im, x + 1, y - 5, 2, "e8c596")
    for j in [1, 0]:
        k = step(u, 0.3, 4.3) if j == 0 else step(u, 4.6, 9.6)
        x = lerp(677, 424, k) if j == 0 else lerp(423, 644, k)
        y = lerp(80, 171, k) if j == 0 else lerp(257, 340, k)
        side = -1 if j == 0 else 1
        for i in range(6):
            path(
                im,
                [
                    (x - side * (34 + i * 7), y - 11 - i * 2),
                    (x - side * (44 + i * 7), y),
                    (x - side * (34 + i * 7), y + 10 + i * 2),
                ],
                "b0d5c7",
            )
        hull = [(-39, -12), (25, -13), (46, 0), (25, 13), (-37, 13), (-43, 1)]
        poly(im, [(x + side * a, y + b) for a, b in hull], "ede5cc", "5b7d77", 2)
        rr(im, x - 22, y - 8, 42, 15, 3, "b46d50" if not j else "6b8c95")
        for i in range(4):
            rect(im, x - 17 + i * 9, y - 5, 5, 5, "dedcca")
    blur = cv2.GaussianBlur(im, (0, 0), 5)
    m = np.clip((abs(Y - (197 + 18 * sin(t * 0.45))) - 50) / 110, 0, 1)[:, :, None]
    return np.uint8(im * (1 - m) + blur * m)


def lowpoly_island(t):
    im = ground("d2d9ed", "f9dcc4").copy()
    cx, cy = 376, 189
    cells = sorted(
        [(a, b) for a in range(-2, 3) for b in range(-2, 3) if abs(a + b) <= 2],
        key=lambda v: v[1] + v[0] * 0.5,
    )
    for j, (a, b) in enumerate(cells):
        x = cx + 52 * a
        y = cy + 31 * (b + a * 0.5)
        u = step(t, abs(a + b) * 0.13, 1.6 + abs(a) * 0.24)
        y += 63 * (1 - u)
        if u < 0.03:
            continue
        h = 28 + (j * 13) % 34
        top = [(x + 33 * cos(i * pi / 3), y + 18 * sin(i * pi / 3)) for i in range(6)]
        for i in range(3):
            p, q = top[i], top[i + 1]
            poly(
                im,
                [p, q, (q[0], q[1] + h), (p[0], p[1] + h)],
                ["b58a83", "aa7e76", "c7967c"][i],
            )
        poly(im, top, ["b5c2a0", "a7bca2", "cfccab", "c4c9a9"][j % 4])
        if j in [1, 3, 5, 7, 10, 14, 17]:
            g = step(t, 1.8 + j * 0.12, 3 + j * 0.13)
            if g:
                hh = (31 + j % 4 * 5) * g
                line(im, (x, y), (x, y - hh * 0.47), "796e61", 3)
                for off, k, c in [
                    (-7, 0.78, "839b88"),
                    (6, 0.80, "9caf8f"),
                    (0, 1.1, "a4ba97"),
                ]:
                    p = [
                        (x + off - 12 * g, y - hh * 0.43),
                        (x + off, y - hh * k),
                        (x + off + 13 * g, y - hh * 0.43),
                        (x + off, y - hh * 0.32),
                    ]
                    poly(im, p, c)
                    poly(im, [p[1], p[2], p[3]], shade(c, 0.87))
        if (a, b) == (0, 0):
            g = step(t, 4.6, 6.4)
            wind = (t - 4) * 2.4
            if g:
                poly(
                    im,
                    [
                        (x - 14, y),
                        (x - 8, y - 55 * g),
                        (x + 8, y - 55 * g),
                        (x + 14, y),
                    ],
                    "f6dfb6",
                )
                for k in range(4):
                    ang = wind + k * pi / 2
                    ax, ay = x, y - 53 * g
                    p = [
                        (ax, ay),
                        (ax + 27 * g * cos(ang), ay + 27 * g * sin(ang)),
                        (
                            ax + 27 * g * cos(ang) - 7 * sin(ang),
                            ay + 27 * g * sin(ang) + 7 * cos(ang),
                        ),
                    ]
                    poly(im, p, "b97766")
    for k in range(5):
        x = 540 + k * 19 + 12 * sin(t * 0.7)
        y = 106 + 8 * sin(k + t)
        path(im, [(x - 5, y - 3), (x, y), (x + 5, y - 3)], "aa9fa7")
    return view(im, 1.21 + 0.06 * sin(t * 0.47), 380, 205)


def glass_product(t):
    im = ground("19212a", "05070a", 0, light=True).copy()
    # Radial profile is revolved about the vertical axis; refraction bands follow the silhouette.
    u = step(t, 1.9, 4.4) * (1 - step(t, 6.1, 8.8))
    cx = 384 + 15 * sin(t * 0.46)
    y0 = 209
    lay = blank("000000")
    ell(im, cx + 6, 353, 129, 12, "182128")
    ell(im, cx + 8, 350, 79, 4, "304048")
    for sign in (-1, 1):
        off = sign * 32 * u
        for k in range(111):
            h = k / 110
            r = 4 + 78 * (sin(h * pi * 0.53) ** 1.32)
            y = y0 + sign * k + off
            line(
                im,
                (cx - r, y),
                (cx + r, y),
                mix("17252c", "34434a", 0.24 * sin(h * 8 + t * 0.7) + 0.25),
            )
            for f, c, w in [
                (-1, "aec4cd", 2),
                (-0.95, "7095aa", 2),
                (-0.77, "689197", 1),
                (0.94, "d4dbd2", 2),
                (1, "6a87ab", 1),
            ]:
                dx = 3 * sin(h * 5 + t * 0.5) if abs(f) < 0.9 else 0
                line(
                    lay,
                    (cx + r * f + dx, y),
                    (cx + r * f + dx, y + 1),
                    shade(c, 0.48 + 0.41 * h),
                    w,
                )
        yy = y0 + sign * 111 + off
        ell(im, cx, yy, 82, 10, "343f49")
        ell(lay, cx, yy, 82, 10, "adb9bc", 1)
        arc(lay, cx, yy, 77, 7, 5, 160, "c1d6cf", 2)
    fill = step(t, 0.5, 9.4)
    for k in range(420):
        q = (k * 0.61803399) % 1
        r = ((k * 0.41421356) % 1) ** 0.5
        if k / 420 > fill:
            yy = 173 - 25 * r - 32 * u
            xx = cx + (q - 0.5) * r * 57
        else:
            yy = 311 - 19 * (1 - r) - 4 * sin(r * pi) + 32 * u
            xx = cx + (q - 0.5) * r * (72 + 46 * fill)
        dot(im, xx, yy, 1, "d7ae77")
    for k in range(23):
        y = 181 + (k * 8 + t * 105) % 127
        dot(im, cx + sin(k * 12 + t) * 1.5, y, 1, "d9b97e")
    glow(im, lay, 0.72, 5)
    return view(im, 1 + 0.19 * step(t, 0.6, 2.6) * (1 - step(t, 5, 7)), cx, 210)
