"""Record source-region and native evidence for Construction static furnishings."""
import hashlib
import json
import shutil
from pathlib import Path
import numpy as np
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT/'assets/construction-material-v2'
source = PACK/'floor-equipment-candidate.png'
pixels = np.asarray(Image.open(source).convert('RGB')).astype(float)/255
visible = np.minimum(pixels[:,:,0],pixels[:,:,2])-pixels[:,:,1] <= .18
regions = {'cradle':(85,565,370,320),'bench':(535,535,450,350),'hatch':(1070,565,390,340)}
bounds = {k:Image.fromarray(visible[y:y+h,x:x+w]).getbbox() for k,(x,y,w,h) in regions.items()}
assert not visible[720,190] and not visible[720,350]
assert visible[730,1250]
for k,box in bounds.items():
    w,h=regions[k][2:]
    assert box[0]>0 and box[1]>0 and box[2]<w and box[3]<h
capture = ROOT/'output/construction-owner-repair-2026-09-12/floor-native/construction_drone_bay-q0.png'
card = ROOT/'assets/construction-directional-v1/cards/construction_drone_bay.png'
shutil.copyfile(capture,card)
review = {'status':'cradle, bench and hatch integrated and native-reviewed',
          'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
          'source_regions':regions,'visible_bounds_within_regions':bounds,
          'alpha_probes':{'cradle_gaps':True,'hatch_lid_retained':True},
          'native':'output/construction-owner-repair-2026-09-12/floor-native',
          'native_quarters':[0,1,2,3], 'regressions':'output/test-runs/20260912-194110-headless',
          'card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),
          'remaining':['panel rack material and overhead review','drone visual decision','floor equipment inward-facing review'],
          'owner_acceptance':None}
(PACK/'floor-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
note='\n\nConstruction static-atlas lesson (September 12): use an explicit optional texture for static cradle/bench/hatch draws when a repaint belongs to one bay. Keep the default atlas and drone draw path intact. Check candidate pixels against existing source rectangles and probe both through-gaps and solid lids; matching canvas dimensions alone is insufficient. The Construction repaint passes four native material views, but material review does not establish inward-facing floor-equipment compliance.\n'
for path in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Construction static-atlas lesson (September 12)' not in path.read_text(encoding='utf-8'):
        with path.open('a',encoding='utf-8') as out: out.write(note)
status=ROOT/'docs/CURRENT_STATUS.md'
prefix=b'## Construction static equipment material pass - September 12, 2026\n\nCradle, bench and launch hatch now select a Construction-only matte atlas. Source-region and transparency probes plus q0-q3 native review pass. Original drone source retained. Panel rack and floor-equipment facing review remain open. See docs/CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md. No export.\n\n'
if not status.read_bytes().startswith(prefix): status.write_bytes(prefix+status.read_bytes())
print('Static source-region, alpha, card and documentation checks recorded.')
