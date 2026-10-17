"""Replace one drifted crouch with original-master whole-pose authorship."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,copy,hashlib,subprocess,sys
P=Path(__file__).resolve().parent;R=P.parent;OLD=R/'bill-land-water-west-v5';S=P/'sources'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
raw=S/'crouch-master-v2.png';im=Image.open(raw).convert('RGBA');assert im.size==(1536,1024),im.size
a=np.array(im);lab,_=label(a[:,:,3]>250);counts=np.bincount(lab.ravel());keep=binary_dilation(lab==np.argmax(counts[1:])+1,iterations=3)&(a[:,:,3]>0);a[~keep]=0
ratio=148/956;small=Image.fromarray(a).resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.LANCZOS)
b=np.array(small);yy,xx=np.indices(b.shape[:2]);op=b[:,:,3]>180;top=int(yy[op].min());crown=int(np.median(xx[op&(yy<top+5)]));sole=int(yy[op].max())+1
shift=(148-crown,224-sole);out=Image.new('RGBA',(320,320));out.alpha_composite(small,shift)
assert np.count_nonzero(np.array(out)[:,:,3])==np.count_nonzero(b[:,:,3])
frames=[Image.open(OLD/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA') for i in range(7)];frames[2]=out
F=P/'bare/frames/land-swim-west';F.mkdir(parents=True,exist_ok=True)
for i,frame in enumerate(frames):frame.save(F/f'{i:03}.png')
unchanged=[0,1,3,4,5,6]
for i in unchanged:assert frames[i].tobytes()==Image.open(OLD/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA').tobytes()
manifest=copy.deepcopy(json.loads((OLD/'bare/manifest.json').read_text(encoding='utf-8')));manifest['name']='Bill West original-master crouch candidate';manifest['states'][0]['provenance']='Pose2 newly authored from sole original directional master at148/956 source density, complete anatomy articulated at knees/hips/shoulders. Whole-figure registration only. Other six poses exactV5. Source candidate unselected.'
(P/'bare/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
times=manifest['states'][0]['frameDurationsMs'];assert sum(times)==500
frames[0].save(P/'bare/source-enter.png',save_all=True,append_images=frames[1:],duration=times,loop=1,disposal=0,blend=0)
crowns=[]
for frame in frames[1:6]:
    c=np.array(frame);yyy,xxx=np.indices(c.shape[:2]);mask=c[:,:,3]>180;t=int(yyy[mask].min());crowns.append((int(np.median(xxx[mask&(yyy<t+5)])),t))
helmet=(OLD/'build_helmet.py').read_text(encoding='utf-8');start=helmet.index('HEADS=');end=helmet.index('\n',start);helmet=helmet[:start]+'HEADS='+repr(crowns)+helmet[end:]
(P/'build_helmet.py').write_text(helmet,encoding='utf-8');subprocess.run([sys.executable,str(P/'build_helmet.py')],check=True)
for gear in ['bare','helmet']:
    for i in unchanged:assert Image.open(P/gear/f'frames/land-swim-west/{i:03}.png').convert('RGBA').tobytes()==Image.open(OLD/gear/f'frames/land-swim-west/{i:03}.png').convert('RGBA').tobytes()
    with Image.open(P/gear/'source-enter.png') as ap:
        assert ap.n_frames==7 and ap.info['loop']==1
        for i in range(7):ap.seek(i);assert ap.convert('RGBA').tobytes()==Image.open(P/gear/f'frames/land-swim-west/{i:03}.png').convert('RGBA').tobytes() and ap.info['duration']==times[i]
board=Image.new('RGB',(1280,720),'#182932');d=ImageDraw.Draw(board);master=Image.open(R/'bill-land-water-west-v4/master-comparison.png').crop((0,25,320,345))
for row,gear in enumerate(['bare','helmet']):
    y=row*360
    tiles=[('Original bare master',master),('Repaired arm-ready',Image.open(OLD/gear/'frames/land-swim-west/001.png').convert('RGBA')),('Previous crouch',Image.open(OLD/gear/'frames/land-swim-west/002.png').convert('RGBA')),('New master crouch',Image.open(P/gear/'frames/land-swim-west/002.png').convert('RGBA'))]
    for col,(title,frame) in enumerate(tiles):board.paste(frame,(col*320,y+25),frame if frame.mode=='RGBA' else None);d.text((col*320+4,y+4),gear+' '+title,fill='white');d.line((col*320,y+249,col*320+319,y+249),fill='#6aa39e')
board.save(P/'master-crouch-comparison.png')
html=(OLD/'index.html').read_text(encoding='utf-8').replace('The standing reference matches current idle. The arm-ready pose follows the original master’s head, build and suit detail. Remaining poses still need consistency review.','Standing and arm-ready remain unchanged. The new crouch follows the original master’s anatomy and drawing scale. Remaining poses still need consistency review.').replace('Original master and preceding pose','Original master and preceding crouch').replace('master-arm-comparison.png','master-crouch-comparison.png').replace('Master and preceding arm-ready comparison','Master and preceding crouch comparison');(P/'index.html').write_text(html,encoding='utf-8')
inputs=[R/'crew-side-masters-v1/bill-side-master-01.png',raw,S/'crouch-master-prompt-v2.txt',OLD/'bare/manifest.json',OLD/'helmet/manifest.json',R/'bill-cargo-helmet-west-v1/sources/canonical-head.png']+[OLD/g/f'frames/land-swim-west/{i:03}.png' for g in ['bare','helmet'] for i in range(7)]
review=dict(scope='Single original-master crouch repair; candidate only.',raw=raw.relative_to(R).as_posix(),wholeSourceDensity=ratio,rawCanvas=im.size,translation=shift,registeredCrown=crowns[1],opaqueSupportAfter=224,allPaintedSupportPreserved=True,unchangedPosesBothGears=unchanged,unchangedDecodedPoseCount=12,decodedAPNGFramesExact=14,finiteAPNGLoop=1,timelineMs=500,inputSHA256={f.relative_to(R).as_posix():sha(f) for f in inputs},visualAcceptance='Pending raw/full pose/master/neck inspection',nativeAcceptance=False,normalSelected=False)
(P/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in review.items() if k!='inputSHA256'}))
