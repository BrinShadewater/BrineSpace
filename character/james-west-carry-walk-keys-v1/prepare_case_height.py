from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];name='walk00-case-v2'
source=p/'walk00-tool-fix.png';crop=(80,88,176,184)
Image.open(source).convert('RGBA').crop(crop).resize((768,768),Image.Resampling.LANCZOS).save(p/f'{name}-target.png')
ref=r/'character/james-carry-headcaps-v1/frames/004.png'
Image.open(ref).convert('RGBA').crop(crop).resize((768,768),Image.Resampling.LANCZOS).save(p/f'{name}-master-reference.png')
prompt='''Edit image1 only, a fixed96x96native upper-body crop enlarged8x. Image2 is the standing master carrying reference at EXACTLY the same native scale/camera/crop. Correct image1 case/grip: current case is too narrow/small and sits too high against chest. Match image2 complete case physical width/height and low waist-level placement, neutral matte graphite hard panels and dull silver latches. Its upper edge should be approximately native world y131 and bottom y154, left edge x91 and right edge x125 before glove overlap. In crop coordinates these correspond top43/bottom66/left11/right45. This is a heavy two-hand case carried in FRONT toward character-facing LEFT. Both hands should support it naturally, no hand hanging loose or body clipping, near silver wrist cuff connects sleeve into right glove. Remove old high case/hands completely, rebuild coherent graphite torso behind them. Preserve image1 original torso walking pose, head/collar, shoulder gear, backpack, suit marking, hips and legs. Do not copy image2 body stance or head. Keep image1 real lower belt meter and its yellow screen/housing, wrench and belt equipment; add NO additional yellow screens or duplicate tools above wrist. Match image1 subdued matte exposure, no magenta/purple, bright chrome or dark cavity. Preserve full square framing and transparent margins. Return only edited image1 upper crop, with master-size case at low waist level and coherent grip.'''
(p/f'{name}-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=[source,ref,p/f'{name}-target.png',p/f'{name}-master-reference.png',p/f'{name}-prompt.txt',Path(__file__)]
(p/f'{name}-inputs.json').write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':list(crop),'admissionRegion':[88,104,166,169],'baseFile':source.name,'scope':'Case height/scale and grip source correction against standing master; whole-cycle/tool acceptance pending.'},indent=2)+'\n',encoding='utf-8')
print('Phase0case height/scale correction prepared against same-scale standing master.')
