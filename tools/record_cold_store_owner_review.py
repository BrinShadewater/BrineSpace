"""Byte-preserving CURRENT_STATUS milestone for the verified Cold Store asset pass."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
status = root / "docs/CURRENT_STATUS.md"
prefix = (
    "## Cold Store owner asset repair verified - September 12, 2026\r\n\r\n"
    "Matte blue overhead banks and two central coolers rotate through four layouts. "
    "Native crew scale, route, powered frost, retained cache and actual station pause "
    "checks pass; selected card is refreshed. See docs/COLD_STORE_OWNER_ASSET_REPAIR_2026-09-12.md. "
    "No gameplay/character animation change, export or owner acceptance.\r\n\r\n"
).encode("utf-8")
data = status.read_bytes()
if prefix not in data:
    status.write_bytes(prefix + data)
print("Recorded Cold Store owner asset milestone.")
