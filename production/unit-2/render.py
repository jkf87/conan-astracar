"""Rebuild locally: python3 render.py [slug ...]. Run verify.py after all movies."""

from pathlib import Path
import argparse, json, subprocess, tempfile, importlib, sys, os

sys.dont_write_bytecode = True
from draw import Desk
from score import write_score

ROOT = Path(__file__).resolve().parent
MEDIA = ROOT.parents[1] / "site" / "media"
SLUGS = json.loads((ROOT / "styles.json").read_text())
POSTER = [
    1.85,
    4.75,
    7.3,
    4.46,
    7.8,
    5.0,
    6.87,
    7.4,
    4.3,
    5.2,
    5.6,
    7.7,
    5.5,
    4.85,
    5,
    6.81,
    7.94,
    8.73,
    5.62,
    4.5,
    4.6,
    4.5,
    6.9,
    7.45,
    7,
    7.5,
    4.72,
    5.6,
    6.4,
    4.7,
    4.8,
    6.8,
    5.8,
]


def render(slug):
    idx = SLUGS.index(slug)
    module = (
        "printroom"
        if idx < 10
        else "workshop"
        if idx < 18
        else "toon"
        if idx < 25
        else "afterhours"
    )
    scene = getattr(importlib.import_module(module), slug.replace("-", "_"))
    MEDIA.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="astra-u2-") as tmp:
        temp = Path(tmp)
        wav = temp / "score.wav"
        out = temp / "film.mp4"
        poster = temp / "poster.jpg"
        write_score(slug, wav)
        with subprocess.Popen(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-y",
                "-f",
                "rawvideo",
                "-pix_fmt",
                "bgra",
                "-s",
                "768x432",
                "-r",
                "24",
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
                "20",
                "-pix_fmt",
                "yuv420p",
                "-profile:v",
                "high",
                "-c:a",
                "aac",
                "-b:a",
                "96k",
                "-movflags",
                "+faststart",
                str(out),
            ],
            stdin=subprocess.PIPE,
        ) as enc:
            try:
                for n in range(216):
                    d = Desk()
                    scene(d, n / 24)
                    enc.stdin.write(d.image().data)
            finally:
                enc.stdin.close()
            if enc.wait():
                raise RuntimeError(slug)
        subprocess.run(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-y",
                "-ss",
                str(POSTER[idx]),
                "-i",
                str(out),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(poster),
            ],
            check=True,
        )
        import shutil

        for src, ext in [(out, "mp4"), (poster, "jpg")]:
            shutil.move(src, MEDIA / f"{slug}.{ext}")
    print(slug, flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("slugs", nargs="*")
    args = p.parse_args()
    for name in args.slugs or SLUGS:
        render(name)
