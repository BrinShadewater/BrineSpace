"""Fixed-scale extraction, loop search and master comparison; no invented poses."""
from pathlib import Path
import json,hashlib
import numpy as np,imageio.v2 as iio
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent
cfg=json.loads((P/'source-selection.json').read_text());scale=cfg['scaleAt768'];offset=cfg['offsetAt768'];size=round(768*scale)
r=iio.get_reader(P/'source.mp4');raw=[np.asarray(a) for a in r];fps=r.get_meta_data()['fps'];r.close()
frames=[];smalls=[];bounds=[];source_clips=[];colour=[];corrected_colour=[]
gain=np.array([69/75,67/69,65/70]) # One constant neutral-midtone correction for the entire clip.
def fabric(a,mask):
 v=a.astype(float);good=mask&(np.ptp(v,axis=2)<24)&(v.mean(axis=2)>25)&(v.mean(axis=2)<145)
 # Broad neutral midtone diagnostic, not semantic segmentation or an exact palette test.
 return np.percentile(v[good],[25,50,75],axis=0).tolist()
ref=np.array(Image.open(P/'master-input.png').resize((768,768),Image.Resampling.LANCZOS));refkey=(ref[:,:,1].astype(float)>ref[:,:,0]*1.3)&(ref[:,:,1].astype(float)>ref[:,:,2]*1.3)&(ref[:,:,1]>90)
for a in raw:
 v=a.astype(float);key=(v[:,:,1]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,2]*1.3)&(v[:,:,1]>90)
 lab,_=ndimage.label(~key);counts=np.bincount(lab.ravel());counts[0]=0;mask=lab==counts.argmax();ys,xs=np.where(mask);source_clips.append(bool(xs.min()==0 or ys.min()==0 or xs.max()==767 or ys.max()==767));colour.append(fabric(a,mask))
 value=v.mean(axis=2);weight=np.clip((40-np.ptp(v,axis=2))/16,0,1)*np.clip((160-value)/35,0,1)*np.clip(value/25,0,1)
 corrected=np.rint(v+(v*gain-v)*weight[:,:,None]).clip(0,255).astype('uint8');corrected_colour.append(fabric(corrected,mask))
 im=Image.fromarray(np.dstack([corrected,mask.astype('uint8')*255]));f=Image.new('RGBA',(184,184));f.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),tuple(offset));frames.append(f)
 aa=np.array(f);ys,xs=np.where(aa[:,:,3]>=128);bounds.append([int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)])
 small=np.array(f.resize((92,92),Image.Resampling.LANCZOS)).astype(float)/255;smalls.append(small[:,:,:3]*small[:,:,3:4])
scores=[]
for start in range(12,min(65,len(raw)-60)):
 for length in range(60,105):
  end=start+length
  if end+2>=len(raw) or any(source_clips[start:end]):continue
  score=sum(np.mean((smalls[start+k][45:]-smalls[end+k][45:])**2) for k in [-2,-1,0,1,2])/5;scores.append((float(score),start,length))
scores.sort();(P/'cycle-candidates.json').write_text(json.dumps(scores[:30],indent=2)+'\n')
sheet=Image.new('RGB',(184*8,210*3),'#263139');draw=ImageDraw.Draw(sheet)
for j,n in enumerate(np.linspace(0,len(raw)-1,24).astype(int)):
 x=j%8*184;y=j//8*210;sheet.paste(frames[n],(x,y+20),frames[n]);draw.text((x+5,y+4),f'Source {n}',fill='white')
sheet.save(P/'source-contact.png')
_,start,length=scores[0];indices=list(range(start,start+length));dest=P/'frames/walk-west';dest.mkdir(parents=True,exist_ok=True);paths=[]
for j,n in enumerate(indices):
 path=dest/f'{j:03d}.png';frames[n].save(path);paths.append(path.relative_to(P).as_posix())
durations=[round((i+1)*1000/fps)-round(i*1000/fps) for i in range(length)]
manifest=dict(name='Branforth west walk pilot from revised side master',status='candidate_not_installed',frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,precomposed=True,sharedScale=scale,sharedOffset=offset,states=[dict(id='walk-west',frameCount=length,frameFiles=paths,frameDurationsMs=durations,loop=True,sourceFrames=indices,sourceVideo='source.mp4',mirrored=False)])
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
master=Image.open(P/'master-standing.png').convert('RGBA')
def preview(indices,path):
 out=[]
 for n in indices:
  bg=Image.new('RGB',(736,445),'#263139');d=ImageDraw.Draw(bg)
  for x,im in [(0,master),(368,frames[n])]:
   big=im.resize((368,368),Image.Resampling.NEAREST);bg.paste(big,(x,25),big)
  tiny=frames[n].resize((64,64),Image.Resampling.LANCZOS);bg.paste(tiny,(520,380),tiny);d.text((10,7),'BRANFORTH / SELECTED MASTER',fill='white');d.text((378,7),'WEST WALK / SOURCE SPEED',fill='white');out.append(bg)
 out[0].save(path,save_all=True,append_images=out[1:],duration=[10*(round((i+1)*100/fps)-round(i*100/fps)) for i in range(len(out))],loop=0,optimize=False)
preview(indices,P/'west-loop-review.gif');None
diff=[float(np.mean(abs(smalls[indices[i]]-smalls[indices[(i+1)%length]]))) for i in range(length)];bs=[bounds[n] for n in indices]
audit=dict(sourceFrameCount=len(raw),sourceFps=fps,selectedSourceFrames=indices,sourceSha256=hashlib.sha256((P/'source.mp4').read_bytes()).hexdigest(),sourceClippedFrames=sum(source_clips[n] for n in indices),exportClippedFrames=sum(b[0]<=0 or b[1]<=0 or b[2]>=184 or b[3]>=184 for b in bs),heightRange=[min(b[3]-b[1] for b in bs),max(b[3]-b[1] for b in bs)],soleYRange=[min(b[3] for b in bs),max(b[3] for b in bs)],seamDifference=diff[-1],internalMedianDifference=float(np.median(diff[:-1])),internalMaxDifference=max(diff[:-1]),masterNeutralMidtoneQuartiles=fabric(ref,~refkey),selectedNeutralMidtoneMedianRange=[np.min([colour[n][1] for n in indices],axis=0).tolist(),np.max([colour[n][1] for n in indices],axis=0).tolist()],processing='Original source RGB, green key, fixed body scale; no recolour, pose interpolation, mirroring or per-frame geometry normalization.')
audit['processing']='Green key and fixed body scale. One constant neutral-midtone RGB gain for whole clip, chromatic patches/skin and bright silver excluded by feathered mask; no pose interpolation, mirroring or per-frame geometry normalization.'
audit['neutralMidtoneGain']=gain.tolist();audit['correctedNeutralMidtoneMedianRange']=[np.min([corrected_colour[n][1] for n in indices],axis=0).tolist(),np.max([corrected_colour[n][1] for n in indices],axis=0).tolist()]
(P/'checks.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit))
