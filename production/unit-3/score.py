"""Original cues in seconds, MIDI pitch and beat-space. No recordings or external instruments."""

import wave, zlib
import numpy as np
from drawing import TAU

# root / seconds per pulse / pitch contour / voice / scene-synchronous foley and times
CUES = {
    "dark-keynote": (
        48,
        0.50,
        [0, 7, 12, 7, 2, 9, 14, 9],
        "mallet",
        "click",
        [0.5, 2.5, 4.5, 6.5, 7.5],
    ),
    "living-screencast": (
        62,
        0.40,
        [0, 4, 7, 11, 9, 7, 4, 2],
        "pixel",
        "drop",
        [1.1, 3, 3.6, 4.25, 4.85, 5.5, 6.1, 7.7],
    ),
    "hologram-hud": (
        43,
        0.60,
        [0, 7, 12, 14, 7, 5],
        "glass",
        "scan",
        [0.3, 2, 4.1, 6.2, 8.2],
    ),
    "desktop-flythrough": (
        57,
        0.42,
        [0, 3, 7, 10, 14, 10, 7, 3],
        "wood",
        "tap",
        [0.65, 2.9, 3.65, 5.35, 6.8, 8.1],
    ),
    "spreadsheet": (
        55,
        0.31,
        [0, 2, 5, 7, 10, 7, 5, 2],
        "key",
        "click",
        [0.4, 1, 2.8, 3, 4.3, 5.7, 6.8, 7.9],
    ),
    "one-bit-dither": (
        47,
        0.66,
        [0, 0, 7, 5, 3, 2],
        "felt",
        "brush",
        [0.4, 2.4, 3.1, 4.7, 5.3, 6.7, 8.1],
    ),
    "circuit-board": (
        48,
        0.375,
        [0, 7, 12, 15, 12, 7, 5, 3],
        "pulse",
        "relay",
        [0.1, 2.4, 4.8, 6, 6.4, 6.8, 7.2, 7.6],
    ),
    "firefly-pointillism": (
        67,
        0.64,
        [0, 7, 12, 14, 11, 7, 4, 2],
        "harp",
        "air",
        [1.65, 3.2, 5.8, 7.6],
    ),
    "flow-field": (
        41,
        0.81,
        [0, 7, 10, 5, 2, 5],
        "reed",
        "air",
        [0.3, 2.1, 4.8, 7.3, 8.9],
    ),
    "oscilloscope-math": (
        52,
        0.72,
        [0, 12, 7, 0, 7, 12],
        "sine",
        "scan",
        [0.3, 2, 4, 5.7, 7.5],
    ),
    "neon-tubes": (
        45,
        0.40,
        [0, 7, 3, 10, 7, 5, 2, 7],
        "pulse",
        "relay",
        list(np.arange(0.4, 9, 0.4)),
    ),
    "brick-toy": (
        62,
        0.48,
        [0, 4, 7, 12, 9, 4, 7, 2],
        "wood",
        "tap",
        [0.6, 1.3, 2.2, 3, 5.1, 6.3, 8.8],
    ),
    "paper-popup": (
        64,
        0.60,
        [0, 3, 7, 10, 7, 5, 3, 2],
        "harp",
        "brush",
        [0.4, 1.1, 2.2, 3.1, 5.4, 7.9],
    ),
    "tilt-shift": (
        55,
        0.33,
        [0, 4, 5, 7, 12, 5, 9, 7],
        "mallet",
        "water",
        [0.6, 2.1, 4.3, 5.1, 7, 8.7],
    ),
    "lowpoly-island": (
        60,
        0.46,
        [0, 2, 7, 9, 12, 14, 9, 7],
        "wood",
        "drop",
        [0.1, 0.45, 0.75, 1.3, 2.7, 3.5, 4.7, 6.35],
    ),
    "glass-product": (
        50,
        0.83,
        [0, 7, 19, 14, 12, 7],
        "glass",
        "glass",
        [1.1, 2.1, 4.4, 6.2, 8.8],
    ),
    "memphis-diorama": (
        60,
        0.45,
        [0, 4, 9, 7, 2, 5, 9, 4],
        "felt",
        "tap",
        [1.5, 2.7, 4.4, 6.1, 8],
    ),
    "isometric-picture-book": (
        58,
        0.56,
        [0, 7, 9, 4, 2, 5, 7, 12],
        "felt",
        "foot",
        [0.8, 1.3, 2, 2.7, 3.5, 4.1, 6.7, 7.5, 8.5],
    ),
    "crayon-world": (
        62,
        0.46,
        [0, 2, 4, 9, 7, 2, 5, 4],
        "wood",
        "brush",
        [0.6, 1.4, 2.5, 3.8, 5.4, 6.8, 8.2],
    ),
    "satellite-briefing": (
        43,
        0.90,
        [0, 7, 12, 14, 7],
        "glass",
        "scan",
        [0.2, 2.2, 4.6, 6.1, 8.2],
    ),
    "briefing-board": (
        53,
        0.65,
        [0, 5, 7, 3, 2, 0],
        "felt",
        "tap",
        [0.5, 1.4, 2.3, 3.8, 5.6, 7.2],
    ),
    "lidar-survey": (
        42,
        0.72,
        [0, 12, 7, 14, 12, 5],
        "sine",
        "scan",
        [0.3, 2.1, 4.2, 6.1, 8.4],
    ),
    "microscope": (
        65,
        0.93,
        [0, 5, 7, 12, 7, 3],
        "glass",
        "relay",
        [0.7, 2.4, 4.3, 6.3, 8.6],
    ),
    "archive-lighttable": (
        54,
        0.74,
        [0, 7, 3, 5, 2, 0],
        "felt",
        "brush",
        [0.7, 2.6, 4.2, 6.4, 8.1],
    ),
    "security-xray": (
        46,
        0.55,
        [0, 5, 12, 7, 3, 5],
        "sine",
        "relay",
        [0.4, 2.4, 4.3, 6.4, 8.1],
    ),
    "dark-documentary": (
        38,
        0.82,
        [0, 5, 7, 3, 0, 7],
        "reed",
        "water",
        [0.2, 2.8, 4.9, 6.6, 8.7],
    ),
    "thermal-camera": (
        47,
        0.75,
        [0, 7, 2, 5, 0, 12],
        "sine",
        "drop",
        [0.4, 2.6, 3.7, 4.9, 6.4, 8.1],
    ),
    "dataviz": (
        59,
        0.39,
        [0, 2, 3, 7, 8, 7, 5, 2],
        "wood",
        "brush",
        [0.4, 1.7, 3.1, 4.7, 6.3, 8.5],
    ),
    "white-model": (
        42,
        0.86,
        [0, 7, 12, 5, 9, 7],
        "glass",
        "relay",
        [0.5, 2.5, 4.5, 6.5, 8.5],
    ),
    "data-physical": (
        55,
        0.48,
        [0, 3, 5, 7, 10, 12, 7, 5],
        "mallet",
        "tap",
        [0.3, 1.3, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3],
    ),
    "transit-map": (
        60,
        0.44,
        [0, 4, 7, 9, 5, 2, 7, 12],
        "harp",
        "click",
        [0.4, 1.5, 2.6, 3.8, 5.2, 6.4, 7.6, 8.8],
    ),
    "map-explainer": (
        48,
        0.67,
        [0, 5, 7, 12, 7, 3],
        "harp",
        "air",
        [0.4, 2.3, 4.1, 6.2, 8.4],
    ),
    "pip-simulation": (
        63,
        0.36,
        [0, 3, 7, 10, 5, 3, 2, 7],
        "wood",
        "foot",
        [0.5, 1.4, 2.8, 3.7, 5.1, 6.4, 7.7, 8.5],
    ),
}


def make(slug, duration, dest):
    root, beat, notes, voice, fx, events = CUES[slug]
    sr = 32000
    rng = np.random.default_rng(zlib.crc32(slug.encode()))
    out = np.zeros((int(duration * sr), 2))

    def add(t, s, pan=0):
        idx = round(t * sr)
        n = min(len(s), len(out) - idx)
        if n > 0:
            out[idx : idx + n] += s[:n, None] * np.array(
                [1 - pan * 0.34, 1 + pan * 0.34]
            )

    def note(freq, voice, dur):
        x = np.arange(int(dur * sr)) / sr
        phase = TAU * freq * x
        decay = {
            "glass": 2.8,
            "felt": 4,
            "harp": 4.1,
            "sine": 3,
            "wood": 12,
            "mallet": 7,
            "reed": 2.5,
            "pixel": 8,
            "pulse": 7,
            "key": 11,
        }[voice]
        if voice in ("glass", "mallet", "wood"):
            s = (
                np.sin(phase)
                + 0.35
                * np.sin(phase * ({"glass": 2.71, "wood": 3.85, "mallet": 3.01}[voice]))
                * np.exp(-x * 9)
                + 0.12 * np.sin(phase * 5.04)
            )
        elif voice in ("key", "pixel", "pulse"):
            s = (
                np.sin(phase)
                + 0.33 * np.sin(phase * 3)
                + 0.17 * np.sin(phase * 5) * np.exp(-x * 4)
            )
        elif voice == "reed":
            s = (
                np.sin(phase + 0.15 * np.sin(30 * x))
                + 0.17 * np.sin(phase * 2)
                + 0.09 * np.sin(phase * 3)
            )
        else:
            s = (
                np.sin(phase)
                + 0.26 * np.sin(2 * phase) * np.exp(-x * 3)
                + 0.15 * np.sin(3 * phase) * np.exp(-x * 7)
            )
        return (
            s
            * np.minimum(1, x / (0.035 if voice in ("reed", "sine") else 0.008))
            * np.exp(-x * decay)
            * np.minimum(1, (dur - x) / 0.09)
        )

    for j, t in enumerate(np.arange(0.16, duration - 0.45, beat)):
        ix = (j + (1 if t > 6.5 else 0)) % len(notes)
        f = 440 * 2 ** ((root + notes[ix] - 69) / 12)
        add(t, note(f, voice, 1.45) * (0.16 if j % 4 else 0.21), np.sin(j * 1.6) * 0.8)
        if j % 4 == 0:
            add(t, note(f / 2, "sine", 1.8) * 0.10)
        if j % 4 == 2 and t > 3:
            add(t + beat * 0.5, note(f * 1.5, voice, 0.8) * 0.065, 0.7)
    for j, t in enumerate(events):
        dur = 0.67 if fx in ["water", "air", "brush", "scan", "glass"] else 0.21
        x = np.arange(int(sr * dur)) / sr
        n = rng.normal(0, 1, len(x))
        f = 450 + 70 * (j % 4)
        if fx in ["water", "drop"]:
            v = np.sin(TAU * (f * x + 360 * x * x)) * np.exp(
                -x * 18
            ) + 0.15 * n * np.exp(-x * 35)
        elif fx == "scan":
            v = np.sin(TAU * (650 * x + 320 * x * x)) * np.exp(
                -x * 9
            ) + 0.13 * n * np.exp(-x * 18)
        elif fx == "glass":
            v = note(1200 + 50 * j, "glass", dur)
        elif fx in ["air", "brush"]:
            v = (
                np.convolve(n, np.ones(9) / 9, "same") if fx == "air" else n * 0.45
            ) * np.sin(np.pi * x / dur) ** 2
        else:
            v = 0.65 * n * np.exp(-x * (90 if fx == "foot" else 180)) + np.sin(
                TAU * (140 if fx == "tap" else 320) * x
            ) * np.exp(-x * 42)
        add(t, v * 0.19, (-1) ** j * 0.6)
    x = np.arange(len(out)) / sr
    if slug == "oscilloscope-math":

        def smooth(a, b):
            u = np.clip((x - a) / (b - a), 0, 1)
            return u * u * (3 - 2 * u)

        for i, f in enumerate(
            [1 + smooth(2, 4) + smooth(5.7, 7.5), 1 + smooth(5.7, 7.5)]
        ):
            out[:, i] += 0.044 * np.sin(TAU * 110 * np.cumsum(f) / sr)
    if slug in ["neon-tubes", "archive-lighttable", "thermal-camera", "white-model"]:
        out += 0.014 * np.sin(TAU * 100 * x)[:, None]
    out *= (
        np.minimum(1, x / 0.05)[:, None] * np.minimum(1, (duration - x) / 0.55)[:, None]
    )
    out *= 0.78 / max(0.01, np.max(abs(out)))
    with wave.open(str(dest), "wb") as w:
        w.setparams((2, 2, sr, 0, "NONE", "not compressed"))
        w.writeframes(np.int16(out * 32767).tobytes())
