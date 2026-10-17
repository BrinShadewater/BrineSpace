"""Pack whole held-cargo source figures for review, without normal admission."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageSequence
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'character/marsh-cargo-held-material-v1';S=B/'sources';O=B/'east-unload-02-unselected';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def binary(im):
    a=np.array(im.convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>=128,255,0);return Image.fromarray(a)
r=json.loads((S/'east-unload-02.request.json').read_text())
assert sha(S/'east-unload-02.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
raw=Image.open(S/'east-unload-02.raw.png').convert('RGBA');a=np.array(raw)
xs=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2)
groups=np.split(xs,np.flatnonzero(np.diff(xs)>8)+1);assert len(groups)==3
edges=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(2)]+[raw.width]
cuts=[(edges[i],0,edges[i+1],raw.height) for i in range(3)]
cells=[binary(raw.crop(c)) for c in cuts];nb=cells[2].getbbox();scale=147/(nb[3]-nb[1])
frames=[];records=[]
for i,c in enumerate(cells):
    dense=binary(c.resize((round(c.width*scale),round(c.height*scale)),Image.Resampling.BOX));b=dense.getbbox()
    if i==2:anchor=(b[0]+b[2]-1)/2;method='whole neutral occupied midpoint'
    else:
        # Body boots occupy left 45% of the action silhouette; exclude floor case.
        aa=np.array(dense)[:,:,3];stop=b[0]+round((b[2]-b[0])*.45)
        sy,sx=np.nonzero(aa[b[3]-5:b[3],b[0]:stop]>=128);assert len(sx)>0
        anchor=b[0]+(sx.min()+sx.max())/2;method='left boot floor-band midpoint, whole translation only'
    offset=(round(92-anchor),172-b[3]);f=Image.new('RGBA',(184,184));f.alpha_composite(dense,offset)
    assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3])
    name=f'intermediate-{i+1}.png' if i<2 else 'ruler.png';f.save(O/name);fb=f.getbbox()
    records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'registration':method,'occupiedBounds':fb,'occupiedSize':[fb[2]-fb[0],fb[3]-fb[1]],'sha256':sha(O/name)});frames.append(f)
idle=ROOT/r['sourceFrames'][0]['path'];carry=ROOT/r['sourceFrames'][1]['path']
U=O/'unload-east';P=O/'pickup-east';U.mkdir(exist_ok=True);P.mkdir(exist_ok=True)
paths=[carry,O/'intermediate-1.png',O/'intermediate-2.png',idle]
for directory,ordered in [(U,paths),(P,list(reversed(paths)))]:
    for i,p in enumerate(ordered):shutil.copy2(p,directory/f'{i:03}.png')
    images=[Image.open(directory/f'{i:03}.png').convert('RGBA') for i in range(4)]
    images[0].save(directory/'review.apng',save_all=True,append_images=images[1:],duration=[130]*4,loop=0,disposal=0,blend=0)
    decoded=[f.convert('RGBA').copy() for f in ImageSequence.Iterator(Image.open(directory/'review.apng'))]
    assert len(decoded)==4 and all(x.tobytes()==y.tobytes() for x,y in zip(images,decoded))
states=[]
selected_manifest=json.loads((ROOT/'character/marsh-master-repair-v1/manifest-p92_0-172_0.json').read_text())
for key,directory in [('unload-east',U),('pickup-east',P)]:
    state=next(s.copy() for s in selected_manifest['states'] if s['id']==key)
    assert state['frameDurationsMs']==[130]*4 and len(state['frameFiles'])==4 and not state['loop']
    state['frameFiles']=['res://'+(directory/f'{i:03}.png').relative_to(ROOT).as_posix() for i in range(4)]
    states.append(state)
(O/'manifest.json').write_text(json.dumps({'revision':'marsh-east-unload-02-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':states},indent=2)+'\n')
for name,images,labels in [
    ('whole-motion-comparison.png',[Image.open(p).convert('RGBA') for p in paths],['Exact staged carry endpoint','Whole half-lowering','Whole floor lowering / contact pending','Exact selected idle endpoint']),
    ('neutral-comparison.png',[Image.open(idle).convert('RGBA'),frames[2]],['Selected East idle PRIMARY','Generated whole neutral / diagnostic'])]:
    board=Image.new('RGB',(368*len(images),430),'#293b40');d=ImageDraw.Draw(board)
    for i,(im,label) in enumerate(zip(images,labels)):
        large=im.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(368*i,45),large);d.text((368*i+4,5),label,fill='white')
    board.save(O/name)
recipe={'normalAdmission':False,'fullGoalComplete':False,'generationId':r['generationId'],'rawSha256':r['rawSha256'],'commonNeutralScale':scale,'neutralTargetHeight':147,'records':records,'exactCarryEndpoint':sha(U/'000.png')==sha(carry),'exactIdleEndpoint':sha(U/'003.png')==sha(idle),'exactPickupReversal':all(sha(P/f'{i:03}.png')==sha(U/f'{3-i:03}.png') for i in range(4)),'decodedApngFrames':8,'timingMs':[130]*4,'operations':'Three whole alpha128 cells, one neutral147 BOX scale; whole integer floor/boot registration; no clipped opaque pixels, mirrors, patches, recolour or per-pose fits. Sole registration does not prove crate floor contact. Source/body/case/joins require visual review; not actual pickup/unload playback.'}
(O/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
print(json.dumps({'scale':scale,'sizes':[q['occupiedSize'] for q in records],'endpointsExact':recipe['exactCarryEndpoint'] and recipe['exactIdleEndpoint'],'pickupReversalExact':recipe['exactPickupReversal'],'normalAdmission':False}))
