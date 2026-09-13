"""Prepend the Biomass Digester milestone without decoding legacy status bytes."""
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "docs/CURRENT_STATUS.md"
entry = b"""## Biomass Digester material correction - September 12, 2026\r\n\r\nBiomass Digester retains the strong four-direction Biomass Processing wall geometry with orange hardware moved into a muted feedstock-moss family. The shared service console now uses a Biomass-only legibility tint. The supplemental service-bench source has true alpha and lifted matte midtones, eliminating its white exterior field. Native q0-q3 reviewed. See docs/BIOMASS_DIGESTER_OWNER_MATERIAL_REPAIR_2026-09-12.md. Source workspace only; no export.\r\n\r\n"""
data = path.read_bytes()
if not data.startswith(entry):
    path.write_bytes(entry + data)
