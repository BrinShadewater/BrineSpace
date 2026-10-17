from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
ref=p/'walk00-case-v2-fleck.png';crop=(80,88,176,184)
Image.open(ref).convert('RGBA').crop(crop).resize((768,768),Image.Resampling.LANCZOS).save(p/'corrected-carry-reference.png')
manifest=r/'character/crew-runtime-matte-v1/branforth/manifest.json'
for index in (8,20):
    name=f'walk{index:02d}-carry'
    donor=r/f'character/crew-runtime-matte-v1/branforth/frames/walk-west-tone-lock-v1/{index:03d}.png'
    im=Image.open(donor).convert('RGBA');assert im.size==(184,184)
    base=Image.new('RGBA',(256,256));base.paste(im,(36,52));base.save(p/f'{name}-original.png')
    base.crop(crop).resize((768,768),Image.Resampling.LANCZOS).save(p/f'{name}-target.png')
    prompt=f'''Edit image1 only: fixed96x96native upper-body crop of James walking West, phase{index}, enlarged8x. Preserve original square framing, alpha margins, subdued matte graphite/ochre/dull silver grade and original torso angle. Image2 is corrected carrying pose at EXACT same scale/camera/crop: use its case physical dimensions, low waist placement and natural two-hand grip, but retain image1 walking body pose. Replace the original hanging arm with both gloved hands supporting this graphite hard equipment case IN FRONT toward character-facing LEFT. Case approximately world x91..125,y131..154 (crop x11..45,y43..66), consistent panel/latches, similar rigid size throughout gait; slight natural arm adjustment only, no chest-high or undersized case. Near forearm folds down into silver cuff and right glove; far hand grips left edge. No hand/body clipping, detached cuff, black underarm/backpack cavity or loose hand behind case. Retain original shoulder patch, straps, backpack, chest tools, real belt meter and wrench, hips/thigh pose. Do not copy reference head/body/legs. No extra yellow dot, screen or tool above wrist: reference has only actual lower belt meter. Keep original head/collar and leg geometry outside arm/case area. No brightening, magenta/purple cast or shiny new materials. Return only original full square image1 crop with coherent master-matched case and grip.'''
    (p/f'{name}-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
    files=[donor,manifest,ref,p/f'{name}-original.png',p/f'{name}-target.png',p/'corrected-carry-reference.png',p/f'{name}-prompt.txt',Path(__file__)]
    (p/f'{name}-inputs.json').write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':list(crop),'admissionRegion':[88,104,166,169],'baseFile':f'{name}-original.png','scope':'New authored carrying upper phase; actual donor head above104/legs below169 exact, intermediate full gait acceptance pending.'},indent=2)+'\n',encoding='utf-8')
print('Two intermediate carrying sources prepared from actual master-family walk8/20.')
