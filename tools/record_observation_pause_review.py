"""Record the completed Observation native state checkpoint without re-encoding status."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / 'output/observation-owner-repair-2026-09-12'
result = json.loads((evidence / 'station-pause/result.json').read_text())
assert result['failures'] == 0 and len(result['samples']) == 4
assert all(s['operating'] and s['pixels_equal'] and s['paused_clock'] > s['clock_before_run'] for s in result['samples'])

def append_once(path, text):
    existing = path.read_bytes()
    encoded = text.encode('utf-8')
    if encoded not in existing:
        path.write_bytes(existing + encoded)

append_once(ROOT / 'docs/OBSERVATION_OWNER_ASSET_REPAIR_2026-09-12.md', '''

Final native state checkpoint: existing retained canvases were reused through
off/on transitions. All six transition rows match the corresponding direct
reference, and initial direct/retained pixels match. Actual station fixture
`verify_observation_station_pause.gd` resolves the view through `rare_room_views`;
four rotations pass with powered state, advancing running clock, frozen paused
clock and identical paused native pixels. Evidence: `station-pause/result.json`
and paired captures under `output/observation-owner-repair-2026-09-12`.
Native q0 station image reviewed for architecture, overhead furnishings and entry.
The run includes existing environment image-load/export warnings; no export was
tested. Earlier 176-layout, 20-side and 47-card checks remain scoped evidence.
Owner acceptance remains separate. Next room in the asset queue: Salvage Workshop.
''')

lesson = '''

Observation retained-state verification (September 12): a steady powered reading
light still requires cache invalidation. Reuse existing production canvases across
off/on changes and compare every orientation against direct references; fresh
canvases alone cannot prove this. Resolve live room views from the current renderer
registry before adapting another room's station fixture. Verify actual running and
paused station state independently of fixed-clock artwork previews.
'''
for path in [ROOT / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
             ROOT / 'skills/brinespace-room-pipeline/references/material-and-scale-review.md',
             Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    append_once(path, lesson)

status = ROOT / 'docs/CURRENT_STATUS.md'
prefix = b'## Observation owner asset repair verified - September 12, 2026\r\n\r\nOverhead furnishings now rotate with the room; portholes remain background architecture. Layout, native visual, retained power-transition and actual station pause checks recorded in docs/OBSERVATION_OWNER_ASSET_REPAIR_2026-09-12.md. Next asset queue item: Salvage Workshop. No export or owner acceptance.\r\n\r\n'
content = status.read_bytes()
if prefix not in content:
    status.write_bytes(prefix + content)
print('Recorded Observation checkpoint and cache-verification lesson in bible and both skill copies.')
