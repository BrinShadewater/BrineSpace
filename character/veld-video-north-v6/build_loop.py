from pathlib import Path
import imageio.v2 as iio
from PIL import Image,ImageDraw
import numpy as np,json
from scipy import ndimage
P=Path(__file__).resolve().parent
r=iio.get_reader(P/'source.mp4'); raw=[np.asarray(a) for a in r]; r.close()
clean=[]; small=[]
for a in raw:
 v=a.astype(float); key=(v[:,:,1]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,2]*1.3)&(v[:,:,1]>90)
 lab,n=ndimage.label(~key); sizes=np.bincount(lab.ravel()); sizes[0]=0; mask=lab==sizes.argmax()
 # Keep the main silhouette, discard compression specks. No colour remapping.
 im=Image.fromarray(np.dstack([a,mask.astype('uint8')*255])); clean.append(im)
 sm=np.array(im.resize((96,96),Image.Resampling.LANCZOS)).astype(float)/255
 small.append(sm[:,:,:3]*sm[:,:,3:4])
scores=[]
for start in range(10,95):
 for length in range(26,55):
  end=start+length
  if end+2>=len(raw): continue
  score=sum(np.mean((small[start+k][42:]-small[end+k][42:])**2) for k in [-2,-1,0,1,2])/5
  scores.append((float(score),start,length))
scores.sort(); (P/'cycle-candidates.json').write_text(json.dumps(scores[:30],indent=2))
print(scores[:10])
sheet=Image.new('RGB',(1280,640),'#263139'); d=ImageDraw.Draw(sheet)
for j,idx in enumerate(range(24,104,4)):
 im=clean[idx].resize((128,128)); sheet.paste(im,((j%10)*128,(j//10)*320+30),im);d.text(((j%10)*128,(j//10)*320),str(idx),fill='white')
sheet.save(P/'cycle-search.png')
_,start,length=scores[0]
scale=148/683
size=round(768*scale)
offset=(92-round(384*scale),172-round(724*scale))
dest=P/'frames/walk-north';dest.mkdir(parents=True,exist_ok=True)
frames=[]; previews=[]; paths=[]
master=Image.open(P.parent/'veld-animation-pilot-v12/frames/idle-north/000.png').convert('RGBA')
for j,im in enumerate(clean[start:start+length]):
 frame=Image.new('RGBA',(184,184)); frame.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),offset)
 frame.save(dest/f'{j:03d}.png'); frames.append(frame); paths.append(f'frames/walk-north/{j:03d}.png')
 bg=Image.new('RGB',(736,448),'#263139'); d=ImageDraw.Draw(bg)
 for x,img in [(0,master),(368,frame)]:
  big=img.resize((368,368),Image.Resampling.NEAREST);bg.paste(big,(x,30),big)
 d.text((12,10),'APPROVED MASTER',fill='white');d.text((380,10),'VIDEO WALK / ORIGINAL SPEED',fill='white')
 tiny=frame.resize((56,56),Image.Resampling.LANCZOS);bg.paste(tiny,(525,390),tiny);previews.append(bg)
durations=[round((j+1)*1000/24)-round(j*1000/24) for j in range(length)]
# GIF uses centiseconds; preserve total cadence using cumulative rounding.
gifdur=[10*(round((j+1)*100/24)-round(j*100/24)) for j in range(length)]
previews[0].save(P/'north-loop-review.gif',save_all=True,append_images=previews[1:],duration=gifdur,loop=0)
sheet=Image.new('RGBA',(184*length,184))
for j,im in enumerate(frames):sheet.alpha_composite(im,(184*j,0))
sheet.save(P/'walk-north-strip.png')
manifest={'name':'Veld Hailuo north walk trial','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'status':'candidate_not_installed','sourceFrames':list(range(start,start+length)),'sharedScale':scale,'sharedOffset':offset,'states':[{'id':'walk-north','frameFiles':paths,'frameCount':length,'frameDurationsMs':durations,'loop':True,'mirrored':False}]}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2))
aa=[np.array(im).astype(float)/255 for im in frames]
diff=lambda a,b:float(np.mean(np.abs(a-b)))
steps=[diff(aa[j],aa[(j+1)%length]) for j in range(length)]
report={'frameCount':length,'durationMs':sum(durations),'sourceRangeInclusive':[start,start+length-1],'seamMeanAbsoluteDifference':steps[-1],'internalMedianDifference':float(np.median(steps[:-1])),'internalMaxDifference':max(steps[:-1]),'clippedFrames':sum(im.getbbox()[0]<=0 or im.getbbox()[2]>=184 or im.getbbox()[1]<=0 or im.getbbox()[3]>=184 for im in frames),'palettePolicy':'Original video RGB; binary source chroma mask; shared Lanczos downsampling. No per-frame colour or scale normalization.'}
assert report['clippedFrames']==0
(P/'loop-audit.json').write_text(json.dumps(report,indent=2));print(report)
