"""Check the delivered streams and build a poster index. All checks use final site/media files."""

import hashlib, itertools, json, subprocess, struct, tempfile
from fractions import Fraction
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from drawing import ROOT, font
from render import SLUGS, MEDIA, POSTERS


def run(args):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE).stdout


def fingerprint(im):
    a = np.asarray(im.convert("L").resize((17, 16), Image.Resampling.LANCZOS))
    return a[:, 1:] > a[:, :-1]


def atoms(path):
    out = []
    with path.open("rb") as f:
        while head := f.read(8):
            size, code = struct.unpack(">I4s", head)
            if size == 1:
                size = struct.unpack(">Q", f.read(8))[0]
                header = 16
            else:
                header = 8
            if not size:
                break
            out.append(code.decode("ascii"))
            f.seek(size - header, 1)
    return out


def verify():
    catalog = json.loads((ROOT / "unit.json").read_text())
    assert [row["slug"] for row in catalog] == SLUGS and len(set(SLUGS)) == 33
    for row in catalog:
        assert all(
            row.get(k) for k in ("slug", "nameKo", "titleKo", "storyKo", "techniqueKo")
        )
    posterboard = Image.new("RGB", (5 * 238, 7 * 162), "#202729")
    draw = ImageDraw.Draw(posterboard)
    records = []
    fingerprints = []
    audio_hashes = set()
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for i, (slug, entry) in enumerate(zip(SLUGS, catalog)):
            mp4 = MEDIA / (slug + ".mp4")
            jpg = MEDIA / (slug + ".jpg")
            probe = json.loads(
                run(
                    [
                        "ffprobe",
                        "-v",
                        "error",
                        "-show_streams",
                        "-show_format",
                        "-of",
                        "json",
                        str(mp4),
                    ]
                )
            )
            v, a = probe["streams"]
            rate = Fraction(v["avg_frame_rate"])
            duration = float(probe["format"]["duration"])
            assert (
                v["codec_name"] == "h264" and v["pix_fmt"] == "yuv420p" and rate >= 20
            )
            assert (
                v["width"] * 9 == v["height"] * 16
                and v["width"] >= 768
                and duration == 10
            )
            assert (
                a["codec_name"] == "aac"
                and a["channels"] == 2
                and a["sample_rate"] == "32000"
                and abs(float(a["duration"]) - duration) < 0.05
            )
            structure = atoms(mp4)
            assert structure.index("moov") < structure.index("mdat")
            pcm = tmp / "sound.raw"
            # Full strict audio/video decode. Small gray thumbnails make every decoded frame testable.
            pic = run(
                [
                    "ffmpeg",
                    "-v",
                    "error",
                    "-xerror",
                    "-err_detect",
                    "explode",
                    "-y",
                    "-i",
                    str(mp4),
                    "-map",
                    "0:v:0",
                    "-vf",
                    "scale=64:36",
                    "-pix_fmt",
                    "gray",
                    "-f",
                    "rawvideo",
                    "pipe:1",
                    "-map",
                    "0:a:0",
                    "-ac",
                    "1",
                    "-ar",
                    "8000",
                    "-f",
                    "f32le",
                    str(pcm),
                ]
            )
            arr = np.frombuffer(pic, np.uint8).reshape((-1, 36, 64))
            assert len(arr) == round(duration * float(rate))
            sound = np.fromfile(pcm, "<f4")
            assert np.sqrt(np.mean(sound**2)) > 0.005
            ah = hashlib.sha256(pcm.read_bytes()).hexdigest()
            assert ah not in audio_hashes
            audio_hashes.add(ah)
            indices = (np.array([0.9, 4.6, 8.9]) * float(rate)).astype(int)
            changes = [
                round(float(np.abs(arr[b].astype(float) - arr[c]).mean()), 2)
                for b, c in itertools.combinations(indices, 2)
            ]
            assert max(changes) > 1
            frames = len({frame.tobytes() for frame in arr})
            assert frames > 30
            extract = tmp / "poster.jpg"
            run(
                [
                    "ffmpeg",
                    "-v",
                    "error",
                    "-y",
                    "-ss",
                    str(POSTERS.get(slug, 6.7)),
                    "-i",
                    str(mp4),
                    "-frames:v",
                    "1",
                    "-q:v",
                    "2",
                    str(extract),
                ]
            )
            assert jpg.read_bytes() == extract.read_bytes()
            im = Image.open(jpg)
            im.load()
            assert im.size == (v["width"], v["height"])
            fp = fingerprint(im)
            fingerprints.append(fp)
            ref = ROOT.parents[2] / "lemo-opuscar" / "styles" / slug / "poster.jpg"
            ref_diff = (
                int(np.count_nonzero(fp != fingerprint(Image.open(ref))))
                if ref.exists()
                else None
            )
            if ref_diff is not None:
                assert ref_diff > 0
            x = i % 5 * 238
            y = i // 5 * 162
            posterboard.paste(
                im.resize((234, 132), Image.Resampling.LANCZOS), (x + 2, y + 2)
            )
            draw.text(
                (x + 6, y + 136),
                entry["titleKo"],
                font=font(16, "bold"),
                fill="#f3efe1",
            )
            records.append(
                dict(
                    slug=slug,
                    bytes=mp4.stat().st_size,
                    frames=len(arr),
                    fps=str(rate),
                    seconds=duration,
                    decoded_frame_variants=frames,
                    three_frame_mean_differences=changes,
                    mono_rms=round(float(np.sqrt(np.mean(sound**2))), 4),
                    upstream_poster_dhash_delta_of_256=ref_diff,
                    sha256=hashlib.sha256(mp4.read_bytes()).hexdigest(),
                )
            )
    mindiff = min(
        int(np.count_nonzero(x != y))
        for x, y in itertools.combinations(fingerprints, 2)
    )
    assert mindiff > 0 and max(v["bytes"] for v in records) < 4000000
    posterboard.save(ROOT / "poster-index.jpg", quality=91)
    report = dict(
        verified=len(records),
        dimensions=[768, 432],
        video="H.264 yuv420p",
        audio="AAC stereo 32 kHz",
        faststart=True,
        distinct_recordings=len(audio_hashes),
        min_pairwise_poster_dhash_delta_of_256=mindiff,
        matching_jpeg_frame_extractions=len(records),
        films=records,
    )
    (ROOT / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        "Verified",
        len(records),
        "films;",
        sum(x["frames"] for x in records),
        "frames;",
        sum(x["bytes"] for x in records),
        "bytes",
    )


if __name__ == "__main__":
    verify()
