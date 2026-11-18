"""Event scores in semitones, with synthesized foley. No samples or network services."""

import math, wave
import numpy as np

RATE = 32000
# Meter in seconds, MIDI root, instrument, melodic cells, bass punctuation, foley material.
SCORES = {
    "pop-art": (
        0.375,
        57,
        "brass",
        [0, 0, 7, None, 3, 10, None, 7],
        [-12, 0, -5, 3],
        "stamp",
    ),
    "vintage-collage": (
        0.53,
        64,
        "reed",
        [0, 4, 7, 9, 7, None, 4, 2],
        [0, -5],
        "paper",
    ),
    "swiss-motion": (
        0.5,
        48,
        "bar",
        [0, 7, 12, None, 0, None, 7, 14],
        [0, 0, -5, 2],
        "block",
    ),
    "spy-titles": (
        0.36,
        50,
        "brass",
        [0, 1, 7, None, 10, 9, 3, None],
        [0, 3, 5, 6],
        "brush",
    ),
    "art-deco": (0.47, 65, "reed", [0, 4, 7, 11, 14, 11, 9, 7], [0, -3, -5, 2], "bell"),
    "pictogram-motion": (
        0.375,
        58,
        "steel",
        [0, None, 5, 0, 7, None, 12, 10],
        [0, 5, 7, 5],
        "drum",
    ),
    "bauhaus-shapes": (
        0.54,
        61,
        "bar",
        [0, None, 7, None, 12, 7, 4, None],
        [0, 7],
        "block",
    ),
    "flat-space-explainer": (
        0.61,
        67,
        "glass",
        [0, 7, 12, 16, 14, 9, 7, None],
        [0, 5, 2],
        "bubble",
    ),
    "text-flash-cuts": (
        0.2,
        57,
        "wire",
        [0, 7, 3, 10, 1, 8, 3, 12],
        [0, 1, -2, 3],
        "snap",
    ),
    "silhouette-rhythm": (
        0.42,
        62,
        "steel",
        [0, 3, 7, 10, None, 7, 5, 3],
        [0, -2, -5, 0],
        "water",
    ),
    "blueprint": (
        0.34,
        62,
        "wire",
        [0, 4, 7, 12, 11, 7, 2, 5],
        [0, 2, -5, 0],
        "pencil",
    ),
    "iso-infographic": (
        0.48,
        60,
        "bar",
        [7, 4, 0, None, 9, 5, 2, 0],
        [0, 5, -3, 2],
        "water",
    ),
    "teardown": (
        0.72,
        54,
        "glass",
        [0, None, 7, 14, None, 12, 9, 7],
        [0, -5, 2],
        "metal",
    ),
    "hardcore-info": (0.52, 69, "flute", [0, 2, 4, 7, 9, 7, 4, 2], [0, -5], "air"),
    "precise-mechanism": (
        0.375,
        52,
        "wire",
        [0, 7, 0, 12, 2, 9, 2, 14],
        [0, 2],
        "tick",
    ),
    "instruction-manual": (
        0.63,
        65,
        "bar",
        [0, None, 4, 7, None, 9, 7, 4],
        [0, -5],
        "wood",
    ),
    "pen-plotter": (
        0.58,
        60,
        "glass",
        [0, None, 5, 7, 12, None, 7, 2],
        [0, 5],
        "motor",
    ),
    "assembly-line-diagram": (
        0.375,
        55,
        "reed",
        [0, 4, 3, 7, 5, 9, 7, 12],
        [0, 3, 5, 7],
        "drum",
    ),
    "rubber-hose": (0.33, 58, "reed", [0, 4, 7, 9, 10, 9, 7, 3], [0, 4, 7, 9], "brush"),
    "cel-anime-80s": (
        0.44,
        61,
        "pad",
        [0, 7, 11, 14, 12, 9, 7, 4],
        [0, -3, -5, -2],
        "train",
    ),
    "scifi-toon": (
        0.37,
        60,
        "slide",
        [0, 6, 9, None, 1, 7, 10, 13],
        [0, 1, 6, 0],
        "zap",
    ),
    "midcentury-toon": (
        0.45,
        65,
        "flute",
        [0, 3, 7, 10, 9, None, 5, 2],
        [0, -2, 3, 5],
        "brush",
    ),
    "comic-history": (0.4, 58, "reed", [0, 2, 5, 7, 9, 7, 5, 4], [0, 5, 7, 0], "paper"),
    "manga-panels": (
        0.3333,
        52,
        "guitar",
        [0, 7, 10, 5, 0, 3, 12, 10],
        [0, 3, -2, 5],
        "snare",
    ),
    "pixel-rpg": (0.3, 64, "chip", [0, 4, 7, 12, 11, 7, 4, 2], [0, -5, 5, 2], "chip"),
    "hd-2d": (0.61, 62, "harp", [0, 7, 10, 14, 12, 9, 5, 2], [0, 5, -2], "bell"),
    "microgame": (
        0.285,
        67,
        "chip",
        [0, 12, 7, 0, 3, 15, 10, 7],
        [0, 3, 5, 7],
        "click",
    ),
    "game-show": (
        0.375,
        60,
        "brass",
        [0, 0, 7, None, 7, 7, 12, None],
        [0, 7, 5, 7],
        "clap",
    ),
    "ascii-crt": (
        0.56,
        45,
        "pulse",
        [0, None, 7, 12, 3, None, 10, 7],
        [0, 3, 7, 0],
        "key",
    ),
    "silent-film": (
        0.32,
        62,
        "piano",
        [0, 4, 7, 12, 11, 9, 7, 4],
        [0, 7, 5, 2],
        "piano",
    ),
    "backrooms": (0.77, 38, "room", [], [], "room"),
    "scratch-film": (
        0.39,
        67,
        "steel",
        [0, 2, 7, None, 10, 12, 7, 2],
        [0, -5, 3, 0],
        "scratch",
    ),
    "double-exposure": (
        0.83,
        55,
        "bow",
        [0, 7, 10, None, 5, 9, 12, 7],
        [0, 5, -2],
        "shutter",
    ),
}


def write_score(slug, path):
    step, root, voice, mel, bass, material = SCORES[slug]
    rate = RATE
    length = 9
    total = length * rate
    mix = np.zeros(total)
    rng = np.random.default_rng(sum(ord(c) * (i + 1) for i, c in enumerate(slug)))

    def add(at, s):
        j = int(at * rate)
        if j >= total:
            return
        n = min(len(s), total - j)
        mix[j : j + n] += s[:n]

    def note(at, midi, duration, kind, vol):
        t = np.arange(int(duration * rate)) / rate
        freq = 440 * 2 ** ((midi - 69) / 12)
        ang = math.tau * freq * t
        a = np.sin(ang)
        h = np.sin(2 * ang)
        env = np.minimum(1, t / 0.009) * np.exp(-t / duration * 3)
        if kind in ["bar", "glass", "steel", "bell"]:
            s = (
                a
                + 0.39
                * np.sin(
                    ang
                    * ({"bar": 3.98, "glass": 2.72, "steel": 2.39, "bell": 4.22}[kind])
                )
                * np.exp(-t * 8)
                + 0.17 * np.sin(ang * 6.1) * np.exp(-t * 13)
            )
        elif kind in ["wire", "harp", "guitar", "piano"]:
            s = (
                a
                + 0.48 * h
                + 0.26 * np.sin(ang * 3.002) * np.exp(-t * 7)
                + 0.2 * np.sin(ang * 5.004) * np.exp(-t * 16)
            )
        elif kind in ["chip", "pulse"]:
            s = sum(np.sin(ang * k) / k for k in [1, 3, 5, 7, 9]) * 0.88
        elif kind == "bass":
            s = a + 0.24 * h
        elif kind == "slide":
            s = np.sin(ang + 2 * np.sin(t * 25) + 2 * np.exp(-t * 22))
        else:
            vib = ang + 0.035 * np.sin(t * 31)
            s = (
                np.sin(vib)
                + (0.47 if kind in ["reed", "brass"] else 0.15) * np.sin(3 * vib)
                + (0.32 if kind == "brass" else 0.12) * np.sin(vib * 2.003)
            )
            env = np.minimum(
                1, t / (0.16 if kind in ["bow", "pad"] else 0.042)
            ) * np.exp(-t / duration * 1.7)
        env *= np.minimum(1, (duration - t) / 0.035)
        add(at, vol * s * env)

    def fx(at, amp, how):
        d = {
            "room": 0.33,
            "train": 0.34,
            "paper": 0.18,
            "pencil": 0.2,
            "air": 0.35,
            "motor": 0.23,
            "water": 0.18,
            "brush": 0.16,
            "scratch": 0.16,
        }.get(how, 0.095)
        x = np.arange(int(rate * d)) / rate
        n = rng.normal(0, 1, len(x))
        bright = np.diff(n, prepend=0) * 0.45
        env = np.minimum(1, x / 0.002) * np.exp(-x / d * 5)
        if how in ["wood", "block", "tick", "key", "click", "piano"]:
            s = np.sin(x * math.tau * (820 if how == "tick" else 590)) + bright * 0.23
        elif how in ["bubble", "water", "zap", "chip"]:
            s = np.sin(math.tau * (400 * x + 2000 * x * x)) + 0.14 * bright
        elif how in ["stamp", "drum", "room"]:
            s = np.sin(
                math.tau * (61 * x + 0.5 * (1 - np.exp(-x * 47)))
            ) + 0.3 * np.convolve(n, np.ones(8) / 8, "same")
        elif how in ["metal", "bell"]:
            s = np.sin(x * 3812) + 0.6 * np.sin(x * 6179)
        elif how == "motor":
            s = 0.4 * np.sin(950 * x + 2 * np.sin(x * 265)) + 0.45 * bright
        else:
            s = bright * (0.55 + 0.45 * np.cos(x * 275) ** 2)
        add(at, amp * s * env)

    if voice == "room":
        t = np.arange(total) / rate
        mix += (
            0.064 * np.sin(math.tau * 60 * t)
            + 0.025 * np.sin(math.tau * 120 * t + 0.2 * np.sin(t))
            + 0.009 * rng.normal(0, 1, total)
        )
        for i in range(11):
            fx(0.4 + i * 0.76, 0.23, "room")
        for i in [2.8, 5.9, 8.3]:
            fx(i, 0.15, "snap")
    else:
        i = 0
        at = 0.03
        while at < 8.88:
            p = mel[i % len(mel)]
            section = min(2, int(at // 3))
            duration = step * (2.8 if voice in ["pad", "bow", "glass", "harp"] else 1.4)
            if p is not None:
                note(
                    at,
                    root + p + (12 if section == 2 and i % 5 == 0 else 0),
                    duration,
                    voice,
                    0.18,
                )
            if i % 2 == 0:
                note(
                    at,
                    root - 19 + bass[(i // 2) % len(bass)],
                    step * 1.75,
                    "bass",
                    0.19,
                )
            if i % 2 == 1 or voice in ["brass", "chip", "pulse", "wire"]:
                fx(at, 0.14, material)
            i += 1
            at += step * (0.87 if slug == "microgame" and section else 1)
        for j in [0, 3, 6, 8.52]:
            fx(j, 0.3, material)
        if voice in ["glass", "bow", "pad", "chip", "slide", "harp"]:
            delay = int(0.174 * rate)
            mix[delay:] += 0.18 * mix[:-delay].copy()
        note(8.52, root + 12, 0.48, voice, 0.17)
    mix *= np.minimum(1, np.arange(total) / (rate * 0.025)) * np.minimum(
        1, np.arange(total)[::-1] / (rate * 0.19)
    )
    mix = np.tanh(mix * 1.8)
    with wave.open(str(path), "wb") as w:
        w.setparams((1, 2, rate, 0, "NONE", ""))
        w.writeframes((mix * 29490).astype("<i2").tobytes())
