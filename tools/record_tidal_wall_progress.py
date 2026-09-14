"""Record verified Tidal wall family without closing the room palette work."""
from pathlib import Path
import json,shutil,hashlib
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/rooms/tidal-condenser/pack'
card=ROOT/'assets/room-declutter-v1/cards/tidal_condenser.png'
shutil.copyfile(ROOT/'output/tidal-owner-repair-2026-09-12/wall-native/tidal_condenser-q0.png',card)
(PACK/'wall-review.json').write_text(json.dumps({'status':'wall family integrated and native-reviewed','native':'output/tidal-owner-repair-2026-09-12/wall-native','quarters':[0,1,2,3],'regressions':'output/test-runs/20260912-201204-headless','card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'remaining':['Tidal-specific riser palette','independent pump and monitor camera/effects'],'owner_acceptance':None},indent=2)+'\n')
note='\n\nTidal overhead family integration (September 12): retain three coil returns, two vessel lids, three cartridges and console through exact turns. Align cartridge long axes with the operator approach so blue releases sit on the inward edge and fixed pipes remain outward. A uniform magenta exterior enabled clean alpha after the prior baked checkerboard failed. Native q0–q3 confirms inventory, inward controls and mounting; the separate orange riser and independent machinery remain separate work.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Tidal overhead family integration (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
p=ROOT/'docs/CURRENT_STATUS.md';prefix=b'## Tidal Condenser overhead wall family - September 12, 2026\n\nAll four walls now share three coil returns, two vessels, three cartridges and console with inward controls. Native q0-q3 reviewed; layout, side and card checks pass. Tidal-specific riser palette and independent pump/monitor remain open. See docs/TIDAL_OWNER_ASSET_REPAIR_2026-09-12.md. No export.\n\n'
if not p.read_bytes().startswith(prefix):p.write_bytes(prefix+p.read_bytes())
