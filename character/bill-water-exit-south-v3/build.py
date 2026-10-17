from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parent;F=P/'bare/frames/swim-land-south';F.mkdir(parents=True,exist_ok=True)
def isolate(im):
 a=np.array(im.convert('RGBA'));labs,n=label(a[:,:,3]>180);c=np.bincount(labs.ravel());c[0]=0;keep=binary_dilation(labs==c.argmax(),iterations=3)&(a[:,:,3]>0);a[~keep]=0;return Image.fromarray(a)
def hair(im,roi):
 a=np.array(im);r=a[:,:,:3].astype(float);y,x=np.indices(a.shape[:2]);x0,y0,x1,y1=roi;m=(a[:,:,3]>180)&(x>=x0)&(x<x1)&(y>=y0)&(y<y1)&(r[:,:,0]>r[:,:,1]*1.2)&(r[:,:,1]>r[:,:,2]*1.3)&(np.ptp(r,axis=2)>35);labs,n=label(m);c=np.bincount(labs.ravel());c[0]=0;yy,xx=np.where(labs==c.argmax());top=int(yy.min());return int(np.median(xx[yy<top+6])),top,int(xx.max()-xx.min()+1)
def context(path,shift):
 im=Image.open(path).convert('RGBA');out=Image.new('RGBA',(320,352));out.paste(im,shift);assert out.crop((shift[0],shift[1],shift[0]+im.width,shift[1]+im.height)).tobytes()==im.tobytes();return out
frames=[context(R/'bill-swim-south-coherent-v1/frames/swim-south/000.png',(56,72))];records=[];atlas=Image.open(P/'sources/exit-atlas-v1.png').convert('RGBA');assert atlas.size==(1536,1024)
# Actual source layout straddles requested row boundary; use common465px split,
# preserving complete isolated figures. No per-pose rescaling.
for i in range(6):
 top=0 if i<3 else 465;bottom=465 if i<3 else 1024
 im=isolate(atlas.crop((i%3*512,top,i%3*512+512,bottom)));axis,crown,width=hair(im,(160,0,350,300));scale=.26
 if i in [4,5]:
  im.save(P/('rejected-rising-squat-atlas.png' if i==4 else 'rejected-near-standing-atlas.png'));continue
 a=np.array(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS));yy,xx=np.where(a[:,:,3]>180)
 shift=(160-round(axis*scale),[194,167][i]-round(crown*scale)) if i<2 else (160-round(axis*scale),224-int(yy.max())-1)
 out=Image.new('RGBA',(320,352));out.paste(Image.fromarray(a),shift);assert np.count_nonzero(np.array(out)[:,:,3])==np.count_nonzero(a[:,:,3]);frames.append(out);records.append(dict(source='sources/exit-atlas-v1.png',cell=i,sourceCell=[i%3*512,top,i%3*512+512,bottom],sourceAxis=axis,sourceCrown=crown,hairWidth=width,scale=scale,translation=shift,crown=[160,round(crown*scale)+shift[1]],alphaBounds=out.getchannel('A').getbbox()))
for source_name,roi in [('rising-squat-master-v3.png',(350,150,680,400)),('near-standing-master-v3.png',(350,20,680,230))]:
 im=isolate(Image.open(P/'sources'/source_name));axis,crown,width=hair(im,roi);scale=148/1295;a=np.array(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS));yy,xx=np.where(a[:,:,3]>180);shift=(160-round(axis*scale),224-int(yy.max())-1);out=Image.new('RGBA',(320,352));out.paste(Image.fromarray(a),shift);assert np.count_nonzero(np.array(out)[:,:,3])==np.count_nonzero(a[:,:,3]);frames.append(out);records.append(dict(source='sources/'+source_name,sourceAxis=axis,sourceCrown=crown,hairWidth=width,scale=scale,translation=shift,crown=[160,round(crown*scale)+shift[1]],alphaBounds=out.getchannel('A').getbbox()))
frames.append(context(R/'crew-runtime-matte-v1/bill/frames/idle-south-breathing-v1/000.png',(68,52)));assert len(frames)==8;times=[40,60,65,65,65,65,65,75];assert sum(times)==500
for i,im in enumerate(frames):im.save(F/f'{i:03}.png')
m=dict(name='Bill South independently authored water exit candidate',frameWidth=320,frameHeight=352,pivot=[160,224],standingHeight=148,precomposed=True,status='source_master_motion_review_pending',integration='unselected',states=[dict(id='swim-land-south',frameFiles=[f'frames/swim-land-south/{i:03}.png' for i in range(8)],frameDurationsMs=times,loop=False,facings=['south']*8)])
(P/'bare/manifest.json').write_text(json.dumps(m,indent=2)+'\n');frames[0].save(P/'bare/source-exit.png',save_all=True,append_images=frames[1:],duration=times,loop=1,disposal=0,blend=0)
with Image.open(P/'bare/source-exit.png') as ap:
 assert ap.n_frames==8 and ap.info['loop']==1
 for i,im in enumerate(frames):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==times[i]
board=Image.new('RGB',(2560,400),'#182932');d=ImageDraw.Draw(board)
for i,im in enumerate(frames):board.paste(im,(i*320,25),im);d.text((i*320+5,5),f'{i} '+['selected swim','elbows retract','palms push','knee/boot plant','half kneel','rising squat','near standing','selected idle'][i],fill='white');d.line((i*320,249,i*320+319,249),fill='#609890')
board.save(P/'exit-contact.png')
r=dict(generation='exec-0777955b-12c4-41b0-a9ff-3f853f4b1515',nearStandingGeneration='exec-62107536-4f67-4cb8-8bbe-3c08182334d0',risingSquatGeneration='exec-444193cd-af5b-4a55-b555-6de757731ec2',registrations=records,decodedFramesExact=8,timelineMs=500,finiteLoopCount=1,endpointsExact=True,newWholePoses=6,sourceHashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (P/'sources').iterdir() if p.is_file()},scope='Independent newly authored whole exit poses, never reversed entry. Fixed atlas .26 anatomical density from existing South swim/entry source; nearstanding original-master148/1295. No per-pose occupied-height fitting. All material/head/hardware/segment/master/motion/contact acceptance provisional; no helmet/native/normal selection.',rejected='Atlas nearstanding too short at shared density; rising squat remained half-kneeling. Both retained but not selected; independent original-master-density whole source replacements.',visualReview='Pending registered full sequence inspection.')
(P/'exit-review.json').write_text(json.dumps(r,indent=2)+'\n')
html='<!doctype html><meta charset="utf-8"><title>Bill South water exit</title><style>body{background:#182932;color:#eee;font:17px sans-serif}canvas{height:min(600px,calc(100vh - 190px));width:auto;max-width:100%}img{max-width:100%}button,select{font:inherit;margin:6px;padding:6px}</style><h1>Bill South â€” independent water exit</h1><p>Six new complete exit poses. Source candidate: master, material, proportions, motion and physical contact remain under review.</p><button id="play">Play once</button><button id="next">Next pose</button><select id="speed"><option value="1">Normal</option><option value="4">Quarter</option></select><span id="pose"></span><br><canvas width="640" height="704"></canvas><br><img src="exit-contact.png"><script>const times='+json.dumps(times)+';const images=times.map((_,i)=>{const im=new Image();im.src="bare/frames/swim-land-south/"+String(i).padStart(3,"0")+".png";return im}),ctx=document.querySelector("canvas").getContext("2d");let index=0,run=0;function draw(){ctx.clearRect(0,0,640,704);if(images[index].complete)ctx.drawImage(images[index],0,0,640,704);document.getElementById("pose").textContent="Pose "+index}images.forEach(im=>im.onload=draw);document.getElementById("next").onclick=()=>{run++;index=(index+1)%8;draw()};document.getElementById("play").onclick=async()=>{const token=++run;for(let i=0;i<8;i++){if(run!==token)return;index=i;draw();await new Promise(r=>setTimeout(r,times[i]*Number(document.getElementById("speed").value)))}};draw();</script>'
(P/'index.html').write_text(html,encoding='utf-8');print(json.dumps(dict(frames=8,newWholePoses=6,decodedExact=8,finiteLoop=1)))
