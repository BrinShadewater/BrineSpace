"""Prepend the v7 furnishing milestone without decoding legacy status bytes."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
MARKER = b"## Clinical and biology themed/universal furnishings v7 - September 13, 2026\r\n"
BLOCK = (
    "## Clinical and biology themed/universal furnishings v7 - September 13, 2026\r\n\r\n"
    "Life Support, Med Bay and Bio Lab now pair a large matte process-specific workstation with one medium neutral support furnishing. The atmosphere-analysis island, sterile triage island and culture-preparation island replace weaker repeated work pieces; a sealed filter chest, enclosed equipment cart and specimen transit case extend the reusable family.\r\n\r\n"
    "All 12 native orientations and three refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-014953-headless`; the focused asset audit reports zero errors. Owner aesthetic acceptance and export remain pending. See `docs/ROOM_FURNISHINGS_V7_2026-09-13.md`.\r\n\r\n"
).encode("ascii")

def main() -> None:
    original = STATUS.read_bytes()
    if MARKER in original:
        print("Room furnishings v7 status already recorded")
        return
    STATUS.write_bytes(BLOCK + original)
    print("Recorded room furnishings v7 status")

if __name__ == "__main__":
    main()
