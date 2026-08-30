"""Command-line interface for the Gaussian Robotics Atlas."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from gaussian_robotics_atlas.io import load_catalog, load_taxonomy
from gaussian_robotics_atlas.model import Issue, Resource, Severity, Taxonomy
from gaussian_robotics_atlas.query import recommend, search
from gaussian_robotics_atlas.render import catalog_stats, render_all, write_outputs
from gaussian_robotics_atlas.validate import validate_catalog, validation_failed


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gr-atlas",
        description="Validate, explore, and build the Gaussian Robotics Atlas.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: current directory).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate catalog data and evidence fields.")
    validate.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    validate.add_argument("--format", choices=("text", "json"), default="text")

    build = subparsers.add_parser("build", help="Regenerate Markdown, JSON, CSV, and the site.")
    build.add_argument("--check", action="store_true", help="Fail if generated files would change.")

    search_parser = subparsers.add_parser("search", help="Search with composable filters.")
    search_parser.add_argument("query", nargs="?", default="")
    search_parser.add_argument("--category")
    search_parser.add_argument("--kind")
    search_parser.add_argument("--input", dest="input_type")
    search_parser.add_argument("--framework")
    search_parser.add_argument("--code-status")
    search_parser.add_argument("--json", action="store_true", dest="as_json")

    recommend_parser = subparsers.add_parser(
        "recommend", help="Rank resources for a task and explain every score."
    )
    recommend_parser.add_argument(
        "task",
        help=(
            "mapping, slam, navigation, manipulation, semantics, simulation, vla, "
            "dynamic, or deployment"
        ),
    )
    recommend_parser.add_argument("--sensor")
    recommend_parser.add_argument("--framework")
    recommend_parser.add_argument("--limit", type=int, default=8)
    recommend_parser.add_argument(
        "--include-paper-only",
        action="store_true",
        help="Include entries without a released implementation.",
    )
    recommend_parser.add_argument("--json", action="store_true", dest="as_json")

    stats = subparsers.add_parser("stats", help="Show catalog coverage.")
    stats.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def _load(root: Path) -> tuple[tuple[Resource, ...], Taxonomy]:
    checkout_catalog = root / "catalog"
    packaged_catalog = Path(__file__).resolve().parent / "catalog"
    catalog = (
        checkout_catalog
        if (checkout_catalog / "taxonomy.json").is_file()
        else packaged_catalog
    )
    if not (catalog / "taxonomy.json").is_file():
        raise ValueError(
            "Catalog data not found. Run inside a repository checkout, pass --root, "
            "or reinstall a wheel that includes catalog data."
        )
    taxonomy = load_taxonomy(catalog / "taxonomy.json")
    resources = load_catalog(catalog)
    return resources, taxonomy


def _print_issue(issue: Issue) -> None:
    location = f" [{issue.resource_id}]" if issue.resource_id else ""
    print(f"{issue.severity.name.lower():7} {issue.code}{location}: {issue.message}")


def _validate_command(root: Path, strict: bool, output_format: str) -> int:
    resources, taxonomy = _load(root)
    issues = validate_catalog(resources, taxonomy)
    if output_format == "json":
        print(json.dumps([issue.to_dict() for issue in issues], ensure_ascii=False, indent=2))
    elif issues:
        for issue in issues:
            _print_issue(issue)
    else:
        print(f"OK: {len(resources)} resources passed validation.")
    if issues and output_format == "text":
        errors = sum(issue.severity == Severity.ERROR for issue in issues)
        warnings = sum(issue.severity == Severity.WARNING for issue in issues)
        print(f"Summary: {errors} error(s), {warnings} warning(s), {len(resources)} resources.")
    return int(validation_failed(issues, strict=strict))


def _build_command(root: Path, check: bool) -> int:
    resources, taxonomy = _load(root)
    issues = validate_catalog(resources, taxonomy)
    if validation_failed(issues):
        for issue in issues:
            _print_issue(issue)
        print("Build stopped: fix catalog validation errors first.", file=sys.stderr)
        return 1
    changed = write_outputs(render_all(resources, taxonomy), root, check=check)
    if check and changed:
        print("Generated outputs are out of date:")
        for path in changed:
            print(f"  - {path.as_posix()}")
        print("Run `gr-atlas build` and commit the results.")
        return 1
    verb = "checked" if check else "generated"
    print(f"OK: {len(resources)} resources; {len(render_all(resources, taxonomy))} outputs {verb}.")
    return 0


def _resource_line(resource: Resource) -> str:
    inputs = ",".join(resource.inputs) or "unknown-input"
    return (
        f"{resource.name} ({resource.year}) · {resource.category} · "
        f"{inputs} · {resource.code_status}"
    )


def _search_command(resources: tuple[Resource, ...], args: argparse.Namespace) -> int:
    results = search(
        resources,
        args.query,
        category=args.category,
        kind=args.kind,
        input_type=args.input_type,
        framework=args.framework,
        code_status=args.code_status,
    )
    if args.as_json:
        print(json.dumps([item.to_dict() for item in results], ensure_ascii=False, indent=2))
    else:
        for resource in results:
            print(_resource_line(resource))
            print(f"  {resource.project_url or resource.paper_url or resource.code_url}")
        print(f"{len(results)} result(s).")
    return 0


def _recommend_command(resources: tuple[Resource, ...], args: argparse.Namespace) -> int:
    results = recommend(
        resources,
        args.task,
        sensor=args.sensor,
        framework=args.framework,
        require_code=not args.include_paper_only,
        limit=max(args.limit, 0),
    )
    if args.as_json:
        print(
            json.dumps(
                [
                    {
                        "score": item.score,
                        "reasons": list(item.reasons),
                        "resource": item.resource.to_dict(),
                    }
                    for item in results
                ],
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print("Scores are discovery aids, not cross-paper performance rankings.\n")
        for index, item in enumerate(results, start=1):
            print(f"{index}. {_resource_line(item.resource)} [fit {item.score}]")
            print("   Why: " + "; ".join(item.reasons))
            primary_url = (
                item.resource.project_url or item.resource.paper_url or item.resource.code_url
            )
            print(f"   {primary_url}")
        if not results:
            print("No evidence-backed match. Try omitting a sensor/framework constraint.")
    return 0


def _stats_command(resources: tuple[Resource, ...], output_format: str) -> int:
    stats = catalog_stats(resources)
    if output_format == "json":
        print(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"Resources:      {stats['resources']}")
        print(f"With code:      {stats['with_code']}")
        print(f"Featured:       {stats['featured']}")
        print(f"Last verified:  {stats['last_verified']}")
        print("Categories:")
        for key, count in stats["categories"].items():
            print(f"  {key:30} {count}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "validate":
            return _validate_command(root, args.strict, args.format)
        if args.command == "build":
            return _build_command(root, args.check)
        resources, _taxonomy = _load(root)
        if args.command == "search":
            return _search_command(resources, args)
        if args.command == "recommend":
            return _recommend_command(resources, args)
        if args.command == "stats":
            return _stats_command(resources, args.format)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 2
