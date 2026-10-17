"""Pair one faithful whole-pose transition key; not a complete start/stop clip."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2]
bare=Image.open(P/'transition-candidate.png').convert('RGBA');a=np.array(bare)
shellpath=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/005.png';shell=Image.open(shellpath).convert('RGBA')
y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];_,sx=np.where(np.array(shell)[-4:,:,3]>160)
pos=(round((hx.min()+hx.max())/2-(sx.min()+sx.max())/2),top+28-shell.height);clear=(int(hx.min())-3,top,int(hx.max())+4,top+27)
helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos)
protected=np.ones((256,256),bool);protected[min(top,pos[1]):max(clear[3],pos[1]+shell.height),min(pos[0],clear[0]):max(clear[2],pos[0]+shell.width)]=False
assert np.array_equal(np.array(helmet)[protected],a[protected]);checks=1
paths=[P/'raw-small-clearance-v1.png',P/'prompt.txt',P/'audit_source.py',P/'source-audit.json',P/'transition-candidate.png',Path(__file__),shellpath]
for gear,im in [('bare',bare),('helmet',helmet)]:
    path=P/f'frames/{gear}/000.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path);paths.append(path)
    z=np.array(im);assert not np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20);checks+=1
    data=json.loads((P.parent/'continuous-video-v3-white'/f'{gear}-source-manifest.json').read_text(encoding='utf-8'))
    state=copy.deepcopy(data['states'][0]);state.update(id='carry-trailing-recovery-key-east',frameCount=1,frameFiles=['res://'+path.relative_to(R).as_posix()],frameDurationsMs=[320],loop=False)
    for key,val in [('facings','east'),('waterKinds','carry'),('waterPoses',False),('depthOffsets',0.0)]:state[key]=[val]
    data.update(name='Veld East independent whole transition KEY '+gear,status='single_source_key_review_only',strideDistanceCells={},states=[state]+data['states'][1:])
    manifest=P/f'{gear}-source-manifest.json';manifest.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');paths.append(manifest)
    for state in data['states'][1:]:paths.extend(R/ref[6:] for ref in state['frameFiles'])
record={'generationId':'a92ca06b-d33b-48db-81af-c3af120fbed6','checks':checks,'failures':0,'helmetPosition':list(pos),'protectedBodyExact':True,'actualPose':'Rear/trailing boot airborne behind forward support boot. Requested tiny FAR forward lift failed; retain as alternative trailing recovery source, not forward first-lift or toe-contact proof. Near/far anatomical identity and support/root calibration pending.','registration':'Whole source height148/head26/upperbody42 matches held148/26/42; cloth68,67,66vs66,64,63 slightly lighter. Forward support foot has moved relative to head, physical root/contact calibration and final fidelity pending.','bindings':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))},'scope':'ONE independent whole-source transition key, paired original equipment only. No invented intermediate frames, full start/stop, gait/stride/contact or normal runtime integration acceptance.'}
(P/'key-record.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:record[k] for k in ['checks','failures','helmetPosition','protectedBodyExact','actualPose']}))
