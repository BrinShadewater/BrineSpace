"""Byte-preserving CURRENT_STATUS amendment for the refinery owner repair."""
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "docs/CURRENT_STATUS.md"
marker = b"## Ore Refinery owner repair complete - September 12, 2026"
if marker in path.read_bytes():
    print("Refinery status already present")
    raise SystemExit(0)

entry = b"""## Ore Refinery owner repair complete - September 12, 2026\r\n\r\nAll selected wall directions and the independent machinery atlas now share a\r\nrestrained burnt-orange engineering palette. Edge-connected neutral backgrounds\r\nare transparent, removing the reported white seams while preserving enclosed pale\r\ntrim, gauges, yellow logistics marks, copper billets and ore. Real-display q0-q3\r\ncaptures were inspected. 176 furnished layouts, 20 side variants, 47 card\r\nidentities and both production-ten route suites pass. The refreshed q0 card is\r\nselected by all three consumers. Evidence: REFINERY_OWNER_REPAIR_2026-09-12.md.\r\n\r\n"""
# Keep the file's existing bytes because older content contains invalid UTF-8.
path.write_bytes(entry + path.read_bytes())
print("Prepended refinery owner-repair status")
