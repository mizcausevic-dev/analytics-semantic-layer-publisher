from __future__ import annotations

import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from app.render import (
    render_api_summary,
    render_catalog,
    render_evidence,
    render_overview,
)
from app.services.semantic_service import build_service

app = FastAPI(
    title="Analytics Semantic Layer Publisher",
    version="0.1.0",
    description=(
        "Publishes a dbt-style semantic layer as structured JSON-LD, AI-readable "
        "metric contracts, and browsable catalog pages."
    ),
)

service = build_service()


@app.get("/", response_class=HTMLResponse)
def overview() -> str:
    return render_overview()


@app.get("/catalog", response_class=HTMLResponse)
def catalog_page() -> str:
    return render_catalog()


@app.get("/evidence", response_class=HTMLResponse)
def evidence_page() -> str:
    return render_evidence()


@app.get("/api-summary", response_class=HTMLResponse)
def api_summary_page() -> str:
    return render_api_summary()


@app.get("/api/dashboard/summary")
def dashboard_summary() -> dict:
    return service.summary()


@app.get("/api/catalog")
def api_catalog() -> dict:
    return service.catalog()


@app.get("/api/metrics")
def api_metrics() -> list[dict]:
    return service.catalog()["metrics"]


@app.get("/api/metrics/{metric_name}")
def api_metric(metric_name: str) -> dict:
    metric = service.metric(metric_name)
    if metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric


@app.get("/api/sample")
def api_sample() -> dict:
    return service.api_payload()


@app.get("/semantic/catalog.jsonld")
def semantic_catalog() -> JSONResponse:
    return JSONResponse(service.catalog_jsonld())


@app.get("/semantic/metrics/{metric_name}.jsonld")
def semantic_metric(metric_name: str) -> JSONResponse:
    try:
        return JSONResponse(service.metric_jsonld(metric_name))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Metric not found") from exc


@app.get("/openapi.json")
def openapi_spec() -> JSONResponse:
    return JSONResponse(json.loads(json.dumps(app.openapi())))


if __name__ == "__main__":
    import os

    import uvicorn

    port = int(os.environ.get("PORT", "4604"))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
