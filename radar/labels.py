from __future__ import annotations

import argparse
import re
from functools import lru_cache
from pathlib import Path

import yaml

from radar.render import ROOT, load_yaml


LABELS_PATH = ROOT / "config" / "labels.yaml"
DATA_PATHS = (ROOT / "data" / "papers.yaml", ROOT / "data" / "candidates.yaml")


@lru_cache(maxsize=1)
def _vocabulary() -> tuple[dict, ...]:
    return tuple(load_yaml(LABELS_PATH)["labels"])


def vocabulary() -> list[dict]:
    return list(_vocabulary())


@lru_cache(maxsize=1)
def label_index() -> dict[str, dict]:
    return {label["id"]: label for label in vocabulary()}


@lru_cache(maxsize=1)
def compiled_vocabulary() -> tuple[tuple[str, tuple[re.Pattern, ...]], ...]:
    return tuple(
        (label["id"], tuple(re.compile(pattern, flags=re.IGNORECASE) for pattern in label.get("patterns", [])))
        for label in vocabulary()
    )


def evidence_text(paper: dict) -> str:
    values = [paper.get("title", ""), paper.get("abstract", ""), paper.get("key_idea", "")]
    values.extend(paper.get("tags", []))
    return "\n".join(str(value) for value in values if value)


def extract_labels(paper: dict) -> list[str]:
    text = evidence_text(paper)
    matches = []
    for label_id, patterns in compiled_vocabulary():
        if any(pattern.search(text) for pattern in patterns):
            matches.append(label_id)
    return matches


def effective_labels(paper: dict) -> list[str]:
    allowed = label_index()
    combined = [*paper.get("labels", []), *paper.get("auto_labels", [])]
    return list(dict.fromkeys(label for label in combined if label in allowed))


def update(check: bool = False) -> int:
    changed = 0
    version = load_yaml(LABELS_PATH)["version"]
    for path in DATA_PATHS:
        payload = load_yaml(path) or {"papers": []}
        for paper in payload.get("papers", []):
            extracted = extract_labels(paper)
            if paper.get("auto_labels") != extracted or paper.get("label_method") != version:
                changed += 1
                if not check:
                    paper["auto_labels"] = extracted
                    paper["label_method"] = version
        if not check:
            path.write_text(
                yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=120),
                encoding="utf-8",
                newline="\n",
            )
    if check and changed:
        raise SystemExit(f"Label metadata is stale for {changed} records; run python -m radar.labels")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract controlled labels from paper evidence text.")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = update(args.check)
    if not args.check:
        print(f"Updated controlled labels for {changed} records")


if __name__ == "__main__":
    main()
