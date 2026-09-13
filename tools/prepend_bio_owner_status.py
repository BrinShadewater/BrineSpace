"""Prepend the Bio Lab wall milestone without decoding legacy status bytes."""
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "docs/CURRENT_STATUS.md"
entry = b"""## Bio Culture Wall overhead family - September 12, 2026\r\n\r\nBio Lab now uses the accepted south overhead microscope bench through exact turns in north/east/south/west. Jar lids, dishes and worktops read from above; microscope eyepieces and work access face inward. Tall trough/front-elevation companions remain archived but are no longer live. Native q0-q3 reviewed. See docs/BIO_LAB_OWNER_OVERHEAD_REPAIR_2026-09-12.md. Source workspace only; no export.\r\n\r\n"""
data = path.read_bytes()
if not data.startswith(entry):
    path.write_bytes(entry + data)
