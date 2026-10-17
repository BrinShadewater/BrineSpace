"""Fixed-source-ruler east candidate, exact selected entry and pooled grade."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
HEADS=[[215,113],[765,311],[1135,346],[99,778],[577,871],[1089,872]]
DURATIONS=[240,260,320,360,360,300]
IDLE=R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def regions(a,head):
    rgb=a[:,:,:3].astype(float);solid=a[:,:,3]>200
    warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.20*rgb[:,:,2]);luma=rgb.mean(2)
    blue=solid&(rgb[:,:,2]>1.30*rgb[:,:,0])&(rgb[:,:,2]>1.10*rgb[:,:,1])
    return {'skin':solid&head&warm&(luma>=80),'hair':solid&head&warm&(luma<80),'science':blue,'neutral':solid&~head&~blue&(np.ptp(rgb,axis=2)<45)}
def main():
    source=P/'sources/rest-v1.png';raw=np.array(Image.open(source).convert('RGBA'))
    master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(IDLE).convert('RGBA'),(36,52));ref=np.array(master)
    yy,xx=np.indices(raw.shape[:2]);head=np.zeros(raw.shape[:2],bool)
    for hx,hy in HEADS:head|=(xx-hx)**2+(yy-hy)**2<54**2
    ry,rx=np.indices(ref.shape[:2]);rh=(rx>=117)&(rx<155)&(ry>=74)&(ry<106)
    sm=regions(raw,head);rm=regions(ref,rh)
    # Anatomical face windows keep bright brown hair out of the skin curve.
    polygons=[[(219,106),(244,111),(253,126),(245,147),(223,153),(208,141),(209,125)],[(771,301),(800,305),(817,321),(802,357),(780,361),(754,346),(750,326)],[(1137,337),(1164,338),(1180,355),(1165,376),(1149,386),(1124,373),(1121,354)],[(103,763),(124,765),(143,786),(132,802),(110,813),(88,798),(89,780)],[(563,856),(579,841),(604,847),(622,865),(606,883),(581,890),(564,879)],[(1071,858),(1087,843),(1112,849),(1130,867),(1114,885),(1089,892),(1072,881)]]
    face_image=Image.new('1',(raw.shape[1],raw.shape[0]));fd=ImageDraw.Draw(face_image)
    for polygon in polygons:fd.polygon(polygon,fill=1)
    warm=sm['skin']|sm['hair'];face=np.array(face_image,dtype=bool)
    sm['skin']=warm&face;sm['hair']=warm&~face
    rwarm=rm['skin']|rm['hair'];rface=(rx>=138)&(ry>=84)&(ry<=104)
    rm['skin']=rwarm&rface;rm['hair']=rwarm&~rface
    graded=raw.copy();curves={};q=[0,15,35,55,75,90,100]
    for name,mask in sm.items():
        authority=rm[name];assert mask.sum()>30 and authority.sum()>5,(name,int(mask.sum()),int(authority.sum()))
        knots=np.percentile(raw[:,:,:3][mask].mean(1),q);target=np.percentile(ref[:,:,:3][authority],q,axis=0)
        for c in range(3):graded[mask,c]=np.interp(raw[:,:,:3][mask].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')
        curves[name]={'knots':knots.tolist(),'targets':target.tolist(),'sourcePixels':int(mask.sum()),'masterPixels':int(authority.sum()),'classification':'spatial face/hair, pooled material palette'}
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
        f=P/f'frames/bare/lie-down-east/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);frame.save(f);files.append(f.relative_to(P).as_posix());hashes[files[-1]]=sha(f)
    state={'id':'lie-down-east','frameFiles':files,'frameDurationsMs':DURATIONS,'loop':False,'terminalFrame':5,'facings':['east']*6,'waterPoses':[False]*6,'waterKinds':['rest']*6,'depthOffsets':[0]*6}
    manifest={'name':'Veld east generic rest bare candidate','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'staged_candidate','states':[state]}
    # Reverse the same authored lowering path; sleep holds the closed-eye endpoint.
    rise=dict(state,id='get-up-east',frameFiles=list(reversed(files)),frameDurationsMs=list(reversed(DURATIONS)))
    sleep={'id':'sleep-east','frameFiles':[files[-1]],'frameDurationsMs':[1000],'loop':True,'facings':['east'],'waterPoses':[False],'waterKinds':['rest'],'depthOffsets':[0]}
    manifest['states']=[state,rise,sleep]
    provenance={'source':source.relative_to(P).as_posix(),'sourceSha256':sha(source),'idle':IDLE.relative_to(R).as_posix(),'idleSha256':sha(IDLE),'fixedRuler':ruler,'heads':HEADS,'facePolygons':polygons,'frames':records,'grade':'one clip-wide curve per material, once before resampling','scope':'bare generic floor rest candidate; canonical helmet, native/world/rest-head contact and interrupted death proof pending; accepted bunk unchanged'}
    for name,data in [('bare-manifest.json',manifest),('bare-frame-hashes.json',hashes),('bare-registration.json',provenance),('material-grade.json',curves)]:
        (P/name).write_text(json.dumps(data,indent=2)+'\n')
    board=Image.new('RGB',(1536,550),'#202a30');draw=ImageDraw.Draw(board)
    for i,frame in enumerate(frames):
        board.paste(frame,(i*256,20),frame);board.paste(master,(i*256,290),master)
        draw.text((i*256+8,3),f'East rest {i}',fill='white');draw.text((i*256+8,273),'Selected east idle',fill='white')
    board.save(P/'bare-contact-sheet.png')
    gif=[]
    for frame in frames:
        bg=Image.new('RGB',(256,256),'#202a30');bg.paste(frame,(0,0),frame);gif.append(bg)
    gif[0].save(P/'bare-rest-review.gif',save_all=True,append_images=gif[1:],duration=DURATIONS,loop=0,disposal=2)
    print(json.dumps({'bareFrames':6,'ruler':ruler,'cycleMs':sum(DURATIONS),'entry':'exact selected idle','normalSelection':False}))
if __name__=='__main__':main()



