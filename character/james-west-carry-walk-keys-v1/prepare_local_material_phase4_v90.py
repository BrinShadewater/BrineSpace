from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'local-material-phase4-v90';out.mkdir(exist_ok=True)
source=p/'master-head-review-v16/bare-004.png';master=r/'character/branforth-west-direct-v2/master-input.png'
box=(80,104,176,200);material_box=(620,390,740,510)
Image.open(source).convert('RGBA').crop(box).resize((1024,1024),Image.Resampling.NEAREST).save(out/'edit-target.png')
Image.open(master).convert('RGBA').crop(material_box).resize((1024,1024),Image.Resampling.LANCZOS).save(out/'master-textile-reference.png')
prompt='''Edit Image1, a fixed96x96 native crop of James' existing carrying-walk phase4, showing his chest, bent arm gripping the rectangular case, and upper legs. Output the EXACT same cropped region and composition, not a new full-body character. Image2 is a small original high-resolution master material sample ONLY, showing the fine diamond quilting, charcoal fabric modelling, subdued stitching and muted yellow shoulder construction. Use its surface material/detail only; never add its anatomy or pose.
Change ONLY Image1's overly white bright seam and hardware highlights to the master sample's subdued matte finish. Preserve the same fine scale of textile quilting, close stitches, dark-fabric folds and detailed existing metal fitting construction. Keep readable softly modelled dark charcoal, muted warm yellow and dull silver metal; no purple/magenta tint, no solid black shadow patches, no flat cartoon simplification or pixel-art style conversion.
Every existing chest panel, shoulder patch, backpack edge, sleeve fold, elbow, wrist cuff, glove gripping the case, case outline/corner fittings, belt tool, thigh, knee plate and ankle strap MUST retain its exact position/shape/size. Keep all near/far limb articulation and perspective unchanged. NO reposing, moving the case, resizing/recentering the body, adding/removing parts, changing knee placement or adding a head/boots. This is only surface material correction of the existing crop. The crop touches existing art at its boundaries; do not replace or reshape those boundaries.
Return exactly the same1024x1024 crop composition with real transparent background, no text, cast shadow, glow or background. Do not produce a complete figure. No green from the material reference.'''
(out/'prompt.txt').write_text(prompt,encoding='utf-8');sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
refs=[out/'edit-target.png',out/'master-textile-reference.png']
(out/'inputs.json').write_text(json.dumps(dict(sourceSha256={f.relative_to(r).as_posix():sha(f) for f in [source,master]},referenceSha256={f.relative_to(r).as_posix():sha(f) for f in refs},promptSha256=sha(out/'prompt.txt'),cropBox=box,materialBox=material_box,normalChanged=False),indent=2)+'\n')
print('Prepared fixed96crop phase4 material repair, with cropped textile authority only.')
