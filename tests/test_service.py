from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.services.semantic_service import build_service


class SemanticLayerTests(unittest.TestCase):
    def test_summary_counts(self) -> None:
        summary = build_service().summary()
        self.assertGreaterEqual(summary["metricCount"], 3)
        self.assertGreaterEqual(summary["ownerCount"], 3)

    def test_metric_jsonld_contains_formula(self) -> None:
        jsonld = build_service().metric_jsonld("customer_acquisition_cost")
        self.assertEqual(jsonld["termCode"], "customer_acquisition_cost")
        self.assertIn("spend / acquired_accounts", jsonld["alternateName"])

    def test_api_routes(self) -> None:
        client = TestClient(app)
        response = client.get("/api/metrics/customer_acquisition_cost")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["owner"], "Revenue Strategy")


if __name__ == "__main__":
    unittest.main()
