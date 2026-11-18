"""Render assigned slugs with local Python and FFmpeg. Pass one or more slugs, or no arguments for all."""

import argparse, importlib, json, os, subprocess, tempfile, time
from pathlib import Path
from drawing import ROOT, W, H
from score import make

SLUGS = json.loads((ROOT / "styles.json").read_text())
MEDIA = ROOT.parent.parent / "site" / "media"
FPS30 = {
    "living-screencast",
    "desktop-flythrough",
    "one-bit-dither",
    "circuit-board",
    "flow-field",
    "neon-tubes",
    "isometric-picture-book",
    "thermal-camera",
    "transit-map",
}
POSTERS = {
    "one-bit-dither": 6.8,
    "firefly-pointillism": 2.3,
    "glass-product": 5.1,
    "desktop-flythrough": 9.25,
    "oscilloscope-math": 8.55,
    "circuit-board": 8.2,
    "living-screencast": 8.7,
    "paper-popup": 4.5,
    "dark-keynote": 8,
    "archive-lighttable": 6.8,
    "satellite-briefing": 5.5,
    "dark-documentary": 8.3,
    "data-physical": 8.5,
    "dataviz": 8.6,
    "transit-map": 8.8,
    "crayon-world": 5.8,
    "pip-simulation": 6.3,
}


def scene(slug):
    i = SLUGS.index(slug)
    name = (
        "reel_a" if i < 8 else "reel_b" if i < 16 else "reel_c" if i < 24 else "reel_d"
    )
    return getattr(importlib.import_module(name), slug.replace("-", "_"))


def render(slug):
    draw = scene(slug)
    fps = (
        60
        if slug in ["firefly-pointillism", "memphis-diorama"]
        else 30
        if slug in FPS30
        else 24
    )
    start = time.time()
    duration = 10
    with tempfile.TemporaryDirectory(dir=ROOT, prefix=".render-") as td:
        tmp = Path(td)
        sound = tmp / "sound.wav"
        video = tmp / "film.mp4"
        poster = tmp / "poster.jpg"
        make(slug, duration, sound)
        # A dense binary dither saturates the VBV budget. One encoding thread
        # makes the rate control repeatable through the last GOP.
        threads = "1" if slug == "one-bit-dither" else "2"
        cmd = [
            "ffmpeg",
            "-nostdin",
            "-v",
            "error",
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{W}x{H}",
            "-r",
            str(fps),
            "-i",
            "pipe:0",
            "-i",
            str(sound),
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-c:v",
            "libx264",
            "-threads",
            threads,
            "-preset",
            "veryfast",
            "-crf",
            "21",
            "-maxrate",
            "2300k",
            "-bufsize",
            "3600k",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "112k",
            "-movflags",
            "+faststart",
            str(video),
        ]
        with subprocess.Popen(cmd, stdin=subprocess.PIPE) as proc:
            try:
                for frame in range(duration * fps):
                    proc.stdin.write(draw(frame / fps).tobytes())
            finally:
                proc.stdin.close()
            if proc.wait():
                raise RuntimeError(slug)
        subprocess.run(
            [
                "ffmpeg",
                "-nostdin",
                "-v",
                "error",
                "-y",
                "-ss",
                str(POSTERS.get(slug, 6.7)),
                "-i",
                str(video),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(poster),
            ],
            check=True,
        )
        os.replace(video, MEDIA / (slug + ".mp4"))
        os.replace(poster, MEDIA / (slug + ".jpg"))
    print(f"{slug}  {fps} fps  {time.time() - start:.1f}s", flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("slugs", nargs="*")
    args = p.parse_args()
    for slug in args.slugs or SLUGS:
        if slug not in SLUGS:
            p.error("unassigned slug: " + slug)
        render(slug)
