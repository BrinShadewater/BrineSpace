from pathlib import Path
import json,re,shutil
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import map_coordinates
P=Path('character/crew-polish-v1');P.mkdir(exist_ok=True);tracks=[];report={};sheet=Image.new('RGB',(1104,880),'#303b40');draw=ImageDraw.Draw(sheet);y,x=np.indices((184,184),dtype=float)
for col,who in enumerate(['bill','veld','branforth']):
 wr=Path('character/bill-side-head-v3') if who=='bill' else Path('character/crew-pose-match-v1')/who
 wm=json.loads((wr/'manifest.json').read_text());ir=Path('character/crew-idle-match-v1')/who;im=json.loads((ir/'manifest.json').read_text());states=[]
 for row,d in enumerate(['south','east','north','west']):
  w=next(s for s in wm['states'] if s['id']=='walk-'+d);idle=next(s for s in im['states'] if s['id']=='idle-'+d);arrays={}
  for s,root in [(idle,ir),(w,wr)]:
   files=[];arr=[]
   for n,f in enumerate(s['frameFiles']):
    a=np.array(Image.open(root/f).convert('RGBA'));b=a.copy();rel=f"frames/{s['id']}/{n:03}.png";dest=P/who/rel;dest.parent.mkdir(parents=True,exist_ok=True)
    if who=='branforth' and d in ['east','west'] and s is idle:
     top=int(np.where(a[:,:,3]>127)[0].min());dy=y-top;weight=np.interp(dy,[0,25,36,67,85,100],[0,0,1,1,0,0]);scale=1-.04*weight;sx=92+(x-92)/scale
     v=a.astype(float)/255;v[:,:,:3]*=v[:,:,3:4];z=np.stack([map_coordinates(v[:,:,k],[y,sx],order=3,mode='constant') for k in range(4)],2);alpha=z[:,:,3:4];z[:,:,:3]=np.divide(z[:,:,:3],alpha,out=np.zeros_like(z[:,:,:3]),where=alpha>0);b=np.clip(np.rint(z*255),0,255).astype('uint8');b[weight==0]=a[weight==0];assert np.array_equal(a[weight==0],b[weight==0]);Image.fromarray(b).save(dest)
    else:shutil.copyfile(root/f,dest)
    files.append(rel);arr.append(b)
   s['frameFiles']=files;states.append(s);arrays[s['id']]=arr
  wa=arrays[w['id']];diff=[]
  for i,a in enumerate(wa):
   b=wa[(i+1)%len(wa)];aa=a.astype(float)/255;bb=b.astype(float)/255;aa[:,:,:3]*=aa[:,:,3:4];bb[:,:,:3]*=bb[:,:,3:4];diff.append(float(np.mean(np.abs(aa-bb))))
  report[who+'-'+d]={'walkFrames':len(wa),'idleFrames':len(arrays[idle['id']]),'seamDifference':diff[-1],'medianAdjacentDifference':float(np.median(diff[:-1])),'walkFilesCopiedExactly':True,'timingUnchanged':True,'idleTorsoWidthScale':.96 if who=='branforth' and d in ['east','west'] else 1}
  for k,a in enumerate([arrays[idle['id']][0],wa[0]]):
   img=Image.fromarray(a);sheet.paste(img,(col*368+k*184,row*220+25),img)
  draw.text((col*368+5,row*220+3),who+' '+d+' idle / walk',fill='white')
  tracks.append(dict(label=who.title()+' '+d,row=row,col=col,idle=who+'/'+idle['frameFiles'][0],idleFiles=[who+'/'+f for f in idle['frameFiles']],idleDurations=idle['frameDurationsMs'],files=[who+'/'+f for f in w['frameFiles']],durations=w['frameDurationsMs']))
 wm['states']=states;(P/who/'manifest.json').write_text(json.dumps(wm,indent=2))
sheet.save(P/'contact.png');(P/'validation.json').write_text(json.dumps(report,indent=2))
h=Path('character/crew-pose-match-v1/index.html').read_text();h=re.sub(r'const tracks=.*?;let ready=',lambda _:'const tracks='+json.dumps(tracks)+';let ready=',h);h=h.replace('Crew pose proportion matching','Crew polish review');h=re.sub(r'<p>.*?</p>','<p>Latest Bill heads retained. James side idle torso narrowed 4% to reduce the idle/walk jump. Walk frames and timing unchanged. Check transition mode at each gameplay size. Preview only.</p>',h,count=1);h=h.replace('<canvas','<label> Speed <select id="speed"><option value="1">Normal</option><option value="0.5">Half speed</option><option value="0.25">Quarter speed</option></select></label><canvas',1);h=h.replace('t+=now-last','t+=(now-last)*Number(document.getElementById("speed").value)');(P/'index.html').write_text(h)
print(json.dumps({'walkFrames':sum(v['walkFrames'] for v in report.values()),'idleFrames':sum(v['idleFrames'] for v in report.values()),'changedIdleFrames':2,'seamRatios':{k:round(v['seamDifference']/v['medianAdjacentDifference'],2) for k,v in report.items()}}))
