from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'case-grip-material-phase24-v57';out.mkdir(exist_ok=True)
box=(80,104,160,184)
sources=[p/'master-head-review-v16/bare-024.png',p/'master-material-v49/bare-head-protected.png',r/'character/james-west-master-carry-v1/registered-original-master.png']
roles=['edit-target','matte-case-finish','original-master']
for role,f in zip(roles,sources):
    im=Image.open(f).convert('RGBA');im=(im.crop(box).resize((960,960),Image.Resampling.NEAREST) if role!='original-master' else im.resize((1024,1024),Image.Resampling.NEAREST));im.save(out/(role+'.png'))
prompt='''Edit Image1, the ORIGINAL exact same-pose case-and-hand crop of James carrying a small rectangular case. Preserve Image1's geometry exactly. Image2 is MATTE FINISH reference only: use its dark neutral case, dull worn silver corners, charcoal gloves and restrained cuffs. Image3 is ORIGINAL character master material/color authority. Do NOT copy either reference pose or case size.
Change ONLY the too-bright white hardware and glove/cuff highlights in Image1: make silver fittings subdued dull neutral gray like Image2 while retaining four square corner fasteners, original rectangular projected front face and side edge, all positions/angles/dimensions. Preserve both original gloves, fingers, wrist contours and two separate arm grips EXACTLY, case against both hands. Keep belt tools in original positions. No new shape, extra tools, pose/size changes, smooth inflated gloves, rounded new fasteners, dark black patches or purple cast.
Return ONE transparent square crop with the EXACT original framing/layout/margins. Original80x80 native crop enlarged960x960. Material-only; do not rescale, rotate, recenter or crop. Surrounding torso/legs are context and must stay unchanged. No text, shadow, background or sheet.'''
(out/'prompt.txt').write_text(prompt,encoding='utf-8');sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(out/'inputs.json').write_text(json.dumps(dict(cropBox=box,sourceSha256={f.relative_to(r).as_posix():sha(f) for f in sources},referenceSha256={str((out/(role+'.png')).relative_to(r)):sha(out/(role+'.png')) for role in roles},promptSha256=sha(out/'prompt.txt'),normalChanged=False),indent=2)+'\n')
print('Original grip geometry isolated as edit target; matte references frozen.')
