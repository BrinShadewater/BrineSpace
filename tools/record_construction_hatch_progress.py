"""Record reviewed hatch rendering and matching card."""
from pathlib import Path
import json,shutil,hashlib
ROOT=Path(__file__).resolve().parents[1]
capture=ROOT/'output/construction-owner-repair-2026-09-12/hatch-native/construction_drone_bay-q0.png'
card=ROOT/'assets/rooms/construction-drone-bay/cards/card.png'
shutil.copyfile(capture,card)
d={'status':'overhead hatch integrated and native-reviewed','states':'output/construction-owner-repair-2026-09-12/hatch-states/states.png','room':'output/construction-owner-repair-2026-09-12/hatch-native','regressions':'output/test-runs/20260912-195709-headless','card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'remaining':['cradle camera review','drone design decision'],'owner_acceptance':None}
(ROOT/'assets/rooms/construction-drone-bay/material/hatch-review.json').write_text(json.dumps(d,indent=2)+'\n')
note='\n\nConstruction circular-hatch integration (September 12): register aperture center and radius in source coordinates and rotate that center with each raster quarter turn. Fit the circular source uniformly inside the former envelope. Native closed/half/open rows across four operator directions established circular alignment without altering deployment state/timing. Remove only measured negligible alpha haze (below 16 here), preserve near-opaque interior alpha, and inspect over the real floor.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Construction circular-hatch integration (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
p=ROOT/'docs/CURRENT_STATUS.md'; prefix=b'## Construction overhead launch hatch - September 12, 2026\n\nCircular overhead hatch and source-aligned opening integrated. Closed/half/open native states reviewed in four directions, plus room placement. Deployment state/timing unchanged. Cradle camera review and drone decision remain open. See docs/CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md. No export.\n\n'
if not p.read_bytes().startswith(prefix):p.write_bytes(prefix+p.read_bytes())
