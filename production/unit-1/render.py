"""Run python3 render.py all, or supply any assigned slug(s)."""

import argparse, json, os, subprocess, tempfile, sys
from pathlib import Path
from functools import lru_cache
import importlib
import numpy as np
from drawing import Canvas, W, H, rnd
from score import synth

HERE = Path(__file__).resolve().parent
MEDIA = HERE.parents[1] / "site/media"
SLUGS = json.loads((HERE / "styles.json").read_text())
FPS = 24
POSTERS = [
    6.9,
    5.4,
    6.7,
    7.0,
    6.85,
    7.2,
    5.75,
    7.5,
    7.7,
    7.8,
    6.7,
    7.15,
    7.8,
    8.5,
    8,
    8,
    8,
    7.7,
    7.65,
    8,
    7.1,
    6.15,
    6.7,
    7.4,
    7.1,
    5.8,
    7.5,
    6.85,
    7.9,
    7.4,
    7.9,
    7.8,
    6.45,
]


@lru_cache(maxsize=33)
def grain(index):
    r = rnd(1910 + index)
    power = 1.7 if index < 8 else 4.1
    if index in [8, 12, 15, 27, 29]:
        power = 6.4
    g = r.normal(0, power, (H, W)).astype(np.int16)
    if index in (8, 9, 11, 12, 20, 22, 26, 30):
        for i in range(1600):
            x, y = r.integers([0, 0], [W - 10, H])
            g[y, x : x + r.integers(2, 10)] -= r.integers(3, 13)
    if index in (22, 29, 32):
        x, y = np.meshgrid(np.arange(W), np.arange(H))
        g += (2 * np.sin(y * 2.1 + 0.7 * np.sin(x * 0.017))).astype(np.int16)
    return g[:, :, None]


def getscene(index):
    module = "broadcast" if index < 8 else "studio" if index < 20 else "prints"
    return getattr(importlib.import_module(module), SLUGS[index].replace("-", "_"))


def frame(index, t):
    c = Canvas()
    try:
        getscene(index)(c, t)
        arr = np.clip(c.buf[:, :, :3].astype(np.int16) + grain(index), 0, 255).astype(
            np.uint8
        )
        return arr.tobytes()
    finally:
        c.close()


def render(slug):
    i = SLUGS.index(slug)
    with tempfile.TemporaryDirectory(dir=HERE) as tmp:
        tmp = Path(tmp)
        wav = tmp / "score.wav"
        video = tmp / "film.mp4"
        jpg = tmp / "poster.jpg"
        synth(i, wav)
        args = [
            "ffmpeg",
            "-v",
            "error",
            "-y",
            "-f",
            "rawvideo",
            "-pixel_format",
            "bgr24",
            "-video_size",
            f"{W}x{H}",
            "-framerate",
            str(FPS),
            "-i",
            "pipe:0",
            "-i",
            str(wav),
            "-c:v",
            "libx264",
            "-threads",
            "2",
            "-preset",
            "veryfast",
            "-crf",
            "22",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "96k",
            "-movflags",
            "+faststart",
            str(video),
        ]
        proc = subprocess.Popen(args, stdin=subprocess.PIPE)
        try:
            for j in range(FPS * 9):
                proc.stdin.write(frame(i, j / FPS))
        finally:
            proc.stdin.close()
            status = proc.wait()
        if status:
            raise RuntimeError(status)
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-ss",
                str(POSTERS[i]),
                "-i",
                str(video),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(jpg),
            ],
            check=True,
        )
        os.replace(video, MEDIA / (slug + ".mp4"))
        os.replace(jpg, MEDIA / (slug + ".jpg"))
        print(slug, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slugs", nargs="+", choices=SLUGS + ["all"])
    args = parser.parse_args()
    for slug in SLUGS if "all" in args.slugs else args.slugs:
        render(slug)
