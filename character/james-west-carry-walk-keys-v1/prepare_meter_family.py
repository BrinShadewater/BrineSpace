from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];crop=[104,112,168,176]
ref=p/'walk00-meter-occlusion-v2.png'
Image.open(ref).convert('RGBA').crop(crop).resize((768,768),Image.Resampling.LANCZOS).save(p/'meter-occlusion-family-reference.png')
for index in (8,12,20,28,36,48):
    name=f'walk{index:02d}-meter-occlusion-v3'
    source=p/f'walk{index:02d}-case-v2.png' if index in (12,28,36) else p/f'walk{index:02d}-carry.png'
    Image.open(source).convert('RGBA').crop(crop).resize((768,768),Image.Resampling.LANCZOS).save(p/f'{name}-target.png')
    prompt=f'''Edit image1 ONLY: fixed64x64native square case/wrist/belt crop enlarged12x of James carrying phase{index}. Image2 is same-scale provisional reference with the wrong visible lower meter removed. In image1 REMOVE the wrongly relocated yellow-screen/bar meter BELOW/BESIDE carrying glove: remove its yellow screen/bars and complete rectangular housing/rim. Phase48has only a small low yellow fragment; remove that fragment and its false lower unit too. Authentic meter is attached higher/left at original belt, naturally hidden behind existing carrying glove here; DO NOT move it outward/down to make it visible, DO NOT draw any new yellow screen/buttons/fleck above or below glove. Fill false lower-unit area with coherent neutral matte graphite belt/hip cloth and original belt seam behind glove, no alpha hole, featureless black cavity or purplish patch. Preserve image1 own exact case dimensions/waist height/panel/latches, near/far gloves and their walking-phase placement, fingertips gripping case and silver cuff connection. Do not copy reference hand position/body pose. Keep separate silver wrench/holster on right belt exactly in place/design, never put wrench in hand; remove meter only. Preserve original sleeve folds, torso hardware, hip/leg anatomy, framing/alpha margins and subdued matte exposure. Return original full square crop with wrong visible lower meter entirely gone, original-position authentic meter naturally occluded, and case/hands/wrench otherwise unchanged.'''
    (p/f'{name}-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
    files=[source,ref,p/f'{name}-target.png',p/'meter-occlusion-family-reference.png',p/f'{name}-prompt.txt',Path(__file__)]
    (p/f'{name}-inputs.json').write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':crop,'admissionRegion':[124,130,145,160],'baseFile':source.name,'scope':'Lower meter/fragment repair behind carrying grip. Tools/hand inside rectangle not exact-protected; per-pose occlusion and wrench identity remain review required.'},indent=2)+'\n',encoding='utf-8')
print('Six bounded meter/fragment repair targets prepared, no pose transforms.')
