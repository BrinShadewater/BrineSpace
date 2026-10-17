"""One pooled master material calibration and unchanged native helmet component."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
original=json.loads((R/'character/veld-carry-west-consistent-v1/original-selection.json').read_text(encoding='utf-8'))
frames=[np.array(Image.open(P/f'v2-study/study-frames/{i:03}.png').convert('RGBA')) for i in range(6)]
master=np.array(Image.open(R/'character/veld-side-foundation-v1/west-standing.png').convert('RGBA'))
def cloth(a,head_end):
    rgb=a[:,:,:3].astype(float)
    m=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>15)&(rgb.mean(2)<125)
    m[:head_end]=False
    if a.shape[0]==256:m[107:157,:128]=False # Case/near hands are protected.
    return m
ref_rgb=master[:,:,:3].astype(float)
target=ref_rgb[cloth(master,55)]
samples=np.concatenate([a[:,:,:3][cloth(a,107)].mean(1) for a in frames])
knots=np.percentile(samples,[0,15,35,55,75,90,100]);values=np.percentile(target,[0,15,35,55,75,90,100],axis=0)
assert np.all(np.diff(knots)>0)
def head_materials(a,end):
    rgb=a[:,:,:3].astype(float);warm=(a[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15)
    warm[end:]=False
    return {'skin':warm&(rgb.mean(2)>85),'hair':warm&(rgb.mean(2)<=85)}
reference_masks=head_materials(master,55)
offsets={}
for material in ['skin','hair']:
    pool=np.concatenate([a[:,:,:3][head_materials(a,102)[material]] for a in frames])
    reference=ref_rgb[reference_masks[material]]
    assert len(pool)>20 and len(reference)>10,material
    offsets[material]=np.clip(np.median(reference,axis=0)-np.median(pool,axis=0),-8,8)
headpath=R/'character/veld-shared-helmet-v1/frames/idle-west/000.png'
helmet_component=Image.open(headpath).convert('RGBA').crop((64,14,108,60))
bare=[];helmet=[];fits=[]
for i,a in enumerate(frames):
    rgb=a[:,:,:3].astype(float);m=cloth(a,107)
    masks=head_materials(a,102)
    for c in range(3):a[m,c]=np.interp(rgb[m].mean(1),knots,values[:,c]).clip(0,255).astype('uint8')
    for material,mask in masks.items():a[mask,:3]=(rgb[mask]+offsets[material]).clip(0,255).astype('uint8')
    assert np.array_equal(a[:,:,3],frames[i][:,:,3])
    warm=masks['skin']|masks['hair'];yy,xx=np.where(warm)
    top=int(yy.min());center=round((xx.min()+xx.max())/2)-3
    # Retain the accepted West +2px placement relative to the original recipe.
    position=(center-20,top-10);cut=top+32
    body=a.copy();body[:cut]=0
    equipped=Image.fromarray(body);equipped.alpha_composite(helmet_component,position)
    bare.append(Image.fromarray(a));helmet.append(equipped)
    fits.append({'pose':i,'warmHeadTop':top,'warmCenterMinus3':center,'position':list(position),'bodyCutY':cut,'componentBox':[64,14,108,60],'componentScale':1,'componentGradeChanged':False})
board=Image.new('RGB',(1536,840),'#202a30');draw=ImageDraw.Draw(board)
bindings={}
for row,(gear,images) in enumerate([('bare',bare),('helmet',helmet)]):
    paths=[]
    for i,im in enumerate(images):
        folder=P/'frames'/gear;folder.mkdir(parents=True,exist_ok=True)
        path=folder/f'{i:03}.png';im.save(path);paths.append(path.relative_to(P).as_posix())
        bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
        a=np.array(im);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20)
        board.paste(im,(i*256,row*280+22),im);draw.text((i*256+4,row*280+3),gear+' candidate '+str(i),fill='white')
    data=dict(original['profile']);data.update(name='Veld West master proportions '+gear,status='staged_not_installed',textureFilter='linear',strideDistanceCells={'carry-west':original['profile']['strideDistanceCells']['carry-west']})
    state=dict(original['state']);state.update(frameFiles=paths,frameCount=6);data['states']=[state]
    (P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
for i in range(6):
    masterim=Image.fromarray(master);canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(masterim,(36,52))
    board.paste(canvas,(i*256,582),canvas);draw.text((i*256+4,563),'Accepted West foundation',fill='white')
board.save(P/'paired-master-contact.png')
record={'clothKnots':knots.tolist(),'clothTargetRGB':values.tolist(),'skinHairFixedRGBOffsets':{k:v.tolist() for k,v in offsets.items()},'onePooledTransform':True,'caseNearHandProtected':True,'alphaUnchangedForGrade':True,'nativeHelmetSource':headpath.relative_to(R).as_posix(),'nativeHelmetSHA256':hashlib.sha256(headpath.read_bytes()).hexdigest(),'helmetFits':fits,'sourceBindings':bindings,'source':'raw-v2.png','sourceSHA256':hashlib.sha256((P/'raw-v2.png').read_bytes()).hexdigest(),'status':'staged_not_installed','scope':'source-family grade and bounded unchanged native helmet fitting; geometry authored, no procedural anatomy or per-pose scaling; motion/world/adoption acceptance separate'}
(P/'package-registration.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'pairedFrames':12,'cycleMs':sum(original['state']['frameDurationsMs']),'skinHairOffsets':record['skinHairFixedRGBOffsets'],'helmetPositions':[x['position'] for x in fits]}))
