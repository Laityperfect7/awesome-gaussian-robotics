"""Small, explicit fixtures shared by the standard-library tests."""

from __future__ import annotations

from dataclasses import replace

from gaussian_robotics_atlas.model import Resource, Taxonomy


def taxonomy() -> Taxonomy:
    return Taxonomy(
        categories={
            "slam-localization": "SLAM & Localization",
            "manipulation-interaction": "Manipulation & Interaction",
            "semantic-perception": "Semantic Perception",
        },
        kinds=("paper", "tool"),
        code_statuses=("released", "partial", "paper-only", "archived", "unavailable"),
        inputs=("rgb", "rgb-d", "lidar"),
        pose_requirements=("estimated-online", "known", "not-applicable"),
        frameworks=("pytorch", "ros2", "cuda"),
        capabilities=("camera-tracking", "grasping", "open-vocabulary", "online"),
        tags=("dynamic", "real-time", "mobile-manipulation"),
    )


def resource(**changes: object) -> Resource:
    base = Resource(
        id="splat-track",
        name="SplatTrack",
        kind="paper",
        category="slam-localization",
        summary=(
            "Tracks a camera online while incrementally maintaining a Gaussian scene "
            "representation."
        ),
        year=2025,
        venue="Robotics Conference 2025",
        paper_url="https://example.org/papers/splat-track",
        project_url="https://example.org/splat-track",
        code_url="https://github.com/example/splat-track",
        code_status="released",
        license="MIT",
        inputs=("rgb-d",),
        pose_requirement="estimated-online",
        frameworks=("pytorch", "cuda"),
        capabilities=("camera-tracking", "online"),
        tags=("real-time",),
        verified_date="2026-08-01",
        sources=(
            "https://example.org/papers/splat-track",
            "https://github.com/example/splat-track",
        ),
        doi="10.1000/splat-track",
        arxiv="2501.12345",
        featured=True,
    )
    return replace(base, **changes)
