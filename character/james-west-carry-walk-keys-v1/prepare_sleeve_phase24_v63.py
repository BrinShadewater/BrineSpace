from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'sleeve-phase24-v63';out.mkdir(exist_ok=True)
box=(110,96,158,144)
sources=[p/'narrow-grip-phase24-v62/bare-candidate.png',p/'master-material-phase23-v58/bare-head-protected.png',p/'master-material-phase25-v59/bare-head-protected.png',r/'character/james-west-master-carry-v1/registered-original-master.png']
roles=['edit-target','previous-frame-material','next-frame-material','original-master']
board=Image.new('RGBA',(576,170),(47,58,63,255));draw=ImageDraw.Draw(board)
for col,(role,f) in enumerate(zip(roles,sources)):
    im=Image.open(f).convert('RGBA');crop=im.crop(box);crop.resize((768,768),Image.Resampling.NEAREST).save(out/(role+'.png'));board.alpha_composite(crop.resize((144,144),Image.Resampling.NEAREST),(col*144,24));draw.text((col*144+2,5),role,fill='white')
board.save(out/'input-sleeve-review.png')
prompt='''Edit Image1, a local48x48-native-unit crop of James's near shoulder and bent sleeve. Image2 and Image3 are the actual immediately preceding/following animation poses and are MATERIAL references only. Image4 is the original character master MATERIAL authority. Preserve Image1's exact pose, geometry and framing, never copy reference arm positions.
Correct ONLY the brighter horizontal sleeve rib/seam highlights in Image1 so its fabric has the same subdued matte neutral/warm charcoal intensity and fine quilt detail as Image2/Image3 and original master Image4. Keep readable original bands/quilting at restrained contrast, not a smooth featureless sleeve. No white glowing stripes, gray shiny outlines, black solid patches or purple/magenta. Dull neutral silver cuff remains restrained.
STRICTLY preserve Image1's sleeve outline/arm size, elbow and wrist positions, shoulder badge/color/design, torso edges and belt, glove/fingers and case pixels. No new equipment, no shifted cuff, no resizing/recentering, no moving the arm or smoothing its anatomy. Return ONE genuinely transparent square crop in the same coordinate layout. Material-only edit; no text, shadow, background or extra sprites.'''
(out/'prompt.txt').write_text(prompt,encoding='utf-8');sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(out/'inputs.json').write_text(json.dumps(dict(cropBox=box,sourceSha256={f.relative_to(r).as_posix():sha(f) for f in sources},referenceSha256={str((out/(role+'.png')).relative_to(r)):sha(out/(role+'.png')) for role in roles},promptSha256=sha(out/'prompt.txt'),normalChanged=False),indent=2)+'\n')
print('Actual adjacent sleeve references frozen; no artwork selection changed.')
