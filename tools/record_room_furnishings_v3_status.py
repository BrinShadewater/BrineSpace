"""Prepend the v3 furnishing milestone without decoding legacy status bytes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
MARKER = b"## Themed and universal room furnishings v3 - September 13, 2026\r\n"
BLOCK = (
    "## Themed and universal room furnishings v3 - September 13, 2026\r\n\r\n"
    "Six additional matte furnishings are integrated across Hydroponics Bay, Ore Refinery, Cryo Chamber, Quarantine Cell, Pressure Control and Isolation Vault. The themed nutrient island, sorting bench and thaw cart reinforce room activity; the neutral parts chest, equipment plinth and task table add sparse station-wide support.\r\n\r\n"
    "All 24 native orientations and six refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-003920-headless`. The batch remains locally saved with owner aesthetic acceptance and export pending. See `docs/ROOM_FURNISHINGS_V3_2026-09-13.md`.\r\n\r\n"
).encode("ascii")


def main() -> None:
    original = STATUS.read_bytes()
    if MARKER in original:
        print("Room furnishings v3 status already recorded")
        return
    STATUS.write_bytes(BLOCK + original)
    print("Recorded room furnishings v3 status")


if __name__ == "__main__":
    main()
