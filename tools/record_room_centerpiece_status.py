"""Prepend the room-centerpiece milestone without decoding legacy status bytes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
MARKER = b"## Room centerpiece asset pass - September 12, 2026\r\n"
BLOCK = (
    "## Room centerpiece asset pass - September 12, 2026\r\n\r\n"
    "Twelve new themed furnishings are selected across ten previously sparse rooms: seven large and five medium assets, including ten square or rectangular silhouettes. All selected rasters are true-alpha 1254-square sources with external silhouette registrations. Ten refreshed room cards and 40 native orientation captures were visually reviewed; the batch audit reports zero errors.\r\n\r\n"
    "Preferred-layout routing passes all 176 furnished orientations after explicit Battery q2 and Storage q2 center corrections. The selected assets, hashes, prompts, rejection record and bounded evidence are in `assets/room-centerpieces-v1/manifest.json` and `docs/ROOM_CENTERPIECE_ASSET_PASS_2026-09-12.md`. Owner aesthetic acceptance and a new export remain pending.\r\n\r\n"
).encode("ascii")


def main() -> None:
    original = STATUS.read_bytes()
    if MARKER in original:
        print("Room centerpiece status already recorded")
        return
    STATUS.write_bytes(BLOCK + original)
    print("Prepended room centerpiece status")


if __name__ == "__main__":
    main()
