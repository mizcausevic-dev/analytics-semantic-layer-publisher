from __future__ import annotations

import json

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.semantic_service import build_service


def main() -> None:
    service = build_service()
    payload = {
        "summary": service.summary(),
        "metricNames": [metric["name"] for metric in service.catalog()["metrics"]],
        "catalogJsonLdKeys": list(service.catalog_jsonld().keys()),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
