"""Deterministic catalog exports and the dependency-free explorer."""

from __future__ import annotations

import csv
import html
import io
import json
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import TypedDict

from gaussian_robotics_atlas.model import Resource, Taxonomy
from gaussian_robotics_atlas.urls import canonical_url


class CatalogStats(TypedDict):
    resources: int
    with_code: int
    featured: int
    last_verified: str | None
    categories: dict[str, int]
    kinds: dict[str, int]
    code_statuses: dict[str, int]
    years: dict[str, int]
    inputs: dict[str, int]


def _sorted(resources: Iterable[Resource]) -> tuple[Resource, ...]:
    return tuple(
        sorted(
            resources,
            key=lambda item: (item.category, -int(item.featured), -item.year, item.name.casefold()),
        )
    )


def catalog_stats(resources: Iterable[Resource]) -> CatalogStats:
    items = tuple(resources)
    return {
        "resources": len(items),
        "with_code": sum(item.code_status in {"released", "partial"} for item in items),
        "featured": sum(item.featured for item in items),
        "last_verified": max((item.verified_date for item in items), default=None),
        "categories": dict(sorted(Counter(item.category for item in items).items())),
        "kinds": dict(sorted(Counter(item.kind for item in items).items())),
        "code_statuses": dict(sorted(Counter(item.code_status for item in items).items())),
        "years": dict(sorted(Counter(str(item.year) for item in items).items(), reverse=True)),
        "inputs": dict(sorted(Counter(value for item in items for value in item.inputs).items())),
    }


def _export_dict(resource: Resource) -> dict[str, object]:
    raw = resource.to_dict()
    for field in ("paper_url", "project_url", "code_url"):
        value = raw[field]
        raw[field] = canonical_url(str(value)) if value else None
    raw["sources"] = [canonical_url(str(value)) for value in raw["sources"]]
    return raw


def render_catalog_json(resources: Iterable[Resource]) -> str:
    items = _sorted(resources)
    payload = {
        "schema_version": 1,
        "generated_from": "catalog resource JSON files",
        "stats": catalog_stats(items),
        "resources": [_export_dict(item) for item in items],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def render_catalog_csv(resources: Iterable[Resource]) -> str:
    stream = io.StringIO(newline="")
    fields = [
        "id",
        "name",
        "kind",
        "category",
        "summary",
        "year",
        "venue",
        "code_status",
        "license",
        "inputs",
        "pose_requirement",
        "frameworks",
        "capabilities",
        "tags",
        "paper_url",
        "project_url",
        "code_url",
        "doi",
        "arxiv",
        "verified_date",
    ]
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for item in _sorted(resources):
        raw = _export_dict(item)
        writer.writerow(
            {
                key: _csv_safe(
                    "|".join(str(value) for value in raw[key])
                    if isinstance(raw.get(key), list)
                    else raw.get(key)
                )
                for key in fields
            }
        )
    return stream.getvalue()


def _md_link(label: str, url: str | None) -> str:
    if not url:
        return "—"
    safe_label = label.replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")
    safe_url = canonical_url(url).replace(")", "%29")
    return f"[{safe_label}]({safe_url})"


def _csv_safe(value: object) -> object:
    if not isinstance(value, str):
        return value
    dangerous = value.lstrip(" \t\r")
    if dangerous.startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r")):
        return "'" + value
    return value


def render_catalog_markdown(resources: Iterable[Resource], taxonomy: Taxonomy) -> str:
    items = _sorted(resources)
    stats = catalog_stats(items)
    lines = [
        "# Gaussian Robotics Catalog",
        "",
        "This is the reviewable Markdown view of the structured catalog. Entries are sorted",
        "deterministically; compatibility claims come from the linked paper, project, or code",
        "sources—not from cross-system benchmark guesses.",
        "",
        f"**{stats['resources']} resources · {stats['with_code']} with released or partial code · "
        f"verified through {stats['last_verified']}**",
        "",
        "> Generated from `catalog/*.json`. Edit the source data, then run `python -m "
        "gaussian_robotics_atlas build`.",
        "",
        "## Categories",
        "",
    ]
    present = {item.category for item in items}
    for key, label in taxonomy.categories.items():
        if key in present:
            lines.append(f"- [{label}](#{key})")
    lines.append("")
    for key, label in taxonomy.categories.items():
        group = [item for item in items if item.category == key]
        if not group:
            continue
        lines.extend(
            [
                f"## {label}",
                f"<a id=\"{key}\"></a>",
                "",
                "| Resource | Year | Inputs | Code | What it helps with |",
                "|---|---:|---|---|---|",
            ]
        )
        for item in group:
            primary = item.project_url or item.paper_url or item.code_url
            name = _md_link(item.name, primary)
            inputs = ", ".join(item.inputs) or "—"
            code = _md_link(item.code_status, item.code_url) if item.code_url else item.code_status
            summary = item.summary.replace("|", "\\|").replace("\n", " ")
            marker = " ⭐" if item.featured else ""
            lines.append(f"| {name}{marker} | {item.year} | {inputs} | {code} | {summary} |")
        lines.extend(
            [
                "",
                "_⭐ Editorial starter pick. It is not a universal performance ranking._",
                "",
            ]
        )
    lines.extend(
        [
            "## Data contract",
            "",
            "- `released` means a public code link was verified; it does not mean this project reproduced it.",
            "- `partial` means some implementation assets are public, but the full paper pipeline is unavailable.",
            "- `paper-only` means no public implementation was verified at the review date.",
            "- Missing framework or sensor values mean unknown, not unsupported.",
            "- Performance numbers are intentionally omitted unless hardware, dataset, and protocol are comparable.",
            "",
            "Use the [interactive explorer](docs/index.html), [JSON](docs/catalog.json), or",
            "[CSV](docs/catalog.csv) for deeper filtering.",
            "",
        ]
    )
    return "\n".join(lines)


def _json_for_script(value: object) -> str:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def render_site(resources: Iterable[Resource], taxonomy: Taxonomy) -> str:
    items = _sorted(resources)
    payload = [_export_dict(item) for item in items]
    stats = catalog_stats(items)
    category_options = "".join(
        f'<option value="{html.escape(key, quote=True)}">{html.escape(label)}</option>'
        for key, label in taxonomy.categories.items()
        if any(item.category == key for item in items)
    )
    input_options = "".join(
        f'<option value="{html.escape(value, quote=True)}">{html.escape(value)}</option>'
        for value in taxonomy.inputs
        if any(value in item.inputs for item in items)
    )
    data = _json_for_script(payload)
    category_labels = _json_for_script(taxonomy.categories)
    last_verified = html.escape(str(stats["last_verified"] or "not yet"))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="A verified, queryable atlas of Gaussian Splatting systems for robotics and embodied AI.">
  <meta name="color-scheme" content="dark light">
  <title>Gaussian Robotics Atlas</title>
  <style>
    :root {{ --bg:#07100f; --panel:#0d1a18; --ink:#edf7f2; --muted:#9bb1a8; --line:#294039; --mint:#71f6b6; --amber:#ffd479; --red:#ff8d85; --shadow:0 18px 50px #0006; color-scheme:dark; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:radial-gradient(circle at 75% -10%,#153c32 0,transparent 38rem),var(--bg); color:var(--ink); font:15px/1.55 ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    a {{ color:var(--mint); text-underline-offset:3px; }}
    .shell {{ width:min(1180px,calc(100% - 32px)); margin:auto; }}
    header {{ padding:72px 0 40px; }}
    .eyebrow {{ color:var(--mint); font:700 12px/1.2 ui-monospace,SFMono-Regular,Consolas,monospace; letter-spacing:.16em; text-transform:uppercase; }}
    h1 {{ max-width:830px; margin:12px 0 14px; font-size:clamp(38px,7vw,78px); line-height:.98; letter-spacing:-.055em; }}
    .lede {{ max-width:720px; color:var(--muted); font-size:clamp(17px,2.3vw,21px); }}
    .proof {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:25px; }}
    .proof span {{ padding:7px 11px; border:1px solid var(--line); border-radius:999px; background:#0b1715bb; color:var(--muted); }}
    .controls {{ position:sticky; top:0; z-index:4; display:grid; grid-template-columns:minmax(220px,2fr) repeat(3,minmax(130px,1fr)); gap:10px; padding:14px; border:1px solid var(--line); border-radius:16px; background:#091412ed; backdrop-filter:blur(15px); box-shadow:var(--shadow); }}
    label {{ position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); }}
    input,select {{ width:100%; padding:12px 13px; border:1px solid var(--line); border-radius:10px; background:var(--panel); color:var(--ink); font:inherit; }}
    input:focus,select:focus,a:focus-visible {{ outline:2px solid var(--mint); outline-offset:2px; }}
    .bar {{ display:flex; align-items:center; justify-content:space-between; gap:16px; margin:30px 0 16px; color:var(--muted); }}
    .bar strong {{ color:var(--ink); }}
    #grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; padding-bottom:80px; }}
    article {{ display:flex; flex-direction:column; min-height:260px; padding:22px; border:1px solid var(--line); border-radius:16px; background:linear-gradient(145deg,#0f1f1c,#0a1513); box-shadow:0 12px 35px #0003; }}
    article:hover {{ border-color:#426f5f; transform:translateY(-1px); }}
    article h2 {{ margin:10px 0 8px; font-size:22px; letter-spacing:-.02em; }}
    article p {{ margin:0; color:var(--muted); }}
    .meta,.tags,.links {{ display:flex; flex-wrap:wrap; gap:7px; }}
    .meta span,.tags span {{ padding:3px 8px; border-radius:7px; background:#132823; color:#bad0c6; font-size:12px; }}
    .meta .released {{ color:var(--mint); }} .meta .paper-only {{ color:var(--amber); }} .meta .unavailable {{ color:var(--red); }}
    .tags {{ margin-top:16px; }} .tags span {{ background:#0a1513; border:1px solid var(--line); }}
    .links {{ margin-top:auto; padding-top:18px; }} .links a {{ font-weight:650; }}
    .empty {{ grid-column:1/-1; padding:54px; border:1px dashed var(--line); border-radius:16px; text-align:center; color:var(--muted); }}
    footer {{ padding:28px 0 55px; border-top:1px solid var(--line); color:var(--muted); }}
    @media (max-width:820px) {{ .controls {{ grid-template-columns:1fr 1fr; }} #grid {{ grid-template-columns:1fr; }} }}
    @media (max-width:520px) {{ .shell {{ width:min(100% - 20px,1180px); }} header {{ padding-top:44px; }} .controls {{ position:static; grid-template-columns:1fr; }} }}
    @media (prefers-reduced-motion:no-preference) {{ article {{ transition:border-color .18s,transform .18s; }} }}
  </style>
</head>
<body>
  <header class="shell">
    <div class="eyebrow">Open data · Evidence first</div>
    <h1>Find the right Gaussian stack for your robot.</h1>
    <p class="lede">Filter verified systems across mapping, SLAM, semantics, navigation, manipulation, simulation, and embodied learning. No scraped star counts. No invented compatibility claims.</p>
    <div class="proof"><span>{stats['resources']} reviewed resources</span><span>{stats['with_code']} with code</span><span>verified through {last_verified}</span></div>
  </header>
  <main class="shell">
    <section class="controls" aria-label="Catalog filters">
      <label for="search">Search</label><input id="search" type="search" placeholder="Search task, method, sensor…" autocomplete="off">
      <label for="category">Category</label><select id="category"><option value="">All categories</option>{category_options}</select>
      <label for="input">Input</label><select id="input"><option value="">All inputs</option>{input_options}</select>
      <label for="code">Code status</label><select id="code"><option value="">Any code status</option><option value="released">Released</option><option value="partial">Partial</option><option value="paper-only">Paper only</option><option value="archived">Archived</option><option value="unavailable">Unavailable</option></select>
    </section>
    <div class="bar"><div id="count" aria-live="polite"></div><a href="https://github.com/Laityperfect7/awesome-gaussian-robotics/blob/main/CATALOG.md">Markdown view</a></div>
    <section id="grid" aria-label="Catalog results"></section>
  </main>
  <footer><div class="shell">Built from reviewable JSON. Missing metadata means unknown—not unsupported. <a href="https://github.com/Laityperfect7/awesome-gaussian-robotics">Contribute evidence</a>.</div></footer>
  <script id="atlas-data" type="application/json">{data}</script>
  <script>
  (() => {{
    'use strict';
    const data = JSON.parse(document.getElementById('atlas-data').textContent);
    const labels = {category_labels};
    const controls = ['search','category','input','code'].map(id => document.getElementById(id));
    const grid = document.getElementById('grid');
    const count = document.getElementById('count');
    const params = new URLSearchParams(location.search);
    controls.forEach(el => {{ if (params.has(el.id)) el.value = params.get(el.id); }});
    function node(tag, text, cls) {{ const el=document.createElement(tag); if(text!==undefined) el.textContent=text; if(cls) el.className=cls; return el; }}
    function addLink(box, label, url) {{ if(!url) return; const link=node('a',label); link.href=url; link.rel='noopener noreferrer'; box.append(link); }}
    function card(item) {{
      const article=node('article');
      const meta=node('div',undefined,'meta');
      meta.append(node('span',labels[item.category] || item.category),node('span',String(item.year)),node('span',item.code_status,item.code_status));
      article.append(meta,node('h2',item.name),node('p',item.summary));
      const tags=node('div',undefined,'tags');
      [...item.inputs,...item.capabilities.slice(0,3)].forEach(value=>tags.append(node('span',value)));
      article.append(tags);
      const links=node('div',undefined,'links');
      addLink(links,'Paper',item.paper_url); addLink(links,'Project',item.project_url); addLink(links,'Code',item.code_url);
      article.append(links); return article;
    }}
    function update() {{
      const q=controls[0].value.trim().toLowerCase(), category=controls[1].value, input=controls[2].value, code=controls[3].value;
      const visible=data.filter(item => {{
        const hay=[item.name,item.summary,item.venue,item.category,...item.inputs,...item.frameworks,...item.capabilities,...item.tags].join(' ').toLowerCase();
        return (!q || q.split(/\\s+/).every(term=>hay.includes(term))) && (!category || item.category===category) && (!input || item.inputs.includes(input)) && (!code || item.code_status===code);
      }});
      grid.replaceChildren(...(visible.length ? visible.map(card) : [node('div','No verified resources match these filters. Try removing one constraint.','empty')]));
      count.textContent=`${{visible.length}} of ${{data.length}} resources`;
      const next=new URLSearchParams(); controls.forEach(el=>{{if(el.value)next.set(el.id,el.value);}}); history.replaceState(null,'',next.size?'?'+next:'./');
    }}
    controls.forEach(el=>el.addEventListener(el.id==='search'?'input':'change',update)); update();
  }})();
  </script>
</body>
</html>
"""


def render_all(resources: Iterable[Resource], taxonomy: Taxonomy) -> dict[Path, str]:
    items = tuple(resources)
    return {
        Path("CATALOG.md"): render_catalog_markdown(items, taxonomy),
        Path("docs/catalog.json"): render_catalog_json(items),
        Path("docs/catalog.csv"): render_catalog_csv(items),
        Path("docs/stats.json"): json.dumps(
            catalog_stats(items), ensure_ascii=False, indent=2, sort_keys=True
        )
        + "\n",
        Path("docs/index.html"): render_site(items, taxonomy),
    }


def write_outputs(
    outputs: dict[Path, str],
    root: str | Path,
    *,
    check: bool = False,
) -> tuple[Path, ...]:
    base = Path(root)
    changed: list[Path] = []
    for relative, content in sorted(outputs.items(), key=lambda pair: pair[0].as_posix()):
        path = base / relative
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        changed.append(relative)
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    return tuple(changed)
