"""Record reviewed Tidal riser palette and matching card."""
import json,shutil,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/tidal-owner-v2'
card=ROOT/'assets/room-declutter-v1/cards/tidal_condenser.png'
shutil.copyfile(ROOT/'output/tidal-owner-repair-2026-09-12/riser-native/tidal_condenser-q0.png',card)
(PACK/'riser-review.json').write_text(json.dumps({'status':'Tidal-specific riser integrated and native-reviewed','source_sha256':hashlib.sha256((PACK/'riser.png').read_bytes()).hexdigest(),'native':'output/tidal-owner-repair-2026-09-12/riser-native','card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'card_check':'output/test-runs/20260912-201533-headless','remaining':['independent pump and monitor overhead/effects'],'owner_acceptance':None},indent=2)+'\n')
note='\n\nTidal rear-wall palette lesson (September 12): room machinery and architectural risers have separate source selection. A room-specific catalog override can match grey-blue panels and brass pipes while retaining shared face/cap rectangles and other engineering rooms. Verify both the cap seam and doorway joins in native orientations, and update the selected room card after the architectural change.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Tidal rear-wall palette lesson (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
p=ROOT/'docs/CURRENT_STATUS.md';prefix=b'## Tidal matching rear wall - September 12, 2026\n\nTidal now selects grey-blue rear-wall panels and dull-brass pipes through a room-specific riser entry. Native joins/palette reviewed; original geometry retained. Independent pump/monitor overhead and effects remain open. See docs/TIDAL_OWNER_ASSET_REPAIR_2026-09-12.md. No export.\n\n'
if not p.read_bytes().startswith(prefix):p.write_bytes(prefix+p.read_bytes())
