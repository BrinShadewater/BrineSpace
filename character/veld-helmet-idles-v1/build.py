"""Extract true idle motion using fixed walk-compatible registration."""
from pathlib import Path
import json,hashlib
import imageio.v2 as iio,numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent
walk=json.loads((P.parent/'veld-helmet-walks-v1/manifest.json').read_text())
manifest={'name':'Veld matching helmet idle candidates','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'precomposed':True,'status':'candidate_not_installed','states':[]}
audits={};clips={}
sheet=Image.new('RGB',(184*8,210*4),'#263139');draw=ImageDraw.Draw(sheet)
for row,direction in enumerate(['south','east','north','west']):
 profile=next(e for e in walk['states'] if e['id']=='walk-'+direction);scale=profile['sharedScale'];size=round(768*scale);offset=profile['sharedOffset'];source=P/f'{direction}-source.mp4';r=iio.get_reader(source);raw=[np.asarray(x) for x in r];r.close();allframes=[];small=[];bounds=[];source_clips=[]
 for a in raw:
  v=a.astype(float);key=(v[:,:,1]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,2]*1.3)&(v[:,:,1]>90);lab,n=ndimage.label(~key);sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==sizes.argmax();ys,xs=np.where(mask);source_clips.append(xs.min()==0 or ys.min()==0 or xs.max()==767 or ys.max()==767)
  im=Image.fromarray(np.dstack([a,mask.astype('uint8')*255]));f=Image.new('RGBA',(184,184));f.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),tuple(offset));allframes.append(f)
  a=np.array(f);ys,xs=np.where(a[:,:,3]>=128);bounds.append([int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]);sm=np.array(f.resize((92,92),Image.Resampling.LANCZOS)).astype(float)/255;small.append(sm[:,:,:3]*sm[:,:,3:4])
 scores=[]
 for start in range(24,65):
  for length in range(48,73):
   end=start+length
   if end+2>=len(small) or any(source_clips[start:end]):continue
   score=sum(np.mean((small[start+k]-small[end+k])**2) for k in [-2,-1,0,1,2])/5;scores.append((float(score),start,length))
 scores.sort();score,start,count=scores[0];source_count=count;indices=list(range(start,start+count))+list(range(start+count-2,start,-1));chosen=[allframes[i] for i in indices];count=len(indices);dest=P/'frames'/('idle-'+direction);dest.mkdir(parents=True,exist_ok=True);paths=[]
 for i,im in enumerate(chosen):
  target=dest/f'{i:03d}.png';im.save(target);paths.append(target.relative_to(P).as_posix())
 durations=[round((i+1)*1000/24)-round(i*1000/24) for i in range(count)]
 manifest['states'].append({'id':'idle-'+direction,'frameCount':count,'frameFiles':paths,'frameDurationsMs':durations,'loop':True,'sourceFrames':indices,'motionDerivation':'Forward then reverse existing breathing poses; endpoints not duplicated','sourceVideo':source.name,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sharedScale':scale,'sharedOffset':offset})
 selected_bounds=[bounds[i] for i in indices];a=[np.asarray(f).astype(float)/255 for f in chosen];diff=[float(np.mean(np.abs(a[i]-a[(i+1)%count]))) for i in range(count)]
 audits[direction]={'sourceStart':start,'uniqueSourceFrames':source_count,'frames':count,'durationMs':sum(durations),'sourceClippedFrames':int(sum(source_clips[i] for i in indices)),'exportClippedFrames':sum(b[0]<=0 or b[1]<=0 or b[2]>=184 or b[3]>=184 for b in selected_bounds),'soleYRange':[min(b[3] for b in selected_bounds),max(b[3] for b in selected_bounds)],'heightRange':[min(b[3]-b[1] for b in selected_bounds),max(b[3]-b[1] for b in selected_bounds)],'seamDifference':diff[-1],'internalMedianDifference':float(np.median(diff[:-1])),'internalMaxDifference':max(diff[:-1])}
 assert audits[direction]['sourceClippedFrames']==0 and audits[direction]['exportClippedFrames']==0
 clips[direction]=chosen
 for col,i in enumerate(np.linspace(0,len(allframes)-1,8).astype(int)):
  im=allframes[i];sheet.paste(im,(col*184,row*210+20),im);draw.text((col*184+5,row*210+3),f'{direction} source {i}',fill='white')
sheet.save(P/'source-contact.png')
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');(P/'checks.json').write_text(json.dumps({'directions':audits,'processing':'Original RGB, green key, constant registration from matching walk. Forward/reverse authored breathing poses form a seamless loop; no repeated endpoint, blending, per-frame resizing or recolouring.','installed':False},indent=2)+'\n',encoding='utf-8')
review=[]
for i in range(144):
 bg=Image.new('RGB',(736,880),'#263139');draw=ImageDraw.Draw(bg)
 for j,d in enumerate(['south','east','north','west']):
  row=clips[d];im=row[i%len(row)];x=j%2*368;y=j//2*440;draw.text((x+10,y+8),d.upper()+' / HELMET IDLE',fill='white');big=im.resize((368,368),Image.Resampling.NEAREST);bg.paste(big,(x,y+25),big);tiny=im.resize((64,64),Image.Resampling.LANCZOS);bg.paste(tiny,(x+152,y+374),tiny)
 review.append(bg)
review[0].save(P/'four-idles-review.gif',save_all=True,append_images=review[1:],duration=[40,40,40,50,40,40]*24,loop=0,optimize=False)
print(json.dumps(audits,indent=2))
