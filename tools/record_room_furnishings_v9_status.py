"""Prepend the v9 furnishing milestone without decoding legacy status bytes."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
MARKER = b"## Communications themed/universal furnishings v9 - September 13, 2026\r\n"
BLOCK = (
    "## Communications themed/universal furnishings v9 - September 13, 2026\r\n\r\n"
    "Radio Lab, Listening Post and Holographic Core now pair a large matte process-specific work surface with one medium neutral support furnishing. The signal-routing console, hydrophone-analysis table and projection-alignment deck replace older centerpieces; a patch-cable organizer, rugged power conditioner and instrument-calibration case extend the reusable family.\r\n\r\n"
    "All 12 native orientations and three refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-024217-headless`; the focused asset audit reports zero errors. Owner aesthetic acceptance and export remain pending. See `docs/ROOM_FURNISHINGS_V9_2026-09-13.md`.\r\n\r\n"
).encode("ascii")


def main() -> None:
    original = STATUS.read_bytes()
    if MARKER in original:
        refreshed = original.replace(b"output/test-runs/20260913-023559-headless", b"output/test-runs/20260913-024217-headless")
        STATUS.write_bytes(refreshed)
        print("Refreshed room furnishings v9 status evidence")
        return
    STATUS.write_bytes(BLOCK + original)
    print("Recorded room furnishings v9 status")


if __name__ == "__main__":
    main()
