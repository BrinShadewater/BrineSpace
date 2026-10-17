"""Retain source and package whole transitions with one neutral scale."""
from pathlib import Path
import json,hashlib,shutil,sys
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];mode,side,generation=sys.argv[1:4]
revision=next((v.removeprefix('revision') for v in sys.argv[4:] if v.startswith('revision')),'01')
assert revision in ('01','02','03','04','05','06')
stem=f'{mode}-{side}-{revision}';B=ROOT/'character/marsh-water-transition-material-v1';S=B/'sources';O=B/(stem+'-unselected');O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((S/(stem+'.request.json')).read_text());assert sha(S/(stem+'.prompt.txt'))==r['promptSha256']
for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96')/(generation+'.png');rawpath=S/(stem+'.raw.png')
if not rawpath.exists():shutil.copy2(original,rawpath)
assert sha(original)==sha(rawpath)
r.update(generationId=generation,originalGeneratedPath=original.as_posix(),rawSha256=sha(rawpath),status='whole source retained; provisional packaging/review')
(S/(stem+'.request.json')).write_text(json.dumps(r,indent=2)+'\n')
def binary(im):
    a=np.array(im.convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>=128,255,0);return Image.fromarray(a)
def midpoint(im):
    b=im.getbbox();return ((b[0]+b[2]-1)/2,(b[1]+b[3]-1)/2)
raw=Image.open(rawpath).convert('RGBA');a=np.array(raw)[:,:,3];xs=np.flatnonzero(np.sum(a>=128,axis=0)>=2);groups=np.split(xs,np.flatnonzero(np.diff(xs)>8)+1);assert len(groups)==5
edges=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(4)]+[raw.width];cuts=[(edges[i],0,edges[i+1],raw.height) for i in range(5)]
cells=[binary(raw.crop(c)) for c in cuts]
observed_order=[1,2,3,4,0] if 'neutral-first' in sys.argv[4:] else [0,1,2,3,4]
cells=[cells[i] for i in observed_order];cuts=[cuts[i] for i in observed_order]
n=cells[-1].getbbox();assert (n[3]-n[1])/(n[2]-n[0])>2.2,'observed ruler must be upright'
scale=r['neutralOccupiedTargetHeight']/(n[3]-n[1])
endpoints=[];endpoint_records=[]
for i,q in enumerate(r['stagedEndpoints']):
    p=ROOT/q['path'];im=Image.open(p).convert('RGBA');assert im.size in [(184,184),(224,208)]
    f=Image.new('RGBA',(224,208));offset=(20,0) if im.width==184 else (0,0);f.paste(im,offset)
    assert f.crop((offset[0],0,offset[0]+im.width,im.height)).tobytes()==im.tobytes()
    name='endpoint-'+('origin' if i==0 else 'destination')+'.png';f.save(O/name);endpoints.append(f)
    endpoint_records.append({'file':name,'source':q,'wholeTranslation':offset,'operations':'Whole unchanged source pixels padded to224x208;184-wide p92 translates20px to p112, no resampling','sha256':sha(O/name)})
centers=[midpoint(im) for im in endpoints];frames=[];records=[]
for i,cell in enumerate(cells):
    dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX));b=dense.getbbox()
    planted=i==4 or (mode=='drain' and i==3) or (mode=='pickup' and i<2)
    if planted:offset=(round(112-(b[0]+b[2]-1)/2),172-b[3]);registration='whole midpoint112/occupied sole172, planted/ruler diagnostic'
    else:
        t=(i+1)/5;target=tuple(centers[0][j]+(centers[1][j]-centers[0][j])*t for j in range(2));source=midpoint(dense)
        offset=tuple(round(target[j]-source[j]) for j in range(2));registration='whole occupied midpoint between exact normalized endpoints, diagnostic not physical-root proof'
    f=Image.new('RGBA',(224,208));f.alpha_composite(dense,offset)
    assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]),'opaque clipping'
    name='ruler.png' if i==4 else f'intermediate-{i+1}.png';f.save(O/name);bb=f.getbbox();frames.append(f)
    records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'registration':registration,'occupiedBounds':bb,'occupiedSize':[bb[2]-bb[0],bb[3]-bb[1]],'sha256':sha(O/name)})
paths=[O/'endpoint-origin.png']+[O/f'intermediate-{i}.png' for i in range(1,5)]+[O/'endpoint-destination.png']
state=r['selectedTransitionState'].copy();assert len(state['frameFiles'])==6 and not state['loop'];state['frameFiles']=['res://'+p.relative_to(ROOT).as_posix() for p in paths]
(O/'manifest.json').write_text(json.dumps({'revision':'marsh-water-'+stem+'-staged','normalAdmission':False,'frameWidth':224,'frameHeight':208,'pivot':[112,172],'standingHeight':148,'textureFilter':'nearest','states':[state]},indent=2)+'\n')
board=Image.new('RGB',(1792,238),'#293b40');d=ImageDraw.Draw(board)
master=Image.open(ROOT/r['selectedIdleMaster']['path']).convert('RGBA')
for i,im in enumerate([endpoints[0]]+frames[:4]+[endpoints[1],frames[4],master]):
    board.paste(im,(224*i+(20 if im.width==184 else 0),25),im);d.text((224*i+4,5),['exact origin','whole1','whole2','whole3','whole4 planted' if mode=='drain' else 'whole4 prone','exact destination','neutral ruler','own master'][i],fill='white')
board.save(O/'whole-transition-comparison.png')
(O/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'generationId':generation,'rawSha256':sha(rawpath),'observedSourceOrder':observed_order,'commonNeutralScale':scale,'neutralOccupiedTargetHeight':r['neutralOccupiedTargetHeight'],'records':records,'endpointRecords':endpoint_records,'operations':'Five unequal whole alpha128cells, one neutral BOX scale/integer whole translations/no opaque clipping/patch/mirror/recolour/perposefit. Exact endpoint pixels only padded/translated for common metadata. Planted pose/root/case contact and perspective require actual world review.'},indent=2)+'\n')
print(json.dumps({'stem':stem,'scale':scale,'sizes':[q['occupiedSize'] for q in records],'slots':6,'durations':state['frameDurationsMs'],'normalAdmission':False}))
