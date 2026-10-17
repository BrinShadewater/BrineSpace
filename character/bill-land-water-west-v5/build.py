"""Build West master-authored arm-ready candidate at original drawing density."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,copy,hashlib,subprocess,sys
P=Path(__file__).resolve().parent;R=P.parent;OLD=R/'bill-land-water-west-v4'
S=P/'sources';raw=S/'arm-ready-matte-v2.png'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
im=Image.open(raw).convert('RGBA');a=np.array(im)
assert im.size==(1536,1024),im.size
lab,_=label(a[:,:,3]>250);counts=np.bincount(lab.ravel());keep=binary_dilation(lab==np.argmax(counts[1:])+1,iterations=3)&(a[:,:,3]>0);a[~keep]=0
ratio=148/956
small=Image.fromarray(a).resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.LANCZOS)
b=np.array(small);yy,xx=np.indices(b.shape[:2]);op=b[:,:,3]>180
top=int(yy[op].min());crown=int(np.median(xx[op&(yy<top+5)]));sole=int(yy[op].max())+1
shift=(157-crown,224-sole)
new=Image.new('RGBA',(320,320));new.alpha_composite(small,shift)
assert np.count_nonzero(np.array(new)[:,:,3])==np.count_nonzero(b[:,:,3])
frames=[Image.open(OLD/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA') for i in range(7)]
normalfile=R/'crew-runtime-matte-v1/bill/manifest.json';m=json.loads(normalfile.read_text(encoding='utf-8'));st=next(s for s in m['states'] if s['id']=='idle-west');idlefile=normalfile.parent/st['frameFiles'][0];idle=Image.open(idlefile).convert('RGBA')
assert m['standingHeight']==148
standing=Image.new('RGBA',(320,320));standing.alpha_composite(idle,(round(160-m['pivot'][0]),round(224-m['pivot'][1])))
frames[0]=standing;frames[1]=new
F=P/'bare/frames/land-swim-west';F.mkdir(parents=True,exist_ok=True)
for i,frame in enumerate(frames):frame.save(F/f'{i:03}.png')
for i in range(2,7):assert frames[i].tobytes()==Image.open(OLD/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA').tobytes()
manifest=copy.deepcopy(json.loads((OLD/'bare/manifest.json').read_text(encoding='utf-8')))
manifest['name']='Bill West original-master arm-ready and current normal standing context candidate'
manifest['status']='source_study_unselected'
manifest['states'][0]['provenance']='Pose1 newly articulated directly from original left-facing side master at148/956 source density, whole-figure translation only. Pose0 exact current normal bare idle. Poses2..6 unchanged fromV4. Full motion/contact/native acceptance pending.'
(P/'bare/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
times=manifest['states'][0]['frameDurationsMs'];assert sum(times)==500
frames[0].save(P/'bare/source-enter.png',save_all=True,append_images=frames[1:],duration=times,loop=1,disposal=0,blend=0)
crowns=[]
for frame in frames[1:6]:
    c=np.array(frame);yyy,xxx=np.indices(c.shape[:2]);mask=c[:,:,3]>180;t=int(yyy[mask].min());crowns.append((int(np.median(xxx[mask&(yyy<t+5)])),t))
helmet=(OLD/'build_helmet.py').read_text(encoding='utf-8');start=helmet.index('HEADS=');end=helmet.index('\n',start);helmet=helmet[:start]+'HEADS='+repr(crowns)+helmet[end:];helmet=helmet.replace('loop=0','loop=1')
(P/'build_helmet.py').write_text(helmet,encoding='utf-8')
subprocess.run([sys.executable,str(P/'build_helmet.py')],check=True)
for gear in ['bare','helmet']:
    with Image.open(P/gear/'source-enter.png') as ap:
        assert ap.n_frames==7 and ap.info['loop']==1
        for i in range(7):
            ap.seek(i);expected=Image.open(P/gear/f'frames/land-swim-west/{i:03}.png').convert('RGBA');assert ap.convert('RGBA').tobytes()==expected.tobytes() and ap.info['duration']==times[i]
board=Image.new('RGB',(1280,720),'#182932');d=ImageDraw.Draw(board)
master=Image.open(OLD/'master-comparison.png').crop((0,25,320,345))
for row,gear in enumerate(['bare','helmet']):
    y=row*360
    for col,(title,frame) in enumerate([('Original bare master',master),('V4 standing context',Image.open(OLD/gear/'frames/land-swim-west/000.png').convert('RGBA')),('V4 arm-ready',Image.open(OLD/gear/'frames/land-swim-west/001.png').convert('RGBA')),('V5 master arm-ready',Image.open(P/gear/'frames/land-swim-west/001.png').convert('RGBA'))]):
        board.paste(frame,(col*320,y+25),frame if frame.mode=='RGBA' else None);d.text((col*320+4,y+4),gear+' '+title,fill='white');d.line((col*320,y+249,col*320+319,y+249),fill='#6aa39e')
board.save(P/'master-arm-comparison.png')
review=dict(scope='West source candidate only, no normal selection/native acceptance.',generationMode='built-in image_gen edit',generations=['exec-17a46ca0-7ba3-4e0c-a45d-148806f18187','exec-01a57aa3-f277-4ad4-8936-7f230dde3529'],raw=raw.relative_to(R).as_posix(),rawSHA256=sha(raw),promptSHA256=sha(S/'arm-ready-matte-prompt-v2.txt'),master='crew-side-masters-v1/bill-side-master-01.png',masterSHA256=sha(R/'crew-side-masters-v1/bill-side-master-01.png'),rawCanvas=im.size,wholeSourceDensity=ratio,translation=shift,registeredCrown=crowns[0],opaqueSupportAfter=224,allPaintedSupportPreserved=True,currentNormalBareIdle=idlefile.relative_to(R).as_posix(),normalIdleManifestSHA256=sha(normalfile),normalIdleSourceSHA256=sha(idlefile),unchangedBarePoses=list(range(2,7)),decodedAPNGFramesExact=14,finiteAPNGLoop=1,timelineMs=500,visualAcceptance='Pending graded raw, registered whole-figure and neck inspection',nativeAcceptance=False,normalSelected=False)
(P/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
print(json.dumps(review))
