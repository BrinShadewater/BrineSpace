from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1]
checks=0;failures=[]
def check(ok,why):
    global checks
    checks+=1
    if not ok:failures.append(why)
def arr(p):return np.array(Image.open(p).convert('RGBA'))
reg=json.loads((P/'registration.json').read_text());hashes=json.loads((P/'frame-hashes.json').read_text())
src=R/'character/james-lying-north-v1'
check(reg['sourceSha256']==hashlib.sha256((src/'source-lying-v6.png').read_bytes()).hexdigest(),'Immutable selected source')
check(reg['helmetSourceSha256']==hashlib.sha256((src/'source-helmet.png').read_bytes()).hexdigest(),'Immutable helmet donors')
states={};old=json.loads((src/'bare-manifest.json').read_text())
for mode in ['bare','helmet']:
    m=json.loads((P/(mode+'-manifest.json')).read_text());states[mode]={s['id']:s for s in m['states']}
    check(m['pivot']==[128,224] and m['standingHeight']==148,'Physical contract '+mode)
    for s in m['states']:
        reference=next(q for q in old['states'] if q['id']==s['id'])
        for field in ['frameDurationsMs','depthOffsets','waterKinds','waterPoses','facings','loop']:
            check(s[field]==reference[field],'Preserved selected '+field+mode+s['id'])
        check(s['provenance']['fixedScale']==reg['fixedScale'],'One source ruler '+mode+s['id'])
        for i,rel in enumerate(s['frameFiles']):
            a=arr(P/rel);check(a.shape==(256,256,4),'Canvas '+rel)
            check(hashlib.sha256((P/rel).read_bytes()).hexdigest()==hashes[rel],'Exact selected hash '+rel)
            check(not np.any(a[[0,-1],:,3]) and not np.any(a[:,[0,-1],3]),'Unclipped '+rel)
            check(np.any(a[:,:,3]==0) and np.any(a[:,:,3]>180),'Genuine alpha '+rel)
    for i in range(6):
        check(np.array_equal(arr(P/states[mode]['lie-down-north']['frameFiles'][i]),arr(P/states[mode]['get-up-north']['frameFiles'][5-i])),'Exact reverse '+mode+str(i))
    neutral=arr(P/states[mode]['sleep-north']['frameFiles'][0])
    check(np.array_equal(neutral,arr(P/states[mode]['lie-down-north']['frameFiles'][-1])),'Exact rest join '+mode)
    check(np.array_equal(neutral,arr(P/states[mode]['sleep-north']['frameFiles'][-1])),'Exact closed breathing loop '+mode)
    check(len({hashlib.sha256((P/f).read_bytes()).hexdigest() for f in states[mode]['sleep-north']['frameFiles']})>=3,'Authored breathing is no longer static '+mode)
    master=Image.new('RGBA',(256,256))
    if mode=='helmet':im=Image.open(src/'selected-helmet-master.png').convert('RGBA')
    else:
        folder=R/'character/crew-runtime-matte-v1/branforth';mm=json.loads((folder/'manifest.json').read_text());s=next(s for s in mm['states'] if s['id']=='idle-north');im=Image.open(folder/s['frameFiles'][0]).convert('RGBA')
    master.alpha_composite(im,(36,52))
    check(np.array_equal(arr(P/states[mode]['lie-down-north']['frameFiles'][0]),np.array(master)),'Exact selected standing master '+mode)
for key,hs in states['helmet'].items():
    bs=states['bare'][key]
    check(hs.get('restHeadOffset')==bs.get('restHeadOffset'),'Paired pillow anchor '+key)
    for i,(hf,bf) in enumerate(zip(hs['frameFiles'],bs['frameFiles'])):
        source_pose=hs['provenance']['sourcePoses'][i]
        if source_pose==0:continue
        x0,y0,x1,y1=reg['helmetTracking'][source_pose]['editRegion'];mask=np.ones((256,256),bool);mask[y0:y1,x0:x1]=False
        check(np.array_equal(arr(P/hf)[mask],arr(P/bf)[mask]),'Owned head edit only '+key+str(i))
sleep=[arr(P/f) for f in states['bare']['sleep-north']['frameFiles']]
bounds=[]
for a in sleep:
    y,x=np.where(a[:,:,3]>180);bounds.append([int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)])
check(max(b[3]-b[1] for b in bounds)-min(b[3]-b[1] for b in bounds)<=1,'Stable sleeping body length')
check(max(b[2]-b[0] for b in bounds)-min(b[2]-b[0] for b in bounds)<=2,'Stable sleeping width')
report=dict(checks=checks,failures=failures,passed=not failures,sleepBounds=bounds,scope='Selected North3-state source/alpha/paired ownership/joins/clock stability; visual anatomy and native berth evidence separate.')
(P/'packaging-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(checks,'package checks;',len(failures),'failures; sleep bounds',bounds)
for f in failures[:10]:print(f)
raise SystemExit(bool(failures))
