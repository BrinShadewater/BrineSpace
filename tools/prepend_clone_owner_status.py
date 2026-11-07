"""Prepend the Clone Lab wall milestone without decoding legacy status bytes."""
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "docs/CURRENT_STATUS.md"
entry = b"""## Clone Growth Wall overhead family - September 12, 2026\r\n\r\nClone Lab now uses the owner-approved east Clone Growth bank through exact turns in north/east/south/west. The outer service rail stays wall-side while the tissue window, microscope, keyboard and consumables face inward. The former frontal north composition and unrelated shallow south appliance strip remain archived but are no longer live. Native q0-q3 reviewed. See docs/CLONE_LAB_OWNER_OVERHEAD_REPAIR_2026-09-12.md. Source workspace only; no export.\r\n\r\n"""
data = path.read_bytes()
if not data.startswith(entry):
    path.write_bytes(entry + data)
