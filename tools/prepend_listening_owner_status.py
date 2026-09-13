"""Prepend the Listening Post repair milestone without decoding legacy status bytes."""
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "docs/CURRENT_STATUS.md"
entry = b"""## Listening Post Deepwater standardization - September 12, 2026\r\n\r\nThe live Listening Post now uses inward-facing navy/teal/brass Deepwater wall banks in all four orientations. North is an exact 180-degree counterpart of the accepted south bank; the old q0 U installation and bright north pack remain archived but are no longer selected. Listening-only floor equipment replaces saturated red trim with muted brass while preserving geometry, activity anchors, operating effects and the Radio Lab source. Native q0-q3 reviewed; 176 layouts, 20 side variants, 47 cards and native operating-effect checks pass. See docs/LISTENING_OWNER_REPAIR_2026-09-12.md. Source workspace only; no export.\r\n\r\n"""
data = path.read_bytes()
if not data.startswith(entry):
    path.write_bytes(entry + data)
