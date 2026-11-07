"""Install the reviewed Bio Lab q0 card and directional review."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets/bio-directional-v2"
CAPTURE = ROOT / "output/bio-owner-repair-2026-09-12/candidate-native/bio_lab-q0.png"
CARD = ROOT / "assets/bio-directional-v1/cards/bio_lab.png"


def main() -> None:
    shutil.copyfile(CAPTURE, CARD)
    review = {
        "room": "bio_lab",
        "status": "integrated and native-reviewed",
        "evidence": "output/bio-owner-repair-2026-09-12/candidate-native",
        "directions_reviewed": ["north", "east", "south", "west"],
        "card": str(CARD.relative_to(ROOT)).replace("\\", "/"),
        "card_sha256": hashlib.sha256(CARD.read_bytes()).hexdigest(),
        "findings": [
            "Every wall uses the accepted shallow Bio Culture bench.",
            "Microscope eyepieces, jar access and the instrument case face inward.",
            "Tall trough and front-elevation companions remain archived but are no longer selected.",
            "Independent centrifuge and sample cabinet remain unchanged.",
        ],
    }
    (PACK / "review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
