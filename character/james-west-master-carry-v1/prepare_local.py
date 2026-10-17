from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
m=json.loads((r/'character/crew-runtime-matte-v1/branforth/manifest.json').read_bytes());state=next(s for s in m['states'] if s['id']=='idle-west');source=r/'character/crew-runtime-matte-v1/branforth'/state['frameFiles'][0]
base=Image.new('RGBA',(256,256));base.alpha_composite(Image.open(source).convert('RGBA'),(128-round(m['pivot'][0]),224-round(m['pivot'][1])));base.save(p/'local-original.png')
base.crop((86,96,166,176)).resize((640,640),Image.Resampling.LANCZOS).save(p/'local-target.png')
case=Image.open(r/'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png').convert('RGBA').crop((86,120,132,154));case.resize((case.width*8,case.height*8),Image.Resampling.LANCZOS).save(p/'local-case-reference.png')
prompt='''Edit IMAGE 1 ONLY. This is a fixed square 80x80-native crop of James's torso/arms/belt, enlarged8x, NOT a complete character. Keep exact crop framing, margins, collar/shoulder/backpack positions, waist/hips and belt device positions. Do not extend the crop to reveal a head/legs, zoom or recenter the body. IMAGE 2 shows ONLY the dark grey case and two-handed waist-level grip to insert. IMAGE 3 is the original high-resolution West master for fine painted identity/equipment/style; do not copy its brighter finish or create a whole figure.

Change the arms from hanging at sides to naturally bent elbows and BOTH gloved hands holding one compact horizontal dark graphite case in front at waist level, at the same screen position and size as the case reference. Preserve the torso, shoulder patch/gear emblem, backpack, near-hip diagnostic meter and far-side belt wrench; tools remain on belt, not in hands. Erase the old hanging-hand silhouettes and reveal coherent original trouser material beneath them. Do not leave duplicate hands, clip arm through torso/backpack or conceal the actual hand grip behind the case. Shoulder stays attached in its original pose; only elbow/forearm/hand movement and case insertion. No extra limbs or shifted belt equipment.

Match IMAGE 1's exact subdued neutral MATTE graphite cloth, muted ochre patches, dark gloves and worn silver fittings; no exposure lift, purple/magenta, shiny metal, bright yellow, new black patches or pale outline. Fine painted sprite detail matching the original master. GENUINELY transparent background and clean antialiasing, no green/checkerboard/halo/text. Return the complete ORIGINAL square crop with all original empty margins, still only the cropped torso/arms/belt. Keep every unchanged feature at its target position.'''
(p/'local-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=[source,p/'local-original.png',p/'local-target.png',p/'local-case-reference.png',p/'master-input.png',p/'local-prompt.txt']
(p/'local-inputs.json').write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':[86,96,166,176],'admissionRegion':[86,104,160,169],'selected':False},indent=2)+'\n',encoding='utf-8')
print('Local arm/case edit frozen; fixed selected idle base retains master head/legs outside admitted region.')
