"""Record integrated overhead bench evidence and preserve current card parity."""
import json,shutil,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
capture=ROOT/'output/construction-owner-repair-2026-09-12/bench-native/construction_drone_bay-q0.png'
card=ROOT/'assets/construction-directional-v1/cards/construction_drone_bay.png'
shutil.copyfile(capture,card)
review={'status':'overhead bench integrated; native q0/q1/q3 reviewed','native':'output/construction-owner-repair-2026-09-12/bench-native','q2':'bench omitted by existing layout','card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'remaining':['cradle and hatch camera review','drone design decision'],'owner_acceptance':None}
(ROOT/'assets/construction-material-v2/bench-review.json').write_text(json.dumps(review,indent=2)+'\n')
note='\n\nConstruction overhead bench lesson (September 12): show parked arm joint caps from above and place service controls on a named operator edge. Native views must verify that edge after placement-dependent rotation. Preserve genuine generated alpha even when the preview background looks black; do not apply a black color key to charcoal machinery. Aspect-preserving quarter-turn variants may occupy less of the old maximum rectangle, so inspect readability at the resulting native size.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Construction overhead bench lesson (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
p=ROOT/'docs/CURRENT_STATUS.md'
prefix=b'## Construction overhead assembly bench - September 12, 2026\n\nThe assembly bench now uses an overhead parked-arm companion with controls facing room center. Native q0/q1/q3 reviewed; q2 omits the bench. Cradle/hatch camera review and drone design decision remain open. See docs/CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md. No export.\n\n'
if not p.read_bytes().startswith(prefix):p.write_bytes(prefix+p.read_bytes())
