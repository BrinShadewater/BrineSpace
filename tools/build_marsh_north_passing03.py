"""Pack complete right-support pose and ruler with one neutral calibration."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw
from rebuild_bill_art import binary
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-north-run-material-v1'
S = BASE / 'sources'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
rawpath = S/'passing-03.raw.png'
req = json.loads((S/'passing-03.request.json').read_text())
assert sha(rawpath) == req['rawSha256']
assert sha(S/'passing-03.prompt.txt') == req['promptSha256']
for r in req['orderedReferences'] + [req['poseSourceFrame']]:
    assert sha(ROOT/r['path']) == r['sha256']
raw = Image.open(rawpath).convert('RGBA')
a = np.array(raw)
xs = np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2)
groups = np.split(xs,np.flatnonzero(np.diff(xs)>8)+1)
assert len(groups)==2
edge = round((groups[0].max()+groups[1].min())/2)
cuts = [(0,0,edge,raw.height),(edge,0,raw.width,raw.height)]
cells = [binary(raw.crop(c)) for c in cuts]
nb = cells[1].getbbox()
scale = 146/(nb[3]-nb[1])
out = BASE/'passing-03-unselected'
out.mkdir(exist_ok=True)
names = ['right-passing.png','ruler.png']
records,frames = [],[]
for i,c in enumerate(cells):
    dense = binary(c.resize((round(c.width*scale),round(c.height*scale)),Image.Resampling.BOX))
    b = dense.getbbox()
    offset = (92-round((b[0]+b[2])/2),172-b[3])
    f = Image.new('RGBA',(184,184))
    f.alpha_composite(dense,offset)
    assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3])
    f.save(out/names[i])
    fb = f.getbbox()
    frames.append(f)
    records.append({'file':names[i],'sourceCell':cuts[i],'wholeTranslation':offset,'bounds':fb,'size':[fb[2]-fb[0],fb[3]-fb[1]],'sha256':sha(out/names[i])})
recipe = {'normalAdmission':False,'fullGoalComplete':False,'commonNeutralScale':scale,'neutralOccupiedTargetHeight':146,'rawSha256':sha(rawpath),'records':records,'operations':'Two complete alpha128 cells, one neutral BOX scale, whole translation to bbox bottom172, no clipping, mirroring, patches, recolour or per-pose fitting. Standard alpha threshold only; raw retained.','visualReview':'Raw right leg supports and left sole raised. Arms remain asymmetrical like contact reference, left knee/sole lift stronger than requested. Packed body/grade and phase joins pending. Transparent corners and middle gutter confirmed; renderer preview haze is not proof of an opaque background.'}
(out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
guide = json.loads((S/'guide-provenance.json').read_text())
idle = Image.open(ROOT/guide['primarySourceFrames'][0]['path']).convert('RGBA')
board = Image.new('RGB',(3*368,440),'#293b40')
draw = ImageDraw.Draw(board)
for i,f in enumerate([idle]+frames):
    large = f.resize((368,368),Image.Resampling.NEAREST)
    board.paste(large,(i*368,50),large)
    draw.text((i*368+4,5),(['Selected North idle']+names)[i],fill='white')
board.save(out/'comparison.png')
print(json.dumps({'scale':scale,'sizes':[r['size'] for r in records],'normalAdmission':False}))
