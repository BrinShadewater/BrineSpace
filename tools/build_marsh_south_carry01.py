"""Pack five complete figures using one unobstructed neutral calibration."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageSequence
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-south-carry-material-v1';S=BASE/'sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
gid='exec-93058684-6a69-4380-ad91-8a7f50de23b5'
original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96')/(gid+'.png')
rawpath=S/'carry-01.raw.png';shutil.copy2(original,rawpath)
rp=S/'carry-01.request.json';req=json.loads(rp.read_text());assert sha(S/'carry-01.prompt.txt')==req['promptSha256']
for r in req['orderedReferences']+req['sourceFrames']:assert sha(ROOT/r['path'])==r['sha256']
req.update(status='Retained unselected complete four-pose cargo cycle plus neutral',generationId=gid,originalGeneratedPath=str(original),rawSha256=sha(rawpath));rp.write_text(json.dumps(req,indent=2)+'\n')
raw=Image.open(rawpath).convert('RGBA');a=np.array(raw);xs=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2);groups=np.split(xs,np.flatnonzero(np.diff(xs)>8)+1);assert len(groups)==5,len(groups)
edges=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(4)]+[raw.width];cuts=[(edges[i],0,edges[i+1],raw.height) for i in range(5)];cells=[binary(raw.crop(c)) for c in cuts];nb=cells[4].getbbox();scale=147/(nb[3]-nb[1])
out=BASE/'candidate-01';out.mkdir(exist_ok=True);records=[];frames=[]
phases=['left-contact','left-support-passing','right-contact','right-support-passing','neutral-ruler']
for i,c in enumerate(cells):
    dense=binary(c.resize((round(c.width*scale),round(c.height*scale)),Image.Resampling.BOX));b=dense.getbbox();offset=(92-round((b[0]+b[2])/2),172-b[3]);f=Image.new('RGBA',(184,184));f.alpha_composite(dense,offset);assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]);name=f'{i:03d}.png' if i<4 else 'ruler.png';f.save(out/name);fb=f.getbbox();records.append({'file':name,'phase':phases[i],'sourceCell':cuts[i],'wholeTranslation':offset,'bounds':fb,'size':[fb[2]-fb[0],fb[3]-fb[1]],'sha256':sha(out/name)});frames.append(f)
cat=ROOT/'character/marsh-v2/catalog.json';strides={};state=None
for name in json.loads(cat.read_text())['body']:
    p=ROOT/name.removeprefix('res://') if name.startswith('res://') else (cat.parent/name).resolve();d=json.loads(p.read_text());strides.update(d.get('strideDistanceCells',{}))
    for s in d['states']:
        if s['id']=='carry-south':state=dict(s)
assert state and len(state['frameFiles'])==4 and state['loop'];state['frameFiles']=[f'{i:03d}.png' for i in range(4)]
manifest={'revision':'marsh-south-carry-material-01-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','strideDistanceCells':{'carry-south':strides['carry-south']},'states':[state]}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(out/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'commonNeutralScale':scale,'neutralOccupiedTargetHeight':147,'rawSha256':sha(rawpath),'records':records,'operations':'Five complete alpha128 cells, ONE unobstructed neutral BOX scale, whole translation to bbox bottom172, no clipped pixels. No mirror, limb/crate patch, recolour or pose/cargo-specific fitting.','limits':'Raw opposite support poses and two-hand crate support inspected; packed body/head/camera/grade/cargo/hand joins and native motion remain provisional. Generic bbox anchor is not anatomical contact certification.'},indent=2)+'\n')
guide=json.loads((S/'guide-provenance.json').read_text());idle=Image.open(ROOT/guide['primarySourceFrames'][0]['path']).convert('RGBA');old=[idle]+[Image.open(ROOT/r['path']).convert('RGBA') for r in guide['guideSourceFrames']]
board=Image.new('RGB',(5*368,2*410),'#293b40');draw=ImageDraw.Draw(board)
for row,series in enumerate([old,[idle]+frames[:4]]):
    for col,f in enumerate(series):
        pivot=[92,172] if row==1 or col==0 else guide['guideSourceFrames'][col-1]['metadata']['pivot'];reg=Image.new('RGBA',(184,184));reg.alpha_composite(f,(92-int(pivot[0]),172-int(pivot[1])));assert np.count_nonzero(np.array(reg)[:,:,3])==np.count_nonzero(np.array(f)[:,:,3]);large=reg.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(col*368,row*410+35),large);draw.text((col*368+4,row*410+4),('Selected ' if row==0 else 'Unselected01 ')+('idle' if col==0 else ('carry'+str(col-1)+' / phase unverified' if row==0 else phases[col-1])),fill='white')
board.save(out/'comparison.png')
neutral=Image.new('RGB',(736,420),'#293b40');draw=ImageDraw.Draw(neutral)
for i,f in enumerate([idle,frames[4]]):
    large=f.resize((368,368),Image.Resampling.NEAREST);neutral.paste(large,(i*368,40),large);draw.text((i*368+4,5),['Selected South idle','Unobstructed neutral ruler'][i],fill='white')
neutral.save(out/'neutral-comparison.png')
frames[0].save(out/'source-motion.apng',save_all=True,append_images=frames[1:4],duration=state['frameDurationsMs'],loop=0,disposal=1,blend=0)
decoded=[frame.copy() for frame in ImageSequence.Iterator(Image.open(out/'source-motion.apng'))];assert len(decoded)==4
for i,f in enumerate(decoded):assert np.array_equal(np.array(f.convert('RGBA')),np.array(frames[i]))
print(json.dumps({'commonNeutralScale':scale,'sizes':[r['size'] for r in records],'frameDurationsMs':state['frameDurationsMs'],'strideDistanceCells':strides['carry-south'],'normalAdmission':False}))
