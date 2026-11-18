"""A municipal pool, a bakery, a crayon garden and five observational films."""

import json
from drawing import *


def swimmer(im, x, y, phase):
    ell(im, x, y + 2, 11, 4, "f0b396")
    dot(im, x + 7, y - 3, 5, "373456")
    path(
        im,
        [(x - 6, y), (x - 14, y - 5 - 4 * cos(phase)), (x - 22, y + 3 * sin(phase))],
        "955e71",
        3,
    )
    path(
        im,
        [(x + 4, y), (x + 11, y - 10 + 3 * sin(phase)), (x + 19, y - 7)],
        "ffceb3",
        3,
    )


def memphis_diorama(t):
    im = ground("f6d5a7", "f7c9a2", 2, 41).copy()
    ink = "39344c"
    purple = "7d6991"
    for i in range(160):
        x = (i * 103) % 769
        y = (i * 89) % 433
        if i % 3:
            line(im, (x, y), (x + 3, y - 3), "e8a89d", 2)
        else:
            dot(im, x, y, 2, "93778e")
    hull = [(160, 166), (451, 106), (647, 239), (343, 328)]
    poly(im, np.array(hull) + [12, 12], purple)
    poly(im, hull, "fff1d4", ink, 2)
    basin = [(180, 169), (450, 121), (620, 234), (345, 310)]
    poly(im, basin, "73c9bf", ink, 2)
    for j in range(3):
        path(
            im,
            [(204 + j * 37, 192 + j * 27), (479 + j * 39, 140 + j * 27)],
            "f5e5a3",
            3,
        )
    for k in range(3):
        x = 226 + k * 43 + (155 + 20 * k) * (0.5 + 0.5 * sin(t * 0.58 + k))
        y = 194 + k * 27 - (x - 226 - k * 43) * 0.18
        swimmer(im, x, y, t * 3 + k)
        for i in range(2):
            arc(im, x - 18 - i * 9, y + 4, 7, 3, 100, 280, "e1f1ce", 2)
    # A diver waits on a white springboard, arcs into the water, then leaves three widening rings.
    board = [(152, 178), (166, 174), (201, 192), (189, 196)]
    poly(im, np.array(board) + [3, 4], purple)
    poly(im, board, "f8e7b7", ink)
    dive = step(t, 2.4, 4.1)
    dx = 188 + 55 * dive
    dy = 185 + 21 * dive - 42 * sin(pi * dive)
    if t < 4:
        dot(im, dx, dy - 13, 4, "745069")
        line(im, (dx, dy - 9), (dx + 4 * dive, dy), "d77b6e", 4)
        path(
            im,
            [(dx - 2, dy - 1), (dx - 5 - 7 * dive, dy + 4), (dx - 7, dy + 8)],
            ink,
            2,
        )
        line(im, (dx, dy - 7), (dx + 5 + 11 * dive, dy - 9), "a66b61", 2)
    if 3.9 < t < 6.2:
        for k in range(3):
            r = 2 + (t - 3.9) * 12 - k * 4
            if r > 1:
                ell(im, 243, 206, r, r * 0.35, "fff0c6", 1)
    for j, (x, y) in enumerate([(176, 282), (491, 93), (577, 130)]):
        ell(im, x + 12, y + 4, 29, 8, purple)
        line(im, (x, y), (x, y - 43), ink, 3)
        for k in range(8):
            a = TAU * k / 8 + 0.08 * t
            b = a + TAU / 8
            poly(
                im,
                [
                    (x, y - 49),
                    (x + 33 * cos(a), y - 43 + 14 * sin(a)),
                    (x + 33 * cos(b), y - 43 + 14 * sin(b)),
                ],
                ("ec727b", "fae5b6")[k % 2],
                ink,
            )
    for j in range(3):
        x = 243 + j * 48
        y = 118 - j * 9
        box(im, x, y, 22, 15, 16, ["b799c4", "ed8e7f", "e5af59"][j], ink)
        for k in range(3):
            line(im, (x + 1 + k * 4, y + 4 + k), (x + 6 + k * 4, y + 6 + k), ink)
    # Organic cut-paper window, on its own unprinted sheet.
    a = np.linspace(0, TAU, 290)
    g = 0.56 + 0.44 * step(t, 0, 1.45)
    r = 1 + 0.038 * np.sin(5 * a + 0.25) + 0.035 * np.cos(7 * a)
    cut = np.column_stack(
        (384 + 338 * g * r * np.cos(a), 217 + 179 * g * r * np.sin(a))
    )
    m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [pts(cut)], 255, AA)
    paper = ground("fff9eb", "fcf3df", 1, 17)
    im = np.where(m[:, :, None] > 0, im, paper)
    return im


def baker(im, x, y, shirt, t, scale=1, apron=False):
    s = scale
    leg = sin(t) * 3 * s
    ell(im, x + 3 * s, y, 8 * s, 2 * s, "b5ab97")
    for side in (-1, 1):
        xx = x + side * 2.7 * s
        line(
            im,
            (xx, y - 11 * s),
            (xx + side * leg, y - 1 * s),
            "54554d",
            max(1, round(2 * s)),
        )
        line(
            im,
            (xx + side * leg, y - 1 * s),
            (xx + side * leg + 2 * s, y - 1 * s),
            "47453f",
            max(1, round(2 * s)),
        )
    poly(
        im,
        [
            (x - 4 * s, y - 24 * s),
            (x + 4 * s, y - 25 * s),
            (x + 6 * s, y - 11 * s),
            (x - 5 * s, y - 10 * s),
        ],
        shirt,
        "5d5349",
    )
    if apron:
        rect(im, x - 3 * s, y - 21 * s, 7 * s, 10 * s, "eee4ce")
    dot(im, x, y - 29 * s, 4.8 * s, "d8a783")
    arc(im, x, y - 30 * s, 5 * s, 4 * s, 170, 340, "51463e", max(1, round(2 * s)))
    line(
        im,
        (x + 4 * s, y - 22 * s),
        (x + 8 * s, y - 17 * s + leg),
        "776557",
        max(1, round(s * 2)),
    )


def iso_counter(im, x, y, n=8):
    ink = "796b58"
    box(im, x, y, 102, 59, 42, "d8b785", ink)
    for j in range(n):
        a = x + (j % 4) * 22 - (j // 4) * 21 - 6
        b = y + ((j % 4) * 22 + (j // 4) * 21) * 0.44 + 10
        ell(im, a, b, 11, 5, "bb824b", rot=24)
        for k in range(3):
            line(im, (a - 5 + k * 4, b - 3 + k * 0.5), (a - 6 + k * 4, b), "edd3a1")


def isometric_picture_book(t):
    im = ground("f2e9d6", "e8ddc3", 1, 19).copy()
    # A bakery at a single continuous scale; floor diamonds meet across the full sheet.
    for i in range(-20, 22):
        line(im, (i * 64, -15), (i * 64 + 774, 432), "d4cbb6")
        line(im, (i * 64, -15), (i * 64 - 774, 432), "d4cbb6")
    for j in range(4):
        x = 95 + j * 162
        y = 16 + (j % 2) * 9
        box(im, x, y, 96, 52, 37, "c5b99e", "897e69")
        for k in range(4):
            ell(im, x - 10 + k * 19, y + 20 + k * 7, 8, 4, "b3835e", rot=23)
    iso_counter(im, 282, 115)
    iso_counter(im, 493, 111)
    q = step(t, 0.7, 5.3)
    x = 140 + 225 * q
    y = 192 + 57 * q
    crew = [
        (
            389 + j * 44 + 20 * step(t, 6.1 + j * 0.3, 8.4 + j * 0.3),
            241 + j * 16,
            ["809b8b", "b57f70", "75929a", "ba9c6a"][j],
            j * 1.8,
            1.1,
            False,
        )
        for j in range(4)
    ]
    crew += [
        (x - 18, y + 2, "7f9e90", t * 7, 1.25, True),
        (198, 145, "b38671", t * 2, 1.05, True),
        (563, 152, "81a4a0", t * 2, 1.08, True),
    ]
    for xx, yy, c, a, s, ap in sorted(crew, key=lambda p: p[1]):
        baker(im, xx, yy, c, a, s, ap)
    for dx in [0, 32]:
        ell(im, x + dx, y + 13, 5, 6, "665f56")
    box(im, x + 8, y - 19, 41, 23, 24, "c49d70", "786650")
    for j in range(3):
        ell(im, x + 6 + j * 10, y - 11 + j * 3, 8, 4, "c18b55", rot=25)
    if t > 5.4:
        u = step(t, 5.4, 7.5)
        ell(
            im,
            lerp(x + 20, 396, u),
            lerp(y - 14, 220, u) - 18 * sin(pi * u),
            10,
            4,
            "c18b55",
            rot=18,
        )
    return view(im, 1.16, 333 + 69 * step(t, 1, 7), 200 + 14 * sin(t * 0.45))


@lru_cache(None)
def tooth():
    return np.random.default_rng(772).random((H, W)).astype(np.float32)


def crayon_world(t):
    tick = floor(t * 12)
    u = tick / 12
    im = ground("f5e8c3", "f6e8ce", 2, 111).copy()
    horizon = 207 + 5 * sin(u * 0.8)
    vanish = 373 + 29 * sin(u * 0.49)

    def proj(x, z, h=0):
        return (vanish + 430 * x / z, horizon + (140 - 385 * h) / z)

    def wax(p, c, thick=3, closed=False):
        arr = np.asarray(p, float)
        rough = arr.copy()
        for j in range(len(arr)):
            rough[j] += [1.5 * sin(tick * 1.7 + j * 9), 1.3 * cos(tick + j * 4)]
        path(im, rough, c, thick, closed)

    # Road vanishes between two rows of sunflowers. Each stalk is a fixed point in garden space.
    for side in (-1, 1):
        wax([proj(side * 1.24, z) for z in np.linspace(0.5, 24, 70)], "b69568", 4)
    for j in range(38):
        z = 0.56 + ((j * 0.81 - u * 0.88) % 29)
        x = -1.12 + (j * 1.037) % 2.2
        a, b = proj(x, z)
        wax([(a, b), (a + 12 / z, b - 2 / z)], "c9ad77", max(1, min(5, round(4 / z))))
    sun = (609, 79)
    ell(im, *sun, 38, 36, "e6bb59")
    wax(
        [
            (sun[0] + (39 + 2 * sin(a * 5)) * cos(a), sun[1] + 37 * sin(a))
            for a in np.linspace(0, TAU, 44)
        ],
        "d8a343",
        4,
        True,
    )
    for k in range(13):
        a = k * TAU / 13
        wax(
            [
                (609 + 49 * cos(a), 79 + 48 * sin(a)),
                (609 + 59 * cos(a + 0.03), 79 + 59 * sin(a + 0.03)),
            ],
            "cc9948",
            3,
        )
    # Pencil-hatched rolling hills; a fence passes behind each row of flower heads.
    for k in range(3):
        ridge = [
            (i, 183 + k * 8 + 13 * sin(i * 0.009 + k * 1.3 + u * 0.04))
            for i in range(-5, 782, 9)
        ]
        wax(ridge, ["a1b6a2", "93a88f", "96a982"][k], 2)
    for side in (-1, 1):
        fence = []
        for j in range(19, 0, -1):
            z = (j * 1.3 - u * 0.9) % 23 + 0.9
            x = side * 2.18
            base = proj(x, z)
            cap = proj(x, z, 0.49)
            wax([base, cap], "ad8969", max(1, int(3 / z + 1)))
            fence.append((z, proj(x, z, 0.32)))
        wax([p for _, p in sorted(fence, reverse=True)], "c29a73", 2)
    for j in sorted(range(36), key=lambda k: -((2 + k * 1.07 - u * 0.90) % 20 + 0.64)):
        z = (2 + j * 1.07 - u * 0.90) % 20 + 0.64
        side = 1 if j % 2 else -1
        x = side * (1.58 + 0.62 * abs(sin(j * 2)))
        ht = 1.05 + 0.33 * sin(j * 5)
        a, b = proj(x, z)
        c, d = proj(x + 0.05 * sin(u * 2 + j), z, ht)
        r = min(55, 65 / z)
        if a < -90 or a > 858:
            continue
        wax(
            [(a, b), ((a + c) / 2 + 3, (b + d) / 2), (c, d)],
            "71845a",
            max(1, int(r * 0.15)),
        )
        for k in [-1, 1]:
            e = (a + (c - a) * 0.6, (b + d) * 0.5)
            ell(
                im, e[0] + r * 0.33 * k, e[1], r * 0.75, r * 0.23, "91a66a", rot=-32 * k
            )
        for k in range(8):
            ang = k * pi / 4 + 0.12 * sin(u + j)
            ell(
                im,
                c + r * 0.65 * cos(ang),
                d + r * 0.64 * sin(ang),
                r * 0.49,
                r * 0.24,
                "e1aa48" if j % 3 else "db9476",
                rot=ang * 180 / pi,
            )
        dot(im, c, d, r * 0.39, "89654d")
        for k in range(8):
            ang = k * 2.4
            dot(
                im,
                c + cos(ang) * r * 0.20,
                d + sin(ang) * r * 0.22,
                max(1, r * 0.038),
                "c3a05f",
            )
    xx = 220 + 148 * step(u, 1, 7)
    yy = 96 - 25 * sin(u * 0.65)
    p = [(xx, yy - 23), (xx + 24, yy), (xx - 1, yy + 31), (xx - 22, yy + 2)]
    poly(im, p, "c96867")
    poly(im, [p[0], p[1], p[2]], "dca461")
    wax(p, "755b68", 3, True)
    wax(
        [(xx, yy + 31), (xx - 4, yy + 42), (xx - 20, yy + 47), (xx - 28, yy + 63)],
        "7f7990",
        2,
    )
    # Wax skips over the stationary tooth of the paper, including the hand-hatched sky.
    for j in range(23):
        x = (j * 97) % 767
        y = 27 + (j * 43) % 125
        wax([(x, y), (x + 23 + 0.3 * j, y - 5), (x + 40, y - 8)], "b3c9c0", 2)
    m = tooth()
    im[m > 0.82] = (
        (im[m > 0.82].astype(float) * 0.42) + np.array([246, 233, 206]) * 0.58
    ).astype(np.uint8)
    return im


@lru_cache(None)
def source(n):
    return plate(n)


def satellite_briefing(t):
    src = source("world.jpg")
    h, w = src.shape[:2]
    # The NASA Blue Marble plate is equirectangular. All marks use the same projection.
    fac = (
        0.55
        + 0.79 * step(t, 0.3, 4.4)
        + 0.69 * step(t, 4.9, 7.25)
        - 0.14 * step(t, 8.6, 10)
    )
    lon = lerp(33, 46.9, step(t, 0, 5))
    lat = lerp(-7, -19.15, step(t, 0, 5))

    def geo(lo, la):
        return (384 + (lo - lon) * w / 360 * fac, 222 - (la - lat) * h / 180 * fac)

    cx = (lon + 180) * w / 360
    cy = (90 - lat) * h / 180
    m = np.float32([[fac, 0, 384 - cx * fac], [0, fac, 222 - cy * fac]])
    im = cv2.warpAffine(src, m, (W, H), flags=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    im = cv2.addWeighted(im, 0.22, cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB), 0.78, 0)
    a, b = geo(43.1, -11.8)
    c, d = geo(50.7, -25.8)
    bracket(im, a - 6, b - 5, c - a + 12, d - b + 10, "e6e8dc", 10)
    if t > 3:
        for lo, la, desc in [(49.25, -12, "남위 12°"), (45.18, -25.6, "남위 25.6°")]:
            x, y = geo(lo, la)
            q = step(t, 3 + (la < -20) * 1.5, 4.5 + (la < -20) * 1.5)
            reveal(im, [(x, y), (x + 27, y - 12), (x + 106, y - 12)], q, "f2deb2", 1)
            if q > 0.8:
                label(im, x + 36, y - 32, desc, 15, "f1e1c2", "bold")
    rect(im, 0, 0, 768, 50, "172022")
    label(im, 24, 15, "인도양의 마다가스카르", 20, "eeeae2", "bold")
    label(im, 742, 17, "2004년 5월", 15, "d0d3c8", anchor="right")
    for i in range(18):
        line(im, (32 + 40 * i, 414), (32 + 40 * i, 410 - (i % 3 == 0) * 5), "aeb7b0")
    return im


def briefing_board(t):
    im = ground("faf8eb", "d1d5c8", 1, 21, True).copy()
    rect(im, 0, 0, 768, 9, "85928a")
    rect(im, 0, 413, 768, 19, "84928b")
    rect(im, 0, 415, 768, 3, "bdc4ba")
    for i in range(8):
        path(im, [(55 + i * 78, 42), (99 + i * 78, 54), (89 + i * 78, 65)], "e8eadd")
    label(im, 56, 39, "벽돌 사이의 흰 선", 26, "344b46", "bold")
    photo = cv2.rotate(source("brick.png"), cv2.ROTATE_90_CLOCKWISE)
    y = lerp(153, 111, step(t, 0, 0.85))
    rect(im, 55, y + 6, 335, 232, "bec2b3")
    rect(im, 49, y, 335, 232, "fffbed")
    patch(im, photo, 58, y + 9, 317, 213)
    dot(im, 211, y + 1, 8, "a25749")
    dot(im, 209, y - 1, 3, "d39975")
    # Draw the horizontal and staggered vertical mortar joints from the photographic study.
    reveal(im, [(102, 213), (201, 213), (278, 213)], step(t, 1.2, 3), "edb25c", 3)
    reveal(
        im,
        [(280, 213), (387, 213), (427, 166), (479, 166)],
        step(t, 2.5, 4.3),
        "8a544e",
        3,
    )
    for j in range(3):
        y2 = 161 + j * 36
        reveal(
            im,
            [(468, y2), (693, y2 + 1)],
            step(t, 3.5 + j * 0.4, 4.6 + j * 0.4),
            "475e64",
            3,
        )
        for k in range(2):
            x = 493 + k * 94 + 43 * (j % 2)
            reveal(
                im,
                [(x, y2), (x + 1, y2 + 34)],
                step(t, 4.8 + j * 0.28, 5.8 + j * 0.3),
                "475e64",
                3,
            )
    if t > 5.5:
        label(im, 469, 299, "엇갈린 세로줄눈", 20, "46685c", "bold")
        reveal(im, [(476, 335), (562, 333), (646, 334)], step(t, 5.8, 7.3), "ac6458", 3)
    rect(im, 566, 401, 72, 9, "587d71")
    rect(im, 646, 401, 54, 9, "ae6f5b")
    pan = step(t, 0.8, 2.2) * (1 - step(t, 5.6, 8))
    return view(im, 1 + 0.12 * pan, 384 - 20 * sin(t * 0.52) * pan, 216)


@lru_cache(None)
def section():
    return json.loads((PLATES / "section.json").read_text())


def lidar_survey(t):
    data = section()
    p = np.array(data["pts"])
    px, pz = p.T
    im = ground("101b20", "070e12", 0, light=True).copy()
    label(im, 43, 36, "지표를 가른 단면", 23, "d4e1d8", "bold")
    label(im, 725, 40, "애슈퍼드  /  2016", 15, "8bada7", anchor="right")
    # The deposited sample is a two-dimensional section; never fabricate a third coordinate.
    baseline = 310
    gain = 159 + 13 * step(t, 2, 6)
    xx = 384 + px * 43
    yy = baseline - pz * gain
    for j in range(5):
        y = baseline - j * 0.25 * gain
        line(im, (105, y), (692, y), "203139")
        label(im, 87, y - 5, f"{j * 0.25:.2f}", 12, "7a9695", anchor="right")
    front = lerp(70, 705, step(t, 0.2, 4.3))
    for x, y, z in zip(xx, yy, pz):
        if x <= front:
            dot(im, x, y, 1.3, mix("669c9f", "ead494", sat(z)))
    if t < 4.5:
        line(im, (front, 117), (front, 348), "b4ebe0", 2)
    median = np.column_stack(
        (384 + 43 * np.array(data["bins"]), baseline - gain * np.array(data["median"]))
    )
    if t > 4:
        reveal(im, median, step(t, 4, 6.65), "efcc86", 3)
    if t > 6.2:
        x, y = median[np.argmax(data["median"])]
        reveal(
            im,
            [(x, y), (x + 57, y - 54), (x + 167, y - 54)],
            step(t, 6.2, 7.6),
            "bec9bb",
        )
        label(im, x + 74, y - 81, "0.56 m", 24, "f1d295", "bold")
    label(im, 93, 365, "지면 기준 높이 (m)", 15, "93b4ad")
    return im


def microscope(t):
    src = source("cell.png")
    h, w = src.shape[:2]
    z = 0.43 + 1.23 * step(t, 0.65, 5.4) + 0.87 * step(t, 5.8, 8.25)
    cx = lerp(w / 2, 425, step(t, 0.85, 5.1))
    cy = lerp(h / 2, 374, step(t, 1, 5.1))
    m = np.float32([[z, 0, 383 - z * cx], [0, z, 215 - z * cy]])
    im = ground("2f383a", "131919", 0, light=True).copy()
    x = 383 - z * cx
    y = 215 - z * cy
    rect(im, x - 12, y - 10, w * z + 24, h * z + 20, "c0c7bd")
    warped = cv2.warpAffine(src, m, (W, H))
    mask = cv2.warpAffine(np.full((h, w), 255, np.uint8), m, (W, H))
    im[mask > 0] = warped[mask > 0]
    blur = 2.1 * np.exp(-(((t - 2.35) / 0.42) ** 2)) + 1.8 * np.exp(
        -(((t - 6.4) / 0.36) ** 2)
    )
    if blur > 0.12:
        im = cv2.GaussianBlur(im, (0, 0), blur)
    rect(im, 0, 0, 768, 47, "20292a")
    label(im, 22, 14, "식염수 속 세포", 20, "e9e9dd", "bold")
    label(im, 745, 16, "정량 위상 영상", 14, "c4cbbf", anchor="right")
    size = 10 if z < 1.5 else 5
    length = size * z / 0.107
    right = min(704, x + w * z - 16) if z > 1.5 else 704
    line(im, (right - length, 375), (right, 375), "f4edce", 3)
    label(im, right, 387, f"{size} μm", 15, "f4edce", anchor="right")
    return im


def archive_lighttable(t):
    src = source("coins.png")
    im = ground("e3eeeb", "b6c6c4", 1, 33, True).copy()
    # Original photographic plate mounted with translucent tabs on a gridded light box.
    for i in range(12):
        line(im, (i * 70, 19), (i * 70, 405), "c0cecb")
    for i in range(6):
        line(im, (15, i * 73), (755, i * 73), "c3d2cc")
    x, y, w, h = 102, 63, 423, 334
    rect(im, x + 7, y + 8, w, h, "a2b1aa")
    rect(im, x - 7, y - 7, w + 14, h + 14, "f4f1de")
    patch(im, src, x, y, w, h)
    for a in [x - 10, x + w - 12]:
        poly(
            im,
            [(a, y - 11), (a + 24, y - 11), (a + 15, y + 13), (a - 9, y + 13)],
            "c7cbbb",
        )
    label(im, 552, 84, "폼페이 출토 동전", 21, "414d49", "bold")
    label(im, 552, 123, "소장 사진 51611", 15, "5e6d67")
    u = step(t, 0.75, 4.5)
    v = step(t, 5.65, 8.2)
    target = (x + w * (0.49 + 0.36 * v), y + h * (0.63 - 0.44 * v))
    lx = lerp(639, target[0], u)
    ly = lerp(309, target[1], u)
    under = im.copy()
    line(im, (lx + 43, ly + 48), (lx + 91, ly + 100), "555f5b", 15)
    ell(im, lx + 3, ly + 5, 66, 66, "79867e")
    gy, gx = np.mgrid[:H, :W].astype(np.float32)
    mask = (gx - lx) ** 2 + (gy - ly) ** 2 < 61**2
    # Reproject the original archival plate directly at the loupe magnification.
    sx = (lx - x) / w * src.shape[1] + (gx - lx) / 2.05
    sy = (ly - y) / h * src.shape[0] + (gy - ly) / 2.05
    mag = cv2.remap(
        src,
        sx.astype("f"),
        sy.astype("f"),
        cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )
    worldx = lx + (gx - lx) * 0.5
    worldy = ly + (gy - ly) * 0.5
    table = cv2.remap(
        under,
        worldx.astype("f"),
        worldy.astype("f"),
        cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE,
    )
    inset = (sx >= 0) & (sy >= 0) & (sx < src.shape[1] - 1) & (sy < src.shape[0] - 1)
    im[mask] = table[mask]
    im[mask & inset] = mag[mask & inset]
    ell(im, lx, ly, 64, 64, "4e5955", 5)
    arc(im, lx, ly, 62, 62, 195, 283, "eef1dd", 3)
    return im
