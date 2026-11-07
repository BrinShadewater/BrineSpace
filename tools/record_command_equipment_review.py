"""Record integrated Command props without claiming remaining room checks."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/command-owner-v2'
states=ROOT/'output/command-owner-repair-2026-09-12/equipment-states'
assert ImageChops.difference(Image.open(states/'states.png').convert('RGB'),Image.open(states/'retained.png').convert('RGB')).getbbox() is None
card=ROOT/'assets/command-directional-v1/cards/command_center.png'
shutil.copyfile(ROOT/'output/command-owner-repair-2026-09-12/systems-native/command_center-q0.png',card)
(PACK/'equipment-review.json').write_text(json.dumps({'status':'native-static-operating-retained-reviewed','native':'output/command-owner-repair-2026-09-12/systems-native','state_samples':36,'retained_rgb_equal':True,'tests':'output/test-runs/20260912-204558-headless','card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'remaining':['actual station pause','wall-bank source camera review'],'owner_acceptance':None},indent=2)+'\n')
note='\n\nCommand consumer inventory lesson (September 12): read the split-wall replaces/preserve list before identifying a small console from its silhouette. Command preserves systems and table while replacing operations and comms. A new comms sprite cannot stand in for the single-screen systems terminal. Inventory-correct sources, oriented visual bounds and common art/effect transforms are verified separately through native room fit and direct/retained state captures.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Command consumer inventory lesson (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
