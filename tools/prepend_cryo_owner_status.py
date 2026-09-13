"""Byte-preserving CURRENT_STATUS amendment for the Cryo owner repair."""
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "docs/CURRENT_STATUS.md"
marker = b"## Cryo Chamber strict overhead walls - September 12, 2026"
if marker in path.read_bytes():
    print("Cryo owner status already present")
    raise SystemExit(0)
entry = b"""## Cryo Chamber strict overhead walls - September 12, 2026\r\n\r\nAll four selected Cryo support banks now derive from one strict orthographic\r\noverhead source. The compressor, two vessel lids, coil, pipes, coolant cylinder,\r\nterminal, three samples and gas bottle remain, without tall cabinet or cylinder\r\nfronts rotating around the room. Real-display q0-q3 captures were inspected; 176\r\nfurnished layouts, 20 side variants, 47 card identities and both Cryo recovery\r\nsuites pass. q0 card bindings were refreshed. Concurrent q2 pod selection changed\r\nafter the baseline; this asset pass did not edit pod logic or placement. Evidence:\r\nCRYO_OWNER_OVERHEAD_REPAIR_2026-09-12.md.\r\n\r\n"""
path.write_bytes(entry + path.read_bytes())
print("Prepended Cryo owner-repair status")
