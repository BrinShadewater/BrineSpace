"""Prepend the Current Turbine art milestone without decoding concurrent status bytes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
ENTRY = b"""## September 12 Current Turbine owner art repair (source only)\r\n\r\nNorth q0 now uses a low overhead companion with an inward elliptical intake instead of the tall frontal source. East, south and west retain their accepted geometry with bright orange paint reduced to muted rust-brown. The arrow, rotation rules and power behavior are unchanged. Built-in generation returned RGB imitation transparency; deterministic cleanup removed the neutral exterior and 25 disconnected alpha specks before registration. Native q0-q3 review, Power Expansion, 176 preferred orientations, 20 side variants and all 47 card identities pass. See [Turbine owner repair](CURRENT_TURBINE_OWNER_REPAIR_2026-09-12.md). No character animation or export work.\r\n\r\n"""


def main() -> None:
    data = STATUS.read_bytes()
    if ENTRY in data:
        print("PASS status already contains Turbine entry")
        return
    if not data.startswith(b"## "):
        raise SystemExit("Unexpected CURRENT_STATUS.md prefix; refusing to prepend")
    STATUS.write_bytes(ENTRY + data)
    print("PASS prepended Turbine status while preserving existing bytes")


if __name__ == "__main__":
    main()
