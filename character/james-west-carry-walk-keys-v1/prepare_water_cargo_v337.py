from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'water-cargo-master-v337';o.mkdir(exist_ok=True)
d=json.loads((p/'water-family-review-v335/review.json').read_bytes());inputs=[]
for key,name in [('swim-carry-west','target.png'),('swim-west','ordinary-swim-reference.png')]:
 x=next(x for x in d['samples'] if x['gear']=='bare' and x['slot']==0 and x['key']==key)
 source=r/x['source'];im=Image.open(source).convert('RGBA');assert im.size==(256,276)
 assert hashlib.sha256(im.tobytes()).hexdigest()==x['pixelHash']
 canvas=Image.new('RGBA',(320,320));canvas.alpha_composite(im,(32,22));canvas.resize((1280,1280),Image.Resampling.NEAREST).save(o/name)
 inputs.append(dict(role=name,source=str(source.relative_to(r)),sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),referenceSha256=hashlib.sha256((o/name).read_bytes()).hexdigest(),padding=[32,22],wholeCanvasScale=4))
master=r/'character/branforth-west-direct-v2/master-input.png'
inputs.append(dict(role='original master',source=str(master.relative_to(r)),sourceSha256=hashlib.sha256(master.read_bytes()).hexdigest()))
prompt='''Use case: identity-preserve. Edit Image 1, the transparent square west-facing James swimming-with-cargo sprite. Image 2 is the selected ordinary swim pose, for shoulder/body scale reference only. Image 3 is James's ORIGINAL high-density character master: authoritative for fine soft curved quilted graphite cloth, muted warm metal and yellow, matte colour grade and individual identity.
Make ONE west-facing cargo-swim key pose. Refine the coarse blocky shoulder/upper arm and torso suit in image 1 into the master's soft curved finely stitched quilt fabric. Match the original master's body build: the shoulder/upper arm should feel like soft fitted cloth rather than thick hard armour. Reduce only the excessive shoulder/suit bulk modestly, preserving the underlying body anatomy and the cargo swimming posture. Keep the same face, head size, grey hair, moustache, goggles, collar, backpack, anatomical tool locations and wrench on belt. Keep the same suitcase in both hands, with the same case dimensions and its exact position. Preserve hand/case contact, elbow and knee joint positions, boot tips, pose direction, camera perspective, silhouette length and overall placement on the full square canvas. Retain the bent knees and swim posture of Image 1. Image 2 must not replace the cargo pose or remove its case.
Fine painted game sprite, matte graphite cloth, muted mustard yellow, worn warm silver/brass. Match the master without purple/magenta cast, black cavities, bright white shiny patches or extra illumination. Transparent background with real alpha. Preserve the entire input square framing and padding; return one pose at exactly the same placement and scale as Image 1, no tight crop, no recentering, no text, no new objects, no helmet. This is a local material/body-volume repair, not a new pose or composition.'''
(o/'submitted-prompt.txt').write_text(prompt,encoding='utf-8')
(o/'inputs.json').write_text(json.dumps(dict(inputs=inputs,promptSha256=hashlib.sha256(prompt.encode()).hexdigest(),nativeSourceSize=[256,276],authoringCanvas=[320,320],padding=[32,22],normalChanged=False),indent=2)+'\n')
print(str(o))
