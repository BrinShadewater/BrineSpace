"""Close the pallet-facing evidence gap without closing unrelated room work."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'assets/rooms/construction-drone-bay/material/panel-review.json'
d=json.loads(p.read_text())
d['status']='live q2 and four component placement directions native-reviewed'
d['placement_fixture']='output/construction-owner-repair-2026-09-12/panel-facings'
d['remaining']=['other floor machinery overhead/facing','drone design decision']
p.write_text(json.dumps(d,indent=2)+'\n')
note='\n\nConstruction pallet-facing verification (September 12): when normal layouts omit a prop in three quarters, use a native component fixture invoking the production texture/bounds helpers at four placement centers. Inspect the inward release edge and measured footprint in each. Keep this evidence distinct from occupied-room/crew-clearance review. The maintained fixture is tools/capture_construction_panel_facings.gd.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Construction pallet-facing verification (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f: f.write(note)
p=ROOT/'docs/CURRENT_STATUS.md'
d=p.read_bytes().replace(b'Other floor equipment facing and alternate pallet placements remain open.',b'Four alternate pallet placements now pass native inward-facing/bounds review. Other floor equipment facing remains open.',1)
p.write_bytes(d)
print('Pallet facing evidence recorded; room remains open.')
