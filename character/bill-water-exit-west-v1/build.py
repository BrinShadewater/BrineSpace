"""Package independently articulated West exit sources at common native density."""
from pathlib import Path
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation
import numpy as np, json, hashlib

P=Path(__file__).resolve().parent; R=P.parent; S=P/'sources'
TIMES=[60,50,60,70,100,100,60]
JOBS=[('low-elbow',2,'exec-134922ab-ad2c-4206-9aeb-f780df4bba6e',131),
      ('palm-push',1,'exec-6465e38a-c512-44d5-930c-c57a6b4c4621',130),
      ('knee-tuck',1,'exec-7605a6b8-faea-43ff-8e93-672ac9b06c94',133),
      ('half-kneel',1,'exec-0d91d7ff-e11a-4c95-ac05-d2a0609c0389',147),
      ('rise',2,'exec-9dc957e9-ac5d-4978-909d-7ad92100511e',157)]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
frames=[Image.open(R/'bill-land-water-west-v4/bare/frames/land-swim-west/006.png').convert('RGBA')]
records=[];crowns=[]; yy,xx=np.indices((320,320))
for kind,version,generation,head_x in JOBS:
    raw=S/f'{kind}-canvas-v{version}.png';im=Image.open(raw).convert('RGBA');assert im.width==im.height==1254
    a=np.array(im);lab,_=label(a[:,:,3]>250);count=np.bincount(lab.ravel())
    keep=binary_dilation(lab==np.argmax(count[1:])+1,iterations=3)&(a[:,:,3]>0);a[~keep]=0
    im=Image.fromarray(a).resize((320,320),Image.Resampling.LANCZOS);b=np.array(im);op=b[:,:,3]>180
    top=int(yy[op].min());crown_x=int(np.median(xx[op&(yy<top+5)]));contact=int(yy[op].max())+1
    shift=(head_x-crown_x,224-contact)
    out=Image.new('RGBA',(320,320));out.paste(im,shift)
    assert np.count_nonzero(np.array(out)[:,:,3])==np.count_nonzero(b[:,:,3])
    out.save(S/f'{kind}-native-v{version}.png');frames.append(out)
    crowns.append((head_x,top+shift[1]))
    records.append(dict(pose=len(frames)-1,kind=kind,generation=generation,raw=raw.name,rawSHA256=sha(raw),prompt=f'{kind}-prompt-v{version}.txt',promptSHA256=sha(S/f'{kind}-prompt-v{version}.txt'),rawSize=list(a.shape[:2]),wholeCanvasScale=320/1254,translation=shift,opaqueSupportBefore=contact,opaqueSupportAfter=224,registeredCrown=crowns[-1],paintedSupportPreserved=True))
frames.append(Image.open(R/'bill-land-water-west-v4/bare/frames/land-swim-west/000.png').convert('RGBA'))
assert sum(TIMES)==500
F=P/'bare/frames/swim-land-west';F.mkdir(parents=True,exist_ok=True)
for i,im in enumerate(frames):im.save(F/f'{i:03}.png')
for i,j in [(0,6),(6,0)]:assert frames[i].tobytes()==Image.open(R/f'bill-land-water-west-v4/bare/frames/land-swim-west/{j:03}.png').convert('RGBA').tobytes()
manifest=dict(name='Bill separately articulated West water exit',status='source_study_unselected',frameWidth=320,frameHeight=320,pivot=[160,224],standingHeight=148,textureFilter='linear',precomposed=True,states=[dict(id='swim-land-west',frameFiles=[f'frames/swim-land-west/{i:03}.png' for i in range(7)],frameDurationsMs=TIMES,loop=False,facings=['west']*7,provenance='Five newly articulated exit poses, not reversed entrance or mirrored East art. Exact standing/swim endpoint contexts; dynamic actual gait binding remains runtime work.')])
(P/'bare/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
frames[0].save(P/'bare/source-leave.png',save_all=True,append_images=frames[1:],duration=TIMES,loop=0,disposal=0,blend=0)
with Image.open(P/'bare/source-leave.png') as decoded:
    assert decoded.n_frames==7
    for i,im in enumerate(frames):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==im.tobytes() and decoded.info['duration']==TIMES[i]
helmet=(R/'bill-land-water-west-v4/build_helmet.py').read_text(encoding='utf-8')
start=helmet.index('HEADS=');end=helmet.index('\n',start);helmet=helmet[:start]+'HEADS='+repr(crowns)+helmet[end:]
helmet=helmet.replace("ENDS=['bill-shared-helmet-runtime-v2/frames/idle-west/000.png','bill-swim-helmet-west-coherent-v1/frames/swim-west/000.png']","ENDS=['bill-swim-helmet-west-coherent-v1/frames/swim-west/000.png','bill-shared-helmet-runtime-v2/frames/idle-west/000.png']")
helmet=helmet.replace('PIVOTS=[(92,172),(86,88)]','PIVOTS=[(86,88),(92,172)]').replace('TIMES=[60,70,80,60,80,90,60]','TIMES='+repr(TIMES)).replace("kind='idle-west' if j==0 else 'swim-west'","kind='swim-west' if j==0 else 'idle-west'").replace('land-swim-west','swim-land-west').replace('source-enter','source-leave').replace('compact water entry','independent water exit')
helmet=helmet.replace('poly=[(x-17,y-3),(x+18,y-3),(x+19,y+23),(x+8,y+33),(x-17,y+33),(x-18,y+22)]','poly=[(x-17,y-3),(x+14,y-3),(x+12,y+18),(x+5,y+27),(x-15,y+27),(x-18,y+20)]')
helmet=helmet.replace('(yy>=y+27)&(xx>=x+7)','(yy>=y+23)&(xx>=x+8)').replace("'foregroundRightMinXMinY':[x+7,y+27]","'foregroundRightMinXMinY':[x+8,y+23]")
helmet=helmet.replace('crowns=[(157,78)]+HEADS+[(134,195)]','crowns=[(131,188)]+HEADS+[(157,80)]')
(P/'build_helmet.py').write_text(helmet,encoding='utf-8')
board=Image.new('RGB',(2560,350),'#182932');d=ImageDraw.Draw(board)
master=Image.open(R/'crew-side-masters-v1/bill-side-master-01.png').convert('RGB');ratio=148/956
sm=master.crop((850,0,1280,1024)).resize((round(430*ratio),round(1024*ratio)),Image.Resampling.LANCZOS)
board.paste(sm,(125,25+224-round(977*ratio)));d.text((5,5),'Original master /148 ruler',fill='white')
for i,im in enumerate(frames):
    x=(i+1)*320;board.paste(im,(x,25),im);d.text((x+5,5),['Swim context','Low elbow','Palm push','Knee tuck','Half kneel','Rise','Standing context'][i],fill='white');d.line((x,249,x+319,249),fill='#6aa39e')
board.save(P/'master-review.png')
review=dict(scope='New separate West exit source candidate only; full anatomy/material/contact/motion acceptance pending.',registrations=records,crowns=crowns,timelineMs=500,decodedBareAPNGFramesExact=7,endpointContextsRGBAExact=True,normalSelected=False,nativeAcceptance=False,rejectedCandidates={'rejected-low-elbow-canvas-v1.png':dict(generation='exec-da3e75a8-5a64-4442-bc9b-44e8c803e555',reason='Expanded head/body and spread boots despite preservation instruction.'),'rise-canvas-v1.png':dict(generation='exec-abb53574-6d53-42bd-a6e3-ce6cb5daf0ee',reason='Head enlarged and insufficient knee bend; replaced by anatomical repair V2.')})
(P/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(poses=7,newArticulatedInteriors=5,decodedExact=7,crowns=crowns,scale=320/1254,ms=500)))
