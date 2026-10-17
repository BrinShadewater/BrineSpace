"""Fit independently authored shell pitch views at one measured physical scale."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'sources/helmet-pitch-v1.png'
SCALE=.07
def main():
    raw=np.array(Image.open(SOURCE).convert('RGBA'));rgb=raw[:,:,:3].astype(float);labs,n=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
    ids=sorted(np.argsort(counts)[-4:],key=lambda k:(np.where(labs==k)[0].min()//512,np.where(labs==k)[1].min()))
    ref=np.array(Image.open(HERE.parent/'bill-cargo-helmet-south-v1/sources/canonical-head.png').convert('RGBA'));r=ref[:,:,:3].astype(float)
    neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<20);target=(ref[:,:,3]>200)&(np.ptp(r,axis=2)<20)
    q=[0,.05,.2,.4,.5,.7,.85,.95,1];src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(r.mean(2)[target],q)
    weight=np.clip((20-np.ptp(rgb,axis=2))/12,0,1)*(raw[:,:,3]>0);mapped=np.interp(rgb.mean(2),src,dst)
    graded=raw.copy();graded[:,:,:3]=np.clip(rgb*(1-weight[:,:,None])+mapped[:,:,None]*weight[:,:,None],0,255).astype('uint8')
    records=[];(HERE/'components').mkdir(exist_ok=True)
    for i,k in enumerate(ids):
        mask=binary_dilation(labs==k,iterations=3)&(raw[:,:,3]>0);y,x=np.where(mask);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
        pix=graded.copy();pix[~mask]=0;im=Image.fromarray(pix).crop(box);im=im.resize((round(im.width*SCALE),round(im.height*SCALE)),Image.Resampling.LANCZOS)
        path=HERE/'components'/f'{i:03}.png';im.save(path);records.append({'file':path.relative_to(HERE).as_posix(),'sourceBox':box,'scale':SCALE,'pitchDegrees':[0,35,65,85][i],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'nativeSize':list(im.size)})
    (HERE/'component-registration.json').write_text(json.dumps({'source':'sources/helmet-pitch-v1.png','sourceGeneration':'exec-0b0bbcab-d200-476b-a1fc-eefd5cf0d38e','sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'scale':SCALE,'scope':'fixed physical shell width about32px;upright generated candidate unused in runtime','neutralInput':src.tolist(),'neutralOutput':dst.tolist(),'components':records},indent=2)+'\n',encoding='utf-8')
    print('Four shell pitch components:fixed.07 scale and atlas neutral grade')
if __name__=='__main__':main()
