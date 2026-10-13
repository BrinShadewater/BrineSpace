"""Prepare six consecutive whole poses as one animation-sheet edit target."""
from pathlib import Path
from PIL import Image
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1]
P=R/'character/bill-east-walk-master-pilot-v1'
D=P/'sequence-000-005-v1'
D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sheet=Image.new('RGBA',(1536,1024))
inputs=[]
for slot in range(6):
    p=R/f'character/bill-walk-east-material-v1/frames/bare/walk-east/{slot:03}.png'
    im=Image.open(p).convert('RGBA')
    assert im.size==(256,256)
    sheet.paste(im.resize((512,512),Image.Resampling.NEAREST),((slot%3)*512,(slot//3)*512))
    inputs.append(dict(slot=slot,path=str(p),sha256=sha(p)))
sheet.save(D/'edit-target.png')
refs=[dict(path=str(D/'edit-target.png'),sha256=sha(D/'edit-target.png'),role='Only edit target; exact six consecutive poses, row-major 3x2 grid, 512px square cells')]
for src,name,role in [(P/'stride-000-v1/raw-000.png','preferred-walk-reference.png','Whole detailed walking Bill identity/material continuity, not a sheet layout or pose replacement'),(P/'original-master.png','original-master.png','Original master identity/material authority, not a pose replacement')]:
    shutil.copyfile(src,D/name)
    refs.append(dict(path=str(D/name),sha256=sha(D/name),source=str(src),sourceSha256=sha(src),role=role))
prompt='''Edit image1 as ONE animation sprite sheet. Exact output 1536x1024 pixels, transparent background. Exactly SIX complete Bill figures in a 3-column by 2-row grid of 512x512 cells, read left to right, top then bottom. Preserve every figure's exact placement, crown, feet, body scale, arm and leg pose, gait phase, cell and transparent padding from image1. These are six CONSECUTIVE subtly changing walking poses, not six different designs or six identical repeated poses. Image2 is the preferred detailed walking rendering; image3 is the original master identity authority. Restore the same warm angular face, brown hair, small head, fine matte charcoal quilt stitches, worn metal hardware and exact square/ring suit insignia in ALL six poses. Keep face, collar, suit grade and lighting identical across the sequence. Avoid shiny/bright armor and black faces. Preserve articulation and foot placement. Do not move heads, enlarge bodies, modify the stride or add props. No captions, borders, extra figures, shadows, opaque backgrounds or grid lines. Each figure stays entirely within its original cell. This edits only whole-figure design/material fidelity while retaining the original six-frame motion.'''
(D/'prompt.txt').write_text(prompt,encoding='utf-8')
(D/'references.json').write_text(json.dumps(refs,indent=2)+'\n',encoding='utf-8')
(D/'selected-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n',encoding='utf-8')
print('Prepared 6 consecutive phases; 1536x1024 target with fixed 512px cells; selected sources unchanged.')
