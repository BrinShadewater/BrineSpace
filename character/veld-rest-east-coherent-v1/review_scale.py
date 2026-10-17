"""Unselected source geometry review at one standing-derived anatomical ruler."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
def main():
    source=P/'sources/rest-v1.png';im=Image.open(source).convert('RGBA');a=np.array(im)
    labs,n=label(a[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
    ids=sorted(np.argsort(sizes)[-6:],key=lambda k:(np.where(labs==k)[0].mean()//512,np.where(labs==k)[1].mean()))
    y,x=np.where(labs==ids[0]);ruler=148/(int(y.max()-y.min())+1)
    contact_x=[229,699,1160,221,769,1280];target_x=[130,130,130,130,130,130]
    frames=[];records=[]
    for i,k in enumerate(ids):
        y,x=np.where(labs==k);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
        keep=binary_dilation(labs==k,iterations=3)&(a[:,:,3]>0);cut=a.copy();cut[~keep]=0
        cropped=Image.fromarray(cut).crop(box);cropped=cropped.resize((round(cropped.width*ruler),round(cropped.height*ruler)),Image.Resampling.LANCZOS)
        position=[round(target_x[i]-(contact_x[i]-box[0])*ruler),round(223-(y.max()-box[1])*ruler)]
        out=Image.new('RGBA',(256,256));out.alpha_composite(cropped,position);frames.append(out)
        records.append({'pose':i,'box':box,'position':position,'size':list(cropped.size),'sourceFloorY':int(y.max()),'floorTarget':223})
    master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png').convert('RGBA'),(36,52))
    board=Image.new('RGB',(1792,310),'#202a30');draw=ImageDraw.Draw(board)
    for i,frame in enumerate([master]+frames):
        board.paste(frame,(i*256,24),frame);draw.text((i*256+8,4),'Selected master' if i==0 else f'Raw pose{i-1} — ungraded',fill='white')
    board.save(P/'source-scale-review.png')
    data={'source':source.relative_to(P).as_posix(),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'fixedRuler':ruler,'standingOpaqueHeight':int(np.where(labs==ids[0])[0].max()-np.where(labs==ids[0])[0].min()+1),'masterStandingHeight':148,'records':records,'status':'unselected geometry diagnostic; opaque height alone does not establish anatomical matching','pending':'compare crown/chin/neck/waist/knee construction visually; grade and native helmet not fitted'}
    (P/'source-scale-review.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'ruler':ruler,'poses':len(frames),'diagnosticOnly':True}))
if __name__=='__main__':main()

