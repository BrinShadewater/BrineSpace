from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib,copy
P=Path(__file__).resolve().parent;R=P.parent;OLD=R/'bill-land-water-west-v3';RAW=R/'bill-land-water-west-v1/sources'
S=P/'sources';S.mkdir(parents=True,exist_ok=True)
jobs=[(1,'arm-ready',5,'exec-0ac37457-b3ca-4e3a-b738-d2381ffe8d73',None),(4,'lift',3,'exec-051b3767-1a8c-4a58-a35c-7c5617a00781',(130,150)),(5,'prone',2,'exec-9770dcdd-1880-4aeb-b070-aad43b96382f',(131,188))]
frames=[Image.open(OLD/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA') for i in range(7)]
records=[]
for i,kind,version,generation,target in jobs:
    file=RAW/f'{kind}-canvas-v{version}.png';raw=Image.open(file).convert('RGBA');assert raw.width==raw.height
    a=np.array(raw);lab,_=label(a[:,:,3]>250);counts=np.bincount(lab.ravel());keep=binary_dilation(lab==np.argmax(counts[1:])+1,iterations=3)&(a[:,:,3]>0);a[~keep]=0
    im=Image.fromarray(a).resize((320,320),Image.Resampling.LANCZOS);b=np.array(im);yy,xx=np.indices((320,320));op=b[:,:,3]>180;top=int(yy[op].min());x=int(np.median(xx[op&(yy<top+5)]));sole=None
    if target is None:
        boot=op&(xx>=130)&(xx<185)&(yy>=190)&(yy<260);assert boot.any();sole=int(yy[boot].max())+1;shift=(0,224-sole)
    else:shift=(target[0]-x,target[1]-top)
    out=Image.new('RGBA',(320,320));out.paste(im,shift);assert np.count_nonzero(np.array(out)[:,:,3])==np.count_nonzero(b[:,:,3]);out.save(S/f'{kind}-native-v{version}.png')
    old=np.array(frames[i]);new=np.array(out);oldop=old[:,:,3]>180;newop=new[:,:,3]>180
    records.append({'pose':i,'kind':kind,'source':file.relative_to(R).as_posix(),'prompt':(RAW/f'{kind}-prompt-v{version}.txt').relative_to(R).as_posix(),'generation':generation,'rawCanvas':raw.size,'wholeCanvasScale':320/raw.width,'translation':shift,'sourceCrown':[x,top],'registeredCrown':[x+shift[0],top+shift[1]],'soleBefore':sole,'allPaintedSupportPreserved':True,'oldBBox':frames[i].getchannel('A').getbbox(),'newBBox':out.getchannel('A').getbbox(),'opaqueSilhouetteIoU':np.count_nonzero(oldop&newop)/np.count_nonzero(oldop|newop)})
    frames[i]=out
F=P/'bare/frames/land-swim-west';F.mkdir(parents=True,exist_ok=True)
for i,im in enumerate(frames):im.save(F/f'{i:03}.png')
for i in [0,2,3,6]:assert frames[i].tobytes()==Image.open(OLD/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA').tobytes()
manifest=copy.deepcopy(json.loads((OLD/'bare/manifest.json').read_text()));manifest['name']='Bill West complete intermediate material-detail candidate';manifest['states'][0]['provenance']='Four V3 source poses exact. Original-master material/detail edits for arm-ready/lift/prone, wholecanvas normalization and wholefigure contact/crown translation only. Source-only unselected; fresh native proof pending.'
(P/'bare/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
times=manifest['states'][0]['frameDurationsMs'];assert sum(times)==500
frames[0].save(P/'bare/source-enter.png',save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=0,blend=0)
with Image.open(P/'bare/source-enter.png') as ap:
 assert ap.n_frames==7
 for i,im in enumerate(frames):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==times[i]
crowns=[]
for im in frames[1:6]:
 a=np.array(im);yy,xx=np.indices((320,320));op=a[:,:,3]>180;top=int(yy[op].min());x=int(np.median(xx[op&(yy<top+5)]));crowns.append((x,top))
s=(OLD/'build_helmet.py').read_text();start=s.index('HEADS=');end=s.index('\n',start);s=s[:start]+'HEADS='+repr(crowns)+s[end:];(P/'build_helmet.py').write_text(s)
board=Image.new('RGB',(2560,720),'#182932');d=ImageDraw.Draw(board);master=Image.open(R/'crew-side-masters-v1/bill-side-master-01.png').convert('RGB');scale=148/956;sm=master.crop((850,0,1280,1024)).resize((round(430*scale),round(1024*scale)),Image.Resampling.LANCZOS)
for row in range(2):
 y=row*360;board.paste(sm,(125,y+25+224-round(977*scale)));d.text((5,y+5),'Original master /148 ruler',fill='white')
 for i,name in enumerate(['idle','arm ready','crouch','push-off','lift','near-prone','swim']):
  im=Image.open(OLD/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA') if row==0 else frames[i];x=(i+1)*320;board.paste(im,(x,y+25),im);d.text((x+5,y+5),('V3 ' if row==0 else 'V4 ')+name,fill='white')
  if i<3:d.line((x,y+249,x+319,y+249),fill='#6aa39e')
board.save(P/'master-comparison.png')
detail=Image.new('RGB',(1600,720),'#182932');d=ImageDraw.Draw(detail)
for col,i in enumerate([1,4,5]):
 x,y=crowns[i-1]
 for row in range(2):
  im=Image.open(OLD/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA') if row==0 else frames[i];crop=im.crop((x-45,y-10,x+55,y+75)).resize((400,340),Image.Resampling.NEAREST);detail.paste(crop,(col*530,row*360+20),crop);d.text((col*530+5,row*360+3),('V3' if row==0 else 'V4')+f' pose{i} /native4x ruler',fill='white')
detail.save(P/'material-detail-comparison.png')
raws=[RAW/f'{kind}-{part}-v{version}.{ext}' for _,kind,version,_,_ in jobs for part,ext in [('canvas','png'),('prompt','txt')]]
e={'scope':'Three new material/detail source edits finish pass across all five West entry intermediates. Source-only unselected; endpoint consistency/full motion/new native proof still pending.','generationMode':'built-in image_gen','registrations':records,'crowns':crowns,'exactOriginalV3BarePoses':[0,2,3,6],'decodedBareAPNGFramesExact':7,'timelineMs':500,'rawAndPromptSHA256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in raws},'rejectedArmReady':{'source':'bill-land-water-west-v1/sources/rejected-arm-ready-detail-v4.png','generation':'exec-e1be26fb-33f9-431f-92a3-0f1c4ce10f94','prompt':'bill-land-water-west-v1/sources/arm-ready-prompt-v4.txt','reason':'Figure recentered lower and standing build shortened; materials alone not acceptance.'},'visualAcceptance':'pending shared master and material/neck comparison'}
(P/'review.json').write_text(json.dumps(e,indent=2)+'\n');print(json.dumps({'registrations':records,'crowns':crowns,'decodedExact':7,'ms':500}))
