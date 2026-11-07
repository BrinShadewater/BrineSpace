"""Prepend the Solar Array art milestone without decoding concurrent status bytes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
ENTRY = b"""## September 12 Solar Array orange correction (source only)\r\n\r\nThe selected north, side and south wall-length sources now use restrained burnt-orange structural accents while preserving their machinery, geometry and shading. The q0 card matches the live room. Native q0-q3 review passes, along with 176 preferred orientations, 20 side variants and all 47 card identities. Explicit Hydroponics stand, Anomaly task-light and Shield cradle removals were also confirmed already effective; Isolation Vault's old q0 flush wings remain open. See [Solar handoff](SOLAR_FACING_HANDOFF_2026-09-12.md) and [removal audit](OWNER_ASSET_REMOVALS_2026-09-12.md). No gameplay, character animation or export work.\r\n\r\n"""


def main() -> None:
    data = STATUS.read_bytes()
    if ENTRY in data:
        print("PASS status already contains Solar entry")
        return
    if not data.startswith(b"## "):
        raise SystemExit("Unexpected CURRENT_STATUS.md prefix; refusing to prepend")
    STATUS.write_bytes(ENTRY + data)
    print("PASS prepended Solar status while preserving existing bytes")


if __name__ == "__main__":
    main()
