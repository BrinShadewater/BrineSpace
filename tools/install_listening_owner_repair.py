"""Install the reviewed Listening Post q0 capture as its live catalog card."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPTURE = ROOT / "output/listening-owner-repair-2026-09-12/final-native/listening_post-q0.png"
CARD = ROOT / "assets/listening-directional-v1/live-cards/listening_post.png"


def main() -> None:
    shutil.copyfile(CAPTURE, CARD)
    review = {
        "room": "listening_post",
        "status": "integrated and native-reviewed",
        "evidence": "output/listening-owner-repair-2026-09-12/final-native",
        "directions_reviewed": ["north", "east", "south", "west"],
        "north_source": "assets/rooms/listening-post/walls/north.png",
        "equipment_source": "assets/rooms/listening-post/source/listening-equipment.png",
        "card": str(CARD.relative_to(ROOT)).replace("\\", "/"),
        "card_sha256": hashlib.sha256(CARD.read_bytes()).hexdigest(),
        "findings": [
            "All four selected wall banks use the navy, teal and brass Deepwater family and face inward.",
            "The retired q0 U-shaped installation remains on disk but is no longer selected by the live view.",
            "Listening-only equipment trim changes saturated radio red to muted brass without changing geometry or operation.",
        ],
    }
    (ROOT / "assets/listening-directional-v2/review.json").write_text(
        json.dumps(review, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
