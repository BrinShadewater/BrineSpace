"""Record static Construction repairs; keep drone recommendation distinct."""
import json,hashlib,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PACK=ROOT/'assets/rooms/construction-drone-bay/material'
card=ROOT/'assets/rooms/construction-drone-bay/cards/card.png'
shutil.copyfile(ROOT/'output/construction-owner-repair-2026-09-12/cradle-native/construction_drone_bay-q0.png',card)
sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for pattern in ['*-overhead.png','bench-overhead-*.png','hatch-overhead-*.png','panel-pallet-*.png','cradle-square-*.png'] for p in PACK.glob(pattern) if 'raw' not in p.name}
(PACK/'static-review.json').write_text(json.dumps({'status':'static equipment integrated and agent-reviewed','sources':sources,'native':'output/construction-owner-repair-2026-09-12/cradle-native','dock_fixture':'output/construction-owner-repair-2026-09-12/cradle-square/empty-docked.png','card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'drone_recommendation':'Preserve recognizable silhouette; consider material repaint. Existing original sprite and animation remain selected.','owner_acceptance':None},indent=2)+'\n')
note='\n\nConstruction square cradle lesson (September 12): a broad near-square support deck maintained docked support in every quarter turn where the long slotted candidate failed. Inspect both empty and occupied at actual draw size; preserve the drone offset and merge its original envelope into static bounds so deployment does not change layout. Material/style recommendations for the drone remain distinct from stationary machinery acceptance.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Construction square cradle lesson (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
p=ROOT/'docs/CURRENT_STATUS.md';prefix=b'## Construction static equipment repair - September 12, 2026\n\nFabrication bank, assembly bench, flat panel pallet, circular hatch and square docking deck now use matte overhead art. Native room/dock/hatch state reviews recorded. Drone silhouette retained; material repaint recommended separately. See docs/CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md. Source workspace only; no export or owner acceptance.\n\n'
if not p.read_bytes().startswith(prefix):p.write_bytes(prefix+p.read_bytes())
