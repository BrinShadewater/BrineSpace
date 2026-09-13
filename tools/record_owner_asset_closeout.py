"""Prepend the owner asset closeout without decoding concurrent status bytes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
ENTRY = b"""## Remaining owner room-asset queue closed in source - September 12, 2026\r\n\r\nMedical Treatment, Mycelium Cultivation, Crew Lounge, Mining Drone Service and Research Analysis now use exact four-direction turns of their strongest south overhead banks. Blue medical upholstery, stable inventories and inward access carry across every wall. BRINE corner banks sit six world units lower in all quarters. Current Quarantine and Anomaly facing/cutout repairs were independently re-reviewed and retained. Native review, 176 layouts, 20 side variants, 47 card identities and the BRINE route fixture pass. See [asset closeout](OWNER_ASSET_STRICT_OVERHEAD_CLOSEOUT_2026-09-12.md). The incomplete Mining sentence and optional Construction-drone redesign remain owner questions; no character animation, gameplay behavior, export or owner acceptance is claimed.\r\n\r\n"""


def main() -> None:
    data = STATUS.read_bytes()
    if ENTRY in data:
        print("PASS status already contains owner asset closeout")
        return
    if not data.startswith(b"## "):
        raise SystemExit("Unexpected CURRENT_STATUS.md prefix; refusing to prepend")
    STATUS.write_bytes(ENTRY + data)
    print("PASS prepended owner asset closeout while preserving existing bytes")


if __name__ == "__main__":
    main()
