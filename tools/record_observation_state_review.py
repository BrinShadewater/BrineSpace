"""Record verified Observation furnishing states and refresh its selected card."""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/rooms/observation-room/pack'
folder=ROOT/'output/observation-owner-repair-2026-09-12/furnishing-states'
a=Image.open(folder/'direct.png').convert('RGB');b=Image.open(folder/'retained.png').convert('RGB')
assert ImageChops.difference(a,b).getbbox() is None
assert ImageChops.difference(a.crop((0,300,1200,600)),a.crop((0,600,1200,900))).getbbox() is None
assert ImageChops.difference(a.crop((0,0,1200,300)),a.crop((0,300,1200,600))).getbbox() is not None
card=ROOT/'assets/observation-directional-v1/cards/observation_room.png'
shutil.copyfile(ROOT/'output/observation-owner-repair-2026-09-12/rotated-layout-native/observation_room-q0.png',card)
(PACK/'state-review.json').write_text(json.dumps({'status':'native-furnishing-states-reviewed','direct_retained_equal':True,'powered_clock_samples_equal':True,'off_on_different':True,'native':str(folder.relative_to(ROOT)),'card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'remaining':['actual station and static-cache power transition review'],'owner_acceptance':None},indent=2)+'\n')
note='\n\nObservation reading-light lesson (September 12): a powered reading lamp should remain steady, not pulse with the machine clock. Keep its illumination inside the desktop and transform it with the furniture. Verify an off/on difference, identical powered samples at two clocks, and direct/retained parity; separately test cache invalidation when power changes on an existing retained room.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Observation reading-light lesson (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
