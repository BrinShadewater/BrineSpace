"""Preserve initial Tidal candidate and verified mismatch findings."""
from pathlib import Path
import shutil,json,hashlib
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/rooms/tidal-condenser/pack'
raw=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-9327b43b-d2b5-4b2a-a76f-1c25be17dc02.png')
shutil.copyfile(raw,PACK/'source-v1.png')
(PACK/'review-v1.json').write_text(json.dumps({'status':'rejected pending correction; not installed','sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'findings':['inventory restored','cartridge releases face left rather than operator edge','RGB baked checkerboard','console top-plane clarity unproven'],'baseline':'output/tidal-owner-repair-2026-09-12/before'},indent=2)+'\n')
note='\n\nTidal inventory/facing audit (September 12): existing directional companions changed inventory (three north coil returns and console versus two returns and no console south). Lock the whole-bank inventory before deriving rotations. A candidate can restore counts yet fail individual cartridge access; inspect every release edge. Check actual alpha mode because a rendered checkerboard can be baked RGB. Rear-wall palette is a separate live consumer from the machinery bank.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Tidal inventory/facing audit (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
