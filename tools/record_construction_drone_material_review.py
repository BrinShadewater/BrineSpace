"""Prepend the Construction drone material milestone without decoding status bytes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
ENTRY = b"""## Construction drone material review complete - September 12, 2026\r\n\r\nThe live Construction ROV now receives a matte ochre/graphite transform inside its own shared-atlas rectangle. The atlas bytes, silhouette and articulated UVs remain exact; Mining and Salvage regions are untouched. Docked, travelling and working states were natively reviewed, and the q0 card is refreshed. Drone fleet/jobs/lifecycle, Production Ten connections/walker paths, 176 layouts, 20 side variants and 47 card identities pass. Final integration also moved Med Center q3 stations against its closed wall, restoring both side-door routes. See [Construction repair](CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md) and [asset closeout](OWNER_ASSET_STRICT_OVERHEAD_CLOSEOUT_2026-09-12.md). No gameplay timing, animation geometry, export or owner acceptance.\r\n\r\n"""


def main() -> None:
    data = STATUS.read_bytes()
    if ENTRY in data:
        print("PASS status already contains Construction drone material entry")
        return
    if not data.startswith(b"## "):
        raise SystemExit("Unexpected CURRENT_STATUS.md prefix; refusing to prepend")
    STATUS.write_bytes(ENTRY + data)
    print("PASS prepended Construction drone material status")


if __name__ == "__main__":
    main()
