"""Finalize provenance and card selection for the Xeno overhead wall repair."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets/xeno-directional-v2"
REJECTED = Path(r"C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-3212e429-aa29-4bef-924c-3342ca038460.png")
CAPTURE = ROOT / "output/xeno-owner-repair-2026-09-12/candidate-native/xeno_lab-q0.png"
CARD = ROOT / "assets/xeno-directional-v1/cards/xeno_lab.png"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    # The tool-returned rejected path can vary; retain it when available, while
    # keeping the rejection recorded even if a cache cleanup has removed it.
    rejected_target = PACK / "raw/north-overhead-rejected-elevation-v1.png"
    if REJECTED.exists():
        shutil.copyfile(REJECTED, rejected_target)
    shutil.copyfile(CAPTURE, CARD)
    selected_raw = PACK / "raw/north-overhead-v1.png"
    prompts = {
        "room": "xeno_lab",
        "selected_raw": str(selected_raw.relative_to(ROOT)).replace("\\", "/"),
        "selected_raw_sha256": digest(selected_raw),
        "selected_direction": "strict top-down shallow specimen bench with inward glove ports",
        "rejected_reason": "First candidate retained a frontal product elevation and checkerboard-like exterior.",
        "rejected_path": str(rejected_target.relative_to(ROOT)).replace("\\", "/") if rejected_target.exists() else "",
        "rejected_sha256": digest(rejected_target) if rejected_target.exists() else "",
    }
    (PACK / "prompts.json").write_text(json.dumps(prompts, indent=2) + "\n", encoding="utf-8")
    review = {
        "room": "xeno_lab",
        "status": "integrated and native-reviewed",
        "evidence": "output/xeno-owner-repair-2026-09-12/candidate-native",
        "directions_reviewed": ["north", "east", "south", "west"],
        "card": str(CARD.relative_to(ROOT)).replace("\\", "/"),
        "card_sha256": digest(CARD),
        "findings": [
            "One strict-overhead containment bank is used through exact quarter turns.",
            "Rear rail stays wall-side and glove ports, controls and access edge face inward in every direction.",
            "Existing independent Xeno machinery, activity anchors and gameplay behavior are unchanged.",
        ],
    }
    (PACK / "review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
