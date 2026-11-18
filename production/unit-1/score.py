"""Original nine-second miniature scores. Scale degrees, phrases and foley are written per film."""

import wave
import numpy as np
from drawing import TAU

# tonic (MIDI), beat length, timbre, intervals, event sounds and their times.
SCORES = [
    (
        55,
        0.43,
        "pluck",
        [0, 7, 10, 12, 7, 3],
        "pop",
        [2.8, 3.6, 4.1, 4.4, 4.8, 5.2, 5.65],
    ),
    (58, 0.32, "reed", [0, 4, 7, 9, 7, 5, 4, 2], "click", [0.1, 2.5, 6.4]),
    (45, 0.5, "mallet", [0, None, 7, None, 12, None, 7, None], "bell", [7.32]),
    (52, 0.34, "keys", [0, 7, 12, 14, 16, 7, 11, 14], "rail", [0.1, 3.2, 5.9, 7.4]),
    (53, 0.87, "air", [0, None, None, 7, None], "chime", [3.25, 3.42, 3.6, 4.14]),
    (
        42,
        0.31,
        "bass",
        [0, 0, 7, 0, 3, 5, 7, 3],
        "press",
        [0.65, 1.24, 2.5, 3, 3.8, 4.6, 5.4, 6, 7.2, 8.4],
    ),
    (48, 0.49, "bass", [0, None, 3, 5, 7, None, 5, 3], "slide", [0.3, 2.85, 6.8]),
    (57, 0.35, "brass", [0, 4, 7, 12, None, 9, 7, 4], "tick", [0.2, 3, 6, 7.3]),
    (65, 0.48, "mallet", [0, 4, 7, 9, 7, 4, 2, 0], "rub", [0.2, 2.7, 5.3, 7.5]),
    (62, 0.73, "air", [0, 5, 9, 7, 4, 2], "drop", [1.0, 3.4, 5.2, 7.3]),
    (50, 0.47, "reed", [0, 3, 7, 10, 7, 5, 3], "brush", [0.5, 2.8, 4.5, 6.4]),
    (57, 0.44, "pluck", [0, 7, 4, 2, 9, 7, 4, 2], "bicycle", [1, 3.6, 6.3]),
    (60, 0.66, "keys", [0, 2, 5, 9, 7, 5, 2], "rub", [0.8, 3.3, 6.4]),
    (62, 0.57, "pluck", [0, 7, 12, 9, 5, 2, 0], "brush", [0.1, 3.1, 6.3]),
    (58, 0.43, "mallet", [0, None, 5, 7, 0, 9, 7, None], "tick", [1.9, 4.3, 6.8]),
    (48, 0.75, "keys", [0, 7, 12, 5, 9, 7], "rub", [0.1, 2.8, 5.8]),
    (64, 0.36, "pluck", [0, 2, 7, 4, 9, 7, 2, 4], "pen", [0.3, 2.8, 5.1, 7.5]),
    (
        54,
        0.46,
        "bass",
        [0, None, 7, 0, 5, None, 7, 12],
        "step",
        [1.2, 2.5, 3.6, 5.3, 7.2],
    ),
    (65, 0.52, "keys", [0, 4, 9, 7, 5, 2, 4], "brush", [0.15, 2.7, 4.2, 6.6]),
    (59, 0.54, "mallet", [0, 5, 2, 7, 4, 2], "pen", [0.2, 2.7, 5.4, 7.1]),
    (50, 0.91, "pluck", [0, 7, None, 12, 10, None, 5], "water", [0.1, 3.2, 5.8, 7.4]),
    (55, 0.45, "reed", [0, 2, 7, 9, 12, 7, 5, 2], "gong", [0.3, 3.5, 6.9]),
    (57, 0.53, "pluck", [0, 5, 7, 12, 10, 7, 5], "water", [0.4, 2.7, 5.1, 7.3]),
    (67, 0.34, "mallet", [0, 2, 7, 4, 7, 9, 7, 2], "snip", [0.5, 2.1, 3.8, 5.8, 7.2]),
    (51, 0.81, "air", [0, 7, 12, 14, 10, 7], "chime", [1.2, 4.2, 7.1]),
    (48, 0.92, "organ", [0, 7, 12, 4, 11, 7], "bell", [2.3, 5.4, 7.8]),
    (55, 0.52, "lute", [0, 7, 4, 9, 7, 2, 5, 4], "chime", [1.6, 4.3, 7.6]),
    (52, 0.37, "bass", [0, 0, 7, 10, None, 5, 7, 3], "press", [0.2, 2.9, 5.7]),
    (56, 0.42, "keys", [0, 3, 7, 5, 2, 5, 7, 10], "stamp", [0.4, 3.1, 6.2, 7.8]),
    (44, 0.65, "reed", [0, 5, 7, 3, 0, 7], "scrape", [0.5, 3.0, 4.8, 7.1]),
    (64, 0.62, "lute", [0, 4, 7, 11, 9, 7, 4], "pen", [0.2, 3.4, 5.6, 7.2]),
    (58, 0.4, "brass", [0, 7, 4, 12, 9, 7, 2, 5], "sweep", [0.3, 2.1, 4.2, 6.5]),
    (47, 0.69, "pluck", [0, 7, 12, None, 5, 9, 7], "rail", [0.8, 3.6, 5.7, 7.4]),
]


def synth(index, path):
    root, beat, voice, notes, fx, cues = SCORES[index]
    sr = 32000
    n = 9 * sr
    out = np.zeros(n)
    rng = np.random.default_rng(index + 400)

    def add(at, a):
        start = round(sr * at)
        length = min(len(a), n - start)
        if length > 0:
            out[start : start + length] += a[:length]

    harmonics = {
        "pluck": [1, 0.36, 0.18, 0.07],
        "lute": [1, 0.61, 0.26, 0.15, 0.07],
        "keys": [1, 0.42, 0.09],
        "mallet": [1, 0.12, 0.25],
        "reed": [1, 0.12, 0.31, 0.08, 0.12],
        "bass": [1, 0.58, 0.23],
        "air": [1, 0.15, 0.05],
        "brass": [1, 0.6, 0.33, 0.23],
        "organ": [1, 0.6, 0.25, 0.11],
    }
    for k, at in enumerate(np.arange(0.08, 8.8, beat)):
        note = notes[k % len(notes)]
        if note is None:
            continue
        f = 440 * 2 ** ((root + note - 69) / 12)
        sustained = voice in ("reed", "air", "organ", "brass")
        a = np.arange(int(sr * beat * (1.5 if sustained else 2.1))) / sr
        env = (1 - np.exp(-a * (22 if sustained else 260))) * np.exp(
            -a / beat * (1.9 if sustained else 3.6)
        )
        sig = sum(
            h * np.sin(TAU * f * j * a + 0.012 * np.sin(33 * a))
            for j, h in enumerate(harmonics[voice], 1)
        )
        add(at, 0.14 * env * sig)
        if k % 4 == 0:
            add(
                at,
                0.12
                * np.sin(TAU * (f / 2) * a)
                * np.exp(-a * 4)
                * (1 - np.exp(-a * 30)),
            )
    for at in cues:
        a = np.arange(int(sr * min(1.4, 9 - at))) / sr
        noise = rng.normal(0, 1, len(a))
        if fx in ("bell", "chime", "bicycle", "gong", "drop"):
            pitch = {
                "bell": 602,
                "chime": 950,
                "bicycle": 1300,
                "gong": 168,
                "drop": 760,
            }[fx]
            sig = sum(
                np.sin(TAU * pitch * r * a) * np.exp(-a * (2.5 + r)) / r
                for r in (1, 2.38, 3.82)
            )
        elif fx in ("pop", "stamp", "press", "step", "click", "tick", "snip"):
            sig = (
                0.7 * np.sin(TAU * (108 * a + 4 * (1 - np.exp(-a * 38)))) + 0.55 * noise
            ) * np.exp(-a * (24 if fx in ("press", "step") else 72))
        else:
            grain = np.convolve(noise, np.ones(15) / 15, mode="same")
            sig = (
                grain
                * np.sin(np.minimum(1, a / 0.5) * np.pi / 2)
                * np.exp(-a * 2.4)
                * (1 + 0.6 * np.sin(a * (38 if fx == "rail" else 17)))
            )
        add(at, 0.31 * sig * (1 - np.exp(-600 * a)))
    out[-int(sr * 0.35) :] *= np.linspace(1, 0, int(sr * 0.35))
    out *= 0.81 / max(0.25, np.abs(out).max())
    with wave.open(str(path), "wb") as w:
        w.setparams((1, 2, sr, 0, "NONE", "not compressed"))
        w.writeframes((out * 32767).astype("<i2").tobytes())
