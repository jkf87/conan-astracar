"""Decode all 33 streams. Optional --proof-dir writes three storyboard sheets and results."""

import argparse
from pathlib import Path
import json, subprocess, hashlib, itertools
import numpy as np
from PIL import Image, ImageDraw
from render import MEDIA, ROOT, POSTER, SLUGS


def cmd(*args):
    return subprocess.run(args, stdout=subprocess.PIPE, check=True).stdout


def verify(proof_dir=None):
    entries = json.loads((ROOT / "unit.json").read_text())
    assert [r["slug"] for r in entries] == SLUGS
    assert all(
        all(
            isinstance(r[k], str) and r[k]
            for k in ["nameKo", "titleKo", "storyKo", "techniqueKo"]
        )
        for r in entries
    )
    boards = [Image.new("RGB", (1000, 6 * 110), "#24252a") for i in range(3)]
    metrics = []
    thumbs = []
    for i, s in enumerate(SLUGS):
        p = MEDIA / f"{s}.mp4"
        j = MEDIA / f"{s}.jpg"
        meta = json.loads(
            cmd(
                "ffprobe",
                "-v",
                "error",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                str(p),
            )
        )
        vs, au = meta["streams"]
        assert (
            vs["codec_name"],
            vs["pix_fmt"],
            vs["width"],
            vs["height"],
            vs["r_frame_rate"],
        ) == ("h264", "yuv420p", 768, 432, "24/1")
        assert (int(vs["nb_frames"]), au["codec_name"]) == (216, "aac")
        assert abs(float(meta["format"]["duration"]) - 9) < 0.02
        src = p.read_bytes()
        assert 0 < src.index(b"moov") < src.index(b"mdat")
        assert len(src) < 4_000_000
        raw = cmd(
            "ffmpeg",
            "-v",
            "error",
            "-xerror",
            "-i",
            str(p),
            "-map",
            "0:v:0",
            "-vf",
            "scale=160:90:flags=area",
            "-pix_fmt",
            "rgb24",
            "-f",
            "rawvideo",
            "pipe:1",
        )
        f = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 90, 160, 3)
        assert len(f) == 216
        audio = cmd(
            "ffmpeg",
            "-v",
            "error",
            "-xerror",
            "-i",
            str(p),
            "-map",
            "0:a:0",
            "-f",
            "f32le",
            "pipe:1",
        )
        a = np.frombuffer(audio, dtype="<f4")
        rms = float(np.sqrt(np.mean(a * a)))
        assert rms > 0.012
        rms_sections = [np.sqrt(np.mean(chunk**2)) for chunk in np.array_split(a, 3)]
        assert min(rms_sections) > 0.008
        movement = [
            np.abs(g[4:].astype("int16") - g[:-4]).mean(axis=(1, 2, 3)).max()
            for g in np.array_split(f, 3)
        ]
        assert min(movement) > 0.15, (s, movement)
        im = Image.open(j)
        im.load()
        assert im.format == "JPEG" and im.size == (768, 432)
        thumb = np.array(
            im.convert("RGB").resize((160, 90), Image.Resampling.BOX)
        ).astype("float32")
        # Seek time converted to a following presentation frame by ffmpeg.
        index = int(np.ceil(POSTER[i] * 24 - 1e-8))
        error = min(
            abs(f[k].astype(float) - thumb).mean()
            for k in [index - 1, index, index + 1]
        )
        assert error < 5, (s, error)
        thumbs.append(thumb)
        ref = ROOT.parents[2] / "lemo-opuscar" / "styles" / s / "poster.jpg"
        up_dist = None
        if ref.exists():
            original = np.array(
                Image.open(ref).convert("RGB").resize((160, 90), Image.Resampling.BOX)
            ).astype(float)
            up_dist = float(abs(original - thumb).mean())
            assert up_dist > 5
        row = {
            "slug": s,
            "bytes": len(src),
            "mp4_sha256": hashlib.sha256(src).hexdigest(),
            "poster_sha256": hashlib.sha256(j.read_bytes()).hexdigest(),
            "rms": round(rms, 4),
            "peak_motion_per_third": [round(float(x), 3) for x in movement],
            "upstream_poster_mean_difference": round(up_dist, 2)
            if up_dist is not None
            else None,
        }
        metrics.append(row)
        if proof_dir:
            board = boards[i // 11]
            slot = i % 11
            x = (slot % 2) * 500
            y = (slot // 2) * 110
            for z, n in enumerate([33, 114, 187]):
                board.paste(Image.fromarray(f[n]), (x + 2 + z * 163, y))
            ImageDraw.Draw(board).text((x + 5, y + 91), s, fill="white")
    assert len({r["mp4_sha256"] for r in metrics}) == 33
    min_pair = min(
        (abs(thumbs[i] - thumbs[j]).mean(), SLUGS[i], SLUGS[j])
        for i, j in itertools.combinations(range(33), 2)
    )
    assert min_pair[0] > 7
    if proof_dir:
        proof_dir.mkdir(parents=True, exist_ok=True)
        for i, board in enumerate(boards):
            board.save(proof_dir / f"unit-2-board-{i + 1}.jpg", quality=91)
        (proof_dir / "decode.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(
        f"{len(metrics)} films; 7128 frames and 33 audio streams decoded; {sum(r['bytes'] for r in metrics):,} bytes total; largest {max(r['bytes'] for r in metrics):,}; closest poster pair {min_pair}"
    )
    print("RMS range", min(r["rms"] for r in metrics), max(r["rms"] for r in metrics))
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof-dir", type=Path)
    verify(parser.parse_args().proof_dir)
