from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'master-material-v49';out.mkdir(exist_ok=True)
sources=[p/'master-head-review-v16/bare-000.png',r/'character/james-west-master-carry-v1/registered-original-master.png',r/'character/james-west-master-carry-v1/local-v3-carry-pose.png']
refs=[]
for role,f in zip(['edit-target','original-master','carry-case-reference'],sources):
    dest=out/(role+'.png');Image.open(f).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(dest);refs.append(dest)
prompt='''Edit Image1, the single walking James sprite on a transparent square canvas. Image2 is the ORIGINAL AUTHORITATIVE James master for suit material, color, stitching, perspective and identity. Image3 is supporting carrying-case design/finish only, not pose authority.
Change only the excessive material brightness/detail of Image1 to match Image2: matte neutral charcoal fabric, subdued original stitching and quilting, restrained dull silver armor and belt tools, muted yellow accents, no white glowing seam outlines. Preserve the original master's amount and scale of surface detail. Retain readable dark fabric without purple or magenta cast and without solid black shadow patches.
STRICTLY KEEP Image1's walking-entry pose, silhouette, head/face/hair identity and exact head size, head position, shoulders, hands and grip, case outer dimensions and position, tool positions, two-leg stance, knees, boot ground contact and foot pivot. No body reproportioning, no pose rotation, no broadening stance, no moving head, no new tools or case fittings. Do not paste Image2 standing legs onto Image1. Case hardware finish should be matte like Image3, same Image1 geometry. This is a material correction of ONE pose, not a new character or animation sheet.
Return exactly one sprite in the same 1024x1024 coordinate layout, full transparent background, no text, no cast shadow, no glow. Native source corresponds to256x256; retain that compact pixel-art density and keep crown/soles registered. No rescaling, no cropping, no recentering.'''
(out/'prompt.txt').write_text(prompt,encoding='utf-8')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(out/'inputs.json').write_text(json.dumps(dict(sourceSha256={f.relative_to(r).as_posix():sha(f) for f in sources},referenceSha256={f.relative_to(r).as_posix():sha(f) for f in refs},promptSha256=sha(out/'prompt.txt'),normalChanged=False),indent=2)+'\n')
print(json.dumps(dict(references=[str(f) for f in refs],prompt=prompt)))
