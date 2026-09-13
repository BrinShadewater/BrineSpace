"""Prepend the current native room-art coverage milestone byte-for-byte safely."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
HEADING = b"## Current room-art coverage reconciled - September 12, 2026\r\n"
ENTRY = (
    HEADING
    + b"\r\n"
    + b"A fresh current-source native catalog covers all 47 room identities and 167 applicable renders across rotatable and fixed rooms. Four quarter contact sheets were visually reviewed against the entirely top-down, inward-facing contract. The coverage ledger has 47 unique rows, every declared direction, and 47 evidence-linked current-contract review gates. Historical per-direction pending labels remain as provenance. See [coverage audit](ROOM_ART_CURRENT_COVERAGE_AUDIT_2026-09-12.md) and [asset closeout](OWNER_ASSET_STRICT_OVERHEAD_CLOSEOUT_2026-09-12.md). Owner acceptance, packaging, gameplay, character animation/art, and the incomplete Mining sentence remain outside this milestone.\r\n\r\n"
)


def main() -> None:
    data = STATUS.read_bytes()
    if HEADING in data:
        print("Current room-art coverage milestone already recorded")
        return
    STATUS.write_bytes(ENTRY + data)
    print("Recorded current room-art coverage milestone")


if __name__ == "__main__":
    main()
