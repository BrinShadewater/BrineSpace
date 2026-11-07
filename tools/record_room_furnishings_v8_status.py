"""Prepend the v8 furnishing milestone without decoding legacy status bytes."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
MARKER = b"## Service and logistics themed/universal furnishings v8 - September 13, 2026\r\n"
BLOCK = (
    "## Service and logistics themed/universal furnishings v8 - September 13, 2026\r\n\r\n"
    "Maintenance Bay, Storage Bay and Data Archive now pair a large matte process-specific workstation with one medium neutral support furnishing. The component-rebuild cradle, cargo-sorting island and media-restoration table replace scattered legacy floor clusters; a fastener chest, folded handling dolly and sealed transit case extend the reusable family.\r\n\r\n"
    "All 12 native orientations and three refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-021608-headless`; the focused asset audit reports zero errors. Owner aesthetic acceptance and export remain pending. See `docs/ROOM_FURNISHINGS_V8_2026-09-13.md`.\r\n\r\n"
).encode("ascii")

def main() -> None:
    original = STATUS.read_bytes()
    if MARKER in original:
        refreshed = original.replace(b"output/test-runs/20260913-021008-headless", b"output/test-runs/20260913-021608-headless")
        STATUS.write_bytes(refreshed); print("Refreshed room furnishings v8 status evidence"); return
    STATUS.write_bytes(BLOCK + original); print("Recorded room furnishings v8 status")

if __name__ == "__main__": main()
