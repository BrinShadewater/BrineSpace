"""Record verified Galley source milestone and scale-review workflow."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
result=json.loads((root/'output/galley-owner-repair-2026-09-12/station-pause/result.json').read_text())
assert result['failures']==0 and len(result['samples'])==4
lesson='''

Galley communal-table review (September 12): judge long seating furniture against
the production crew sprite and its actual pivot/standing-height metadata, using
the same room draw_actor scale. A source image or empty-room fit cannot establish
seat scale. Keep table/bench gaps transparent and reserve circulation separately
from the combined furniture collision rectangle. Review all orientations and
distinguish standing scale comparison from seated interaction acceptance.
'''
for p in [root/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',root/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    data=p.read_bytes()
    if lesson.encode() not in data:p.write_bytes(data+lesson.encode())
p=root/'docs/CURRENT_STATUS.md';data=p.read_bytes()
prefix=b'## Galley owner asset repair verified - September 12, 2026\r\n\r\nOverhead kitchen/serving and two communal tables rotate through four layouts. Native crew-scale, cooktop direct/retained and actual pause checks recorded; card refreshed. 176 layouts, 20 side variants and 47 cards pass. See docs/GALLEY_OWNER_ASSET_REPAIR_2026-09-12.md. Next: Cold Store blue equipment, scale and central coolers. No export or owner acceptance.\r\n\r\n'
if prefix not in data:p.write_bytes(prefix+data)
print('Galley milestone and scale-review lesson recorded.')
