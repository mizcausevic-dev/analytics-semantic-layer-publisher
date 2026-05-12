from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class SemanticLayerService:
    source_path: Path

    def load(self) -> dict[str, Any]:
        return yaml.safe_load(self.source_path.read_text(encoding="utf-8"))

    def catalog(self) -> dict[str, Any]:
        data = self.load()
        models = data["semantic_models"]
        metrics = data["metrics"]
        owners = sorted(
            {
                *(metric["owner"] for metric in metrics),
                *(
                    owner
                    for model in models
                    for owner in model.get("owners", [])
                ),
            }
        )
        dimension_count = sum(len(model.get("dimensions", [])) for model in models)
        measure_count = sum(len(model.get("measures", [])) for model in models)
        return {
            "catalog": data["catalog"],
            "semanticModels": models,
            "metrics": metrics,
            "stats": {
                "modelCount": len(models),
                "metricCount": len(metrics),
                "dimensionCount": dimension_count,
                "measureCount": measure_count,
                "owners": owners,
            },
        }

    def metric(self, name: str) -> dict[str, Any] | None:
        data = self.catalog()
        for metric in data["metrics"]:
            if metric["name"] == name:
                return metric
        return None

    def metric_jsonld(self, metric_name: str) -> dict[str, Any]:
        metric = self.metric(metric_name)
        if metric is None:
            raise KeyError(metric_name)
        catalog = self.catalog()["catalog"]
        return {
            "@context": "https://schema.org",
            "@type": "DefinedTerm",
            "name": metric["label"],
            "termCode": metric["name"],
            "description": metric["description"],
            "alternateName": metric["formula"],
            "inDefinedTermSet": f"{catalog['publication_url']}/semantic/catalog.jsonld",
            "keywords": metric["tags"],
            "measurementTechnique": metric["formula"],
            "maintainer": {
                "@type": "Organization",
                "name": metric["owner"],
            },
            "variableMeasured": [
                {
                    "@type": "PropertyValue",
                    "name": dependency,
                    "description": f"Dependency required for {metric['label']}",
                }
                for dependency in metric.get("dependencies", [])
            ],
        }

    def catalog_jsonld(self) -> dict[str, Any]:
        data = self.catalog()
        catalog = data["catalog"]
        return {
            "@context": "https://schema.org",
            "@type": "DataCatalog",
            "name": catalog["name"],
            "description": catalog["description"],
            "keywords": catalog["tags"],
            "creator": {
                "@type": "Organization",
                "name": catalog["owner"],
            },
            "dataset": [
                {
                    "@type": "Dataset",
                    "name": model["label"],
                    "identifier": model["name"],
                    "description": model["description"],
                    "keywords": [model["primary_entity"], model["grain"]],
                    "measurementTechnique": [
                        measure["label"] for measure in model.get("measures", [])
                    ],
                    "variableMeasured": [
                        {
                            "@type": "PropertyValue",
                            "name": dimension["name"],
                            "description": dimension["description"],
                        }
                        for dimension in model.get("dimensions", [])
                    ],
                }
                for model in data["semanticModels"]
            ],
            "hasPart": [
                self.metric_jsonld(metric["name"]) for metric in data["metrics"]
            ],
        }

    def summary(self) -> dict[str, Any]:
        data = self.catalog()
        metrics = data["metrics"]
        board_metrics = [metric for metric in metrics if metric["service_tier"] == "board"]
        operator_metrics = [
            metric for metric in metrics if metric["service_tier"] == "operator"
        ]
        return {
            "catalogName": data["catalog"]["name"],
            "metricCount": len(metrics),
            "boardMetricCount": len(board_metrics),
            "operatorMetricCount": len(operator_metrics),
            "ownerCount": len(data["stats"]["owners"]),
            "leadRecommendation": (
                "Publish semantic definitions as JSON-LD so AI agents can resolve "
                "metric meaning before hallucinating KPI answers."
            ),
        }

    def api_payload(self) -> dict[str, Any]:
        data = self.catalog()
        return {
            "dashboard": self.summary(),
            "metrics": [
                {
                    "name": metric["name"],
                    "label": metric["label"],
                    "owner": metric["owner"],
                    "formula": metric["formula"],
                    "questions": metric["ai_questions"],
                }
                for metric in data["metrics"]
            ],
            "catalogJsonLdUrl": f"{data['catalog']['publication_url']}/semantic/catalog.jsonld",
        }


def build_service(root: Path | None = None) -> SemanticLayerService:
    base = root or Path(__file__).resolve().parents[2]
    return SemanticLayerService(base / "app" / "data" / "sample_semantic_layer.yml")
