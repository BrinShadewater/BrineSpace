"""Compose paired west water family from authored sources and exact native helmets."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
from build_loop_trials import curves,masks,face_box,master,targetFaceHeight

H=Path(__file__).resolve().parent;R=H.parents[1];cov=json.loads((R/'character/veld-consistency-audit-v2/coverage.json').read_text())
source=H/'transition-source-v1.png';a=np.array(Image.open(source).convert('RGBA'));lab,n=label(a[:,:,3]>160);sizes=np.bincount(lab.ravel());ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:4];ids.sort(key=lambda k:np.where(lab==k)[1].mean());assert len(ids)==4
crops=[]
for k in ids:
    y,x=np.where(lab==k);box=[int(x.min())-2,int(y.min())-2,int(x.max())+3,int(y.max())+3];assert box[0]>=0 and box[1]>=0 and box[2]<=a.shape[1] and box[3]<=a.shape[0]
    cut=a.copy();cut[~binary_dilation(lab==k,iterations=2)]=0;raw=Image.fromarray(cut).crop(box);crops.append((raw,box,face_box(np.array(raw))))
scale=targetFaceHeight/float(np.median([fb[3]-fb[1] for _,_,fb in crops]));records=[];checks=0
rows={v:{kind+'-west':[Image.open(H/f'loop-trials/{v}/{kind}/{i:03}.png').convert('RGBA') for i in range(6)] for kind in ['tread','swim']} for v in ['bare','helmet']}
launch={v:[rows[v]['tread-west'][0]] for v in rows}
for i,(raw,box,fb) in enumerate(crops):
    a=np.array(raw);v=a[:,:,:3].astype(float);originalGrade=a.copy();materialMasks=masks(a);gradedSupport=np.logical_or.reduce(list(materialMasks.values()))
    for key,m in materialMasks.items():
        for c in range(3):a[m,c]=np.interp(v[m].mean(1),curves[key]['knots'],curves[key]['targets'][:,c]).clip(0,255).astype('uint8')
    assert np.array_equal(a[:,:,3],originalGrade[:,:,3]);checks+=1
    assert np.array_equal(a[~gradedSupport],originalGrade[~gradedSupport]);checks+=1
    pose=Image.fromarray(a).resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS);faceLeft=[116,111,106,101][i];faceBottom=128 if i<2 else 127
    pos=(round(faceLeft-fb[0]*scale),round(faceBottom-fb[3]*scale));bare=Image.new('RGBA',(256,256));bare.alpha_composite(pose,pos)
    head=master.rotate([4,8,12,16][i],resample=Image.Resampling.BICUBIC,expand=True);hfb=face_box(np.array(head));headPos=(faceLeft-hfb[0],faceBottom-hfb[3]);clear=(faceLeft-2,faceBottom-34,faceLeft+34,faceBottom+1)
    helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(head,headPos);before=np.array(bare);after=np.array(helmet);protected=np.ones(before.shape[:2],bool);protected[clear[1]:clear[3],clear[0]:clear[2]]=False;protected[headPos[1]:headPos[1]+head.height,headPos[0]:headPos[0]+head.width]=False;assert np.array_equal(before[protected],after[protected]);checks+=1
    for variant,image in [('bare',bare),('helmet',helmet)]:launch[variant].append(image)
    records.append({'slot':i+1,'sourceBox':box,'sourceFaceBox':fb,'fixedAtlasScale':scale,'bodyPosition':pos,'headPosition':headPos,'clear':clear,'tiltDegrees':[-4,-8,-12,-16][i]})
for variant in rows:
    launch[variant].append(rows[variant]['swim-west'][0]);rows[variant]['swim-start-west']=launch[variant];rows[variant]['swim-stop-west']=list(reversed(launch[variant]));states=[]
    for key,images in rows[variant].items():
        selected=cov['selected'][variant][key];old=json.loads((R/selected['manifest']).read_text());state=next(s for s in old['states'] if s['id']==key).copy();files=[]
        for i,image in enumerate(images):
            ar=np.array(image);assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1
            file=f'frames/{variant}/{key}/{i:03}.png';(H/file).parent.mkdir(parents=True,exist_ok=True);image.save(H/file);files.append(file)
        state['frameFiles']=files;states.append(state)
    manifest={**old,'name':'Veld coherent west water '+variant,'frameWidth':256,'frameHeight':256,'pivot':[128,128],'states':states,'status':'staged_coherent_body_pending_visual_acceptance'}
    (H/f'{variant}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
board=Image.new('RGBA',(1536,560),'#202a30');draw=ImageDraw.Draw(board)
for row,variant in enumerate(rows):
    for i,image in enumerate(launch[variant]):board.alpha_composite(image,(i*256,row*280+24));draw.text((i*256+4,row*280+4),variant+' start / '+str(i),fill='white')
board.save(H/'paired-launch-v1.png')
(H/'family-fit-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'installed':False,'transitionFixedScale':scale,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'records':records},indent=2)+'\n');print(f'{checks} transition support/family border checks PASS;8 paired states/48 frames staged.')
