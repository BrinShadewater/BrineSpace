"""Install the reviewed Biomass Digester card and material review record."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets/biomass-material-v2"
CAPTURE = ROOT / "output/biomass-owner-repair-2026-09-12/candidate-native/biomass_digester-q0.png"
CARD = ROOT / "assets/room-declutter-v1/cards/biomass_digester.png"


def main() -> None:
    shutil.copyfile(CAPTURE, CARD)
    review = {
        "room": "biomass_digester",
        "status": "integrated and native-reviewed",
        "evidence": "output/biomass-owner-repair-2026-09-12/candidate-native",
        "directions_reviewed": ["north", "east", "south", "west"],
        "card": str(CARD.relative_to(ROOT)).replace("\\", "/"),
        "card_sha256": hashlib.sha256(CARD.read_bytes()).hexdigest(),
        "findings": [
            "Strong Biomass Processing wall geometry retained in every direction.",
            "Orange wall hardware now uses a muted moss family tied to feedstock and process windows.",
            "Shared service console receives a Biomass-only legibility tint instead of the inherited dark multiplier.",
            "Biomass service-support source now has true alpha and lifted matte bench midtones.",
        ],
    }
    (PACK / "review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
