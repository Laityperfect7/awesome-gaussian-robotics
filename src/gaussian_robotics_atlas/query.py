"""Catalog search and explainable stack recommendations."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from gaussian_robotics_atlas.model import Resource


@dataclass(frozen=True, slots=True)
class Recommendation:
    resource: Resource
    score: int
    reasons: tuple[str, ...]


_TASK_SIGNALS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "mapping": (("mapping-reconstruction", "slam-localization"), ("dense-mapping", "online")),
    "slam": (("slam-localization",), ("camera-tracking", "online")),
    "navigation": (("navigation-planning", "semantic-perception"), ("planning", "free-space")),
    "manipulation": (
        ("manipulation-interaction", "semantic-perception"),
        ("grasping", "affordance"),
    ),
    "semantics": (("semantic-perception",), ("open-vocabulary", "semantics")),
    "simulation": (
        ("simulation-digital-twins", "robot-learning-vla"),
        ("real-to-sim", "simulation"),
    ),
    "vla": (("robot-learning-vla", "simulation-digital-twins"), ("vla", "policy-learning")),
    "dynamic": (("dynamic-scenes",), ("dynamic", "deformation")),
    "deployment": (("deployment-tooling",), ("compression", "edge")),
}


def _haystack(resource: Resource) -> str:
    return " ".join(
        (
            resource.id,
            resource.name,
            resource.kind,
            resource.category,
            resource.summary,
            resource.venue,
            resource.code_status,
            *resource.inputs,
            *resource.frameworks,
            *resource.capabilities,
            *resource.tags,
        )
    ).casefold()


def search(
    resources: Iterable[Resource],
    text: str = "",
    *,
    category: str | None = None,
    kind: str | None = None,
    input_type: str | None = None,
    framework: str | None = None,
    code_status: str | None = None,
) -> tuple[Resource, ...]:
    """Apply composable filters and deterministic relevance ordering."""

    terms = tuple(term for term in text.casefold().split() if term)

    def matches(resource: Resource) -> bool:
        return (
            (not category or resource.category == category)
            and (not kind or resource.kind == kind)
            and (not input_type or input_type in resource.inputs)
            and (not framework or framework in resource.frameworks)
            and (not code_status or resource.code_status == code_status)
            and all(term in _haystack(resource) for term in terms)
        )

    def rank(resource: Resource) -> tuple[int, int, int, str]:
        haystack = _haystack(resource)
        exact_name = int(bool(text) and resource.name.casefold() == text.casefold())
        occurrences = sum(haystack.count(term) for term in terms)
        return (-exact_name, -occurrences, -resource.year, resource.name.casefold())

    return tuple(sorted((resource for resource in resources if matches(resource)), key=rank))


def recommend(
    resources: Iterable[Resource],
    task: str,
    *,
    sensor: str | None = None,
    framework: str | None = None,
    require_code: bool = True,
    limit: int = 8,
) -> tuple[Recommendation, ...]:
    """Rank catalog entries with transparent, non-benchmark scoring."""

    normalized = task.strip().casefold()
    categories, capabilities = _TASK_SIGNALS.get(normalized, ((normalized,), (normalized,)))
    results: list[Recommendation] = []
    for resource in resources:
        if require_code and resource.code_status not in {"released", "partial"}:
            continue
        score = 0
        reasons: list[str] = []
        if resource.category in categories:
            score += 6
            reasons.append(f"task category: {resource.category}")
        matches = sorted(set(resource.capabilities).intersection(capabilities))
        if matches:
            score += 3 * len(matches)
            reasons.append("capabilities: " + ", ".join(matches))
        task_text_match = normalized and normalized in _haystack(resource)
        if task_text_match:
            score += 2
            reasons.append("task term appears in verified metadata")
        if sensor:
            if sensor in resource.inputs:
                score += 4
                reasons.append(f"sensor input: {sensor}")
        if framework:
            if framework in resource.frameworks:
                score += 3
                reasons.append(f"framework: {framework}")
        if resource.code_status == "released":
            score += 2
            reasons.append("code released")
        elif resource.code_status == "partial":
            score += 1
            reasons.append("partial code released")
        if resource.featured:
            score += 1
            reasons.append("editorial starter pick")
        if score > 0:
            results.append(Recommendation(resource, score, tuple(reasons)))
    results.sort(
        key=lambda item: (-item.score, -item.resource.year, item.resource.name.casefold())
    )
    return tuple(results[: max(limit, 0)])
