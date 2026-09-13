"""Install the reviewed Crew Hab q0 card and record directional review."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets/crew-hab-directional-v2"
CAPTURE = ROOT / "output/crew-hab-owner-repair-2026-09-12/candidate-native/crew_hab-q0.png"
CARD = ROOT / "assets/room-declutter-v1/cards/crew_hab.png"


def main() -> None:
    shutil.copyfile(CAPTURE, CARD)
    review = {
        "room": "crew_hab",
        "status": "integrated and native-reviewed",
        "evidence": "output/crew-hab-owner-repair-2026-09-12/candidate-native",
        "directions_reviewed": ["north", "east", "south", "west"],
        "card": str(CARD.relative_to(ROOT)).replace("\\", "/"),
        "card_sha256": hashlib.sha256(CARD.read_bytes()).hexdigest(),
        "findings": [
            "Every wall uses the same three compact overhead berth pods.",
            "Mattress and pillow access faces the room interior in all four directions.",
            "Rejected oversized bed, wardrobe and canopy elevations are no longer selected.",
            "Independent desk, chair and freestanding bed remain unchanged.",
        ],
    }
    (PACK / "review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
