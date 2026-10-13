"""Freeze unchanged selected South anatomy and old cargo-motion references."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-south-carry-material-v1'
S=BASE/'sources'
assert not (S/'guide-provenance.json').exists()
S.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cat=ROOT/'character/marsh-v2/catalog.json'
def resolve(p,name):return ROOT/name.removeprefix('res://') if name.startswith('res://') else (p.parent/name).resolve()
selected={}
for name in json.loads(cat.read_text())['body']:
    p=resolve(cat,name);d=json.loads(p.read_text())
    for state in d['states']:selected[state['id']]=(p,d,state)
def record(key,slot):
    manifest,d,state=selected[key];p=resolve(manifest,state['frameFiles'][slot]);f=Image.open(p).convert('RGBA');b=f.getbbox()
    metadata={k:d[k] for k in ['pivot','standingHeight']}
    metadata.update(frameWidth=f.width,frameHeight=f.height)
    return {'key':key,'slot':slot,'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'manifest':manifest.relative_to(ROOT).as_posix(),'metadata':metadata,'declaredCanvasDimensions':[d.get('frameWidth'),d.get('frameHeight')],'canvasDimensionsFromDecodedImage':True,'occupiedBounds':b,'occupiedSize':[b[2]-b[0],b[3]-b[1]],'stateTiming':{k:state[k] for k in ['fps','frameDurationsMs','loop'] if k in state}}
primary=[record('idle-south',0),record('idle-south',1),record('walk-south',0),record('walk-south',2)]
motion=[record('carry-south',i) for i in range(4)]
for name,records in [('selected-south-idle-gait.png',primary),('carry-motion-guide.png',motion)]:
    board=Image.new('RGB',(4*512,592),'#293b40');draw=ImageDraw.Draw(board)
    for i,r in enumerate(records):
        f=Image.open(ROOT/r['path']).convert('RGBA');pivot=r['metadata']['pivot'];reg=Image.new('RGBA',(256,256));offset=(128-int(pivot[0]),224-int(pivot[1]));reg.alpha_composite(f,offset)
        assert np.count_nonzero(np.array(reg)[:,:,3])==np.count_nonzero(np.array(f)[:,:,3])
        large=reg.resize((512,512),Image.Resampling.NEAREST);board.paste(large,(i*512,65),large)
        draw.text((i*512+4,5),r['key']+' slot'+str(r['slot']),fill='white');draw.text((i*512+4,25),'PRIMARY body/camera/grade' if records is primary else 'MOTION/CARGO ONLY; old body not calibration',fill='#b1d5c6');r['guideWholeTranslation']=offset
    board.save(S/name)
idle=Image.open(ROOT/primary[0]['path']).convert('RGBA');assert idle.size==(184,184);idle.resize((736,736),Image.Resampling.NEAREST).save(S/'selected-idle0-only.png')
master=ROOT/'character/marsh-motion-polish-v1/sources/south-standing-identity-01.png'
data={'normalAdmission':False,'fullGoalComplete':False,'primarySourceFrames':primary,'guideSourceFrames':motion,'originalOwnMaster':{'path':master.relative_to(ROOT).as_posix(),'sha256':sha(master)},'guideArtifacts':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in [S/'selected-south-idle-gait.png',S/'carry-motion-guide.png',S/'selected-idle0-only.png']],'operations':'Eight complete unchanged source figures, common256canvas/p128224 whole translations, nearest2x boards; single selected idle nearest4x. No anatomy edits/mirror/patch/recolour.','limits':'Cargo extent is not body height or width. Compare selected adult head/torso/limbs/camera behind crate and maintain its support/occlusion. Old cargo poses supply cargo geometry/motion only. Guide preparation is not source, runtime or art acceptance.'}
(S/'guide-provenance.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'wholeReferenceFrames':8,'selectedIdleOccupiedSize':primary[0]['occupiedSize'],'carryFrameSizes':[r['occupiedSize'] for r in motion],'normalAdmission':False}))
