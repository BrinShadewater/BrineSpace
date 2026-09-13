"""Prepend the v4 furnishing milestone without decoding legacy status bytes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs/CURRENT_STATUS.md"
MARKER = b"## Power-room themed and universal furnishings v4 - September 13, 2026\r\n"
BLOCK = (
    "## Power-room themed and universal furnishings v4 - September 13, 2026\r\n\r\n"
    "Current Turbine, Biomass Digester and Heat Recovery no longer repeat the same generic service bench. Each now has a large matte themed work anchor paired with one medium neutral support furnishing: a flow-governor console and instrument cabinet, feedstock-prep island and maintenance trestle, or exchanger manifold and cable caddy.\r\n\r\n"
    "All 12 native orientations and three refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-010049-headless`; the focused asset and dependency audits report zero errors. Owner aesthetic acceptance and export remain pending. See `docs/ROOM_FURNISHINGS_V4_2026-09-13.md`.\r\n\r\n"
).encode("ascii")


def main() -> None:
    original = STATUS.read_bytes()
    if MARKER in original:
        print("Room furnishings v4 status already recorded")
        return
    STATUS.write_bytes(BLOCK + original)
    print("Recorded room furnishings v4 status")


if __name__ == "__main__":
    main()
