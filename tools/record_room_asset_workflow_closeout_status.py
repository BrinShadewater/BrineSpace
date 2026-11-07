"""Prepend the room-asset workflow closeout without decoding legacy status bytes."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
MARKER = b"## Room asset workflow session closeout - September 13, 2026\r\n"
BLOCK = (
    "## Room asset workflow session closeout - September 13, 2026\r\n\r\n"
    "The large/medium room-asset lessons are consolidated in the maintained room-pipeline skill, `docs/ROOM_ART_PRODUCTION.md` and `docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md`. Future batches use one process-specific anchor plus at most one smaller functional universal support, preserve quiet floor, verify both asset IDs and silhouettes in four native orientations, then publish cards and dependency hashes.\r\n\r\n"
    "The communications furnishing v9 batch closes with six audited assets across Radio Lab, Listening Post and Holographic Core, 12 reviewed native orientations and a passing focused suite at `output/test-runs/20260913-024217-headless`. Owner aesthetic acceptance and a fresh export remain pending. See `docs/ROOM_ASSET_WORKFLOW_CLOSEOUT_2026-09-13.md`.\r\n\r\n"
).encode("ascii")


def main() -> None:
    original = STATUS.read_bytes()
    if MARKER in original:
        print("Room asset workflow closeout already recorded")
        return
    STATUS.write_bytes(BLOCK + original)
    print("Recorded room asset workflow closeout status")


if __name__ == "__main__":
    main()
