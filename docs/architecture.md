# Analytics Semantic Layer Publisher Architecture

## Intent

This repo turns a dbt-style semantic layer into two publishing surfaces:

- a browsable HTML catalog for humans
- JSON-LD exports for AI systems, search systems, and internal copilots

The goal is to make metric definitions queryable by name before someone asks a
copilot "what does CAC mean here?" and gets an answer that drifts away from the
real semantic contract.

## Flow

1. `app/data/sample_semantic_layer.yml` stores the semantic layer source of truth.
2. `app/services/semantic_service.py` loads and normalizes the catalog.
3. `app/main.py` exposes FastAPI routes for:
   - HTML proof pages
   - metric and catalog APIs
   - JSON-LD exports
4. `app/render.py` produces the visual proof pages used by the README.
5. `scripts/render_readme_assets.py` renders static HTML files and captures PNG screenshots.

## Core Surfaces

- `/`
  - Overview page for the publisher and key metric stats
- `/catalog`
  - Human-readable semantic model and metric lane
- `/evidence`
  - JSON-LD proof and explanation of why the export is useful
- `/api-summary`
  - API-oriented surface for the route contract and sample payload
- `/api/catalog`
  - Full semantic catalog payload
- `/api/metrics`
  - Metric list
- `/api/metrics/{name}`
  - Single metric definition
- `/semantic/catalog.jsonld`
  - Schema.org DataCatalog export
- `/semantic/metrics/{name}.jsonld`
  - Schema.org DefinedTerm export for a single metric

## Why This Matters

Semantic layers usually stop at BI tooling. This project pushes the same
definitions into a portable structured format so:

- AI agents can ground their answers in official metric definitions
- search systems can ingest named KPI definitions
- internal docs can point at one canonical semantic layer instead of duplicating logic
- ownership and dependency chains stay attached to every metric

## Validation

- `py -3.11 -m unittest discover -s tests`
- `py -3.11 scripts\run_demo.py`
- `py -3.11 scripts\smoke_check.py`
- `py -3.11 scripts\render_readme_assets.py`
