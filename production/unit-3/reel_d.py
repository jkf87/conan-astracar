"""Material studies, evidence drawn to scale, terrain and a deterministic café simulation."""

import json
from drawing import *


def security_xray(t):
    # A museum material study of a music box. Each channel sums positive path lengths.
    cx = lerp(610, 374, step(t, 0, 3.3)) + 22 * step(t, 7.6, 9.9)
    cy = 223
    dx = X - cx
    dy = Y - cy
    wood = np.zeros_like(X)
    metal = np.zeros_like(X)
    for w, h in [(165, 91), (153, 78)]:
        a = np.maximum(abs(dx) - w + 14, 0)
        b = np.maximum(abs(dy) - h + 14, 0)
        d = np.sqrt(a * a + b * b)
        wood += (
            np.exp(-(((d - 14) / 4.4) ** 2)) * 0.66
            + ((abs(dx) < w) & (abs(dy) < h)) * 0.12
        )
    for k in range(15):
        tx = -80 + k * 10
        length = 58 + k * 2.7
        metal += (
            np.exp(-(((dx - tx) / 2.75) ** 2))
            * ((dy > -53) & (dy < -53 + length))
            * (0.62 + 0.18 * sin(k))
        )
    # Round winding drum: actual chord lengths in a circular cross section.
    chord = np.sqrt(np.maximum(0, 1 - ((dy - 37) / 21) ** 2))
    metal += chord * ((dx > -98) & (dx < 97)) * 0.76
    for k in range(47):
        lx = -83 + (k * 29) % 169
        ly = 37 + 16 * sin(k * 1.8 + t * 2)
        metal += np.exp(-((dx - lx) ** 2 + (dy - ly) ** 2) / 5) * 0.7
    for x in (-124, 126):
        for y in (-56, 58):
            metal += np.exp(-(((np.hypot(dx - x, dy - y) - 5) / 2) ** 2))
    organic = np.array([0.1, 0.60, 1.35])
    steel = np.array([1.8, 1.04, 0.15])
    im = np.uint8(
        239 * np.exp(-(wood[:, :, None] * organic + metal[:, :, None] * steel))
    )
    rect(im, 0, 0, 768, 55, "233137")
    label(im, 29, 17, "오르골의 속", 23, "f0f1df", "bold")
    label(im, 740, 21, "재료 투과 모형", 15, "a9c3bb", anchor="right")
    xx = 118 + 512 * step(t, 2.4, 5.8)
    if 2.4 < t < 6:
        line(im, (xx, 65), (xx, 358), "6d9c94", 2)
    if t > 5.7:
        bx = cx - 92
        bracket(im, bx, cy - 60, 180, 105, "556568", 12)
        path(im, [(bx + 178, cy - 57), (cx + 128, 121), (cx + 192, 121)], "56656a")
        label(im, cx + 123, 96, "금속 빗살", 16, "425660")
    rect(im, 0, 376, 768, 56, "d6dbd3")
    dot(im, 53, 402, 6, "ce894b")
    label(im, 68, 394, "나무 상자", 16, "485754")
    dot(im, 196, 402, 6, "536fa0")
    label(im, 211, 394, "금속 장치", 16, "485754")
    return im


def dark_documentary(t):
    im = blank("050b10")
    # A radial acoustic pulse travels across a submerged basin. Afterglow decays with distance behind the wave.
    u = (0.19 + t * 0.285) % 1
    origin = (322, 216)
    front = u * 486
    for k in range(50):
        a = np.linspace(0, TAU, 280)
        r = 19 + k * 5.9
        x = (
            389
            + (r + np.sin(3 * a + 0.6) * r * 0.17 + np.cos(5 * a) * r * 0.09)
            * np.cos(a)
            * 1.24
        )
        y = (
            225
            + (r + np.sin(3 * a + 0.6) * r * 0.17 + np.cos(5 * a) * r * 0.09)
            * np.sin(a)
            * 0.64
        )
        p = np.column_stack((x, y))
        d = np.hypot(x - origin[0], (y - origin[1]) * 1.36)
        for lo, hi, c in [
            (-3, 12, "c7ecdc"),
            (12, 35, "79b7b4"),
            (35, 91, "367275"),
            (91, 153, "214749"),
            (153, 480, "19323b"),
            (-486, -3, "0c1c24"),
        ]:
            sel = ((front - d) > lo) & ((front - d) <= hi)
            for ix in np.split(
                np.flatnonzero(sel), np.where(np.diff(np.flatnonzero(sel)) != 1)[0] + 1
            ):
                if len(ix) > 1:
                    path(im, p[ix], c, 1)
    ell(im, *origin, front, front / 1.36, "528c8c", 1)
    # Keep only the rim of the pulse; the ellipse must never occlude its echo contours.
    for k in range(3):
        xx, yy = [(400, 192), (466, 250), (535, 177)][k]
        distance = np.hypot(xx - origin[0], (yy - origin[1]) * 1.36)
        if front > distance:
            dot(im, xx, yy, 2, "e5d9ab")
            arc(im, xx, yy, 7 + 9 * u, 4 + 5 * u, 0, 360, "b9ac84", 1)
    # Once heard, a return stays on a little time strip; the survey ends with three distinct arrivals.
    for i, (xx, yy) in enumerate([(400, 192), (466, 250), (535, 177)]):
        tm = [1.1, 3.9, 6.8][i]
        g = step(t, tm, tm + 0.78)
        if g:
            reveal(im, [(xx, yy), (xx + 21, yy - 25), (xx + 56, yy - 25)], g, "99ad9f")
            if g > 0.92:
                label(im, xx + 30, yy - 41, "0" + str(i + 1), 14, "c9d4b7")
            xx2 = 87 + i * 63
            path(
                im,
                [
                    (xx2, 372),
                    (xx2 + 10, 372),
                    (xx2 + 13, 372 - 13 * g),
                    (xx2 + 16, 376),
                    (xx2 + 19, 372),
                    (xx2 + 45, 372),
                ],
                "83a69f",
                2,
            )
    label(im, 41, 37, "물밑의 세 메아리", 22, "c6dcce", "bold")
    label(im, 726, 374, "모의 수중 지형", 14, "78928c", anchor="right")
    return im


@lru_cache(None)
def sensor():
    yy, xx = np.mgrid[:162, :288].astype("f")
    return yy, xx, np.random.default_rng(81).normal(0, 0.34, xx.shape)


def thermal_camera(t):
    y, x, noise = sensor()
    u = step(t, 1.1, 6.2)
    v = step(t, 4.3, 9.5)
    base = 20.1 + noise + 1.3 * (x / 288) - 0.8 * (y / 162)
    # Cup wall, opening, handle and spoon are separate simulated temperature fields.
    dx = x - 138
    dy = y - 98
    wall = (abs(dx) < 51 - 10 * np.clip((dy + 22) / 59, 0, 1)) & (dy > -27) & (dy < 34)
    base[wall] += 11 + 13 * u - 4 * v + 2 * np.cos(dx[wall] / 53 * pi / 2)
    base += np.exp(-(((np.hypot((x - 189) / 21, (y - 91) / 24) - 1) / 0.13) ** 2)) * (
        8 + 9 * u
    )
    rim = (dx / 52) ** 2 + ((y - 70) / 13) ** 2
    inside = rim < 1
    base[inside] = 46 + 15 * u - 4 * v + 0.4 * noise[inside]
    base += np.exp(-(((rim - 1) / 0.19) ** 2)) * 4
    # Insertion moves the spoon into the hot centre, then heat travels up the stem.
    sx = lerp(86, 139, u)
    sy = lerp(65, 74, u)
    vx, vy = 27.0, -56.0
    q = np.clip(((x - sx) * vx + (y - sy) * vy) / (vx * vx + vy * vy), 0, 1)
    dist = np.hypot(x - sx - q * vx, y - sy - q * vy)
    spoon = dist < 2.15
    base[spoon] = 23 + (28 * np.exp(-q[spoon] * 2.3)) * u + (8 * q[spoon]) * v
    lut = np.array(
        [
            col(c)
            for c in [
                "110e23",
                "312355",
                "71315e",
                "ac4565",
                "da6550",
                "f49744",
                "f9c960",
                "fcf1ae",
                "fff9e4",
            ]
        ]
    )
    grad = np.linspace(18, 65, len(lut))
    im = np.stack([np.interp(base, grad, lut[:, i]) for i in range(3)], 2).astype(
        np.uint8
    )
    im = cv2.resize(im, (768, 432), interpolation=cv2.INTER_NEAREST)
    samplex = int(sx + vx * 0.7)
    sampley = int(sy + vy * 0.7)
    xx = samplex * 768 / 288
    yy = sampley * 432 / 162
    for a, b in [
        ((xx - 13, yy), (xx - 4, yy)),
        ((xx + 4, yy), (xx + 13, yy)),
        ((xx, yy - 13), (xx, yy - 4)),
        ((xx, yy + 4), (xx, yy + 13)),
    ]:
        line(im, a, b, "f8f3dc")
    label(im, xx + 16, yy - 8, f"{base[sampley, samplex]:.1f}°", 16, "fff5dd", "bold")
    for j in range(168):
        p = j / 167 * (len(lut) - 1)
        k = min(len(lut) - 2, int(p))
        line(im, (710, 303 - j), (723, 303 - j), mix(lut[k], lut[k + 1], p - k))
    label(im, 704, 114, "65°", 14, "f2e8cc")
    label(im, 704, 312, "18°", 14, "f2e8cc")
    label(im, 30, 27, "차에 담근 숟가락", 22, "eee5d5", "bold")
    label(im, 32, 387, "열전달 모의 실험", 14, "e8daca")
    return im


@lru_cache(None)
def iris():
    return np.loadtxt(PLATES / "iris.csv", delimiter=",", skiprows=1)


def dataviz(t):
    d = iris()
    im = ground("f7eed9", "f0e4c9", 2, 41).copy()
    grid(im, 17, "c7bda4", dots=True)
    label(im, 53, 37, "붓꽃 150송이의 꽃잎", 27, "514a41", "bold")
    label(im, 55, 80, "꽃잎 길이  (cm)", 15, "776d5f")
    axis = 139
    unit = 78
    for k in range(1, 8):
        x = axis + (k - 1) * unit
        line(im, (x, 123), (x, 349), "d6cab4")
        label(im, x, 360, str(k), 16, "756d60", anchor="center")
    for j, (name, c) in enumerate(
        [("세토사", "4f8395"), ("버시컬러", "847f80"), ("버지니카", "b96a57")]
    ):
        y = 158 + j * 76
        label(im, 123, y - 8, name, 16, c, "bold", "right")
        vals = d[d[:, 4] == j, 2]
        counts = {}
        take = int(50 * step(t, 0.35 + 1.45 * j, 3.2 + 1.5 * j))
        for k, val in enumerate(vals[:take]):
            count = counts.get(val, 0)
            counts[val] = count + 1
            x = axis + (val - 1) * unit
            yy = y + 12 - (count % 8) * 4.5
            dot(im, x + ((count // 8) * 3), yy, 2.8, c)
        if t > 6:
            p = np.median(vals)
            x = axis + (p - 1) * unit
            reveal(
                im,
                [(x, y - 14), (x + 14, y - 31), (x + 40, y - 31)],
                step(t, 6.1 + j * 0.3, 7.4 + j * 0.3),
                "655c4e",
            )
            if t > 7.25 + j * 0.32:
                label(im, x + 16, y - 50, f"{p:g}", 16, c, "bold")
    label(im, 703, 397, "점 하나는 한 송이", 15, "796e5c", anchor="right")
    return im


@lru_cache(None)
def roofs():
    return [
        (h, np.array(poly))
        for h, poly in json.loads((PLATES / "roofs.json").read_text())
    ]


def white_model(t):
    im = ground("232b2c", "080d10", 0, light=True).copy()
    buildings = roofs()
    angle = -0.54 + 0.18 * step(t, 0, 10)
    sc = 975 + 105 * step(t, 1.1, 4.8) - 62 * step(t, 7, 10)

    def project(p, h):
        u = p[:, 0] + 0.155
        v = p[:, 1] - 0.06
        return np.column_stack(
            (
                380 + (u * cos(angle) - v * sin(angle)) * sc,
                238 + (u * sin(angle) + v * cos(angle)) * 0.54 * sc - h * sc * 0.75,
            )
        )

    footprint = np.array(
        [[-0.393, -0.15], [0.082, -0.15], [0.082, 0.271], [-0.393, 0.271]]
    )
    pl = project(footprint, 0)
    poly(im, pl + [0, 14], "34413f")
    poly(im, pl, "8f9c98")
    for h, p in buildings:
        shadow = project(p, 0) + np.array([h * sc * 0.42, h * sc * 0.17])
        poly(im, shadow, "778481")
    gate = step(t, 2, 5.5)
    band = lerp(-0.42, 0.10, gate)
    for h, p in sorted(
        buildings, key=lambda e: np.dot(np.mean(e[1], axis=0), [sin(angle), cos(angle)])
    ):
        x = np.mean(p[:, 0])
        base = project(p, 0)
        top = project(p, h)
        tint = step(t, 4.8, 7.4) * sat((h - 0.017) / 0.034)
        lit = exp(-(((x - band) / 0.033) ** 2)) * 0.8
        color = mix("d7dfdb", "77c1bd", tint)
        for k in range(len(top)):
            l = (k + 1) % len(top)
            if top[l, 0] > top[k, 0]:
                poly(
                    im,
                    [base[k], base[l], top[l], top[k]],
                    shade(color, 0.65 + 0.12 * lit),
                )
        poly(im, top, mix(color, "f5dc9c", lit))
    label(im, 38, 29, "로테르담의 지붕 높이", 22, "e4e6dd", "bold")
    rect(im, 0, 383, 768, 49, "1b2528")
    label(im, 732, 398, "3DBAG  /  로테르담 일부", 14, "a5b8b0", anchor="right")
    if t > 6.7:
        label(im, 36, 397, "높은 지붕에 청록빛을 비춥니다", 17, "a8d0c6")
    return im


def data_physical(t):
    im = ground("e8dcca", "c6ae92", 1, 21, True).copy()
    label(im, 45, 36, "윤년의 종이 달력", 25, "51483c", "bold")
    label(im, 47, 75, "2024년  ·  종이 한 장은 하루", 16, "736656")
    base = np.array([(96, 232), (601, 242), (662, 293), (151, 297)])
    poly(im, base + [0, 16], "8e765c")
    poly(im, base, "bda385")
    line(im, tuple(base[3]), tuple(base[2]), "d9c29e", 2)
    for j, count in enumerate([31, 29, 31]):
        x = 196 + j * 168
        y = 248 + j * 3
        ell(im, x + 27, y + 24, 72, 12, "9d886f")
        for k in range(count):
            t0 = 0.12 + j * 0.60 + k * 0.158
            if t < t0:
                continue
            u = step(t, t0, t0 + 0.42)
            fly = 53 * (1 - u)
            xx = x + 18 * (1 - u) + 1.2 * sin(k * 9)
            yy = y - 3.95 * k - fly + 1.2 * sin(k * 0.8)
            c = "b48b54" if (k + 1) % 7 == 0 else ["e9dfbe", "dfcfa8", "eee5ce"][j]
            box(im, xx, yy, 58, 37, 3, c)
            line(im, (xx - 29, yy + 17), (xx + 21, yy + 38), shade(c, 0.86))
        label(im, x + 9, 327 + j * 3, str(j + 1) + "월", 20, "514738", "bold", "center")
        if t > 7.3:
            label(
                im, x + 9, 361 + j * 3, str(count) + "일", 16, "6e5c48", anchor="center"
            )
    return view(im, 1 + 0.10 * step(t, 1, 3) * (1 - step(t, 5.8, 8)), 384, 216)


ROUTES = [
    (
        [
            (70, 307),
            (185, 307),
            (259, 233),
            (395, 233),
            (456, 172),
            (622, 172),
            (681, 113),
        ],
        "b7544f",
        "서점길",
    ),
    (
        [
            (103, 103),
            (179, 103),
            (240, 164),
            (326, 164),
            (395, 233),
            (495, 233),
            (577, 315),
            (693, 315),
        ],
        "477d89",
        "도서관길",
    ),
    (
        [
            (182, 372),
            (262, 372),
            (313, 321),
            (313, 269),
            (349, 233),
            (395, 233),
            (395, 136),
            (452, 79),
            (568, 79),
        ],
        "a08144",
        "인쇄소길",
    ),
]


def transit_map(t):
    im = ground("f7efda", "ecdfc3", 1, 51).copy()
    for i in range(22):
        line(im, (i * 40, -4), (i * 40 + 15, 432), "e8ddc5")
    river = [
        (-23, 238),
        (154, 238),
        (202, 190),
        (281, 190),
        (390, 81),
        (597, 81),
        (700, -22),
    ]
    path(im, river, "a7cbce", 26)
    for j, (p, color, name) in enumerate(ROUTES):
        start = [0.15, 2.25, 4.1][j]
        u = step(t, start, start + 3.2)
        if u < 0.002:
            continue
        reveal(im, p, u, "f9f3e2", 10)
        reveal(im, p, u, color, 6)
        for k in range(7):
            f = k / 6
            if u >= f:
                a, b = onpath(p, f)
                dot(im, a, b, 5, color)
                dot(im, a, b, 2.5, "fbf5e3")
        dot(im, *onpath(p, u), 5, "fff7cf")
    if t > 4.4:
        rr(im, 382, 223, 27, 18, 8, "433e36")
        rr(im, 385, 226, 21, 12, 6, "faf4df")
        label(im, 399, 258, "책마루", 17, "4e5348", "bold")
    labels = [
        (65, 325, "헌책방"),
        (659, 81, "제본소"),
        (101, 70, "작은도서관"),
        (640, 333, "강변열람실"),
        (138, 386, "종이창고"),
        (550, 53, "활판공방"),
    ]
    for j, (x, y, s) in enumerate(labels):
        if t > [0.3, 3.0, 2.4, 5.4, 4.2, 7][j]:
            label(im, x, y, s, 15, "53574c")
    z = 1.05 + 0.34 * step(t, 0.4, 2.4) - 0.36 * step(t, 5.4, 8.4)
    return view(
        im,
        z,
        300 + 84 * step(t, 1.3, 5.6),
        232 - 16 * step(t, 3, 8),
        -2 + 2 * step(t, 4, 9),
    )


@lru_cache(None)
def terrain():
    dem = np.load(PLATES / "ridge.npz")["elevation"].astype("f")
    z = cv2.resize(dem, (76, 69), interpolation=cv2.INTER_AREA)
    yy, xx = np.indices(z.shape)
    x = (xx - 37.5) / 37.5
    y = (yy - 34) / 34
    gy, gx = np.gradient(z)
    light = np.clip(0.72 + gx * 0.005 - gy * 0.007, 0.24, 1.22)
    c = np.zeros((*z.shape, 3))
    for k in range(3):
        c[:, :, k] = (
            np.interp(
                z,
                [240, 530, 850, 1076],
                np.array([col("75866c"), col("8c9771"), col("b6a17a"), col("cab58c")])[
                    :, k
                ],
            )
            * light
        )
    return x, y, z, np.uint8(np.clip(c, 0, 255))


def map_explainer(t):
    x, y, z, colors = terrain()
    im = ground("edf0dc", "c9d5c1", 1, 29).copy()
    a = -0.51 + 0.21 * step(t, 0.1, 7.8)
    sc = 166 + 62 * step(t, 0.3, 4.7) - 28 * step(t, 7.4, 9.9)
    xx = 383 + sc * (x * cos(a) - y * sin(a)) * 1.23
    yy = 261 + sc * (x * sin(a) + y * cos(a)) * 0.47 - (z - 235) * 0.106
    pos = np.rint(np.stack((xx, yy), 2)).astype(np.int32)
    # Painter-sorted quads, true elevations with a vertically exaggerated relief.
    poly(
        im,
        [
            pos[0, 0] + [0, 13],
            pos[0, -1] + [0, 13],
            pos[-1, -1] + [0, 13],
            pos[-1, 0] + [0, 13],
        ],
        "a8a58a",
    )
    q = np.stack([pos[:-1, :-1], pos[:-1, 1:], pos[1:, 1:], pos[1:, :-1]], 2).reshape(
        -1, 4, 2
    )
    order = np.argsort((x[:-1, :-1] * sin(a) + y[:-1, :-1] * cos(a)).ravel())
    cc = colors[:-1, :-1].reshape(-1, 3)
    for i in order:
        cv2.fillConvexPoly(im, q[i], tuple(map(int, cc[i])), lineType=cv2.LINE_4)
    # A geographic section along a single source raster row; projected points retain their elevations.
    row = 32
    u = step(t, 2.5, 5.9)
    r = pos[row]
    if u > 0:
        reveal(im, r, u, "f3d793", 2)
        dot(im, *onpath(r, u), 4, "ffedb8")
    label(im, 33, 28, "능선을 가로지르는 선", 24, "405449", "bold")
    label(im, 33, 63, "잭스버러 단층 주변", 15, "606f5d")
    if t > 5.4:
        t0 = step(t, 5.4, 7.0)
        rect(im, 39, 328, 302, 76, "e8e9d6")
        h = z[row]
        hx = np.linspace(51, 327, len(h))
        hy = 392 - (h - h.min()) / (h.max() - h.min()) * 42
        reveal(im, np.column_stack((hx, hy)), t0, "5e7968", 2)
        label(im, 50, 335, "고도 단면", 13, "56694c")
    return im


@lru_cache(None)
def simulation():
    # One visitor joins the shorter of two lines. Counters serve at different fixed intervals.
    rng = np.random.default_rng(182)
    vis = []
    next_free = [0.0, 0.0]
    for i in range(28):
        arrival = 0.23 + i * 0.17 + rng.uniform(0, 0.07)
        waiting = [
            sum(1 for v in vis if v[1] == s and v[3] > arrival) for s in range(2)
        ]
        station = min(range(2), key=lambda s: (waiting[s], next_free[s], s))
        begin = max(next_free[station], arrival + 0.59)
        end = begin + [0.41, 0.55][station]
        next_free[station] = end
        rank = sum(v[1] == station for v in vis)
        vis.append((arrival, station, begin, end, rank))
    return vis


def pip(im, x, y, c, habit):
    ell(im, x + 2, y + 2, 10, 3, "b4a990")
    ell(im, x - 3, y - 1, 3, 2, "6c6556")
    ell(im, x + 4, y - 1, 3, 2, "6c6556")
    ell(im, x, y - 9, 9, 9, c)
    ell(im, x - 2, y - 12, 6, 5, shade(c, 1.09))
    for dx in [-3, 3]:
        dot(im, x + dx, y - 10, 1, "494b41")
    if habit % 3 == 0:
        ell(im, x - 3, y - 18, 3, 4, shade(c, 0.88), rot=-31)


def pip_simulation(t):
    im = ground("f1e8cd", "e2d8ba", 2, 52).copy()
    rr(im, 42, 68, 685, 292, 22, "cabfa1")
    rr(im, 39, 62, 685, 292, 22, "f3e8cd")
    label(im, 54, 19, "어느 줄이 더 짧을까", 24, "4c5242", "bold")
    st = [(419, 152), (419, 263)]
    colors = ["8fbaa0", "dbac77"]
    vis = simulation()
    for s, (x, y) in enumerate(st):
        line(im, (102, y + 17), (394, y + 17), "c9bfa4", 2)
        box(im, x, y - 26, 27, 20, 27, colors[s])
        label(im, x + 52, y - 14, "빠른 창구" if s == 0 else "느린 창구", 16, "5e6753")
    chars = []
    for i, (arr, s, start, end, rank) in enumerate(vis):
        if t < arr:
            continue
        x, y = st[s]
        if t < end:
            ahead = sum(v[1] == s and v[0] < arr and v[3] > t for v in vis)
            target = 386 - min(ahead, 9) * 24
            u = step(t, arr, arr + 0.58)
            cx = lerp(90, target, u)
            cy = lerp(211, y, u)
            jump = abs(sin(t * 12 + i)) * 3 * (1 - u)
        else:
            tx = 543 + (rank % 6) * 23
            ty = y - 23 + (rank // 6) * 21
            u = step(t, end, end + 0.65)
            cx = lerp(386, tx, u)
            cy = lerp(y, ty, u) - 12 * sin(u * pi)
            jump = 0
        chars.append((cy - jump, cx, i, s))
    for yy, xx, i, s in sorted(chars):
        pip(im, xx, yy, colors[s], i)
    for s in [0, 1]:
        count = sum(v[1] == s and t >= v[3] for v in vis)
        label(im, 686, st[s][1] - 32, str(count), 26, "5b6955", "bold", "center")
    label(im, 57, 383, "도착한 손님은 짧은 줄에 섭니다", 16, "6e715a")
    return im
