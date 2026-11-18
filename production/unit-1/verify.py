"""Decode both streams and check the delivery against the assignment."""

import hashlib
import io
import json
from pathlib import Path
import struct
import subprocess
import tempfile

import numpy as np
from PIL import Image
from render import HERE, MEDIA, SLUGS, FPS, H, W, POSTERS


def run(*cmd):
    return subprocess.run(cmd, check=True, stdout=subprocess.PIPE).stdout


def boxes(blob):
    pos = 0
    while pos + 8 <= len(blob):
        size, tag = struct.unpack_from(">I4s", blob, pos)
        if size < 8:
            raise ValueError("unexpected MP4 box size")
        yield tag
        pos += size


def verify():
    entries = json.loads((HERE / "unit.json").read_text())
    assert [e["slug"] for e in entries] == SLUGS
    assert all(
        all(
            e[k].strip()
            for k in ("slug", "nameKo", "titleKo", "storyKo", "techniqueKo")
        )
        for e in entries
    )
    posters = []
    sounds = set()
    total = 0
    largest = (0, "")
    motion_hist = []
    poster_errors = []
    with tempfile.TemporaryDirectory() as folder:
        pcm = Path(folder) / "audio.pcm"
        for i, slug in enumerate(SLUGS):
            mp4 = MEDIA / (slug + ".mp4")
            blob = mp4.read_bytes()
            order = list(boxes(blob))
            assert order.index(b"moov") < order.index(b"mdat"), slug
            info = json.loads(
                run("ffprobe", "-v", "error", "-show_streams", "-of", "json", str(mp4))
            )["streams"]
            v, a = info
            assert (
                v["codec_name"],
                v["pix_fmt"],
                v["width"],
                v["height"],
                v["avg_frame_rate"],
            ) == ("h264", "yuv420p", W, H, f"{FPS}/1"), slug
            assert int(v["nb_frames"]) == 9 * FPS and float(v["duration"]) == 9, slug
            assert a["codec_name"] == "aac" and abs(float(a["duration"]) - 9) < 0.05, (
                slug
            )
            decoded = run(
                "ffmpeg",
                "-v",
                "error",
                "-xerror",
                "-y",
                "-i",
                str(mp4),
                "-map",
                "0:v",
                "-vf",
                "scale=96:54:flags=area",
                "-pix_fmt",
                "rgb24",
                "-threads:v",
                "1",
                "-f",
                "rawvideo",
                "pipe:1",
                "-map",
                "0:a",
                "-ac",
                "1",
                "-ar",
                "16000",
                "-f",
                "s16le",
                str(pcm),
            )
            frames = np.frombuffer(decoded, np.uint8).reshape((-1, 54, 96, 3))
            assert len(frames) == 9 * FPS
            count = len(set(hashlib.sha256(f.tobytes()).digest() for f in frames))
            motion_hist.append((count, slug))
            # Compression differences alone cannot satisfy this three-beat test.
            looks = frames[[25, 105, 181]].astype(np.float32)
            beat_delta = [
                np.max(np.abs(x - y), axis=2).mean() for x, y in zip(looks, looks[1:])
            ]
            assert min(beat_delta) > 0.3, (slug, beat_delta)
            audio = np.fromfile(pcm, dtype="<i2")
            assert (
                len(audio) >= 9 * 16000 and np.abs(audio.astype(float)).mean() > 75
            ), slug
            sounds.add(hashlib.sha256(audio.tobytes()).digest())
            with Image.open(MEDIA / (slug + ".jpg")) as jpg:
                jpg.load()
                assert jpg.format == "JPEG" and jpg.size == (W, H)
                poster = np.array(
                    jpg.convert("RGB").resize((96, 54), Image.Resampling.BOX),
                    dtype=np.float32,
                )
            # FFmpeg resolves the seek timestamp to a presentation frame.
            ix = round(POSTERS[i] * FPS)
            error = min(
                np.abs(poster - frames[j]).mean() for j in range(ix - 1, ix + 3)
            )
            assert error < 4, (slug, error)
            poster_errors.append(error)
            posters.append(poster)
            assert len(blob) < 4_000_000
            total += len(blob)
            largest = max(largest, (len(blob), slug))
    assert len(sounds) == len(SLUGS)
    distances = [
        (np.abs(posters[i] - posters[j]).mean(), SLUGS[i], SLUGS[j])
        for i in range(len(posters))
        for j in range(i)
    ]
    closest = min(distances)
    assert closest[0] > 4, closest
    print(
        f"{len(SLUGS)} files, {len(SLUGS) * 9 * FPS} frames, {len(SLUGS) * 9} s, {total:,} video bytes"
    )
    print(f"largest MP4 {largest}, distinct decoded audio tracks {len(sounds)}")
    print(
        f"smallest distinct-frame count {min(motion_hist)}, maximum poster error {max(poster_errors):.2f}/255"
    )
    print(
        f"closest of {len(distances)} poster pairs {closest[1:]} at mean RGB difference {closest[0]:.2f}/255"
    )


if __name__ == "__main__":
    verify()
