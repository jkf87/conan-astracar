"""Decode the published shorts, check streams, motion, cover files and catalog membership."""

import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1] / "site"
MEDIA = ROOT / "media"


def ffmpeg(*args):
    return subprocess.check_output(
        ["ffmpeg", "-nostdin", "-v", "error", "-xerror", "-threads", "1", *args]
    )


def check(row):
    slug = row["slug"]
    video = MEDIA / (slug + ".mp4")
    poster = MEDIA / (slug + ".jpg")
    info = json.loads(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_streams", "-of", "json", video]
        )
    )
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next(s for s in info["streams"] if s["codec_type"] == "audio")
    if not (
        v["codec_name"] == "h264"
        and v["pix_fmt"] == "yuv420p"
        and a["codec_name"] == "aac"
    ):
        raise ValueError(f"Unexpected streams in {slug}")
    if (
        min(v["width"] / 768, v["height"] / 432) < 1
        or Fraction(v["avg_frame_rate"]) < 20
        or float(v["duration"]) < 8
        or abs(float(v["duration"]) - row["seconds"]) > 0.1
    ):
        raise ValueError(f"Unexpected format for {slug}")
    ffmpeg("-i", str(video), "-map", "0:v", "-map", "0:a", "-f", "null", "-")
    frames = ffmpeg(
        "-i",
        str(video),
        "-an",
        "-vf",
        "fps=2,scale=48:27,format=gray",
        "-f",
        "rawvideo",
        "-",
    )
    size = 48 * 27
    distinct = {frames[i : i + size] for i in range(0, len(frames), size)}
    if len(distinct) < 4:
        raise ValueError(f"No clear change across shots in {slug}")
    audio = ffmpeg(
        "-i", str(video), "-vn", "-ac", "1", "-ar", "8000", "-f", "s16le", "-"
    )
    if not any(audio):
        raise ValueError(f"Silent audio stream in {slug}")
    ffmpeg("-i", str(poster), "-f", "null", "-")
    return hashlib.sha256(video.read_bytes()).hexdigest()


if __name__ == "__main__":
    rows = json.loads((ROOT / "catalog.json").read_text())
    slugs = {r["slug"] for r in rows}
    if len(slugs) != 99 or len(rows) != 99 or len({r["category"] for r in rows}) != 15:
        sys.exit("Expected 99 unique films in 15 categories")
    for ext in ("mp4", "jpg"):
        if {p.stem for p in MEDIA.glob("*." + ext)} != slugs:
            sys.exit(f"Catalog differs from {ext} files")
    with concurrent.futures.ThreadPoolExecutor(4) as pool:
        hashes = list(pool.map(check, rows))
    if len(set(hashes)) != len(rows):
        sys.exit("Duplicate film files")
    print(f"{len(rows)} unique films decoded, with moving frames, audio, and posters.")
