"""Prepend the Battery Array art milestone without decoding concurrent status bytes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
ENTRY = b"""## September 12 Battery Array orange correction (source only)\r\n\r\nAll eight selected split-wall registrations now use a coherent muted family across north, east, south and west. Large orange shells became dark rust-brown while compact amber/yellow indicators remain readable; geometry, inventory and placements are unchanged. The q0 card matches the live room. Native q0-q3 review, 176 preferred orientations, 20 side variants and all 47 card identities pass. The north source still needs a later camera conversion under the top-down owner contract. See [Battery handoff](BATTERY_ORANGE_HANDOFF_2026-09-12.md). No gameplay, character animation or export work.\r\n\r\n"""


def main() -> None:
    data = STATUS.read_bytes()
    if ENTRY in data:
        print("PASS status already contains Battery entry")
        return
    if not data.startswith(b"## "):
        raise SystemExit("Unexpected CURRENT_STATUS.md prefix; refusing to prepend")
    STATUS.write_bytes(ENTRY + data)
    print("PASS prepended Battery status while preserving existing bytes")


if __name__ == "__main__":
    main()
