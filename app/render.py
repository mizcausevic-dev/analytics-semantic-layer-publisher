from __future__ import annotations

import html
import json
from pathlib import Path

from app.services.semantic_service import build_service


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def page_shell(title: str, kicker: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_escape(title)}</title>
  <style>
    :root {{
      --bg: #07111d;
      --panel: #0d1a2b;
      --panel-2: #12233a;
      --line: #1d3655;
      --text: #eef2ff;
      --muted: #98a7c2;
      --accent: #68b7ff;
      --accent-2: #f0d7a1;
      --green: #6ce1b1;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", Inter, sans-serif;
      background: linear-gradient(180deg, #07111d 0%, #091827 100%);
      color: var(--text);
    }}
    .page {{
      width: 1440px;
      margin: 0 auto;
      padding: 48px 52px 64px;
      background:
        radial-gradient(circle at top right, rgba(104,183,255,0.16), transparent 28%),
        linear-gradient(180deg, rgba(11,25,41,0.95), rgba(6,14,24,0.98));
      min-height: 920px;
    }}
    .frame {{
      border: 1px solid var(--line);
      border-radius: 34px;
      padding: 28px 32px 36px;
      background: rgba(11, 22, 37, 0.88);
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 15px;
      letter-spacing: 0.34em;
      text-transform: uppercase;
      margin-bottom: 18px;
      font-weight: 700;
    }}
    h1 {{
      margin: 0;
      font-size: 68px;
      line-height: 0.96;
      color: #f4f1e3;
      font-family: Georgia, "Times New Roman", serif;
      max-width: 1100px;
    }}
    .lede {{
      margin-top: 18px;
      max-width: 900px;
      color: var(--muted);
      font-size: 18px;
      line-height: 1.6;
    }}
    .pill-row {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 26px;
    }}
    .pill {{
      border-radius: 999px;
      padding: 10px 16px;
      background: #1a2f4d;
      border: 1px solid #29486e;
      color: #f5f8ff;
      font-size: 15px;
      font-weight: 600;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin-top: 28px;
    }}
    .stat {{
      padding: 22px 22px 18px;
      border-radius: 24px;
      background: #12233a;
      border: 1px solid #25415f;
      min-height: 162px;
    }}
    .stat .label {{
      color: #a8b6cd;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 13px;
      margin-bottom: 14px;
    }}
    .stat .value {{
      color: #f4f1e3;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 52px;
      line-height: 0.95;
      margin-bottom: 12px;
    }}
    .stat .copy {{
      color: #c1cadc;
      font-size: 16px;
      line-height: 1.5;
    }}
    .section {{
      margin-top: 34px;
      border-radius: 28px;
      border: 1px solid #203654;
      background: #0d1524;
      padding: 28px;
    }}
    .section-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }}
    .card {{
      border-radius: 22px;
      border: 1px solid #263d5f;
      background: #131e32;
      padding: 22px;
      min-height: 240px;
    }}
    .card .kicker {{
      color: var(--accent);
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.18em;
      margin-bottom: 18px;
      font-weight: 700;
    }}
    .card h2 {{
      font-size: 24px;
      line-height: 1.15;
      margin: 0 0 14px;
      color: #f4f1e3;
      font-family: Georgia, "Times New Roman", serif;
    }}
    .card p, .card li {{
      color: #bdc7d9;
      font-size: 16px;
      line-height: 1.55;
      margin: 0;
    }}
    .card ul {{
      padding-left: 18px;
      margin: 0;
    }}
    pre {{
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      color: #d7f7da;
      font-size: 15px;
      line-height: 1.45;
      font-family: Consolas, "SFMono-Regular", monospace;
    }}
    .json {{
      background: #07101b;
      border: 1px solid #284462;
      border-radius: 22px;
      padding: 24px;
      margin-top: 24px;
    }}
    .footer-note {{
      margin-top: 24px;
      color: #8fa5c3;
      font-size: 15px;
    }}
  </style>
</head>
<body>
  <div class="page">
    <div class="frame">
      <div class="eyebrow">{_escape(kicker)}</div>
      {body}
    </div>
  </div>
</body>
</html>
"""


def render_overview() -> str:
    service = build_service()
    summary = service.summary()
    metrics = service.catalog()["metrics"]
    body = f"""
      <h1>Publish your semantic layer so AI agents stop guessing what CAC means.</h1>
      <p class="lede">
        Analytics Semantic Layer Publisher turns dbt-style metric definitions into
        structured JSON-LD, a browsable metric catalog, and AI-readable evidence
        lanes that explain ownership, formula logic, and dimensional cuts.
      </p>
      <div class="pill-row">
        <div class="pill">dbt semantic models</div>
        <div class="pill">JSON-LD export</div>
        <div class="pill">AI-ready metric definitions</div>
        <div class="pill">DataCatalog proof</div>
      </div>
      <div class="stats">
        <div class="stat"><div class="label">Metrics published</div><div class="value">{summary['metricCount']}</div><div class="copy">Board and operator metrics published as machine-readable semantic definitions.</div></div>
        <div class="stat"><div class="label">Board metrics</div><div class="value">{summary['boardMetricCount']}</div><div class="copy">High-stakes finance metrics with explicit formula and ownership lanes.</div></div>
        <div class="stat"><div class="label">Operator metrics</div><div class="value">{summary['operatorMetricCount']}</div><div class="copy">Day-to-day metrics built for action, not just retrospective reporting.</div></div>
        <div class="stat"><div class="label">Owner lanes</div><div class="value">{summary['ownerCount']}</div><div class="copy">Metric accountability mapped to the teams who can answer follow-up questions.</div></div>
      </div>
      <div class="section">
        <div class="section-grid">
          {''.join(
              f'''<div class="card"><div class="kicker">{_escape(metric["service_tier"])}</div><h2>{_escape(metric["label"])}</h2><p>{_escape(metric["description"])}</p><div class="footer-note">Formula: {_escape(metric["formula"])}</div></div>'''
              for metric in metrics
          )}
        </div>
      </div>
    """
    return page_shell(
        "Analytics Semantic Layer Publisher - Overview",
        "analytics semantic layer publisher",
        body,
    )


def render_catalog() -> str:
    service = build_service()
    catalog = service.catalog()
    body = f"""
      <h1>Metric contracts, dimensions, and owners laid out as an AI-queryable catalog.</h1>
      <p class="lede">
        Instead of burying metric definitions in dashboards and Slack threads, this
        surface turns semantic models into a published catalog that search systems,
        copilots, and internal operators can resolve by name.
      </p>
      <div class="section">
        <div class="section-grid">
          {''.join(
              f'''<div class="card"><div class="kicker">{_escape(model["label"])}</div><h2>{_escape(model["primary_entity"])} at {_escape(model["grain"])}</h2><p>{_escape(model["description"])}</p><div class="footer-note">Owners: {_escape(", ".join(model.get("owners", [])))}</div><div class="footer-note">Measures: {_escape(", ".join(measure["label"] for measure in model.get("measures", [])))}</div></div>'''
              for model in catalog["semanticModels"]
          )}
        </div>
      </div>
      <div class="section">
        <div class="section-grid">
          {''.join(
              f'''<div class="card"><div class="kicker">{_escape(metric["owner"])}</div><h2>{_escape(metric["label"])}</h2><ul>{''.join(f"<li>{_escape(question)}</li>" for question in metric["ai_questions"])}</ul><div class="footer-note">Dimensions: {_escape(", ".join(metric["dimensions"]))}</div></div>'''
              for metric in catalog["metrics"]
          )}
        </div>
      </div>
    """
    return page_shell(
        "Analytics Semantic Layer Publisher - Catalog",
        "catalog lane",
        body,
    )


def render_evidence() -> str:
    service = build_service()
    jsonld = service.catalog_jsonld()
    metric = service.metric_jsonld("customer_acquisition_cost")
    body = f"""
      <h1>JSON-LD proof that gives AI systems a citation-ready definition layer.</h1>
      <p class="lede">
        The publisher emits schema.org DataCatalog and DefinedTerm records so AI
        systems can resolve metric names, formulas, dependencies, and ownership
        before they generate answers, summaries, or decision support.
      </p>
      <div class="section-grid">
        <div class="card">
          <div class="kicker">catalog export</div>
          <h2>Whole semantic layer published as a DataCatalog.</h2>
          <p>Datasets, dimensions, measures, and metric definitions roll up into a single machine-readable knowledge surface.</p>
        </div>
        <div class="card">
          <div class="kicker">metric contract</div>
          <h2>Each KPI can stand alone as a DefinedTerm.</h2>
          <p>That makes terms like CAC, NRR, and Pipeline per Dollar directly referencable by copilots and search systems.</p>
        </div>
        <div class="card">
          <div class="kicker">operator impact</div>
          <h2>Follow-up questions route back to the right team.</h2>
          <p>Ownership is embedded alongside formulas and dependencies, which reduces answer drift and ambiguous metric debates.</p>
        </div>
      </div>
      <div class="json"><pre>{_escape(json.dumps(jsonld, indent=2))}</pre></div>
      <div class="json"><pre>{_escape(json.dumps(metric, indent=2))}</pre></div>
    """
    return page_shell(
        "Analytics Semantic Layer Publisher - Evidence",
        "json-ld proof",
        body,
    )


def render_api_summary() -> str:
    payload = build_service().api_payload()
    body = f"""
      <h1>A lightweight API surface for metrics, catalogs, and semantic exports.</h1>
      <p class="lede">
        This repo ships a practical API layer as well as the semantic export, so teams
        can publish definitions for both humans and agents without standing up a
        whole BI platform first.
      </p>
      <div class="section-grid">
        <div class="card">
          <div class="kicker">routes</div>
          <h2>Catalog, metrics, and JSON-LD endpoints.</h2>
          <p><code>/api/catalog</code>, <code>/api/metrics</code>, <code>/semantic/catalog.jsonld</code>, and metric-specific export routes.</p>
        </div>
        <div class="card">
          <div class="kicker">usage</div>
          <h2>Good for AEO, BI docs, and internal copilots.</h2>
          <p>It can power metric glossaries, schema proof pages, prompt context, and semantic metric explorers.</p>
        </div>
        <div class="card">
          <div class="kicker">payload</div>
          <h2>Sample API response from the local publisher.</h2>
          <p>Small enough to inspect quickly, rich enough to prove the publishing model.</p>
        </div>
      </div>
      <div class="json"><pre>{_escape(json.dumps(payload, indent=2))}</pre></div>
    """
    return page_shell(
        "Analytics Semantic Layer Publisher - API Summary",
        "api summary",
        body,
    )


def write_static_proof_pages(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "01-overview.html": render_overview(),
        "02-catalog-lane.html": render_catalog(),
        "03-jsonld-proof.html": render_evidence(),
        "04-api-summary.html": render_api_summary(),
    }
    written: list[Path] = []
    for name, contents in pages.items():
        target = output_dir / name
        target.write_text(contents, encoding="utf-8")
        written.append(target)
    return written
