"""Strict catalog data models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Any


def _string(data: dict[str, Any], field: str) -> str:
    value = data[field]
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string, got {type(value).__name__}.")
    return value


def _nullable_string(data: dict[str, Any], field: str) -> str | None:
    value = data.get(field)
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be null or a non-empty string.")
    return value


def _string_list(data: dict[str, Any], field: str) -> tuple[str, ...]:
    value = data[field]
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"{field} must be an array of strings.")
    return tuple(value)


class Severity(IntEnum):
    INFO = 1
    WARNING = 2
    ERROR = 3


@dataclass(frozen=True, slots=True)
class Issue:
    severity: Severity
    code: str
    message: str
    resource_id: str | None = None
    path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity.name.lower(),
            "code": self.code,
            "message": self.message,
            "resource_id": self.resource_id,
            "path": self.path,
        }


@dataclass(frozen=True, slots=True)
class Resource:
    id: str
    name: str
    kind: str
    category: str
    summary: str
    year: int
    venue: str
    paper_url: str | None
    project_url: str | None
    code_url: str | None
    code_status: str
    license: str
    inputs: tuple[str, ...]
    pose_requirement: str
    frameworks: tuple[str, ...]
    capabilities: tuple[str, ...]
    tags: tuple[str, ...]
    verified_date: str
    sources: tuple[str, ...]
    doi: str | None = None
    arxiv: str | None = None
    featured: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Resource:
        allowed = {
            "id",
            "name",
            "kind",
            "category",
            "summary",
            "year",
            "venue",
            "paper_url",
            "project_url",
            "code_url",
            "code_status",
            "license",
            "inputs",
            "pose_requirement",
            "frameworks",
            "capabilities",
            "tags",
            "verified_date",
            "sources",
            "doi",
            "arxiv",
            "featured",
        }
        unknown = set(data).difference(allowed)
        missing = {
            "id",
            "name",
            "kind",
            "category",
            "summary",
            "year",
            "venue",
            "paper_url",
            "project_url",
            "code_url",
            "code_status",
            "license",
            "inputs",
            "pose_requirement",
            "frameworks",
            "capabilities",
            "tags",
            "verified_date",
            "sources",
        }.difference(data)
        if unknown or missing:
            raise ValueError(f"Unknown fields {sorted(unknown)}; missing fields {sorted(missing)}.")
        year = data["year"]
        if not isinstance(year, int) or isinstance(year, bool):
            raise ValueError(f"year must be an integer, got {type(year).__name__}.")
        featured = data.get("featured", False)
        if not isinstance(featured, bool):
            raise ValueError("featured must be a boolean when present.")
        return cls(
            id=_string(data, "id"),
            name=_string(data, "name"),
            kind=_string(data, "kind"),
            category=_string(data, "category"),
            summary=_string(data, "summary"),
            year=year,
            venue=_string(data, "venue"),
            paper_url=_nullable_string(data, "paper_url"),
            project_url=_nullable_string(data, "project_url"),
            code_url=_nullable_string(data, "code_url"),
            code_status=_string(data, "code_status"),
            license=_string(data, "license"),
            inputs=_string_list(data, "inputs"),
            pose_requirement=_string(data, "pose_requirement"),
            frameworks=_string_list(data, "frameworks"),
            capabilities=_string_list(data, "capabilities"),
            tags=_string_list(data, "tags"),
            verified_date=_string(data, "verified_date"),
            sources=_string_list(data, "sources"),
            doi=_nullable_string(data, "doi"),
            arxiv=_nullable_string(data, "arxiv"),
            featured=featured,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "kind": self.kind,
            "category": self.category,
            "summary": self.summary,
            "year": self.year,
            "venue": self.venue,
            "paper_url": self.paper_url,
            "project_url": self.project_url,
            "code_url": self.code_url,
            "code_status": self.code_status,
            "license": self.license,
            "inputs": list(self.inputs),
            "pose_requirement": self.pose_requirement,
            "frameworks": list(self.frameworks),
            "capabilities": list(self.capabilities),
            "tags": list(self.tags),
            "verified_date": self.verified_date,
            "sources": list(self.sources),
            "doi": self.doi,
            "arxiv": self.arxiv,
            "featured": self.featured,
        }


@dataclass(frozen=True, slots=True)
class Taxonomy:
    categories: dict[str, str]
    kinds: tuple[str, ...]
    code_statuses: tuple[str, ...]
    inputs: tuple[str, ...]
    pose_requirements: tuple[str, ...]
    frameworks: tuple[str, ...]
    capabilities: tuple[str, ...]
    tags: tuple[str, ...]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Taxonomy:
        required = {
            "categories",
            "kinds",
            "code_statuses",
            "inputs",
            "pose_requirements",
            "frameworks",
            "capabilities",
            "tags",
        }
        if set(data) != required:
            raise ValueError(f"Taxonomy fields must be exactly {sorted(required)}.")
        categories = data["categories"]
        if not isinstance(categories, dict) or any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in categories.items()
        ):
            raise ValueError("categories must be an object with string keys and values.")
        for field in required.difference({"categories"}):
            value = data[field]
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                raise ValueError(f"{field} must be an array of strings.")
        return cls(
            categories=dict(categories),
            kinds=tuple(data["kinds"]),
            code_statuses=tuple(data["code_statuses"]),
            inputs=tuple(data["inputs"]),
            pose_requirements=tuple(data["pose_requirements"]),
            frameworks=tuple(data["frameworks"]),
            capabilities=tuple(data["capabilities"]),
            tags=tuple(data["tags"]),
        )
