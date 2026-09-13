"""Prepend the Xeno owner repair milestone without decoding legacy status bytes."""
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "docs/CURRENT_STATUS.md"
old_entry = b"""## Xeno Containment Wall strict overhead repair - September 12, 2026\r\n\r\nXeno Lab now uses one shallow overhead containment bank through exact quarter turns for north/east/south/west. The sealed specimen lid, scanner, hatch and glove ports remain readable; rear rail stays wall-side and every work edge faces inward. The prior north elevation, unrelated side conversions and unrelated south bank remain archived but are no longer live. Native q0-q3 reviewed; layout, side, card and Xeno registration checks pass. See docs/XENO_OWNER_OVERHEAD_REPAIR_2026-09-12.md. Source workspace only; no export.\r\n\r\n"""
entry = b"""## Xeno Containment Wall strict overhead repair - September 12, 2026\r\n\r\nXeno Lab now uses one shallow overhead containment bank through exact quarter turns for north/east/south/west. The sealed specimen lid, scanner, hatch and glove ports remain readable; rear rail stays wall-side and every work edge faces inward. The prior north elevation, unrelated side conversions and unrelated south bank remain archived but are no longer live. Native q0-q3 reviewed; 176 layouts, 20 side variants and 47 cards pass. The separate native base-view Xeno test still reports q1/q2 workbench status-strip failures; its source-aperture audit passes and this wall repair does not claim that operating-effect issue. See docs/XENO_OWNER_OVERHEAD_REPAIR_2026-09-12.md. Source workspace only; no export.\r\n\r\n"""
data = path.read_bytes()
data = data.replace(old_entry, b"", 1)
if not data.startswith(entry):
    path.write_bytes(entry + data)
