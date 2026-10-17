"""Fixed-source-ruler north candidate, exact selected entry and pooled grade."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
HEADS=[[254,119],[782,193],[1303,333],[142,739],[568,858],[1097,857]]
DURATIONS=[180,160,180,180,220,500]
IDLE=R/'character/crew-runtime-matte-v1/veld/frames/idle-north-breathing-v1/000.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def regions(a,head):
    rgb=a[:,:,:3].astype(float);solid=a[:,:,3]>200
    warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.20*rgb[:,:,2]);luma=rgb.mean(2)
    blue=solid&(rgb[:,:,2]>1.30*rgb[:,:,0])&(rgb[:,:,2]>1.10*rgb[:,:,1])
    return {'skin':solid&head&warm&(luma>=80),'hair':solid&head&warm&(luma<80),'science':blue,'neutral':solid&~head&~blue&(np.ptp(rgb,axis=2)<45)}
def main():
    source=P/'sources/death-local-kneel-v2.png';raw=np.array(Image.open(source).convert('RGBA'))
    master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(IDLE).convert('RGBA'),(36,52));ref=np.array(master)
    yy,xx=np.indices(raw.shape[:2]);head=np.zeros(raw.shape[:2],bool)
    for hx,hy in HEADS:head|=(xx-hx)**2+(yy-hy)**2<54**2
    ry,rx=np.indices(ref.shape[:2]);rh=(rx>=117)&(rx<144)&(ry>=76)&(ry<104)
    sm=regions(raw,head);rm=regions(ref,rh)
    # Rear authority has shaded ear strips, not a visible frontal face. Select
    # those anatomical pixels explicitly instead of inventing a skin reference
    # from highlights or confusing brown scalp/bun with skin.
    rv=ref[:,:,:3].astype(float);rear_ears=((rx>=116)&(rx<=119)&(ry>=89)&(ry<=94))|((rx>=137)&(rx<=140)&(ry>=89)&(ry<=94))
    rear_ears&=(ref[:,:,3]>160)&(rv[:,:,0]>rv[:,:,1]*1.10)&(rv[:,:,1]>rv[:,:,2]*1.10)
    rm['skin']=rear_ears;rm['hair']&=~rear_ears
    graded=raw.copy();curves={};q=[0,15,35,55,75,90,100]
    for name,mask in sm.items():
        authority=rm[name];assert mask.sum()>30 and authority.sum()>5,(name,int(mask.sum()),int(authority.sum()))
        knots=np.percentile(raw[:,:,:3][mask].mean(1),q);target=np.percentile(ref[:,:,:3][authority],q,axis=0)
        for c in range(3):graded[mask,c]=np.interp(raw[:,:,:3][mask].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')
        curves[name]={'knots':knots.tolist(),'targets':target.tolist(),'sourcePixels':int(mask.sum()),'masterPixels':int(authority.sum()),'authority':'spatial rear-ear strips' if name=='skin' else 'selected rear idle material'}
    geometry=json.loads((P/'source-scale-review.json').read_text());ruler=geometry['fixedRuler']
    labs,n=label(raw[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
    ids=sorted(np.argsort(sizes)[-6:],key=lambda k:(np.where(labs==k)[0].mean()//512,np.where(labs==k)[1].mean()))
    frames=[master];records=[]
    for i in range(1,6):
        record=geometry['records'][i];keep=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0)
        pixels=graded.copy();pixels[~keep]=0;cut=Image.fromarray(pixels).crop(record['box']).resize(tuple(record['size']),Image.Resampling.LANCZOS)
        out=Image.new('RGBA',(256,256));out.alpha_composite(cut,tuple(record['position']));frames.append(out);records.append(record)
    hashes={};files=[]
    for i,frame in enumerate(frames):
        f=P/f'frames/bare/death-ground-north/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);frame.save(f);files.append(f.relative_to(P).as_posix());hashes[files[-1]]=sha(f)
    state={'id':'death-ground-north','frameFiles':files,'frameDurationsMs':DURATIONS,'loop':False,'terminalFrame':5,'facings':['north']*6,'waterPoses':[False]*6,'waterKinds':['death-ground']*6,'depthOffsets':[0]*6}
    manifest={'name':'Veld north dry collapse bare candidate','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'staged_candidate','states':[state]}
    provenance={'source':source.relative_to(P).as_posix(),'sourceSha256':sha(source),'idle':IDLE.relative_to(R).as_posix(),'idleSha256':sha(IDLE),'fixedRuler':ruler,'heads':HEADS,'frames':records,'grade':'one clip-wide curve per material, once before resampling','scope':'bare candidate only; native north helmet and runtime/mortality/world proof pending'}
    for name,data in [('bare-manifest.json',manifest),('bare-frame-hashes.json',hashes),('bare-registration.json',provenance),('material-grade.json',curves)]:
        (P/name).write_text(json.dumps(data,indent=2)+'\n')
    board=Image.new('RGB',(1536,550),'#202a30');draw=ImageDraw.Draw(board)
    for i,frame in enumerate(frames):
        board.paste(frame,(i*256,20),frame);board.paste(master,(i*256,290),master)
        draw.text((i*256+8,3),f'North candidate {i}',fill='white');draw.text((i*256+8,273),'Selected north idle',fill='white')
    board.save(P/'bare-contact-sheet.png')
    gif=[]
    for frame in frames:
        bg=Image.new('RGB',(256,256),'#202a30');bg.paste(frame,(0,0),frame);gif.append(bg)
    gif[0].save(P/'bare-death-review.gif',save_all=True,append_images=gif[1:],duration=DURATIONS,loop=0,disposal=2)
    print(json.dumps({'bareFrames':6,'ruler':ruler,'cycleMs':sum(DURATIONS),'entry':'exact selected idle','normalSelection':False}))
if __name__=='__main__':main()
