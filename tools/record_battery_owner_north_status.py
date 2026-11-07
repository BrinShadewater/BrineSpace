"""Prepend the Battery north-camera milestone without decoding concurrent bytes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
ENTRY = b"""## Battery Array north overhead repair - September 12, 2026\r\n\r\nBattery Array q0 now uses shallow overhead cell and distribution banks with four closed cells, three distribution units and three inward-facing gauges. Matte graphite and muted rust replace the former north elevation while the verified q1-q3 family, split frames, collision, placements and gameplay remain unchanged. Native q0 review, exact unchanged-quarter comparison, 176 layouts, 20 side variants, 47 card identities and direct/retained state parity pass. See [Battery owner repair](BATTERY_OWNER_NORTH_REPAIR_2026-09-12.md). Source workspace only; no owner acceptance or export.\r\n\r\n"""


def main() -> None:
    data = STATUS.read_bytes()
    if ENTRY in data:
        print("PASS status already contains Battery north entry")
        return
    if not data.startswith(b"## "):
        raise SystemExit("Unexpected CURRENT_STATUS.md prefix; refusing to prepend")
    STATUS.write_bytes(ENTRY + data)
    print("PASS prepended Battery north status while preserving existing bytes")


if __name__ == "__main__":
    main()
