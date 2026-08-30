"""Evidence-aware catalog validation."""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Callable, Iterable
from datetime import date, datetime

from gaussian_robotics_atlas.model import Issue, Resource, Severity, Taxonomy
from gaussian_robotics_atlas.urls import (
    arxiv_identity,
    canonical_url,
    doi_identity,
    github_identity,
)

_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_PROMOTIONAL = re.compile(
    r"\b(best|breakthrough|cutting[- ]edge|game[- ]changing|revolutionary|"
    r"state[- ]of[- ]the[- ]art)\b",
    re.IGNORECASE,
)
_RELEASED_STATUSES = frozenset({"released", "partial", "archived"})
_REQUIRED_CODE_STATUSES = frozenset(
    {"released", "partial", "paper-only", "archived", "unavailable"}
)


def _issue(
    severity: Severity,
    code: str,
    message: str,
    resource: Resource | None = None,
) -> Issue:
    return Issue(
        severity=severity,
        code=code,
        message=message,
        resource_id=resource.id if resource else None,
    )


def _check_members(
    resource: Resource,
    field: str,
    values: Iterable[str],
    allowed: Iterable[str],
) -> list[Issue]:
    allowed_set = set(allowed)
    return [
        _issue(
            Severity.ERROR,
            "unknown-taxonomy-value",
            f"{field} contains unknown value {value!r}.",
            resource,
        )
        for value in values
        if value not in allowed_set
    ]


def validate_resource(
    resource: Resource,
    taxonomy: Taxonomy,
    *,
    today: date | None = None,
) -> list[Issue]:
    """Validate a single resource without performing duplicate checks."""

    now = today or date.today()
    issues: list[Issue] = []
    if not _SLUG.fullmatch(resource.id):
        issues.append(
            _issue(Severity.ERROR, "invalid-id", "id must be a lowercase slug.", resource)
        )
    if resource.category not in taxonomy.categories:
        issues.append(
            _issue(
                Severity.ERROR,
                "unknown-category",
                f"Unknown category {resource.category!r}.",
                resource,
            )
        )
    for field, value, allowed in (
        ("kind", resource.kind, taxonomy.kinds),
        ("code_status", resource.code_status, taxonomy.code_statuses),
        ("pose_requirement", resource.pose_requirement, taxonomy.pose_requirements),
    ):
        if value not in allowed:
            issues.append(
                _issue(
                    Severity.ERROR,
                    "unknown-taxonomy-value",
                    f"{field} contains unknown value {value!r}.",
                    resource,
                )
            )
    issues.extend(_check_members(resource, "inputs", resource.inputs, taxonomy.inputs))
    issues.extend(
        _check_members(resource, "frameworks", resource.frameworks, taxonomy.frameworks)
    )
    issues.extend(
        _check_members(resource, "capabilities", resource.capabilities, taxonomy.capabilities)
    )
    issues.extend(_check_members(resource, "tags", resource.tags, taxonomy.tags))
    for field, values in (
        ("inputs", resource.inputs),
        ("frameworks", resource.frameworks),
        ("capabilities", resource.capabilities),
        ("tags", resource.tags),
        ("sources", resource.sources),
    ):
        if len(values) != len(set(values)):
            issues.append(
                _issue(
                    Severity.ERROR,
                    "duplicate-field-value",
                    f"{field} must not contain duplicate values.",
                    resource,
                )
            )
    if not resource.capabilities:
        issues.append(
            _issue(
                Severity.ERROR,
                "missing-capability",
                "capabilities must contain at least one evidence-backed value.",
                resource,
            )
        )

    for field, value in (
        ("name", resource.name),
        ("summary", resource.summary),
        ("venue", resource.venue),
        ("license", resource.license),
    ):
        if not value.strip():
            issues.append(
                _issue(Severity.ERROR, "empty-field", f"{field} cannot be empty.", resource)
            )
    if resource.license.casefold() == "unknown" and resource.license != "unknown":
        issues.append(
            _issue(
                Severity.ERROR,
                "noncanonical-unknown",
                "Use lowercase 'unknown' for an unverified license.",
                resource,
            )
        )
    words = resource.summary.split()
    if len(words) < 8 or len(words) > 45:
        issues.append(
            _issue(
                Severity.WARNING,
                "summary-length",
                "summary should contain between 8 and 45 words.",
                resource,
            )
        )
    if resource.summary and not resource.summary.endswith((".", "?", "!")):
        issues.append(
            _issue(
                Severity.WARNING,
                "summary-punctuation",
                "summary should end with punctuation.",
                resource,
            )
        )
    if _PROMOTIONAL.search(resource.summary):
        issues.append(
            _issue(
                Severity.WARNING,
                "promotional-language",
                "summary contains promotional language; describe evidence instead.",
                resource,
            )
        )
    if resource.year < 2023 or resource.year > now.year + 1:
        issues.append(
            _issue(
                Severity.ERROR,
                "invalid-year",
                f"year must be between 2023 and {now.year + 1}.",
                resource,
            )
        )
    if resource.code_status in _RELEASED_STATUSES and not resource.code_url:
        issues.append(
            _issue(
                Severity.ERROR,
                "missing-code-url",
                f"code_status={resource.code_status!r} requires code_url.",
                resource,
            )
        )
    if not any((resource.paper_url, resource.project_url, resource.code_url)):
        issues.append(
            _issue(
                Severity.ERROR,
                "missing-primary-link",
                "At least one paper, project, or code URL is required.",
                resource,
            )
        )
    if not resource.sources:
        issues.append(
            _issue(
                Severity.ERROR,
                "missing-evidence",
                "sources must contain at least one first-party or publication URL.",
                resource,
            )
        )

    urls = [
        ("paper_url", resource.paper_url),
        ("project_url", resource.project_url),
        ("code_url", resource.code_url),
        *(("sources", value) for value in resource.sources),
    ]
    for field, url in urls:
        if not url:
            continue
        try:
            canonical_url(url)
        except (ValueError, UnicodeError) as exc:
            issues.append(
                _issue(
                    Severity.ERROR,
                    "unsafe-url",
                    f"{field} is not a safe absolute HTTPS URL: {exc}",
                    resource,
                )
            )

    try:
        verified = datetime.strptime(resource.verified_date, "%Y-%m-%d").date()
    except ValueError:
        issues.append(
            _issue(
                Severity.ERROR,
                "invalid-verified-date",
                "verified_date must use YYYY-MM-DD.",
                resource,
            )
        )
    else:
        if verified > now:
            issues.append(
                _issue(
                    Severity.ERROR,
                    "future-verified-date",
                    "verified_date cannot be in the future.",
                    resource,
                )
            )
        elif (now - verified).days > 365:
            issues.append(
                _issue(
                    Severity.WARNING,
                    "stale-verification",
                    "Entry has not been re-verified in more than 365 days.",
                    resource,
                )
            )
    return issues


def validate_taxonomy(taxonomy: Taxonomy) -> list[Issue]:
    """Validate the controlled vocabulary itself before checking resources."""

    issues: list[Issue] = []
    for key, label in taxonomy.categories.items():
        if not _SLUG.fullmatch(key):
            issues.append(
                _issue(
                    Severity.ERROR,
                    "invalid-category-id",
                    f"Invalid category slug {key!r}.",
                )
            )
        if not label.strip():
            issues.append(
                _issue(
                    Severity.ERROR,
                    "empty-category-label",
                    f"Category {key!r} has no label.",
                )
            )
    for field, values in (
        ("kinds", taxonomy.kinds),
        ("code_statuses", taxonomy.code_statuses),
        ("inputs", taxonomy.inputs),
        ("pose_requirements", taxonomy.pose_requirements),
        ("frameworks", taxonomy.frameworks),
        ("capabilities", taxonomy.capabilities),
        ("tags", taxonomy.tags),
    ):
        if not values:
            issues.append(
                _issue(Severity.ERROR, "empty-taxonomy", f"{field} cannot be empty.")
            )
        if len(values) != len(set(values)):
            issues.append(
                _issue(Severity.ERROR, "duplicate-taxonomy-value", f"{field} has duplicates.")
            )
        if any(not value or value != value.strip() for value in values):
            issues.append(
                _issue(
                    Severity.ERROR,
                    "invalid-taxonomy-value",
                    f"{field} contains an empty or padded value.",
                )
            )
    missing_statuses = _REQUIRED_CODE_STATUSES.difference(taxonomy.code_statuses)
    if missing_statuses:
        issues.append(
            _issue(
                Severity.ERROR,
                "missing-code-status",
                f"code_statuses is missing required values: {sorted(missing_statuses)}.",
            )
        )
    return issues


def _duplicate_issues(
    resources: Iterable[Resource],
    key_name: str,
    key_getter: Callable[[Resource], str | None],
) -> list[Issue]:
    groups: dict[str, list[Resource]] = defaultdict(list)
    for resource in resources:
        value = key_getter(resource)
        if value:
            groups[str(value)].append(resource)
    issues: list[Issue] = []
    for value, group in sorted(groups.items()):
        if len(group) < 2:
            continue
        ids = ", ".join(resource.id for resource in group)
        for resource in group:
            issues.append(
                _issue(
                    Severity.ERROR,
                    f"duplicate-{key_name}",
                    f"Duplicate {key_name} identity {value!r} is used by: {ids}.",
                    resource,
                )
            )
    return issues


def validate_catalog(
    resources: Iterable[Resource],
    taxonomy: Taxonomy,
    *,
    today: date | None = None,
) -> list[Issue]:
    """Validate taxonomy membership, evidence, safety, and duplicate identities."""

    items = tuple(resources)
    issues = validate_taxonomy(taxonomy)
    issues.extend(
        [
            issue
            for resource in items
            for issue in validate_resource(resource, taxonomy, today=today)
        ]
    )
    issues.extend(_duplicate_issues(items, "id", lambda item: item.id))
    issues.extend(_duplicate_issues(items, "name", lambda item: item.name.casefold()))
    issues.extend(_duplicate_issues(items, "github", lambda item: github_identity(item.code_url)))
    issues.extend(_duplicate_issues(items, "doi", lambda item: doi_identity(item.doi)))
    issues.extend(_duplicate_issues(items, "arxiv", lambda item: arxiv_identity(item.arxiv)))
    return sorted(
        issues,
        key=lambda item: (-int(item.severity), item.code, item.resource_id or ""),
    )


def validation_failed(issues: Iterable[Issue], *, strict: bool = False) -> bool:
    threshold = Severity.WARNING if strict else Severity.ERROR
    return any(issue.severity >= threshold for issue in issues)
