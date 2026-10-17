"""Extract authored poses and compare fixed family scales against selected idle."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation

H=Path(__file__).resolve().parent;R=H.parents[1]
cov=json.loads((R/'character/veld-consistency-audit-v2/coverage.json').read_text())
reference=R/cov['selected']['bare']['idle-west']['files'][0]
ref=Image.open(reference).convert('RGBA')
def face_mask(a):
    v=a[:,:,:3].astype(float)
    m=(a[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>v[:,:,1]*1.25)&(v[:,:,1]>v[:,:,2]*1.12)
    lab,n=label(m);counts=np.bincount(lab.ravel())
    assert n>0
    return lab==(1+np.argmax(counts[1:]))
def face_box(a):
    y,x=np.where(face_mask(a));return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
if __name__ == '__main__':
    records=[]
    for kind in ['tread','swim']:
        source=H/f'{kind}-source-v1.png'
        if not source.exists():continue
        a=np.array(Image.open(source).convert('RGBA'));lab,n=label(a[:,:,3]>160);sizes=np.bincount(lab.ravel())
        ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:6]
        assert len(ids)==6
        rows=2 if kind=='tread' else 3
        ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(a.shape[0]/rows)),np.where(lab==k)[1].mean()))
        for i,k in enumerate(ids):
            y,x=np.where(lab==k);box=[int(x.min())-2,int(y.min())-2,int(x.max())+3,int(y.max())+3]
            assert box[0]>=0 and box[1]>=0 and box[2]<=a.shape[1] and box[3]<=a.shape[0]
            cut=a.copy();cut[~binary_dilation(lab==k,iterations=2)]=0
            im=Image.fromarray(cut).crop(box);p=H/f'source-crops/{kind}/{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
            records.append({'kind':kind,'slot':i,'sourceBox':box,'faceBox':face_box(np.array(im)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
    board=Image.new('RGBA',(1200,840),'#202a30');draw=ImageDraw.Draw(board)
    for row,kind in enumerate(['tread','swim']):
        if not (H/f'source-crops/{kind}/000.png').exists():continue
        im=Image.open(H/f'source-crops/{kind}/000.png').convert('RGBA');fb=face_box(np.array(im))
        board.alpha_composite(ref,(30,row*420+35));draw.text((20,row*420+8),'selected idle at native148 standing height',fill='white')
        for col,scale in enumerate([.20,.22,.24,.26]):
            pose=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
            # Face bottom aligned across the trial row. Scale remains uniform per atlas.
            position=(round(300+col*220-fb[0]*scale),round(row*420+140-fb[3]*scale))
            board.alpha_composite(pose,position);draw.text((230+col*220,row*420+8),kind+' scale '+str(scale),fill='white')
    board.save(H/'physical-scale-trials-v1.png')
    (H/'source-fit-inventory.json').write_text(json.dumps({'selectedFaceBox':face_box(np.array(ref)),'selectedReference':reference.relative_to(R).as_posix(),'records':records,'status':'source crops and physical scale trials; no manifest or runtime selection'},indent=2)+'\n')
    print(f'{len(records)} source crops; selected face box {face_box(np.array(ref))}; trial board saved.')
