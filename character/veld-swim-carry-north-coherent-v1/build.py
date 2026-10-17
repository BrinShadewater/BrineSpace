"""Deterministic extraction and shared material fit of authored north cargo swim."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation

H=Path(__file__).resolve().parent; R=H.parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def face(a):
    # Bound the complete rear skull; warm silver hardware must not join hair.
    v=a[:,:,:3].astype(float);y,x=np.where(a[:,:,3]>160)
    left,right,top,bottom=x.min(),x.max()+1,y.min(),y.max()+1
    yy,xx=np.indices(a.shape[:2]);width=right-left;height=bottom-top;center=(left+right)*.5
    roi=(yy>=top+height*.09)&(yy<top+height*.245)&(xx>center-width*.23)&(xx<center+width*.23)
    m=roi&(a[:,:,3]>200)&(v[:,:,0]>35)&(v[:,:,0]>v[:,:,1]*1.15)&(v[:,:,1]>v[:,:,2]*1.1)
    assert m.any();return m
def box(m):
    y,x=np.where(m); return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
def masks(a):
    v=a[:,:,:3].astype(float); fb=box(face(a)); y,x=np.indices(a.shape[:2]); h=fb[3]-fb[1]
    w=fb[2]-fb[0]; head=(y>=fb[1]-2)&(y<fb[3]+2)&(x>fb[0]-w*.1)&(x<fb[2]+w*.1); case=(y<fb[1])&(x>fb[0]-w*.25)&(x<fb[2]+w*.25)
    # Protect the held case and the complete head from cloth/patch curves.
    body=(~head)&(~case)&(a[:,:,3]>200)
    return dict(cloth=body&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),patch=body&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35))

rawpath=H/'source-v3.png'; raw=np.array(Image.open(rawpath).convert('RGBA'))
lab,n=label(raw[:,:,3]>160); sizes=np.bincount(lab.ravel())
ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:6]; assert len(ids)==6
ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(raw.shape[0]/2)),np.where(lab==k)[1].mean()))
source_order=[0,1,2,3,4,5]; ids=[ids[i] for i in source_order]
crops=[]; records=[]
for i,k in enumerate(ids):
    b=box(lab==k); b=[b[0]-2,b[1]-2,b[2]+2,b[3]+2]
    assert min(b[:2])>=0 and b[2]<=raw.shape[1] and b[3]<=raw.shape[0],('source clipping',i,b)
    cut=raw.copy(); cut[~binary_dilation(lab==k,iterations=2)]=0
    im=Image.fromarray(cut).crop(b); (H/'source-crops').mkdir(exist_ok=True); im.save(H/f'source-crops/{i:03}.png')
    crops.append(im); records.append(dict(slot=i,sourceAtlasSlot=source_order[i],sourceBox=b,sourceSkullBox=box(face(np.array(im)))))
landmarks=json.loads((H/'head-landmarks-v3.json').read_text())
for record in records:
    mark=landmarks['records'][record['sourceAtlasSlot']]; b=record['sourceBox']; span=mark['hairSpan']; row=mark['hairRow']
    scan=raw[row,span[0]-3:span[1]+3,:3].astype(float); mask=(scan[:,0]>35)&(scan[:,0]<160)&(scan[:,0]>scan[:,1]*1.15)
    xs=np.where(mask)[0]+span[0]-3; assert [int(xs.min()),int(xs.max()+1)]==span
    record['sourceHeadLandmark']=mark;record['sourceSkullBox']=[span[0]-b[0],mark['crown']-b[1],span[1]-b[0],mark['crown']+77-b[1]]
reference=R/'character/veld-water-north-coherent-v1/frames/bare/swim-north/000.png'
ref=np.array(Image.open(reference).convert('RGBA')); rv=ref[:,:,:3].astype(float); rm=masks(ref)
values={k:[] for k in rm}
for im in crops:
    a=np.array(im);v=a[:,:,:3].astype(float)
    for k,m in masks(a).items():values[k].extend(v[m])
q=[0,15,35,55,75,90,100]
curves={k:dict(knots=np.percentile(np.mean(values[k],axis=1),q),targets=np.percentile(rv[rm[k]],q,axis=0)) for k in rm}
# One calibrated anatomical ruler for the entire atlas; never normalize each pose.
scale=landmarks['targetHairWidth']/float(np.median([r['sourceSkullBox'][2]-r['sourceSkullBox'][0] for r in records]))
master=Image.open(R/'character/veld-water-master-audit-v1/fitted-swim-north-head.png').convert('RGBA')
head=master
board=Image.new('RGBA',(1536,600),'#202a30');d=ImageDraw.Draw(board)
images={v:[] for v in ['bare','helmet']}; checks=0
for i,im in enumerate(crops):
    a=np.array(im);v=a[:,:,:3].astype(float);fb=records[i]['sourceSkullBox']
    for key,m in masks(a).items():
        for c in range(3):a[m,c]=np.interp(v[m].mean(1),curves[key]['knots'],curves[key]['targets'][:,c]).clip(0,255).astype('uint8')
    pose=Image.fromarray(a).resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    pos=(round(128-(fb[0]+fb[2])*.5*scale),round(104-fb[1]*scale)); bare=Image.new('RGBA',(256,256));bare.alpha_composite(pose,pos)
    clear=(114,103,142,126); hp=(112,99); helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(head,hp)
    before=np.array(bare); after=np.array(helmet); y,x=np.indices((256,256)); v=before[:,:,:3].astype(float)
    foreground=(before[:,:,3]>200)&(np.ptp(v,axis=2)<28)&(y>=99)&(y<109)&(x>=112)&(x<145); after[foreground]=before[foreground]; helmet=Image.fromarray(after)
    protected=np.ones((256,256),bool);protected[clear[1]:clear[3],clear[0]:clear[2]]=False;protected[hp[1]:hp[1]+head.height,hp[0]:hp[0]+head.width]=False
    assert np.array_equal(np.array(bare)[protected],np.array(helmet)[protected]);checks+=1
    records[i].update(fixedAtlasScale=scale,bodyPosition=pos,helmetPosition=hp,headClear=clear,rearSkullTarget=[128,104],foregroundPixels=int(foreground.sum()))
    for row,(gear,image) in enumerate([('bare',bare),('helmet',helmet)]):
        a=np.array(image);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1
        out=H/f'frames/{gear}/swim-carry-north/{i:03}.png';out.parent.mkdir(parents=True,exist_ok=True);image.save(out);images[gear].append(image)
        board.alpha_composite(image,(i*256,row*300+25));d.text((i*256+5,row*300+5),f'{gear} cargo / {i}',fill='white')
board.save(H/'paired-contact-v1.png')
selection=json.loads((R/'character/veld-water-cargo-master-audit-v1/current-selection.json').read_text())
for gear in images:
    old=selection['records'][gear+'/north']; state=old['state'].copy();state['frameFiles']=[f'frames/{gear}/swim-carry-north/{i:03}.png' for i in range(6)]
    m={**old['profile'],'name':'Veld coherent north water cargo '+gear,'states':[state],'status':'staged_authored_source_pending_motion_and_world_review'}
    (H/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    previews=[]
    for image in images[gear]:
        bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(image);previews.append(bg.convert('RGB'))
    previews[0].save(H/f'{gear}-preview-v1.gif',save_all=True,append_images=previews[1:],duration=state['frameDurationsMs'],loop=0,disposal=2)
(H/'fit-checks.json').write_text(json.dumps(dict(checks=checks,failures=0,installed=False,fixedAtlasScale=scale,reference=reference.relative_to(R).as_posix(),referenceSha256=sha(reference),sourceSha256=sha(rawpath),records=records,curves={k:{kk:vv.tolist() for kk,vv in val.items()} for k,val in curves.items()},scope='Extraction, fixed face ruler, shared material curve, protected body and no canvas clipping; motion and world acceptance separate'),indent=2)+'\n')
print(f'{checks} fit checks PASS; paired north cargo source staged at fixed {scale:.5f} ruler.')
