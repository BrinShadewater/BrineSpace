from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent;S=P/'sources';F=P/'bare/frames/land-swim-south';F.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def isolate(im):
 a=np.array(im.convert('RGBA'));labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;assert counts.max()>10000
 keep=binary_dilation(labs==counts.argmax(),iterations=3)&(a[:,:,3]>0);a[~keep]=0;return Image.fromarray(a)
def context(im,shift):
 out=Image.new('RGBA',(320,352));out.paste(im,shift);assert out.crop((shift[0],shift[1],shift[0]+im.width,shift[1]+im.height)).tobytes()==im.tobytes();return out
def register(im,scale,axis,crown,head=None):
 scaled=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);a=np.array(scaled);y,x=np.where(a[:,:,3]>180)
 shift=(160-round(axis*scale),224-int(y.max())-1) if head is None else (160-round(axis*scale),head-round(crown*scale))
 out=Image.new('RGBA',(320,352));out.paste(scaled,shift);assert np.count_nonzero(np.array(out)[:,:,3])==np.count_nonzero(a[:,:,3]),'No clipping'
 return out,dict(scale=scale,translation=shift,crown=[160,round(crown*scale)+shift[1]],opaqueBottom=int(y.max())+shift[1]+1,alphaBounds=out.getchannel('A').getbbox())
idlepath=R/'crew-runtime-matte-v1/bill/frames/idle-south-breathing-v1/000.png';swimpath=R/'bill-swim-south-coherent-v1/frames/swim-south/000.png';kneelpath=R/'bill-bare-south-selected-v1/frames/kneel-south/002.png'
frames=[context(Image.open(idlepath).convert('RGBA'),(68,52))];records=[]
master=np.array(Image.open(R/'bill-video-south-v1/master-source.png').convert('RGBA'));yy,xx=np.where(master[:,:,3]>180);density=148/(int(yy.max())-int(yy.min())+1)
# Each independently generated single source has a different drawing density despite
# identical canvas dimensions. Fixed source calibration follows original hair ruler,
# not occupied posed body height; head proxies are provisional, not anatomy proof.
first=isolate(Image.open(S/'early-crouch-v1.png'));early_density=density*135/149
im,rec=register(first,early_density,515,127);frames.append(im);records.append(dict(rec,source='sources/early-crouch-v1.png',role='authored gentle first crouch',sourceDensityAuthority='original hair component135px vsnew149px at original master148/1295; fixed whole source density, no posed-height fit'))
middle=isolate(Image.open(S/'middle-crouch-v1.png'));middle_density=density*135/166
im,rec=register(middle,middle_density,532,173);frames.append(im);records.append(dict(rec,source='sources/middle-crouch-v1.png',role='authored middle crouch replacing widened legacy context',sourceDensityAuthority='original hair component135px vsnew166px at original master148/1295; fixed whole source density, no posed-height fit'))
atlas=Image.open(S/'entry-atlas-v1.png').convert('RGBA');assert atlas.size==(1536,1024)
# Head-colour component diagnostics use high saturation to exclude warm cuff metals.
rois=[(235,5,335,85),(200,120,325,215),(200,190,325,305),(215,185,350,300),(200,200,330,320),(200,200,330,325)]
anchors=[];hair=[]
for i,roi in enumerate(rois):
 pose=isolate(atlas.crop(((i%3)*512,(i//3)*512,(i%3+1)*512,(i//3+1)*512)));a=np.array(pose);rgb=a[:,:,:3].astype(float);y,x=np.indices(a.shape[:2]);x0,y0,x1,y1=roi
 m=(a[:,:,3]>180)&(x>=x0)&(x<x1)&(y>=y0)&(y<y1)&(rgb[:,:,0]>rgb[:,:,1]*1.2)&(rgb[:,:,1]>rgb[:,:,2]*1.3)&(np.ptp(rgb,axis=2)>35)
 labs,n=label(m);sizes=np.bincount(labs.ravel());sizes[0]=0;yy,xx=np.where(labs==sizes.argmax());assert len(xx)>100
 top=int(yy.min());axis=int(np.median(xx[yy<top+6]));anchors.append((axis,top));hair.append(dict(cell=i,roi=roi,axis=axis,crown=top,componentWidth=int(xx.max()-xx.min()+1),pixels=len(xx)))
 if i==0:
  ruler,ruler_rec=register(pose,.26,axis,top);ruler.save(P/'atlas-standing-study.png');continue
 frame,rec=register(pose,.26,axis,top,None if i<=2 else [180,194,206][i-3]);frames.append(frame);records.append(dict(rec,source='sources/entry-atlas-v1.png',cell=i,sourceCrown=[axis,top],hairComponentWidth=hair[-1]['componentWidth'],role=['','crouch','deep crouch','push','takeoff','near-prone'][i]))
frames.append(context(Image.open(swimpath).convert('RGBA'),(56,72)));assert len(frames)==9
times=[40,50,55,55,60,60,60,60,60];assert sum(times)==500
for i,im in enumerate(frames):im.save(F/f'{i:03}.png')
m=dict(name='Bill South articulated water-entry study',frameWidth=320,frameHeight=352,pivot=[160,224],standingHeight=148,precomposed=True,status='source_master_and_motion_review_pending',integration='unselected',states=[dict(id='land-swim-south',frameFiles=[f'frames/land-swim-south/{i:03}.png' for i in range(9)],frameDurationsMs=times,loop=False,facings=['south']*9,provenance='Seven newly authored complete intermediates; exact padded selected idle/swim endpoints. Fixed atlas anatomical density .26 from current South swim head/hardware; rejected atlas standing ruler not used as size authority. Two singles have separately frozen drawing-density calibration from original master hair, not posed heights. Whole head/hardware/segment matching remains provisional. All master, motion/contact, helmet/native acceptance pending.')])
(P/'bare/manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
frames[0].save(P/'bare/source-enter.png',save_all=True,append_images=frames[1:],duration=times,loop=1,disposal=0,blend=0)
with Image.open(P/'bare/source-enter.png') as ap:
 assert ap.n_frames==9 and ap.info['loop']==1
 for i,im in enumerate(frames):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==times[i]
board=Image.new('RGB',(1600,800),'#182932');d=ImageDraw.Draw(board)
for i,(name,im) in enumerate(list(zip(['idle','gentle crouch','authored middle crouch','crouch','deep crouch','push','takeoff','near-prone','selected swim'],frames))+[('atlas ruler (rejected authority)',ruler)]):
 x=i%5*320;y=i//5*400;board.paste(im,(x,y+25),im);d.text((x+5,y+5),str(i)+' '+name,fill='white');d.line((x,y+249,x+319,y+249),fill='#609890')
board.save(P/'entry-contact.png')
refs=[R/'bill-video-south-v1/master-source.png',R/'bill-swim-south-coherent-v1/sources/swim-v1.png',idlepath]
e=dict(scope='Source-only South9pose500ms finite study. Seven authored intermediates, no reused widened crouch; no helmet, native proof, normal selection or owner-profile access.',generation='exec-618c4264-bb20-4644-9063-27256558e2aa',earlyGeneration='exec-d2f67ae8-e264-4ce6-bd02-e021c9d0d457',middleGeneration='exec-d8e63537-4571-43b9-87c8-b70f958fae4a',sourceCalibration=dict(originalStandingSpan=1295,originalHairComponent=135,earlyHairComponent=149,middleHairComponent=166,earlyDensity=early_density,middleDensity=middle_density,scope='Fixed density per complete independent source based on hair semantic component, not complete head or segment proof; no posed height fitting.'),refs={f.relative_to(R).as_posix():sha(f) for f in refs},sourceHashes={f.name:sha(f) for f in S.iterdir() if f.is_file()},registrations=records,hairDiagnostics=hair,ruler=ruler_rec,rulerDecision='Rejected as anatomical height authority: source opaque span483 at shared .26 gives125.58native vsselected148. Do not solve by posed bbox scaling. Action atlas .26 follows existing South head/hardware density; full segment/proportion acceptance provisional.',endpointExact=True,rejectedReusedCrouch=kneelpath.relative_to(R).as_posix(),decodedFramesExact=9,finiteLoopCount=1,timelineMs=500,materialGrade='Unmodified authored source colours; shared master grading still pending.',visualReview='Pending registered whole sequence/master inspection.')
(P/'entry-review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
data=json.dumps(dict(frames=m['states'][0]['frameFiles'],times=times))
html="""<!doctype html><meta charset="utf-8"><title>Bill South entry study</title><style>body{background:#182932;color:#eee;font:17px sans-serif}canvas{height:min(600px,calc(100vh - 190px));width:auto;max-width:100%}img{max-width:100%}button,select{font:inherit;margin:6px;padding:6px}</style><h1>Bill South water-entry study</h1><p>Seven new whole poses, exact selected idle and swim endpoints. Master/grade/motion, helmet and native contact remain pending.</p><button id="play">Play once</button><button id="next">Next pose</button><select id="speed"><option value="1">Normal</option><option value="4">Quarter</option></select><span id="pose"></span><br><canvas width="640" height="704"></canvas><br><img src="entry-contact.png"><script>const data=DATA;const images=data.frames.map(s=>{const im=new Image();im.src='bare/'+s;return im}),ctx=document.querySelector('canvas').getContext('2d');let index=0,run=0;function draw(){ctx.clearRect(0,0,640,704);if(images[index].complete)ctx.drawImage(images[index],0,0,640,704);document.getElementById('pose').textContent='Pose '+index}images.forEach(im=>im.onload=draw);document.getElementById('next').onclick=()=>{run++;index=(index+1)%9;draw()};document.getElementById('play').onclick=async()=>{const token=++run;for(index=0;index<9;index++){if(run!==token)return;draw();await new Promise(r=>setTimeout(r,data.times[index]*Number(document.getElementById('speed').value)))}index=8;draw()};draw();</script>"""
(P/'index.html').write_text(html.replace('DATA',data),encoding='utf-8')
print(json.dumps(dict(frames=9,newPoses=7,reusedWholeCrouch=0,decodedFramesExact=9,finiteLoop=1,atlasDensity=.26,originalMasterDensity=density,scope='unselected source study')))
