"""Prepend the v5 furnishing milestone without decoding legacy status bytes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
MARKER = b"## Cross-department themed and universal furnishings v5 - September 13, 2026\r\n"
BLOCK = (
    "## Cross-department themed and universal furnishings v5 - September 13, 2026\r\n\r\n"
    "Reactor, Clone Lab and Biodome now pair a large matte themed workstation with one medium neutral support furnishing. The control-rod inspection bench, genome-preparation island and potting-and-seed island replace smaller generic work pieces; a sealed tool chest, rolling sample trolley and folding supply pallet demonstrate the reusable family across engineering, clinical science and cultivation.\r\n\r\n"
    "All 12 native orientations and three refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-011605-headless`; the focused asset audit reports zero errors. Owner aesthetic acceptance and export remain pending. See `docs/ROOM_FURNISHINGS_V5_2026-09-13.md`.\r\n\r\n"
).encode("ascii")


def main() -> None:
    original = STATUS.read_bytes()
    if MARKER in original:
        print("Room furnishings v5 status already recorded")
        return
    STATUS.write_bytes(BLOCK + original)
    print("Recorded room furnishings v5 status")


if __name__ == "__main__":
    main()
