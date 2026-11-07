"""Install the reviewed Maintenance q0 capture and write review provenance."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets/maintenance-directional-v2"
CAPTURE = ROOT / "output/maintenance-owner-repair-2026-09-12/candidate-native/maintenance_bay-q0.png"
CARD = ROOT / "assets/maintenance-directional-v1/cards/maintenance_bay.png"


def main() -> None:
    shutil.copyfile(CAPTURE, CARD)
    review = {
        "room": "maintenance_bay",
        "status": "integrated and native-reviewed",
        "evidence": "output/maintenance-owner-repair-2026-09-12/candidate-native",
        "directions_reviewed": ["north", "east", "south", "west"],
        "card": str(CARD.relative_to(ROOT)).replace("\\", "/"),
        "card_sha256": hashlib.sha256(CARD.read_bytes()).hexdigest(),
        "findings": [
            "Accepted south overhead tool bank supplies all directions through exact turns.",
            "Tool grips, vise and drawer handles face inward in every direction.",
            "Saturated orange is reduced while pale steel tools and the yellow shop cloth remain distinct.",
            "Border-connected neutral removal produces true alpha without erasing interior pale materials.",
        ],
    }
    (PACK / "review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
