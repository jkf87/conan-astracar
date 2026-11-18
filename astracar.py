#!/usr/bin/env python3
"""Browse the Astra film menu and start a new film in Codex."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
MODEL = "gpt-6.2-astra"


def prompt(row, topic):
    return (
        f"$lemo-opuscar {row['nameEn']} ({row['slug']}) 스타일로 "
        f"‘{topic}’에 관한 한국어 단편을 만들어 줘. 아래 스타일 가이드를 참고해 "
        f"새로운 이야기와 장면을 구성하고 실행 가능한 소스, 자료 출처, 완성 MP4를 함께 만들어 줘.\n{row['guide']}"
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="action", required=True)
    listing = sub.add_parser("menu", help="스타일 번호·이름·분류·작품 검색")
    listing.add_argument("query", nargs="?", default="")
    for name, helptext in [
        ("prompt", "제작 프롬프트 출력"),
        ("make", "현재 폴더에서 Codex Astra 6.2 High로 제작 시작"),
    ]:
        cmd = sub.add_parser(name, help=helptext)
        cmd.add_argument("style", help="스타일 번호, slug, 영문명 또는 한국어 이름")
        cmd.add_argument("topic", help="새 작품의 주제")
    args = p.parse_args()
    rows = json.loads((ROOT / "site/catalog.json").read_text())
    if args.action == "menu":
        for r in rows:
            fields = [
                r[k]
                for k in ("number", "slug", "nameKo", "nameEn", "category", "titleKo")
            ]
            if args.query.casefold() in " ".join(fields).casefold():
                print(
                    f"{r['number']:>2}  {r['nameKo']} · {r['titleKo']}  [{r['category']}]  {r['slug']}"
                )
        return 0
    key = args.style.strip().casefold()
    row = next(
        (
            r
            for r in rows
            if key in {r[k].casefold() for k in ("number", "slug", "nameKo", "nameEn")}
            or key.isdecimal()
            and int(key) == int(r["number"])
        ),
        None,
    )
    if not row:
        p.error("스타일을 찾을 수 없습니다. menu 명령으로 이름이나 번호를 확인하세요.")
    if not args.topic.strip():
        p.error("새 단편의 주제를 입력하세요.")
    message = prompt(row, args.topic.strip())
    if args.action == "prompt":
        print(message)
        return 0
    codex = shutil.which("codex")
    if not codex:
        p.error(
            "codex 실행 파일을 찾을 수 없습니다. Codex CLI 설치 후 다시 실행하세요."
        )
    return subprocess.call(
        [codex, "-m", MODEL, "-c", 'model_reasoning_effort="high"', message]
    )


if __name__ == "__main__":
    sys.exit(main())
