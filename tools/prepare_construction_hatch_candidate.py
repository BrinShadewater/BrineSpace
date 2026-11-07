"""Preserve the overhead hatch candidate and inspect its true alpha."""
import json,hashlib,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'assets/rooms/construction-drone-bay/material'
raw=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-7ff10437-9cfe-46b1-99d5-39f1b47c886d.png')
target=PACK/'hatch-overhead-raw.png'
shutil.copyfile(raw,target)
im=Image.open(target).convert('RGBA')
assert im.getpixel((0,0))[3]==0
lid_alpha=im.getpixel((im.width//2,im.height//2))[3]
assert lid_alpha>=250
review={'status':'source candidate reviewed; not installed', 'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
        'size':im.size,'alpha_bbox':im.getchannel('A').getbbox(),'corner_alpha':0,'lid_center_alpha':lid_alpha,
        'source_findings':['overhead circular lid','four radial clamps','bottom operator controls','matte grey and charcoal'],
        'integration_required':['review near-opaque interior alpha (center 253) against floor','fit inside existing hatch envelope','turn controls inward','replace Construction-only offset elliptical opening with aligned circular visual aperture','native closed/partial/open review','preserve hatch_open state and fleet gameplay'],
        'owner_acceptance':None}
(PACK/'hatch-candidate-review.json').write_text(json.dumps(review,indent=2)+'\n')
note='\n\nConstruction hatch camera lesson (September 12): camera conversion applies to runtime visual overlays as well as static art. The inherited hatch opening is an offset ellipse; a circular overhead lid requires a source-aligned circular aperture. Preserve the existing deployment state and timing, change only its visual geometry, and review closed/partial/open states before installation. A passing closed-room capture cannot prove aperture alignment.\n'
for p in [ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-room-pipeline/references/material-and-scale-review.md',Path('C:/Users/Alex/.codex/skills/brinespace-room-pipeline/references/material-and-scale-review.md')]:
    if 'Construction hatch camera lesson (September 12)' not in p.read_text(encoding='utf-8'):
        with p.open('a',encoding='utf-8') as f:f.write(note)
print(json.dumps(review,indent=2))
