"""Registered paired source trials; no runtime or aggregate selection changes."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label
from fit_body_trials import face_mask, face_box

H=Path(__file__).resolve().parent;R=H.parents[1]
inventory=json.loads((H/'source-fit-inventory.json').read_text());ref=np.array(Image.open(R/inventory['selectedReference']).convert('RGBA'));rv=ref[:,:,:3].astype(float)
def masks(a):
    v=a[:,:,:3].astype(float)
    fb=face_box(a); Y,X=np.indices(a.shape[:2]);height=fb[3]-fb[1]
    head=(Y<fb[3])&(X>fb[0]-height*.12)&(X<fb[2]+height*1.15)
    return {'skin':face_mask(a),'cloth':~head&(a[:,:,3]>200)&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),'patch':~head&(a[:,:,3]>200)&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35)}
rm=masks(ref);rm['cloth'][:59]=False; values={k:[] for k in rm}
for record in inventory['records']:
    a=np.array(Image.open(H/f"source-crops/{record['kind']}/{record['slot']:03}.png"));v=a[:,:,:3].astype(float)
    for k,m in masks(a).items():values[k].extend(v[m])
q=[0,15,35,55,75,90,100]
curves={k:{'knots':np.percentile(np.mean(values[k],axis=1),q),'targets':np.percentile(rv[rm[k]],q,axis=0)} for k in rm}
targetFaceHeight=face_box(ref)[3]-face_box(ref)[1]
scales={kind:targetFaceHeight/float(np.median([r['faceBox'][3]-r['faceBox'][1] for r in inventory['records'] if r['kind']==kind])) for kind in ['tread','swim']}
master=Image.open(R/'character/veld-shared-helmet-v1/fitted-west.png').convert('RGBA')
records=[];checks=0;board=Image.new('RGBA',(1536,1120),'#202a30');draw=ImageDraw.Draw(board)
for kind in ['tread','swim']:
    # Native master source resampled once for the inherited accepted16degree side swim camera.
    head=master if kind=='tread' else master.rotate(16,resample=Image.Resampling.BICUBIC,expand=True)
    hfb=face_box(np.array(head));scale=scales[kind]
    for i in range(6):
        raw=Image.open(H/f'source-crops/{kind}/{i:03}.png').convert('RGBA');a=np.array(raw);v=a[:,:,:3].astype(float);fb=face_box(a); originalGrade=a.copy(); materialMasks=masks(a); gradedSupport=np.logical_or.reduce(list(materialMasks.values()))
        for k,m in materialMasks.items():
            for c in range(3):a[m,c]=np.interp(v[m].mean(1),curves[k]['knots'],curves[k]['targets'][:,c]).clip(0,255).astype('uint8')
        assert np.array_equal(a[:,:,3],originalGrade[:,:,3]);checks+=1
        assert np.array_equal(a[~gradedSupport],originalGrade[~gradedSupport]);checks+=1
        pose=Image.fromarray(a).resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS)
        faceLeft,faceBottom=(120,128) if kind=='tread' else (97,127)
        pos=(round(faceLeft-fb[0]*scale),round(faceBottom-fb[3]*scale));bare=Image.new('RGBA',(256,256));bare.alpha_composite(pose,pos)
        headPos=(faceLeft-hfb[0],faceBottom-hfb[3]);clear=(faceLeft-2,faceBottom-34,faceLeft+34,faceBottom+1)
        helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(head,headPos)
        before=np.array(bare);after=np.array(helmet);protected=np.ones(before.shape[:2],bool);protected[clear[1]:clear[3],clear[0]:clear[2]]=False
        protected[headPos[1]:headPos[1]+head.height,headPos[0]:headPos[0]+head.width]=False
        assert np.array_equal(before[protected],after[protected]);checks+=1
        for variant,image in [('bare',bare),('helmet',helmet)]:
            ar=np.array(image);assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1
            p=H/f'loop-trials/{variant}/{kind}/{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);image.save(p)
            row=(0 if kind=='tread' else 2)+(variant=='helmet');board.alpha_composite(image,(i*256,row*280+24));draw.text((i*256+4,row*280+4),variant+' '+kind+' / '+str(i),fill='white')
        records.append({'kind':kind,'slot':i,'scale':scale,'bodyPosition':pos,'sourceFaceBox':fb,'headPosition':headPos,'clear':clear,'faceTarget':[faceLeft,faceBottom]})
board.save(H/'paired-loop-trials-v1.png')
(H/'loop-trial-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'selected':False,'scales':scales,'records':records,'curves':{k:{kk:vv.tolist() for kk,vv in value.items()} for k,value in curves.items()},'scope':'24 registered paired loop trials; body support/alpha-border checks, fixed per-atlas face scale, shared material curves; source motion and helmet fit need review'},indent=2)+'\n')
print(f'{checks} paired protected-body/border checks PASS.24 trial frames; no aggregate selection changed.')
