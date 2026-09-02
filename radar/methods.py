from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
METHOD_CONFIG = ROOT / "config" / "method_families.yaml"


def load_method_config() -> dict[str, Any]:
    with METHOD_CONFIG.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {"axes": [], "families": []}


def method_catalog() -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in load_method_config().get("families", [])}


def method_metadata(paper: dict[str, Any]) -> dict[str, Any]:
    family_id = paper.get("method_family")
    family = method_catalog().get(family_id or "") if family_id else None
    return {
        "id": family_id,
        "title": family.get("title") if family else None,
        "description": family.get("description") if family else None,
        "color": family.get("color") if family else None,
        "predecessors": paper.get("predecessors", []),
        "change_axes": paper.get("change_axes", []),
        "transfer_ideas": paper.get("transfer_ideas", []),
    }
