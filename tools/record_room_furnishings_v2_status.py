"""Prepend the v2 furnishing milestone without decoding legacy status bytes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
MARKER = b"## Themed and universal room furnishings v2 - September 13, 2026\r\n"
BLOCK = (
    "## Themed and universal room furnishings v2 - September 13, 2026\r\n\r\n"
    "Six additional rectangular matte furnishings are integrated across Research Lab, Command Center, Medical Center, Crew Hab, Anomaly Lab and Medical Office. Three are themed and three form a neutral station-wide family; the batch is evenly split between large and medium assets. All sources are true-alpha 1254-square rasters with external registrations.\r\n\r\n"
    "All 24 native orientations and six refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-001455-headless`. The batch remains locally saved with owner aesthetic acceptance and export pending. See `docs/ROOM_FURNISHINGS_V2_2026-09-13.md`.\r\n\r\n"
).encode("ascii")


def main() -> None:
    original = STATUS.read_bytes()
    if MARKER in original:
        print("Room furnishings v2 status already recorded")
        return
    STATUS.write_bytes(BLOCK + original)
    print("Recorded room furnishings v2 status")


if __name__ == "__main__":
    main()
