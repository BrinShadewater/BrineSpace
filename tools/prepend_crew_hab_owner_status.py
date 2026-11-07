"""Prepend the Crew Hab berth milestone without decoding legacy status bytes."""
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "docs/CURRENT_STATUS.md"
old_entry = b"""## Crew Hab three-berth overhead wall - September 12, 2026\r\n\r\nCrew Hab now uses the accepted compact three-pod berth bank through exact turns in north/east/south/west. Mattress and pillow access faces inward and sleeping capacity no longer changes by direction. The rejected oversized bed/wardrobe/canopy family and its lamp overlay remain archived but are no longer live. Native q0-q3 reviewed. See docs/CREW_HAB_OWNER_OVERHEAD_REPAIR_2026-09-12.md. Source workspace only; no export.\r\n\r\n"""
entry = b"""## Crew Hab three-berth overhead wall - September 12, 2026\r\n\r\nCrew Hab now uses the accepted compact three-pod berth bank through exact turns in north/east/south/west. Mattress and pillow access faces inward and sleeping capacity no longer changes by direction. The rejected oversized bed/wardrobe/canopy family and its lamp overlay remain archived but are no longer live. Native q0-q3 reviewed; 176 layouts, 20 side variants, 47 cards and 72 crew-life cases pass. The broader crew-activity run timed out on an unrelated listening_post0bill station-choice assertion and was left to the concurrent gameplay/character work. See docs/CREW_HAB_OWNER_OVERHEAD_REPAIR_2026-09-12.md. Source workspace only; no export.\r\n\r\n"""
data = path.read_bytes()
data = data.replace(old_entry, b"", 1)
if not data.startswith(entry):
    path.write_bytes(entry + data)
