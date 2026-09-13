"""Prepend the Maintenance asset milestone without decoding legacy status bytes."""
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "docs/CURRENT_STATUS.md"
entry = b"""## Maintenance Repair Wall overhead repair - September 12, 2026\r\n\r\nMaintenance Bay now uses the accepted south overhead tool bench through exact turns in all four directions. Tool grips, vise and drawer handles face inward; tall side/elevated north sources are no longer live. Saturated orange is muted and border-connected neutral background is transparent while steel tools and the yellow cloth remain distinct. Native q0-q3 reviewed. See docs/MAINTENANCE_OWNER_OVERHEAD_REPAIR_2026-09-12.md. Source workspace only; no export.\r\n\r\n"""
data = path.read_bytes()
if not data.startswith(entry):
    path.write_bytes(entry + data)
