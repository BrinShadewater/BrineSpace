"""Package authored helmet videos at one fixed body scale; preserve accepted west bytes."""
from pathlib import Path
import json,hashlib,shutil
import imageio.v2 as iio
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent
SCALE=148/911*763/778/.75
SIZE=round(768*SCALE);OFFSET=(92-round(384*SCALE),172-round(747*SCALE))
SELECTION={'east':(84,43),'south':(27,34),'north':(55,42)}
manifest={'name':'Veld four-direction helmet walk candidates','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'precomposed':True,'status':'candidate_not_installed','strideDistanceCells':{},'states':[]}
frames={};audits={}
for direction in ['west','east','south','north']:
 dest=P/'frames'/('walk-'+direction);dest.mkdir(parents=True,exist_ok=True)
 row=[];paths=[];bounds=[];source_clips=0
 scale=SCALE/(870/1024) if direction in ['east','south'] else SCALE
 size=round(768*scale)
 sole=747*(870/1024)+36*.75 if direction in ['east','south'] else 747
 offset=(92-round(384*scale),172-round(sole*scale))
 if direction=='west':
  old=P.parent/'veld-helmet-side-v1';m=json.loads((old/'manifest.json').read_text());e=m['states'][0]
  for j,f in enumerate(e['frameFiles']):
   target=dest/f'{j:03d}.png';shutil.copyfile(old/f,target);row.append(Image.open(target).convert('RGBA'));paths.append(target.relative_to(P).as_posix())
  start,count=52,len(row);source=old/'source.mp4'
 else:
  start,count=SELECTION[direction];source=P/(f'{direction}-padded-source.mp4' if direction in ['east','south'] else f'{direction}-source.mp4');r=iio.get_reader(source);raw=[np.asarray(x) for x in r];r.close()
  for j,a in enumerate(raw[start:start+count]):
   v=a.astype(float);key=(v[:,:,1]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,2]*1.3)&(v[:,:,1]>90)
   lab,n=ndimage.label(~key);sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==sizes.argmax();y,x=np.where(mask)
   source_clips+=int(x.min()==0 or y.min()==0 or x.max()==a.shape[1]-1 or y.max()==a.shape[0]-1)
   im=Image.fromarray(np.dstack([a,mask.astype('uint8')*255]));frame=Image.new('RGBA',(184,184));frame.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),offset)
   target=dest/f'{j:03d}.png';frame.save(target);row.append(frame);paths.append(target.relative_to(P).as_posix())
 durations=[round((j+1)*1500/count)-round(j*1500/count) for j in range(count)]
 manifest['states'].append({'id':'walk-'+direction,'frameFiles':paths,'frameCount':count,'frameDurationsMs':durations,'loop':True,'sourceFrames':list(range(start,start+count)),'sharedScale':scale,'sharedOffset':list(offset),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceVideo':str(source.relative_to(P)) if source.parent==P else '../veld-helmet-side-v1/source.mp4'})
 manifest['strideDistanceCells']['walk-'+direction]=69/384
 arr=[np.array(x).astype(float)/255 for x in row];steps=[float(np.mean(np.abs(arr[j]-arr[(j+1)%count]))) for j in range(count)]
 for im in row:
  a=np.array(im);y,x=np.where(a[:,:,3]>=128);bounds.append([int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)])
 audits[direction]={'frames':count,'sourceRangeInclusive':[start,start+count-1],'durationMs':1500,'sourceDurationMs':round(count*1000/24),'sourceClippedFrames':source_clips,'exportClippedFrames':sum(b[0]<=0 or b[1]<=0 or b[2]>=184 or b[3]>=184 for b in bounds),'opaqueHeightRange':[min(b[3]-b[1] for b in bounds),max(b[3]-b[1] for b in bounds)],'seamDifference':steps[-1],'internalMedianDifference':float(np.median(steps[:-1])),'internalMaxDifference':max(steps[:-1])}
 assert source_clips==0 and audits[direction]['exportClippedFrames']==0, direction+' clipping'
 frames[direction]=row
 # Individual playback at source pixels, 2x and gameplay scale.
 previews=[]
 for im in row:
  bg=Image.new('RGB',(368,460),'#263139');d=ImageDraw.Draw(bg);d.text((12,10),direction.upper()+' / HELMET / 1500ms cycle',fill='white');big=im.resize((368,368),Image.Resampling.NEAREST);bg.paste(big,(0,30),big);tiny=im.resize((81,81),Image.Resampling.LANCZOS);bg.paste(tiny,(143,377),tiny);previews.append(bg)
 gd=[10*(round((j+1)*150/count)-round(j*150/count)) for j in range(count)]
 previews[0].save(P/f'{direction}-review.gif',save_all=True,append_images=previews[1:],duration=gd,loop=0,optimize=False)
 # Twelve sequential samples, including loop end, for inspection.
 sheet=Image.new('RGB',(184*6,210*2),'#263139');d=ImageDraw.Draw(sheet)
 for j,idx in enumerate(np.linspace(0,count-1,12).astype(int)):
  x=(j%6)*184;y=(j//6)*210;sheet.paste(row[idx],(x,y+20),row[idx]);d.text((x+5,y+4),f'{direction} {start+idx}',fill='white')
 sheet.save(P/f'{direction}-loop-contact.png')
combined=[]
for i in range(60):
 bg=Image.new('RGB',(736,880),'#263139');d=ImageDraw.Draw(bg)
 for j,direction in enumerate(['south','east','north','west']):
  row=frames[direction];im=row[int(i*len(row)/60)];x=(j%2)*368;y=(j//2)*440
  d.text((x+12,y+8),direction.upper()+' / HELMET WALK',fill='white');big=im.resize((368,368),Image.Resampling.NEAREST);bg.paste(big,(x,y+25),big);tiny=im.resize((64,64),Image.Resampling.LANCZOS);bg.paste(tiny,(x+152,y+374),tiny)
 combined.append(bg)
combined[0].save(P/'four-direction-review.gif',save_all=True,append_images=combined[1:],duration=[20,30]*30,loop=0,optimize=False)
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(P/'checks.json').write_text(json.dumps({'directions':audits,'processing':'Original video RGB; green key; fixed body scale per input framing and fixed offset. West frame bytes preserved. No per-frame normalization.','status':'candidate_not_installed'},indent=2)+'\n',encoding='utf-8')
print(json.dumps(audits,indent=2))
