"""Interfaces, printed signals and a seed carried on the night air."""

from drawing import *


def dark_keynote(t):
    im = ground("1e2430", "090b11", 0, light=True).copy()
    grid(im, 36, "20252d", dots=True)
    lime = "b8f277"
    line(im, (52, 90), (716, 90), "353b42")
    zoom = step(t, 2.3, 4.3) * (1 - step(t, 6.2, 7.5))
    for i in range(4):
        x = 62 + i * 164
        y = 178 + round(36 * sin(i * 1.5) * (1 - step(t, 0.4, 3)))
        rr(im, x, y, 146, 86, 8, "303740")
        rect(im, x + 12, y + 12, 2, 62, "555e67")
        for j in range(20):
            amp = 2 + 21 * abs(sin(j * 0.47 + i) * cos(j * 0.22 - i))
            xp = x + 18 + j * 5.8
            line(
                im,
                (xp, y + 43 - amp),
                (xp, y + 43 + amp),
                lime if (int(t * 2) % 4 == i or t > 7.3) else "8e9ba9",
                2,
            )
        label(im, x + 2, y + 104, "0" + str(i + 1), 16, "9da7b2")
    scan = 62 + (t * 0.52 % 1) * 638
    line(im, (scan, 141), (scan, 304), lime, 1)
    if t > 6.5:
        u = step(t, 6.5, 7.6)
        rect(im, 0, round(432 - 112 * u), 768, 112, "141a20")
        label(im, 58, 339 + 100 * (1 - u), "박자가 맞았습니다", 24, "e2eae0")
        label(im, 685, 320 + 100 * (1 - u), "4", 86, lime, "bold", "right")
    im = view(im, 1 + 0.19 * zoom, 384 + 17 * zoom, 216 + 5 * zoom)
    label(im, 52, 43, "네 박자의 방", 25, "edf1ec", "bold")
    return im


def frog(im, x, y, s, hop):
    rows = [
        "  XX   XX ",
        " XGGX XGGX",
        " XWXXGXWXX",
        "XGGGGGGGGX",
        "XGPGGGGPGX",
        " XGGXXGGX ",
        "  XGGGGX  ",
        " XXGXXGXX ",
    ]
    colors = {"X": "2e4140", "G": "9bd28b", "W": "fff3d7", "P": "e7a292"}
    for j, row in enumerate(rows):
        for i, k in enumerate(row):
            if k != " ":
                rect(im, x + i * s, y + j * s - hop, s, s, colors[k])


def living_screencast(t):
    im = ground("b9c9f4", "ede1cd", 1, 8).copy()
    rr(im, 54, 53, 659, 337, 16, "8990a4")
    rr(im, 50, 44, 659, 337, 16, "fffdf6")
    label(im, 76, 62, "작은 정원", 24, "283b3a", "bold")
    line(im, (50, 107), (708, 107), "d4dbd2")
    rr(im, 74, 130, 189, 224, 12, "eef2e9")
    label(im, 92, 150, "작업 순서", 17, "4c6257")
    for j, name in enumerate(["씨앗 선택", "물 주기", "새잎 확인"]):
        active = int(min(2, t / 3.2)) == j
        if active:
            rr(im, 85, 185 + j * 50, 165, 39, 8, "cce3c9")
        dot(im, 103, 204 + j * 50, 5, "3b7253" if active or t > j * 3.2 else "bbc3b7")
        label(im, 118, 195 + j * 50, name, 17, "34483f")
    rect(im, 290, 259, 387, 74, "e9e5cf")
    x = 457
    rr(im, x - 47, 263, 96, 14, 3, "c8775e")
    poly(im, [(x - 38, 277), (x + 39, 277), (x + 28, 321), (x - 27, 321)], "b26a54")
    grow = step(t, 4, 7.7)
    h = 9 + 81 * grow
    path(im, [(x, 262), (x + 5, 261 - h * 0.5), (x, 262 - h)], "597748", 5)
    for side, lev in [(-1, 0.60), (1, 0.89)]:
        ell(
            im,
            x + side * 14 * grow,
            262 - h * lev,
            23 * grow,
            10 * grow,
            "70a475",
            rot=side * -32,
        )
    px = 307 + 142 * step(t, 1, 3) - 98 * step(t, 6.6, 8.6)
    frog(im, px, 240, 4, max(0, sin(t * 6)) * 12)
    if 3 < t < 6.8:
        for j in range(5):
            q = (t * 0.95 + j * 0.21) % 1
            dot(im, 438 + 30 * q + j * 4, 143 + 110 * q, 3, "75a9b6")
    cx = lerp(168, 455, step(t, 1.8, 3.2))
    cy = lerp(246, 172, step(t, 1.8, 3.2))
    poly(
        im,
        [(cx, cy), (cx + 2, cy + 23), (cx + 8, cy + 16), (cx + 18, cy + 15)],
        "fffef3",
        "30423c",
        2,
    )
    return view(
        im,
        1 + 0.08 * step(t, 2, 4) * (1 - step(t, 7.4, 9)),
        384 + 10 * step(t, 2, 4) * (1 - step(t, 7.4, 9)),
        216,
    )


def hologram_hud(t):
    im = ground("112e32", "030b0f", 0, light=True).copy()
    grid(im, 20, "296069", dots=True)
    cyan = "75e7df"
    gold = "ffad70"
    lay = blank("000000")
    phase = t * 0.65
    explode = step(t, 2, 4) * (1 - step(t, 6.2, 8.4))

    def pr(x, y, z):
        return (
            365 + x * cos(phase) - y * sin(phase),
            280 + (x * sin(phase) + y * cos(phase)) * 0.34 - z,
        )

    for rad, z, h in [(33, 0, 11), (13, 13, 55), (22, 73, 9)]:
        for dz in (0, h):
            path(
                lay,
                [
                    pr(rad * cos(a), rad * sin(a), z + dz)
                    for a in np.linspace(0, TAU, 60)
                ],
                "52a99e",
                1,
            )
        for a in np.arange(0, TAU, 0.48):
            line(
                lay,
                pr(rad * cos(a), rad * sin(a), z),
                pr(rad * cos(a), rad * sin(a), z + h),
                "478e88",
            )
    cz = 90 + 48 * explode
    for j in sorted(range(3), key=lambda i: sin(i * TAU / 3 + phase)):
        a = j * TAU / 3
        r = 101 + 38 * explode
        line(lay, pr(0, 0, cz), pr(r * cos(a), r * sin(a), cz), cyan, 2)
        for s in np.linspace(0, 1, 9):
            rad = 24 * sin(s * pi / 2) + 2
            z = cz + 23 * s
            path(
                lay,
                [
                    pr(r * cos(a) + rad * cos(v), r * sin(a) + rad * sin(v), z)
                    for v in np.linspace(0, TAU, 35)
                ],
                "62bbb3",
            )
    glow(im, lay, 0.85, 6)
    xp = 140 + 480 * step(t, 0, 2.5)
    if t < 2.8:
        line(im, (xp, 73), (xp, 338), "75c9c2")
    bracket(im, 182, 113, 364, 202, "508f8d", 17)
    path(im, [(470, 181), (540, 124), (631, 124)], gold)
    label(im, 548, 98, "회전 날개", 18, gold)
    label(im, 51, 42, "컵 풍속계", 26, "ceeee4", "bold")
    label(im, 52, 366, "03   /   회전체", 15, "8eb7b3")
    return im


def desktop_flythrough(t):
    im = ground("ead6b4", "bfa580", 2, 55).copy()
    shift = step(t, 0.5, 3.3) * 130 + step(t, 3.7, 6.7) * 120
    wide = step(t, 6.4, 9.5)
    zoom = 1 - 0.20 * wide

    def p(x, y):
        return (100 + (x - shift) * zoom + 286 * wide, y * zoom + 40 * step(t, 7, 10))

    def card(x, y, w, h, pal):
        a = np.array(
            [p(x, y), p(x + w, y - 15), p(x + w + 41, y + h), p(x + 41, y + h + 15)]
        )
        poly(im, a + [14, 15], "bba380")
        poly(im, a + [3, 5], "cabda3")
        poly(im, a, pal, "e8dec7")

    for row in range(15):
        for j in range(35):
            xp, yp = p(j * 36 - 300, row * 32)
            dot(im, xp, yp, 1, "d0ba98")
    card(-170, 107, 245, 156, "fff3cb")
    card(115, 97, 230, 161, "e5f0e0")
    card(390, 103, 240, 157, "fdf0e0")
    for j in range(6):
        xp, yp = p(-143 + j * 32, 154 + 12 * sin(j))
        line(im, (xp, yp), p(-143 + j * 32, 211), "968054", 2)
        ell(im, xp, yp + 57, 8, 4, "927953")
    for j in range(7):
        a, b = p(156 + j * 24, 153)
        rect(im, a, b, 11 * zoom, 42 * (0.5 + 0.5 * abs(sin(j + 1))), "7da795")
    for j in range(5):
        line(im, p(430, 162 + j * 9), p(599, 152 + j * 9), "88746a")
    for j in range(5):
        a, b = p(451 + j * 31, 182 + sin(j * 1.8) * 9 - j)
        ell(im, a, b, 5, 3, "745767")
        line(im, (a + 4, b), (a + 4, b - 18), "745767", 2)
    for xx, st in [(-104, "채집"), (187, "편집"), (471, "악보")]:
        a, b = p(xx, 120)
        label(im, a, b, st, 16, "524c41", "bold")
    x = 30 + 442 * step(t, 0.6, 7.5)
    a, b = p(x, 234 - 11 * abs(sin(t * 5)))
    s = 3.7 * zoom
    ell(im, a + 15, b + 30, 24, 5, "b5a883")
    for j, row in enumerate(
        [
            "  XXXX  ",
            " XXGGXX ",
            "XXGXXGXX",
            "XXGGGGXX",
            "  XYYX  ",
            " XXXYXX ",
            "  X  X  ",
        ]
    ):
        for i, k in enumerate(row):
            if k != " ":
                rect(
                    im,
                    a + i * s,
                    b + j * s,
                    s,
                    s,
                    {"X": "5c4d45", "G": "f4c970", "Y": "6f9e92"}[k],
                )
    a, b = p(592, 333)
    line(im, (a - 110, b + 23), (a, b), "6b7f71", 12)
    poly(im, [(a, b - 6), (a + 22, b - 5), (a, b + 6)], "e8cca7")
    close = (1 - step(t, 0, 3)) * 0.37 + step(t, 2, 4) * (1 - step(t, 5.4, 7.3)) * 0.14
    return view(im, 1 + close, 384 - 97 * (1 - step(t, 0.35, 3.3)), 216)


def spreadsheet(t):
    im = blank("f7f8f1")
    rect(im, 0, 0, 768, 40, "dce2db")
    label(im, 21, 10, "빗물 장부", 21, "324337", "bold")
    rect(im, 15, 47, 70, 27, "e3e8e0", "adb8ad")
    label(im, 26, 52, "합계", 15, "425347")
    rect(im, 90, 47, 660, 27, "ffffff", "b1bcb5")
    n = min(48, int(max(0, t - 3) * 10))
    label(im, 106, 52, "집수량  =  " + str(n) + " 칸", 16, "365044")
    ox, oy = 56, 122
    cw, ch = 16, 13
    for i in range(42):
        if i % 3 == 0:
            label(im, ox + i * cw + 3, 97, str(i + 1), 11, "718078")
    for j in range(20):
        label(im, 20, oy + j * ch + 1, str(j + 1), 11, "829185")
        line(im, (ox, oy + j * ch), (ox + 42 * cw, oy + j * ch), "dce2d8")
    for i in range(43):
        line(im, (ox + i * cw, oy), (ox + i * cw, oy + 20 * ch), "dce2d8")

    def cell(i, j, c):
        if 0 <= j < 20:
            rect(im, ox + i * cw + 1, oy + j * ch + 1, cw - 2, ch - 2, c)

    for i in range(4, 26):
        roof = 6 + abs(i - 14) // 3
        cell(i, roof, "63806b")
        if i % 3 == 0:
            jj = int((t * 5 + i * 2.5) % 9) - 1
            if jj < roof and t < 7.2:
                cell(i, jj, "70a9bd")
    for i in range(25, 33):
        cell(i, 10, "7c8d75")
    for j in range(11, 19):
        cell(31, j, "718771")
        cell(39, j, "718771")
    for i in range(31, 40):
        cell(i, 19, "718771")
    for k in range(n):
        cell(32 + k % 7, 18 - k // 7, "5d9da7" if k // 7 % 2 else "87bdc4")
    ii = 32 + n % 7
    jj = 18 - n // 7
    bracket(im, ox + ii * cw, oy + jj * ch, cw, ch, "286753", 4)
    rect(im, 0, 394, 768, 38, "e8ece3")
    label(im, 55, 403, "집수 지붕", 14, "4c6654")
    return im


BAYER = (
    np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], float) / 16
)


def one_bit_dither(t):
    # Ray-intersection with three oriented spool cylinders, thresholded in cylindrical UV coordinates.
    sc = 1 + 0.23 * step(t, 2, 4) - 0.17 * step(t, 6.8, 9)
    xx = (X - 375) / sc
    yy = (Y - 216) / sc
    thresh = BAYER[(Y.astype(int) // 2) % 4, (X.astype(int) // 2) % 4]
    mask = 0.78 + 0.07 * np.sin(Y * 0.036) > thresh
    tilt = -0.25 + 0.13 * sin(t * 0.50)
    a = xx * cos(tilt) + yy * sin(tilt)
    b = -xx * sin(tilt) + yy * cos(tilt)
    for center, length, r, thread in [
        (64, 16, 102, False),
        (48, 109, 77, True),
        (-61, 18, 102, False),
    ]:
        front = np.sqrt(np.maximum(0, 1 - (a / r) ** 2))
        lower = center + front * r * 0.38
        upper = lower - length
        side = (abs(a) < r) & (b >= upper) & (b <= lower)
        phi = np.arcsin(np.clip(a / r, -1, 1))
        v = b + 15 * phi
        tex = BAYER[
            np.floor(v / 2).astype(int) % 4,
            np.floor((phi + t * 0.72) * r / 2).astype(int) % 4,
        ]
        val = 0.2 + 0.46 * front - 0.18 * (a / r)
        if thread:
            val -= 0.35 * (np.cos((v - t * 6) * 1.3) > 0.45)
        mask = np.where(side, val > tex, mask)
        cap = (a / r) ** 2 + ((b - center + length) / (r * 0.38)) ** 2 < 1
        hole = (a / (r * 0.22)) ** 2 + ((b - center + length) / (r * 0.085)) ** 2 < 1
        mask = np.where(cap, np.where(hole, False, 0.76 > tex), mask)
    im = np.where(
        mask[:, :, None], np.array([239, 232, 211]), np.array([32, 34, 36])
    ).astype(np.uint8)
    tail = step(t, 0.6, 8.3)
    p = [
        (398 + q * 325 * tail, 255 + 40 * q + 22 * sin(q * 9 - t * 1.8) * q)
        for q in np.linspace(0, 1, 90)
    ]
    cv2.polylines(im, [pts(p)], False, (32, 34, 36), 3, cv2.LINE_8)
    return im


@lru_cache(None)
def board():
    im = ground("27584a", "10362d", 2, 1, True).copy()
    for x, y in [(27, 26), (740, 26), (27, 404), (740, 404)]:
        dot(im, x, y, 11, "b6a66a")
        dot(im, x, y, 6, "122e27")
    for i in range(16):
        y = 55 + i * 18
        path(
            im,
            [(35, y), (117 + i * 3, y), (159 + i * 3, y + 42), (209, y + 42)],
            "477457",
            2,
        )
        path(im, [(531, y), (563, y), (584, y - 21), (719, y - 21)], "467457", 2)
    return im


def circuit_board(t):
    im = board().copy()
    gold = "bda86c"
    white = "dcdfbc"
    signal = [
        [(95, 203), (192, 203), (229, 166), (308, 166)],
        [(418, 176), (467, 176), (524, 233), (608, 233)],
        [(635, 212), (635, 118), (612, 95), (530, 95)],
    ]
    for j, p in enumerate(signal):
        path(im, p, "113b30", 13)
        path(im, p, gold, 5)
        dot(im, *p[0], 8, gold)
        dot(im, *p[-1], 8, gold)
        local = step(t, j * 2.4, j * 2.4 + 2.8)
        if local:
            reveal(im, p, local, "ecdc88", 2)
            dot(im, *onpath(p, local), 5, "fff4b0")
    for k in range(7):
        for x in (303, 411):
            rect(im, x, 145 + k * 12, 17, 4, gold)
    rr(im, 318, 135, 93, 102, 6, "232c29")
    rect(im, 325, 142, 79, 87, "34403a")
    dot(im, 334, 151, 4, "c9c8b0")
    for k in range(3):
        x = 69 + k * 13
        path(
            im,
            [(x, 231), (x, 277), (x + 6, 283), (x + 12, 277), (x + 12, 230)],
            gold,
            3,
        )
    dot(im, 627, 235, 30, "849783")
    dot(im, 627, 235, 23, "355541")
    for k in range(4):
        a = t * (1 + 4 * step(t, 3, 5)) + k * pi / 2
        ell(im, 627 + 10 * cos(a), 235 + 10 * sin(a), 11, 5, "b5d6a8", rot=a * 180 / pi)
    for k in range(5):
        x = 482 + k * 14
        rect(im, x, 76, 8, 16, "e9e3a0" if t > 6 + k * 0.4 else "587459")
    label(im, 58, 302, "수분 감지", 15, white)
    label(im, 336, 179, "급수", 18, white)
    label(im, 603, 281, "펌프", 15, white)
    moving = step(t, 0.4, 2.4) * (1 - step(t, 5.6, 8.2))
    im = view(im, 1 + 0.10 * moving, 384 + (12 * sin(t * 0.5)) * moving, 216)
    label(im, 54, 46, "화분 급수 회로", 22, white, "bold")
    return im


@lru_cache(None)
def spores():
    rng = np.random.default_rng(21)
    # Each seed has its own spine and a fan of discrete, glowing filaments.
    p = []
    dest = []
    ids = []
    phase = []
    fixed = []
    for j in range(45):
        a = j * 2.39996
        r = 31 + 61 * np.sqrt((j + 0.5) / 45)
        sx = 225 + r * cos(a)
        sy = 178 + r * sin(a)
        d = np.array([cos(a), sin(a)])
        tangent = np.array([-d[1], d[0]])
        n = j % 12
        cx = 337 + ((n * 89) % 331) + 15 * sin(j)
        cy = 110 + 54 * sin(n * 2.1) + 20 * cos(n * 0.7)
        for k in range(44):
            q = rng.random()
            f = (k % 7 - 3) / 3
            v = np.array([sx, sy])
            if k < 14:
                v -= d * (1 - q) * r
                target = [cx + 1.5 * sin(q * pi), cy + q * 25]
            else:
                v += d * (9 * q - 4 * abs(f) * q) + tangent * f * 14 * q
                target = [cx + f * 19 * q, cy - 13 * q + 5 * f * f * q]
            p.append(v)
            dest.append(target)
            ids.append(j)
            phase.append(q)
            fixed.append(False)
    for k in range(640):
        q = rng.random()
        p.append([225 + 13 * np.sin(q * pi) + rng.normal(0, 1.3), 178 + 173 * q])
        dest.append(p[-1])
        ids.append(0)
        phase.append(q)
        fixed.append(True)
    return np.array(p), np.array(dest), np.array(ids), np.array(phase), np.array(fixed)


def firefly_pointillism(t):
    im = blank("04070d")
    lay = blank("000000")
    p, e, g, q, stalk = spores()
    u = np.clip((t - 1.7 - (g % 12) * 0.17) / 4.4, 0, 1)
    u = u * u * (3 - 2 * u)
    u[stalk] = 0
    xy = p + (e - p) * u[:, None]
    xy[:, 1] += np.sin(pi * u) * (-57 + 18 * np.sin(g + t)) + u * (
        6 * np.sin(t * 1.7 + g) + (97 + 48 * np.cos(g % 12 * 0.7)) * step(t, 6.2, 9.7)
    )
    xy[:, 0] += 8 * np.sin(t * 0.8 + g) * u + 1.3 * np.sin(q * 5 + t)
    br = 0.55 + 0.45 * np.sin(t * 2 + q * 7) ** 2
    co = np.stack((163 + 83 * q, 172 + 73 * q, 116 + 95 * q), 1) * br[:, None]
    co[stalk] *= [0.62, 0.85, 0.67]
    xx, yy = xy.astype(int).T
    lay[yy, xx] = co
    for k in range(0, len(xx), 21):
        dot(lay, xx[k], yy[k], 1, co[k])
    for k in range(95):
        x = (k * 197) % 762
        y = 328 + (k * 59) % 76
        dot(lay, x, y + 2 * sin(t + k), 1, "66836a")
    glow(im, lay, 1.7, 4)
    return im
