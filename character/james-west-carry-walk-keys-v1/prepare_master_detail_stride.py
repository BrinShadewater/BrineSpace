from pathlib import Path
from PIL import Image
import json,hashlib,sys
p=Path(__file__).resolve().parent;r=p.parents[1];phase=int(sys.argv[1]);version=int(sys.argv[2]);out=p/f'master-detail-phase{phase}-v{version}';out.mkdir(exist_ok=True)
sources=[p/f'master-head-review-v16/bare-{phase:03d}.png',r/'character/branforth-west-direct-v2/master-input.png',r/'character/james-west-master-carry-v1/registered-original-master.png']
refs=[]
for role,f in zip(['edit-target','original-high-resolution-master','registered-original-master'],sources):
    dest=out/(role+'.png');im=Image.open(f).convert('RGBA')
    if im.size==(256,256):im=im.resize((1024,1024),Image.Resampling.NEAREST)
    im.save(dest);refs.append(dest)
prompt=f'''Edit only Image1, James walking west carrying his rectangular case in distinct stride phase{phase}. Image2 is the original high-resolution authoritative James illustration; Image3 is that same original master registered to native game size. Use both for material, fine construction, proportions and style. Image2's green background is reference only and must not appear in output.
Correct Image1's overly bright white seam/hardware highlights to the original master's subdued matte warm charcoal fabric, worn dull silver metal, fine brass rivets and muted yellow accents. Preserve/restore the master's close-spaced diamond quilting, subtly modelled fabric folds, fine subdued stitches, articulated cuffs/gloves, knee plates, ankle straps and detailed boot construction. Small material highlights remain readable but never glow or become white outline seams. Do not simplify into smooth empty panels or flat cartoon linework. Keep the illustrated sprite art and original native detail density. No purple/magenta grading and no solid black shadow patches. This is material/detail correction only.
STRICTLY preserve Image1's distinct walking phase{phase}: exact silhouette, camera/perspective, compact proportions, head/face/hair identity and size, head position, shoulders/elbows/wrists, hands gripping the same case, case dimensions/location/fittings, belt tools, both legs, knees, boot contour/spacing, sole rows and physical foot pivot. Keep every hardware piece in its original position. No new accessories, no pose rotation, no change of stance, no widening boots, no movement of case, no standing legs copied from the master. Do not transfer Image2's standing pose.
Return exactly one sprite on the same 1024x1024 full coordinate canvas with actual transparent background; no green, text, cast shadow, glow, crop, recentering, rescaling or pixel-art conversion. Preserve native256x256 illustrated-sprite density. Keep crown and soles registered.'''
(out/'prompt.txt').write_text(prompt,encoding='utf-8');sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(out/'inputs.json').write_text(json.dumps(dict(phase=phase,sourceSha256={f.relative_to(r).as_posix():sha(f) for f in sources},referenceSha256={f.relative_to(r).as_posix():sha(f) for f in refs},promptSha256=sha(out/'prompt.txt'),normalChanged=False),indent=2)+'\n')
print(f'Prepared phase{phase} original-master detail references.')
