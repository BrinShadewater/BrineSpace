"""Prepend the Isolation Vault milestone without decoding legacy status bytes."""
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "docs/CURRENT_STATUS.md"
entry = b"""## Isolation Vault owner asset correction - September 12, 2026\r\n\r\nIsolation Vault now uses the accepted south Emergency Isolation bank through exact turns in north/east/south/west. The obsolete north-only baked perimeter and all Battery Array furnishings inherited by the vault have been removed. The independent Battery Array test-bench source received a matte steel/orange highlight pass without geometry or alpha changes. Native vault q0-q3 and battery-room placement reviewed. See docs/ISOLATION_VAULT_OWNER_ASSET_REPAIR_2026-09-12.md. Source workspace only; no export.\r\n\r\n"""
data = path.read_bytes()
if not data.startswith(entry):
    path.write_bytes(entry + data)
