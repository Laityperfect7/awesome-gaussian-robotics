"""Deterministic catalog loading."""

from __future__ import annotations

import json
from pathlib import Path

from gaussian_robotics_atlas.model import Resource, Taxonomy


def load_taxonomy(path: str | Path) -> Taxonomy:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Taxonomy root must be an object.")
    return Taxonomy.from_dict(data)


def load_catalog(directory: str | Path) -> tuple[Resource, ...]:
    root = Path(directory)
    resources: list[Resource] = []
    for path in sorted(root.glob("*.json")):
        if path.name == "taxonomy.json":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"Catalog file must contain an array: {path}")
        for raw in data:
            if not isinstance(raw, dict):
                raise ValueError(f"Catalog entries must be objects: {path}")
            try:
                resources.append(Resource.from_dict(raw))
            except ValueError as exc:
                raise ValueError(f"{path}: {exc}") from exc
    if not resources:
        raise ValueError(f"No catalog resources found under: {root}")
    return tuple(
        sorted(
            resources,
            key=lambda item: (item.category, -item.year, item.name.casefold()),
        )
    )
