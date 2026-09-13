"""Install the reviewed Isolation Vault card and owner-repair record."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets/isolation-directional-v2"
CAPTURE = ROOT / "output/isolation-owner-repair-2026-09-12/candidate-native/isolation_vault-q0.png"
CARD = ROOT / "assets/isolation-directional-v1/north-cards/isolation_vault.png"


def main() -> None:
    shutil.copyfile(CAPTURE, CARD)
    review = {
        "room": "isolation_vault",
        "status": "integrated and native-reviewed",
        "evidence": "output/isolation-owner-repair-2026-09-12/candidate-native",
        "directions_reviewed": ["north", "east", "south", "west"],
        "card": str(CARD.relative_to(ROOT)).replace("\\", "/"),
        "card_sha256": hashlib.sha256(CARD.read_bytes()).hexdigest(),
        "removed_runtime_assets": [
            "isolation-u-flush-clean-v1 baked perimeter",
            "battery_bank_west",
            "battery_bank_east",
            "battery_breaker",
            "battery_distribution",
            "battery_test_bench",
            "battery_cable_reel",
        ],
        "findings": [
            "Every wall uses the owner-approved south Emergency Isolation bank.",
            "The sealed chamber and supply access face inward through exact quarter turns.",
            "The vault borrowed its battery furnishings by inheriting Battery Array; that accidental layer is removed.",
            "The Battery Array test-bench source received a separate matte highlight pass for any remaining consumer.",
        ],
    }
    (PACK / "review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
