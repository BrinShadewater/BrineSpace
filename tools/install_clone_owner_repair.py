"""Install the reviewed Clone Lab q0 card and directional review record."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets/clone-directional-v2"
CAPTURE = ROOT / "output/clone-owner-repair-2026-09-12/candidate-native/clone_lab-q0.png"
CARD = ROOT / "assets/clone-directional-v1/cards/clone_lab.png"


def main() -> None:
    shutil.copyfile(CAPTURE, CARD)
    review = {
        "room": "clone_lab",
        "status": "integrated and native-reviewed",
        "evidence": "output/clone-owner-repair-2026-09-12/candidate-native",
        "directions_reviewed": ["north", "east", "south", "west"],
        "card": str(CARD.relative_to(ROOT)).replace("\\", "/"),
        "card_sha256": hashlib.sha256(CARD.read_bytes()).hexdigest(),
        "findings": [
            "Every wall uses the owner-approved east Clone Growth bank.",
            "Outer service rail remains wall-side while growth window, microscope and controls face inward.",
            "The prior frontal north bank and shallow south appliance strip remain archived but are no longer selected.",
            "Independent nutrient rack and analysis counter remain unchanged.",
        ],
    }
    (PACK / "review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
