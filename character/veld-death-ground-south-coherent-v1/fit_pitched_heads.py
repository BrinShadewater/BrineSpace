"""One upright-calibrated ruler and pooled master grade for authored pitch heads."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def masks(a):
    v=a[:,:,:3].astype(float);solid=a[:,:,3]>200;warm=(v[:,:,0]>1.12*v[:,:,1])&(v[:,:,1]>1.14*v[:,:,2]);l=v.mean(2)
    return {'skin':solid&warm&(l>=80),'hair':solid&warm&(l<80),'neutral':solid&(np.ptp(v,axis=2)<45),'glass':solid&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.05)}
def main():
    source=P/'sources/pitched-heads-v2.png';raw=np.array(Image.open(source).convert('RGBA'));master=np.array(Image.open(R/'character/veld-shared-helmet-south-v1/fitted-helmet.png').convert('RGBA'))
    labs,n=label(raw[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
    ids=sorted(np.argsort(sizes)[-3:],key=lambda k:np.where(labs==k)[1].mean());regions=[]
    for k in ids:
        keep=binary_dilation(labs==k,iterations=5)&(raw[:,:,3]>24);y,x=np.where(keep)
        regions.append((keep,[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]))
    scale=35/(regions[0][1][2]-regions[0][1][0]);graded=raw.copy();curves={};q=[0,15,35,55,75,90,100]
    sm=masks(raw);rm=masks(master)
    for name,mask in sm.items():
        ref=rm[name];assert mask.sum()>30 and ref.sum()>5,name
        knots=np.percentile(raw[:,:,:3][mask].mean(1),q);target=np.percentile(master[:,:,:3][ref],q,axis=0)
        for c in range(3):graded[mask,c]=np.interp(raw[:,:,:3][mask].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')
        curves[name]={'knots':knots.tolist(),'target':target.tolist()}
    records=[];board=Image.new('RGB',(840,480),'#202a30')
    for i,(keep,box) in enumerate(regions):
        a=graded.copy();a[~keep]=0;cut=Image.fromarray(a).crop(box);size=(round(cut.width*scale),round(cut.height*scale));cut=cut.resize(size,Image.Resampling.LANCZOS)
        file=P/f'sources/fitted-pitch-{i:02}.png';cut.save(file);anchor=[size[0]/2,size[1]-3]
        records.append({'sourceBox':box,'size':list(size),'anchor':anchor,'file':file.relative_to(P).as_posix(),'sha256':sha(file),'pitchDegrees':[0,15,25][i]})
        enlarged=cut.resize((size[0]*6,size[1]*6),Image.Resampling.NEAREST);board.paste(enlarged,(i*280,200),enlarged)
    board.save(P/'sources/pitched-native-comparison.png')
    data={'generation':'exec-80f14b1a-e3b4-4b7c-be2b-3a8bb48473ad','source':source.relative_to(P).as_posix(),'sourceSha256':sha(source),'fixedRuler':scale,'calibration':'35pixel selected master width / generated upright full component width; no per-angle size normalization','heads':records,'materialCurves':curves,'scope':'authored15/25depth-pitch heads for helmet frames1/2; original master0 and other poses protected'}
    (P/'pitch-registration.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({'fixedRuler':scale,'componentSizes':[r['size'] for r in records]}))
if __name__=='__main__':main()
