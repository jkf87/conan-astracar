"""Join the three Astra production logs to the pinned original film index."""

import argparse
import ast
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REV = "00a7f9ec99c8686265a8ca4ed9a3fdaaf27ea6f4"
UPSTREAM = "https://github.com/lemomo-ai/lemo-opuscar"
CATEGORIES = {
    "Edit & Documentary": "편집·다큐멘터리",
    "Painting & Illustration": "회화·일러스트",
    "Sketch & Board": "스케치·판서",
    "Traditional Crafts": "전통 공예",
    "Print & Printmaking": "인쇄·판화",
    "Graphic & Type": "그래픽·타이포그래피",
    "Line Diagrams": "선과 도해",
    "Cartoons": "만화·애니메이션",
    "Games": "게임",
    "Film & Tape": "필름·테이프",
    "Screens & Interfaces": "스크린·인터페이스",
    "Light & Lines": "빛과 선",
    "3D & Miniature": "입체·미니어처",
    "Instruments & Evidence": "관측·기록",
    "Data & Maps": "데이터·지도",
}
AUTHORS = {"crayon-world": "2nd1st", "memphis-diorama": "EianLu"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build(upstream):
    revision = subprocess.check_output(
        ["git", "-C", upstream, "rev-parse", "HEAD"], text=True
    ).strip()
    if revision != REV:
        raise ValueError(f"Expected upstream revision {REV}, found {revision}")
    originals = read(upstream / "styleboard/catalog.json")
    reference = read(upstream / "styleboard/films_repo.json")
    units = {}
    sources = {}
    for directory in sorted((ROOT / "production").glob("unit-*")):
        definitions = {}
        for script in sorted(directory.glob("*.py")):
            for node in ast.parse(script.read_text()).body:
                if isinstance(node, ast.FunctionDef):
                    definitions[node.name] = (
                        f"{script.relative_to(ROOT).as_posix()}#L{node.lineno}"
                    )
        rows = read(directory / "unit.json")
        assigned = read(directory / "styles.json")
        if len(rows) != 33 or {r["slug"] for r in rows} != set(assigned):
            raise ValueError(f"Missing or duplicate films in {directory.name}")
        for row in rows:
            slug = row["slug"]
            if slug in units:
                raise ValueError(f"Duplicate {slug}")
            units[slug] = row
            sources[slug] = definitions[slug.replace("-", "_")]
    if len(units) != 99 or set(units) != {r["slug"] for r in originals}:
        raise ValueError("The production and reference catalogs differ")
    result = []
    for orig in originals:
        slug = orig["slug"]
        row = units[slug]
        media = ROOT / "site/media"
        info = subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "csv=p=0",
                media / f"{slug}.mp4",
            ],
            text=True,
        )
        if not (media / f"{slug}.jpg").stat().st_size:
            raise ValueError(f"Empty poster for {slug}")
        fields = {
            k: row[k].strip() for k in ("nameKo", "titleKo", "storyKo", "techniqueKo")
        }
        if not all(fields.values()):
            raise ValueError(f"Missing copy for {slug}")
        result.append(
            dict(
                slug=slug,
                number=orig["num"],
                nameEn=orig["en"],
                category=CATEGORIES[orig["cat_en"]],
                **fields,
                seconds=round(float(info), 2),
                originalTitle=orig["film"],
                originalAuthor=AUTHORS.get(slug, "Lemomo (LemoLab)"),
                originalPoster=f"https://raw.githubusercontent.com/lemomo-ai/lemo-opuscar/{REV}/styles/{slug}/poster.jpg",
                originalVideo=f"{reference['base']}{slug}.mp4",
                source=sources[slug],
                originalPage=f"https://lemomo-ai.github.io/lemo-opuscar/styles/{slug}/",
                guide=f"{UPSTREAM}/blob/{REV}/styles/{slug}/STYLE.md",
            )
        )
    (ROOT / "site/catalog.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("upstream", type=Path)
    build(parser.parse_args().upstream)
