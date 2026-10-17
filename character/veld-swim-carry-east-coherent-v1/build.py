"""Deterministic extraction and shared material fit of authored east cargo swim."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation

H=Path(__file__).resolve().parent; R=H.parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def face(a):
    v=a[:,:,:3].astype(float)
    m=(a[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>v[:,:,1]*1.25)&(v[:,:,1]>v[:,:,2]*1.12)
    lab,n=label(m); sizes=np.bincount(lab.ravel()); assert n
    return lab==(1+np.argmax(sizes[1:]))
def box(m):
    y,x=np.where(m); return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
def masks(a):
    v=a[:,:,:3].astype(float); fb=box(face(a)); y,x=np.indices(a.shape[:2]); h=fb[3]-fb[1]
    head=(y<fb[3])&(x>fb[0]-h*1.15)&(x<fb[2]+h*.12)
    # Protect the held case and the complete head from cloth/patch curves.
    body=(~head)&(x<fb[2])&(a[:,:,3]>200)
    return dict(skin=face(a),cloth=body&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),patch=body&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35))

rawpath=H/'source-v2.png'; raw=np.array(Image.open(rawpath).convert('RGBA'))
lab,n=label(raw[:,:,3]>160); sizes=np.bincount(lab.ravel())
ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:6]; assert len(ids)==6
ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(raw.shape[0]/3)),np.where(lab==k)[1].mean()))
crops=[]; records=[]
for i,k in enumerate(ids):
    b=box(lab==k); b=[b[0]-2,b[1]-2,b[2]+2,b[3]+2]
    assert min(b[:2])>=0 and b[2]<=raw.shape[1] and b[3]<=raw.shape[0],('source clipping',i,b)
    cut=raw.copy(); cut[~binary_dilation(lab==k,iterations=2)]=0
    im=Image.fromarray(cut).crop(b); (H/'source-crops').mkdir(exist_ok=True); im.save(H/f'source-crops/{i:03}.png')
    crops.append(im); records.append(dict(slot=i,sourceBox=b,sourceFaceBox=box(face(np.array(im)))))
reference=R/'character/veld-water-east-coherent-v1/frames/bare/swim-east/000.png'
ref=np.array(Image.open(reference).convert('RGBA')); rv=ref[:,:,:3].astype(float); rm=masks(ref)
values={k:[] for k in rm}
for im in crops:
    a=np.array(im);v=a[:,:,:3].astype(float)
    for k,m in masks(a).items():values[k].extend(v[m])
q=[0,15,35,55,75,90,100]
curves={k:dict(knots=np.percentile(np.mean(values[k],axis=1),q),targets=np.percentile(rv[rm[k]],q,axis=0)) for k in rm}
# One calibrated anatomical ruler for the entire atlas; never normalize each pose.
scale=(box(face(ref))[3]-box(face(ref))[1])/float(np.median([r['sourceFaceBox'][3]-r['sourceFaceBox'][1] for r in records]))
master=Image.open(R/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png').convert('RGBA').crop((82,17,116,55))
head=master.rotate(-16,resample=Image.Resampling.BICUBIC,expand=True); hfb=box(face(np.array(head)))
board=Image.new('RGBA',(1536,600),'#202a30');d=ImageDraw.Draw(board)
images={v:[] for v in ['bare','helmet']}; checks=0
for i,im in enumerate(crops):
    a=np.array(im);v=a[:,:,:3].astype(float);fb=records[i]['sourceFaceBox']
    for key,m in masks(a).items():
        for c in range(3):a[m,c]=np.interp(v[m].mean(1),curves[key]['knots'],curves[key]['targets'][:,c]).clip(0,255).astype('uint8')
    pose=Image.fromarray(a).resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    pos=(round(159-fb[2]*scale),round(127-fb[3]*scale)); bare=Image.new('RGBA',(256,256));bare.alpha_composite(pose,pos)
    clear=(125,93,161,128); hp=(159-hfb[2],127-hfb[3]); helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(head,hp)
    protected=np.ones((256,256),bool);protected[clear[1]:clear[3],clear[0]:clear[2]]=False;protected[hp[1]:hp[1]+head.height,hp[0]:hp[0]+head.width]=False
    assert np.array_equal(np.array(bare)[protected],np.array(helmet)[protected]);checks+=1
    records[i].update(fixedAtlasScale=scale,bodyPosition=pos,helmetPosition=hp,headClear=clear,faceTarget=[159,127])
    for row,(gear,image) in enumerate([('bare',bare),('helmet',helmet)]):
        a=np.array(image);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1
        out=H/f'frames/{gear}/swim-carry-east/{i:03}.png';out.parent.mkdir(parents=True,exist_ok=True);image.save(out);images[gear].append(image)
        board.alpha_composite(image,(i*256,row*300+25));d.text((i*256+5,row*300+5),f'{gear} cargo / {i}',fill='white')
board.save(H/'paired-contact-v1.png')
selection=json.loads((R/'character/veld-water-cargo-master-audit-v1/current-selection.json').read_text())
for gear in images:
    old=selection['records'][gear+'/east']; state=old['state'].copy();state['frameFiles']=[f'frames/{gear}/swim-carry-east/{i:03}.png' for i in range(6)]
    m={**old['profile'],'name':'Veld coherent east water cargo '+gear,'states':[state],'status':'staged_authored_source_pending_motion_and_world_review'}
    (H/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    previews=[]
    for image in images[gear]:
        bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(image);previews.append(bg.convert('RGB'))
    previews[0].save(H/f'{gear}-preview-v1.gif',save_all=True,append_images=previews[1:],duration=state['frameDurationsMs'],loop=0,disposal=2)
(H/'fit-checks.json').write_text(json.dumps(dict(checks=checks,failures=0,installed=False,fixedAtlasScale=scale,reference=reference.relative_to(R).as_posix(),referenceSha256=sha(reference),sourceSha256=sha(rawpath),records=records,curves={k:{kk:vv.tolist() for kk,vv in val.items()} for k,val in curves.items()},scope='Extraction, fixed face ruler, shared material curve, protected body and no canvas clipping; motion and world acceptance separate'),indent=2)+'\n')
print(f'{checks} fit checks PASS; paired east cargo source staged at fixed {scale:.5f} ruler.')
