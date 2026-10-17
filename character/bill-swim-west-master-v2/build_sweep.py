"""Add a second authored study pose using bounded head registration."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import json,hashlib,numpy as np,subprocess,sys,copy
P=Path(__file__).resolve().parent;R=P.parent
subprocess.run([sys.executable,str(P/'build.py')],check=True,stdout=subprocess.DEVNULL)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
report=json.loads((P/'review.json').read_text(encoding='utf-8'))
inputs=[P/'sources/stroke-sweep-v1.png',P/'sources/stroke-sweep-prompt-v1.txt',P/'sources/stroke-sweep-identity-v2.png',P/'sources/stroke-sweep-identity-prompt-v2.txt',R/'bill-land-water-west-v9/sources/master-head-reference.png',R/'bill-swim-west-coherent-v1/frames/swim-west/001.png']
before={f.relative_to(R).as_posix():sha(f) for f in inputs}
raw=Image.open(P/'sources/stroke-sweep-identity-v2.png').convert('RGBA');assert raw.size==(1536,1024)
a=np.array(raw);lab,_=label(a[:,:,3]>250);counts=np.bincount(lab.ravel());keep=binary_dilation(lab==np.argmax(counts[1:])+1,iterations=3)&(a[:,:,3]>0);a[~keep]=0
# A raised heel may be higher than the head: find hair/face inside inspected ROI.
roi=[250,170,480,420];c=a[170:420,250:480];rgb=c[:,:,:3].astype(float);r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
mask=(c[:,:,3]>180)&(r>=40)&(r<=160)&(r>g*1.15)&(g>b*1.2);lab,_=label(mask);counts=np.bincount(lab.ravel());part=lab==np.argmax(counts[1:])+1;y,x=np.where(part)
box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
assert box[0]>0 and box[1]>0 and box[2]<c.shape[1] and box[3]<c.shape[0]
headtop=int(y.min())+170;axis=int(np.median(x[part.nonzero()[0]<y.min()+5]))+250
density=148/956;small=Image.fromarray(a).resize((round(raw.width*density),round(raw.height*density)),Image.Resampling.LANCZOS)
shift=(134-round(axis*density),200-round(headtop*density));bare=Image.new('RGBA',(320,320));bare.alpha_composite(small,shift)
assert np.count_nonzero(np.array(bare)[:,:,3])==np.count_nonzero(np.array(small)[:,:,3])
original=np.array(bare);yy,xx=np.indices(original.shape[:2]);x,y=134,200
donor=Image.open(R/'bill-cargo-helmet-west-v1/sources/canonical-head.png').convert('RGBA');assert donor.size==(40,40)
pos=(119,196);poly=[(117,197),(152,197),(153,223),(142,233),(117,233),(116,222)]
erase=Image.new('L',bare.size);ImageDraw.Draw(erase).polygon(poly,fill=255);e=np.array(erase)>0
body=original.copy();body[e]=0;helmet=Image.fromarray(body);helmet.alpha_composite(donor,pos);out=np.array(helmet)
fg=(((yy>=y+27)&(xx>=x+7))|((yy>=y+33)&(xx<=x-5))|((yy>=y+18)&(xx<=x-22)))&(original[:,:,3]>0);out[fg]=original[fg]
area=Image.new('L',bare.size);area.paste(donor.getchannel('A'),pos);allowed=e|(np.array(area)>0)
assert np.array_equal(out[~allowed],original[~allowed]) and np.array_equal(out[fg],original[fg]) and np.array_equal(out[yy>=236],original[yy>=236])
helmet=Image.fromarray(out)
board=Image.new('RGB',(1280,720),'#182932');d=ImageDraw.Draw(board)
for row,(gear,im) in enumerate([('bare',bare),('helmet',helmet)]):
    dest=P/gear/'frames/swim-west-sweep/000.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest)
    m=json.loads((P/gear/'manifest.json').read_text(encoding='utf-8'));state=copy.deepcopy(m['states'][0]);state.update(id='swim-west-sweep',frameFiles=['frames/swim-west-sweep/000.png']);m['states'].append(state)
    partial=copy.deepcopy(state);partial.update(id='swim-west-partial-study',frameFiles=['frames/swim-west-extend/000.png','frames/swim-west-sweep/000.png'],frameDurationsMs=[160,160],facings=['west']*2,waterKinds=['swim']*2,waterPoses=[True]*2,depthOffsets=[0]*2,provenance='Two-pose finite320ms source study, NOT complete swim loop or runtime replacement.')
    m['states'].append(partial);(P/gear/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
    ext=Image.open(P/gear/'frames/swim-west-extend/000.png').convert('RGBA');ext.save(P/gear/'source-partial.png',save_all=True,append_images=[im],duration=[160,160],loop=1,disposal=0,blend=0)
    with Image.open(P/gear/'source-partial.png') as ap:
        assert ap.n_frames==2 and ap.info['loop']==1
        for i,frame in enumerate([ext,im]):ap.seek(i);assert ap.convert('RGBA').tobytes()==frame.tobytes() and ap.info['duration']==160
    old=Image.open(R/f'bill-land-water-west-v11/{gear}/frames/land-swim-west/005.png').convert('RGBA')
    prior=Image.open(R/'bill-swim-west-coherent-v1/frames/swim-west/001.png').convert('RGBA');oldswim=Image.new('RGBA',(320,320));oldswim.alpha_composite(prior,(74,136))
    for col,(title,frame) in enumerate([('Entry near-prone',old),('New extend',ext),('New sweep',im),('Old bare sweep',oldswim)]):
        board.paste(frame,(col*320,row*360+25),frame);d.text((col*320+4,row*360+4),gear+' /'+title,fill='white')
board.save(P/'partial-stroke-review.png')
neck=Image.new('RGB',(800,360),'#182932');d=ImageDraw.Draw(neck)
for i,(name,im) in enumerate([('Bare sweep',bare),('Helmet sweep',helmet)]):
    crop=im.crop((89,190,189,265)).resize((400,300),Image.Resampling.NEAREST);neck.paste(crop,(i*400,30),crop);d.text((i*400+5,5),name+' /same4x',fill='white')
neck.save(P/'sweep-neck-review.png')
assert all(sha(f)==before[f.relative_to(R).as_posix()] for f in inputs)
report['inputSHA256'].update(before);assert all(sha(R/f)==h for f,h in report['inputSHA256'].items())
report.update(scope='Two authored stroke study poses, not complete loop/native acceptance.',frozenInputsStable=len(report['inputSHA256']),sweep=dict(raw='sources/stroke-sweep-identity-v2.png',generation='exec-e8956a81-ab18-41df-8d7b-db5b07223361',initialGeneration='exec-495d162f-dec3-45cf-bcf2-4fb672ce9c10',headROI=roi,headComponentBounds=box,headWidth=box[2]-box[0],headHeight=box[3]-box[1],componentTouchesROIEdge=False,sourceCrown=[axis,headtop],translation=shift,canonicalHelmetScale=1,bodyOutsideHeadExact=True,foregroundExact=True),decodedPartialAPNGFramesExact=4,partialMs=320,partialLoop=1)
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html=(P/'index.html').read_text(encoding='utf-8').replace('One representative source pose','Two representative source poses').replace('</p><img','</p><img src="partial-stroke-review.png"><img src="sweep-neck-review.png"><img',1);(P/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(report['inputSHA256']),decodedFrames=4,ms=320,sweepHead=[box[2]-box[0],box[3]-box[1]],sweepTranslation=shift)))
