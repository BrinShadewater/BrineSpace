"""Prepend the v6 furnishing milestone without decoding legacy status bytes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
MARKER = b"## Utility and science themed/universal furnishings v6 - September 13, 2026\r\n"
BLOCK = (
    "## Utility and science themed/universal furnishings v6 - September 13, 2026\r\n\r\n"
    "Tidal Condenser, Gravity Loom and Xeno Lab now pair a large matte process-specific workstation with one medium neutral support furnishing. The condensate-analysis island, field-tensor console and sealed assay table replace smaller generic work pieces; a valve-spares locker, diagnostic rack and narrow decontamination caddy extend the reusable family.\r\n\r\n"
    "All 12 native orientations and three refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-013058-headless`; the focused asset audit reports zero errors. Owner aesthetic acceptance and export remain pending. See `docs/ROOM_FURNISHINGS_V6_2026-09-13.md`.\r\n\r\n"
).encode("ascii")


def main() -> None:
    original = STATUS.read_bytes()
    if MARKER in original:
        print("Room furnishings v6 status already recorded")
        return
    STATUS.write_bytes(BLOCK + original)
    print("Recorded room furnishings v6 status")


if __name__ == "__main__":
    main()
