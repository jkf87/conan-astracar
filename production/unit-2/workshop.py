"""Eight little machines. Geometry, working sections and trajectories are authored here."""

from draw import *


def rule(d, x, y, x2, y2, col, step=9):
    length = math.hypot(x2 - x, y2 - y)
    for i in range(0, int(length), step):
        a = i / length
        b = min(1, (i + step * 0.5) / length)
        d.line([(mix(x, x2, a), mix(y, y2, a)), (mix(x, x2, b), mix(y, y2, b))], col, 1)


def blueprint(d, t):
    d.grad(0, 0, 768, 432, [(0, "17406a"), (0.52, "174b77"), (1, "113857")])
    ink = "e2f2ef"
    weak = "6490aa"
    for x in range(20, 760, 16):
        d.rect(x, 20, 0.5, 392, "487293")
    for y in range(20, 419, 16):
        d.rect(20, y, 728, 0.5, "487293")
    d.rect(20, 19, 728, 393, None, weak, 1)
    d.txt(40, 39, "접이식 받침", 26, ink)
    # Orthographic crossed rails: the seat widens as the legs open.
    a = 0.17 + 0.68 * span(t, 2.6, 6.2)
    h = 166 * cos(a)
    w = 166 * sin(a)
    cx = 334
    cy = 227
    rule(d, cx, 70, cx, 391, weak)
    rule(d, 101, cy, 559, cy, weak)
    for sign in [-1, 1]:
        start = (cx + sign * w, cy + h)
        end = (cx - sign * w, cy - h)
        p = span(t, 0.12 + (sign + 1) * 0.38, 2.25 + (sign + 1) * 0.28)
        x, y = mix(start[0], end[0], p), mix(start[1], end[1], p)
        d.line([start, (x, y)], ink, 9)
        d.line([start, (x, y)], "17476e", 5)
        d.ell(*start, 12, 3, ink)
    d.circ(cx, cy, 11, "17476e", ink, 1.8)
    d.circ(cx, cy, 3, ink)
    d.line([(cx - w - 14, cy - h - 8), (cx + w + 14, cy - h - 8)], ink, 7)
    d.line([(cx - w - 14, cy - h - 8), (cx + w + 14, cy - h - 8)], "2c587b", 3)
    if t > 3:
        for x in [cx - w, cx + w]:
            rule(d, x, cy - h - 14, x, 71, weak)
        d.line([(cx - w, 84), (cx + w, 84)], ink, 1)
        for x in [cx - w, cx + w]:
            d.line([(x - 4, 89), (x + 4, 79)], ink, 1.2)
        d.txt(cx, 60, str(round(w * 2)), 15, ink, "mono", "center")
    d.rect(567, 92, 148, 145, "204a6e", weak, 1)
    d.txt(579, 102, "축 상세", 16, ink)
    for j in range(4):
        d.circ(641, 173, 34 - j * 7, None, ink, 1)
    for j in range(8):
        a = j * pi / 4
        d.line(
            [
                (641 + 35 * cos(a), 173 + 35 * sin(a)),
                (641 + 42 * cos(a), 173 + 42 * sin(a)),
            ],
            weak,
            1,
        )
    d.line([(cx + 15, cy), (544, 185), (567, 185)], weak, 1)
    d.rect(567, 335, 148, 53, None, weak)
    d.txt(
        578,
        349,
        "01 / 03" if t < 3 else "02 / 03" if t < 6 else "03 / 03",
        17,
        ink,
        "mono",
    )


def iso(x, y, z):
    return (383 + (x - y) * 0.866, 214 + (x + y) * 0.5 - z)


def cube(d, x, y, z, w, l, h, colors):
    a = [
        iso(x, y, z + h),
        iso(x + w, y, z + h),
        iso(x + w, y + l, z + h),
        iso(x, y + l, z + h),
    ]
    base = [iso(x, y, z), iso(x + w, y, z), iso(x + w, y + l, z), iso(x, y + l, z)]
    d.poly([a[3], a[2], base[2], base[3]], colors[1])
    d.poly([a[1], a[2], base[2], base[1]], colors[2])
    d.poly(a, colors[0])


def iso_infographic(d, t):
    d.bg("f0e9d5")
    soil = ("976d4f", "70533e", "866044")
    clay = ("f5c498", "ce8369", "a85e54")
    green = ("a5c985", "5e9259", "77a86d")
    # Follow the spillway in close-up, then ease back to all three levels.
    zoom = 0.96 + 0.22 * span(t, 0.25, 3.5) - 0.22 * span(t, 5.8, 8.8)
    track = -24 + 48 * span(t, 1.6, 6.8)
    with d.at(416 - zoom * (383 + track), 50 - (zoom - 0.96) * 148, zoom):
        cube(d, -144, -121, -24, 288, 242, 23, ("d4cab1", "bab29d", "a39c8a"))
        for i in range(3):
            x = -133 + i * 84
            y = -102 + i * 23
            h = 92 - i * 33
            cube(d, x, y, 0, 72, 144, h + 9, clay)
            cube(d, x + 4, y + 4, h + 9, 64, 136, 2, soil)
            for j in range(5):
                for k in range(2):
                    gx = x + 16 + k * 29
                    gy = y + 15 + j * 23
                    g = span(t, 1.3 + i * 1.45 + j * 0.10, 3.5 + i * 1.43 + j * 0.1)
                    sx, sy = iso(gx, gy, h + 10)
                    d.line([(sx, sy), (sx, sy - 4 - 19 * g)], "456a47", 1.7)
                    for side in [-1, 1]:
                        with d.at(sx, sy - 7 * g, 1, side * 0.48):
                            d.ell(
                                side * 3 * g,
                                -4 * g,
                                3 + g * 3,
                                3 + g * 8,
                                green[0] if side == 1 else green[2],
                            )
            # Each metal spout overhangs its bed edge; blue drops fall to the next step.
            for j in range(9):
                p1 = iso(x + 10, y + 9 + j * 15, h + 12)
                p2 = iso(x + 57, y + 9 + j * 15, h + 12)
                d.line([p1, p2], "c3916c", 0.7)
            if t > 1 + i * 1.4:
                # Water zigzags past the rows; visible end advances before the leaves open.
                path = [
                    iso(x + 3, y + 4, h + 12),
                    iso(x + 36, y + 4, h + 12),
                    iso(x + 36, y + 133, h + 12),
                    iso(x + 70, y + 133, h + 12),
                ]
                flow = clamp((t - 1 - i * 1.4) / 1.15) * 3
                for k in range(3):
                    if flow > k:
                        a, b = path[k : k + 2]
                        u = clamp(flow - k)
                        d.line(
                            [a, (mix(a[0], b[0], u), mix(a[1], b[1], u))], "5faabd", 2.4
                        )
            px, py = iso(x + 68, y + 131, h + 13)
            d.line([(px - 4, py), (px + 18, py + 8), (px + 18, py + 13)], "647d79", 4)
            if t > 1 + i * 1.4:
                for k in range(3):
                    d.ell(
                        px + 18, py + 13 + ((t * 54 + k * 12) % 36), 2.1, 3.2, "57a9bd"
                    )
    d.txt(40, 36, "계단 텃밭", 26, "374c47")
    d.txt(40, 72, "물길", 14, "648986")
    for j in range(3):
        x = 589 + j * 40
        y = 373
        d.ell(x, y, 7, 10, "52a4b7" if t > 1 + j * 1.4 else "c7cec0")


def lathe(d, cx, cy, rings, cols, spin=0, tilt=0.26):
    # Surface of revolution, radius/elevation profile, sorted from back to near side.
    faces = []
    n = 68
    for j, ((r1, z1), (r2, z2)) in enumerate(zip(rings, rings[1:])):
        for i in range(n):
            aa = i * tau / n + spin
            bb = (i + 1) * tau / n + spin
            pts3 = [
                (r * cos(a), r * sin(a), z)
                for r, z, a in [(r1, z1, aa), (r1, z1, bb), (r2, z2, bb), (r2, z2, aa)]
            ]
            depth = sum(y for x, y, z in pts3) / 4
            a = (aa + bb) / 2
            light = (
                0.50
                + 0.39 * (1 + cos(a + 1.95)) / 2
                + 0.15 * max(0, cos(a + 2.45)) ** 20
            )
            base = rgba(cols[min(j, len(cols) - 1)])
            col = "".join(f"{min(255, int(c * 255 * light)):02x}" for c in base[:3])
            faces.append(
                (depth, [(cx + x, cy + y * tilt - z) for x, y, z in pts3], col)
            )
    for _, p, c in sorted(faces, key=lambda z: z[0]):
        d.poly(p, c, c, 0.55)


def teardown(d, t):
    d.grad(0, 0, 768, 432, [(0, "161c24"), (0.65, "29323a"), (1, "12191d")])
    d.ell(376, 372, 125, 15, "11181d")
    lift = span(t, 1.1, 4.8) * (1 - span(t, 6.25, 8.65))
    cx = 375
    cy = 339
    # Design source for a three-piece pour-over cup, in drawing units.
    lathe(
        d,
        cx,
        cy,
        [
            (0, 0),
            (55, 0),
            (65, 11),
            (68, 68),
            (73, 73),
            (65, 76),
            (59, 69),
            (55, 14),
            (0, 14),
        ],
        [
            "f2dfbf",
            "bd8462",
            "dc8e65",
            "b77451",
            "f6d7aa",
            "d4a280",
            "674d43",
            "9b745f",
        ],
    )
    d.ell(cx + 66, cy - 39, 27, 22, None, "b58261", 9)
    z = 82 + lift * 42
    lathe(
        d,
        cx,
        cy - z,
        [(0, 0), (84, 0), (87, 3), (84, 5), (0, 5)],
        ["93877c", "c4b3a0", "f3ddc3", "c7b7a2"],
    )
    for i in range(11):
        a = i * tau / 11 + t * 0.17
        d.ell(cx + cos(a) * 45, cy - z - 6 + sin(a) * 12, 3, 1.1, "453e37")
    z = 88 + lift * 110
    lathe(
        d,
        cx,
        cy - z,
        [(28, 0), (32, 4), (88, 86), (91, 91), (87, 95), (82, 91), (27, 10), (24, 6)],
        ["c3d2bd", "9bb6a3", "c2d2be", "e6eedb", "cedbc8", "91aa98", "4b6257"],
    )
    for j in range(17):
        a = j * pi / 16
        d.line(
            [
                (cx + 32 * cos(a), cy - z - 4 + 7 * sin(a)),
                (cx + 86 * cos(a + 0.08), cy - z - 84 + 22 * sin(a + 0.08)),
            ],
            "91ae9999",
            1.1,
        )
    if lift > 0.35:
        for y, name, num in [
            (cy - z - 55, "도자기 드리퍼", "01"),
            (cy - 82 - lift * 42, "받침판", "02"),
            (cy - 41, "잔", "03"),
        ]:
            d.line([(cx + 93, y), (532, y - 12), (564, y - 12)], "9caa9e", 0.85)
            d.txt(574, y - 21, name, 15, "e7e6d8")
    d.txt(39, 42, "세 겹의 커피 잔", 23, "e2e5dc")


def hardcore_info(d, t):
    d.bg("f4f1e7")
    ink = "30332f"
    weak = "b4b4a8"
    accent = "dc5d38"
    b, u = phase(t)
    d.txt(37, 34, "피리 속 바람", 27, ink)
    d.rect(37, 75, 694, 1, ink)
    with d.at(379, 214, 1 + 0.13 * span(t, 2, 5), -0.09):
        body = "M -249 -16 L -166 -36 Q -152 -45 -124 -40 L 181 -30 Q 220 -31 238 -44 L 245 -40 L 245 42 Q 223 32 181 32 L -153 41 L -249 21 Z"
        d.path(body, "e3e0d4", ink, 2)
        with d.clip(body):
            hatch(d, -250, -49, 500, 100, 7, "a6a695")
            d.path(
                "M -256 -2 L -182 -9 L -144 -8 L -111 -20 L 243 -21 L 248 23 L -145 23 L -169 6 L -255 8 Z",
                "f8f6ed",
                ink,
                1.5,
            )
            for i in range(6):
                x = -52 + i * 39
                d.rect(x, -41, 10, 24, "faf8ef", ink, 1)
            if t > 1.5:
                for k in range(3):
                    p = []
                    for i in range(109):
                        x = -248 + i * 4.6
                        y = (k - 1) * 3 + sin(x * 0.045 - t * 6 + k) * min(
                            8, max(0, (x + 160) / 6)
                        )
                        p.append((x, y))
                    end = max(2, int(len(p) * ramp(t, 1.5, 4.5)))
                    d.line(p[:end], accent, 1.55)
                for j in range(7):
                    x = -243 + (j * 76 + t * 74) % 485
                    d.poly([(x - 4, -3), (x + 4, 0), (x - 4, 3)], accent)
        for i in range(3):
            x = [-191, -119, 111][i]
            d.line([(x, -41), (x + 15, -72), (x + 44, -72)], ink, 0.9)
            d.circ(x + 52, -72, 9, "f4f1e7", ink, 1)
            d.txt(x + 52, -78, str(i + 1), 9, ink, "mono", "center")
    d.txt(39, 355, ["취구", "바람길", "진동"][b], 25, accent)
    for i in range(3):
        x = 435 + i * 91
        d.line(
            [
                (x + j, 367 + sin(j * 0.17 - t * 5) * ((i + 1) * 3 if t > 3 else 1))
                for j in range(76)
            ],
            accent if i <= b else weak,
            1.3,
        )


def precise_mechanism(d, t):
    d.bg("ecebdc")
    ink = "334144"
    mint = "82a7a1"
    blue = "476e8c"
    red = "d86b4e"
    cx = 246
    cy = 237
    d.txt(43, 37, "회전을 왕복으로", 27, ink)
    d.rect(106, 308, 559, 17, "c4c4ae")
    d.rect(106, 325, 559, 8, "a9ad98")
    for x in (433, 573):
        d.poly([(x, 308), (x + 14, 253), (x + 43, 253), (x + 53, 308)], mint, ink, 1.3)
    d.rect(404, 219, 252, 10, blue)
    d.rect(404, 252, 252, 10, blue)
    for j in range(19):
        d.line([(413 + j * 13, 264), (413 + j * 13, 269 + j % 5 * 2)], ink, 1)
    theta = t * tau / 3
    radius = 57
    rod = 242
    px = cx + radius * cos(theta)
    py = cy + radius * sin(theta)
    sx = px + sqrt(rod**2 - (py - cy) ** 2)
    for k, col in [(89, "bac4b6"), (82, blue), (67, "e7e7d8")]:
        d.circ(cx, cy, k, col, ink, 1.3)
    for i in range(5):
        a = theta + i * tau / 5
        d.line(
            [
                (cx + 15 * cos(a), cy + 15 * sin(a)),
                (cx + 72 * cos(a), cy + 72 * sin(a)),
            ],
            blue,
            10,
        )
    d.circ(cx, cy, 18, blue, ink, 1.2)
    d.line([(cx, cy), (px, py)], red, 18)
    d.rect(sx - 28, 218, 56, 39, "dfab67", ink, 1.6)
    d.line([(px, py), (sx, cy)], ink, 15)
    d.line([(px, py), (sx, cy)], "e2c999", 11)
    for x, y in [(cx, cy), (px, py), (sx, cy)]:
        d.circ(x, y, 6, "eef0db", ink, 1.6)
        d.circ(x, y, 2, ink)
    b, u = phase(t)
    tx, ty = [(cx - 54, cy - 57), (px, py), (sx, cy)][b]
    d.line([(tx, ty), (tx + 14, 105), (tx + 58, 105)], red, 1)
    d.txt(tx + 60, 94, ["바퀴", "연결봉", "미끄럼판"][b], 15, red)


def instruction_manual(d, t):
    d.bg("f9f7ee")
    k = "292b28"
    white = "fffef6"
    b, u = phase(t)
    d.txt(43, 31, "책 받침 조립", 25, k)
    d.rect(43, 69, 682, 1, k)
    for j in range(3):
        d.circ(68 + j * 48, 105, 13, k if j == b else white, k, 1)
        d.txt(68 + j * 48, 99, str(j + 1), 12, white if j == b else k, "mono", "center")
    # Slotted back plate and two cross feet. Projection fixed to the page.
    with d.at(409, 243, 1, -0.04):
        for j in range(2):
            x = -87 + j * 124
            y = 30 + j * 23
            d.poly(
                [(x - 52, y + 24), (x + 6, y - 13), (x + 77, y + 5), (x + 17, y + 44)],
                white,
                k,
                2,
            )
            d.poly(
                [
                    (x - 52, y + 24),
                    (x + 17, y + 44),
                    (x + 17, y + 54),
                    (x - 52, y + 34),
                ],
                white,
                k,
                1.5,
            )
            d.line([(x - 2, y + 13), (x + 22, y + 20)], k, 4)
        h = 78 * (1 - span(t, 2.7, 5.9))
        for x in (-87, 37):
            rule(d, x, 32, x, -80, k)
        with d.at(0, -h):
            d.poly([(-111, -89), (100, -36), (83, 63), (-130, 10)], white, k, 2)
            d.poly([(-111, -89), (-106, -94), (106, -41), (100, -36)], white, k, 1.3)
            for x in [-81, 43]:
                y = (x + 110) * 0.25
                d.poly(
                    [
                        (x - 8, y + 7),
                        (x - 11, y + 22),
                        (x + 2, y + 24),
                        (x + 6, y + 10),
                    ],
                    white,
                    k,
                    1.4,
                )
        if t > 5.9:
            with d.at(0, -38 * (1 - span(t, 5.9, 7.5))):
                d.path(
                    "M -98 -69 Q -52 -73 -4 -37 Q 46 -43 93 -17 L 73 43 Q 32 20 -15 22 Q -60 -11 -119 -9 Z",
                    white,
                    k,
                    2,
                )
                d.line([(-4, -37), (-15, 22)], k, 1.6)
                for i in range(4):
                    d.path(
                        f"M -88 {-53 + i * 8} Q -59 {-54 + i * 8} -20 {-32 + i * 8} M 10 {-27 + i * 8} Q 38 {-28 + i * 8} 67 {-13 + i * 8}",
                        None,
                        k,
                        0.8,
                    )
    if b == 1:
        d.line([(199, 153), (199, 224)], k, 3)
        d.poly([(188, 211), (199, 229), (211, 211)], k)
    d.txt(43, 364, ["발 두 개를 나란히", "홈에 맞춰 내리기", "책 펼치기"][b], 18, k)


@lru_cache(1)
def survey():
    traces = []
    for j in range(22):
        a = []
        r = 11 + j * 4.4
        for i in range(121):
            ang = i * tau / 120
            v = r * (
                1
                + 0.14 * sin(3 * ang + 0.3)
                + 0.13 * cos(5 * ang)
                + 0.07 * sin(7 * ang + j * 0.06)
            )
            a.append((365 + v * 1.68 * cos(ang), 220 + v * 0.96 * sin(ang)))
        traces.append((a, "597980" if j > 13 else "786d54"))
    traces.append(
        (
            [(167 + i * 3, 302 - i * 0.63 + 10 * sin(i * 0.12)) for i in range(130)],
            "bb5943",
        )
    )
    return traces


def pen_plotter(d, t):
    d.bg("4c3b32")
    d.rect(30, 25, 706, 379, "b8ad94")
    d.rect(44, 35, 677, 355, "f1ecd8")
    d.rect(65, 54, 633, 317, None, "c6bda4", 1)
    d.txt(80, 69, "섬의 등고선", 20, "5d6257")
    d.txt(673, 343, "1 : 500", 13, "5d6257", "mono", "right")
    paths = survey()
    n = clamp(t / 8.55) * len(paths)
    end = (365, 220)
    for j, (p, c) in enumerate(paths):
        if j > n:
            break
        count = max(1, min(len(p), int((n - j) * len(p))))
        end = p[count - 1]
        if count > 1:
            d.line(p[:count], c, 1.2 if j % 5 else 1.9)
    x, y = end
    d.rect(x - 9, 31, 18, 360, "574f463a")
    d.rect(x - 6, 23, 12, 375, "adb1a4")
    d.rect(x - 3, 23, 3, 375, "e1e1d1")
    d.rect(x - 15, y - 28, 30, 28, "374041")
    d.rect(x - 10, y - 24, 20, 11, "687675")
    d.poly([(x - 4, y), (x, y + 4), (x + 4, y)], "303330")
    for a in [26, 390]:
        d.rect(30, a, 706, 6, "7c7c71")


def assembly_line_diagram(d, t):
    # The carrier moves through the cutaway; the camera moves to the working station.
    zoom = 1 + 0.29 * span(t, 0.35, 1.8) - 0.29 * span(t, 7.35, 8.75)
    track = mix(158, 602, span(t, 0.65, 7.75))
    with d.at((1 - zoom) * track, (1 - zoom) * 243, zoom):
        bakery(d, t)
    d.rect(0, 378, 768, 54, "e9dbbc")
    d.txt(42, 389, "빵이 지나가는 집", 22, "383e3c")
    d.txt(721, 394, ["가루", "반죽", "오븐"][phase(t)[0]], 16, "594f40", align="right")


def bakery(d, t):
    d.bg("e9dbbc")
    k = "383e3c"
    o = "cd744e"
    y = "e4b962"
    mint = "88ad99"
    # A dollhouse bakery with three working bays underneath a sawtooth roof.
    d.poly(
        [
            (42, 144),
            (42, 103),
            (130, 77),
            (130, 104),
            (236, 77),
            (236, 104),
            (341, 77),
            (341, 104),
            (446, 77),
            (446, 104),
            (551, 77),
            (551, 104),
            (651, 77),
            (651, 104),
            (724, 104),
            (724, 144),
        ],
        k,
    )
    for i in range(3):
        x = 44 + i * 226
        d.rect(x, 143, 222, 197, ["b5c1a9", "dfca9e", "c4b6a5"][i], k, 3)
        d.rect(x + 10, 151, 34, 20, k)
        d.txt(x + 27, 156, "0" + str(i + 1), 10, "fff2cd", "mono", "center")
        for j in range(5):
            d.rect(x + 11 + j * 42, 322, 28, 4, k)
    d.rect(43, 340, 681, 14, k)
    d.rect(43, 355, 681, 4, o)
    # grain hopper with auger, spiral kneader, fired arch
    d.poly([(90, 179), (201, 179), (176, 220), (159, 235), (144, 235)], "e0b664", k, 3)
    d.line([(151, 234), (151, 254)], k, 7)
    for j in range(8):
        d.circ(150 + sin(j * 2 + t * 3) * 5, 238 + (j * 6 + t * 34) % 31, 1.6, "f8e6b4")
    d.path("M 304 244 Q 305 296 368 296 Q 409 295 422 244 Z", mint, k, 3)
    d.line([(324, 234), (324, 192), (378, 192), (378, 230)], k, 8)
    for j in range(3):
        d.ell(378, 226 + j * 8, 7 + 3 * sin(t * 5 + j), 4, None, k, 2)
    d.path(
        "M 537 286 L 537 225 Q 541 186 600 186 Q 655 189 660 230 L 660 287 Z", o, k, 4
    )
    d.path("M 554 274 L 554 239 Q 556 209 601 209 Q 640 209 643 241 L 643 274 Z", k)
    for j in range(4):
        d.path(
            f"M {561 + j * 21} 267 Q {556 + j * 21} 251 {565 + j * 21} {239 - 7 * sin(t * 4 + j)} Q {566 + j * 21} 253 {573 + j * 21} 267 Z",
            y,
        )
    d.rect(64, 299, 644, 11, k)
    for j in range(34):
        d.circ(70 + j * 19, 304, 3, "aaae92")
    x = 83 + 600 * span(t, 0, 8.7)
    d.ell(
        x,
        292,
        17 + 9 * span(t, 3, 6),
        7 + 10 * span(t, 5.6, 7.8),
        y if t < 6 else "cd8648",
        k,
        2,
    )
    if t > 5:
        for i in [-1, 0, 1]:
            d.line([(x + i * 9 - 2, 283), (x + i * 9 + 2, 289)], "f4d798", 1.4)
