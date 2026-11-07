"""Record static native integration, leaving state acceptance open."""
from pathlib import Path
import json,shutil,hashlib
ROOT=Path(__file__).resolve().parents[1]
pack=ROOT/'assets/rooms/tidal-condenser/pack'
card=ROOT/'assets/room-declutter-v1/cards/tidal_condenser.png'
shutil.copyfile(ROOT/'output/tidal-owner-repair-2026-09-12/equipment-native/tidal_condenser-q0.png',card)
(pack/'equipment-review.json').write_text(json.dumps({'status':'integrated-static-native-reviewed','native':'output/tidal-owner-repair-2026-09-12/equipment-native','tests':'output/test-runs/20260912-202340-headless','card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'remaining':['operating and actual paused-state review','retained-render consumer check'],'owner_acceptance':None},indent=2)+'\n')
note='\n\nTidal independent equipment lesson (September 12): an elevation reference can preserve the wrong camera even with an explicit overhead prompt. The rejected study retained a tall filter face. A plan-geometry brief produced a circular lid and flat controls with cartridge releases toward the operator. Preserve rejected sources, inspect pull-tab apertures during keying, and transform source-local effect anchors with the exact artwork turn. Static native fit does not prove operating or paused-state behavior.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Tidal independent equipment lesson (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
p=ROOT/'docs/CURRENT_STATUS.md'
prefix=b'## Tidal independent overhead equipment - September 12, 2026\n\nPump and monitor now use inward overhead variants. Static native q0-q3 reviewed; 176 layouts, 20 side variants and 47 card checks pass. Card refreshed. Operating/pause and retained effect review remain open. See docs/TIDAL_OWNER_ASSET_REPAIR_2026-09-12.md. No export.\n\n'
if not p.read_bytes().startswith(prefix):p.write_bytes(prefix+p.read_bytes())
