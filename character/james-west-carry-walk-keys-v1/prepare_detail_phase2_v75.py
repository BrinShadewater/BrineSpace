from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'detail-phase2-v75';out.mkdir(exist_ok=True)
sources=[p/'master-material-phase2-v69/bare-head-protected.png',r/'character/branforth-west-direct-v2/master-input.png',r/'character/james-west-master-carry-v1/registered-original-master.png',p/'master-head-review-v16/bare-002.png']
refs=[]
for role,f in zip(['edit-target','original-high-resolution-master','registered-original-master','original-stride'],sources):
    dest=out/(role+'.png');im=Image.open(f).convert('RGBA')
    if im.size==(256,256):im=im.resize((1024,1024),Image.Resampling.NEAREST)
    im.save(dest);refs.append(dest)
prompt='''Edit only Image1, the single west-facing walking James carrying a rectangular case, on its transparent square canvas. Restore suit surface construction and fine material detail lost in an earlier material correction. Image2 is the original high-resolution authoritative character illustration: use its diamond-quilted fabric, subtle worn stitching, small brass rivets, muted yellow trim, restrained silver metal and softly modelled matte fabric as the DETAIL AND MATERIAL authority. Its green backdrop is reference background only and must never appear in the output. Image3 is the exact same original master registered to game scale, showing the intended native detail density. Image4 is this original walking phase, showing its construction and pose; its over-bright seams must not be copied.
Keep Image1's already matte finish, but bring back the original master's close-spaced diamond quilting and fine subdued seam/stitch marks in the sleeve, chest and trouser cloth. Retain the fine articulated cuff, glove, knee plate, ankle strap and boot construction. Materials have softly modelled texture, subdued small highlights and visible dark-fabric folds; avoid smooth empty panels, bold cartoon linework, flat cel shading or white outline seams. Preserve the original warm charcoal material with muted yellow, never purple/magenta and never solid black shadow patches. Do not increase exposure or polish the armor. Match the original master, not a simplified substitute.
STRICT INVARIANTS: keep Image1's exact silhouette, distinct phase2 walking pose, camera and perspective, proportions, head size and position, shoulder/elbow/wrist articulation, hands gripping the same case, case shape/size/location, belt tools, near/far knees, boot shape, foot spacing and ground contact. Change surface construction and detail only. No new accessories, no moving or changing tools, no added limbs, no stance changes. Do not copy standing legs or arms from Image2 or Image3.
Return one sprite on the same full 1024x1024 coordinate canvas with real transparent background, no text, shadow, glow, crop, recentering or rescaling. Preserve its compact original illustrated-sprite density at native256x256. This is an illustrated game character material-detail edit, not a pixel-art style conversion.'''
(out/'prompt.txt').write_text(prompt,encoding='utf-8')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(out/'inputs.json').write_text(json.dumps(dict(sourceSha256={f.relative_to(r).as_posix():sha(f) for f in sources},referenceSha256={f.relative_to(r).as_posix():sha(f) for f in refs},promptSha256=sha(out/'prompt.txt'),normalChanged=False),indent=2)+'\n')
print('Prepared representative phase2 detail edit with full-resolution original master and frozen references.')
