"""Cut a Korean teaser and social card from the released Astra films."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
SIZE = (960, 540)
FEATURES = [
    "text-flash-cuts",
    "ukiyoe",
    "teardown",
    "pixel-rpg",
    "stained-glass",
    "flow-field",
    "crayon-book",
    "art-deco",
]
BASE = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y"]


def font(path, size):
    return ImageFont.truetype(path, size)


def run(*args):
    subprocess.run([*BASE, *map(str, args)], check=True)


def cover(fontfile):
    img = Image.new("RGB", (1200, 630), "#211e1c")
    for i, slug in enumerate(FEATURES):
        x, y = 610 + (i % 2) * 284, 13 + (i // 2) * 151
        tile = ImageOps.fit(Image.open(SITE / f"media/{slug}.jpg"), (279, 147))
        img.paste(tile, (x, y))
    d = ImageDraw.Draw(img)
    d.text((42, 46), "ASTRA FILM LIBRARY", fill="#ff8e72", font=font(fontfile, 24))
    d.text((36, 143), "코난쌤", fill="#f6f3ec", font=font(fontfile, 82), stroke_width=1)
    d.text(
        (36, 242), "아스트라카", fill="#f6f3ec", font=font(fontfile, 82), stroke_width=1
    )
    d.text(
        (42, 411),
        "99가지 스타일로 만든 코드 필름",
        fill="#ffe8d7",
        font=font(fontfile, 33),
    )
    d.text(
        (42, 555),
        "github.com/jkf87/conan-astracar",
        fill="#ffad93",
        font=font(fontfile, 26),
    )
    img.save(SITE / "share.jpg", quality=90, optimize=True)
    return img


def build(fontfile):
    films = {r["slug"]: r for r in json.loads((SITE / "catalog.json").read_text())}
    cover(fontfile)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        parts = []
        for i, slug in enumerate(FEATURES):
            s = films[slug]
            img = Image.new("RGBA", SIZE)
            d = ImageDraw.Draw(img)
            d.rectangle((0, 455, 960, 540), fill=(22, 20, 20, 240))
            d.text((24, 462), s["nameKo"], font=font(fontfile, 33), fill="#fff4df")
            d.text((26, 507), s["titleKo"], font=font(fontfile, 18), fill="#ffc5a9")
            d.text(
                (932, 478),
                f"{i + 1:02} / 08",
                font=font(fontfile, 23),
                fill="#ff9a83",
                anchor="ra",
            )
            lower = tmp / f"{i}.png"
            img.save(lower)
            part = tmp / f"clip{i}.mp4"
            run(
                "-ss",
                round(s["seconds"] * 0.33, 3),
                "-i",
                SITE / f"media/{slug}.mp4",
                "-i",
                lower,
                "-t",
                "2.5",
                "-filter_complex",
                "[0:v]scale=960:540,fps=24,setsar=1[v];[v][1:v]overlay=0:0[out]",
                "-map",
                "[out]",
                "-map",
                "0:a:0",
                "-af",
                "afade=t=in:d=0.07,afade=t=out:st=2.34:d=0.16",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-crf",
                "20",
                "-c:a",
                "aac",
                "-ar",
                "48000",
                "-ac",
                "2",
                part,
            )
            parts.append(part)
        end = tmp / "end.mp4"
        run(
            "-loop",
            "1",
            "-framerate",
            "24",
            "-i",
            SITE / "share.jpg",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=48000:cl=stereo",
            "-t",
            "3",
            "-vf",
            "scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "20",
            "-c:a",
            "aac",
            end,
        )
        parts.append(end)
        listing = tmp / "parts.txt"
        listing.write_text("".join(f"file '{p.name}'\n" for p in parts))
        run(
            "-f",
            "concat",
            "-safe",
            "1",
            "-i",
            listing,
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            SITE / "trailer.mp4",
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--font",
        default="/System/Library/Fonts/AppleSDGothicNeo.ttc",
        help="Korean-capable TrueType/OpenType font",
    )
    build(parser.parse_args().font)
