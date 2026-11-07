"""Prepend the Shield art milestone without decoding concurrent status bytes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
ENTRY = b"""## September 12 Shield Generator orange correction (source only)\r\n\r\nThe weak hull cradle remains absent and all four selected Shield wall directions now use restrained rust-brown construction beneath graphite/steel machinery. Compact amber indicators remain legible; geometry, placements and gameplay state are unchanged. The q0 card matches the live room. Native q0-q3 review, 176 preferred orientations, 20 side variants and all 47 card identities pass. See [Shield handoff](SHIELD_ORANGE_HANDOFF_2026-09-12.md). No gameplay, character animation or export work.\r\n\r\n"""


def main() -> None:
    data = STATUS.read_bytes()
    if ENTRY in data:
        print("PASS status already contains Shield entry")
        return
    if not data.startswith(b"## "):
        raise SystemExit("Unexpected CURRENT_STATUS.md prefix; refusing to prepend")
    STATUS.write_bytes(ENTRY + data)
    print("PASS prepended Shield status while preserving existing bytes")


if __name__ == "__main__":
    main()
