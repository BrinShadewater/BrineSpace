"""Composite imagegen-authored fixed surfaces into immutable original animations.
Original frames remain untouched; only the manifest points to polished derivatives.
"""
from pathlib import Path
import json,hashlib,math
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
from build_surface_polish import R,P,names,arr,fit,warp

def main():
 baseline=P/'manifest-before-polish.json'
 current=json.loads((R/'manifest.json').read_text())
 if not baseline.exists() or 'surfacePolish' not in current:
  baseline.write_bytes((R/'manifest.json').read_bytes())
 data=json.loads(baseline.read_text());states={s['id']:s for s in data['states']};groups=[]
 for h in names:groups.append((h,h,data['headings'][h]['pose'],[states[f'idle-{h}'],states[f'move-{h}']]))
 for h in ['north','east','south','west']:
  for a in ['mine','collect','weld','repair']:
   s=states[f'work-{a}-{h}'];groups.append((a+'-'+h,h,s.get('pose',data['actions'][a]['pose']),[s,states[f'job-{a}-{h}']]))
 report=[];board=Image.new('RGB',(1280,1536),'#192930');draw=ImageDraw.Draw(board);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
 for gi,(key,h,posepath,clips) in enumerate(groups):
  source=arr(R/'poses'/f'{h}.png');target=arr(R/posepath);mask=np.array(Image.open(P/f'{h}-mask.png'))/255.; rgb=np.load(P/f'{h}-rgb.npy')
  v=[0,0,1,1] if key==h else fit(source,target,mask)
  paint=warp(rgb,v);w=warp(mask[:,:,None],v)[:,:,0]
  # Protect structure and coloured fittings in both registered images. Work
  # sources have small lens/vent differences which must never be pasted over.
  oldrgb=target[:,:,:3].astype(float)
  protected=(np.ptp(oldrgb,axis=2)>24)|(oldrgb.mean(2)<64)
  protected|=(np.ptp(paint,axis=2)>24)|(paint.mean(2)<64)
  protected|=ndimage.gaussian_gradient_magnitude(oldrgb.mean(2),.65)>15
  protected|=ndimage.gaussian_gradient_magnitude(paint.mean(2),.65)>15
  protected=ndimage.binary_dilation(protected,iterations=2)
  w*=np.clip(ndimage.distance_transform_edt(~protected)/2,0,1)
  # Only pixels proven stationary across both travel clips or work+complete job.
  stable=target[:,:,3]>245
  for clip in clips:
   for path in clip['frameFiles']:
    frame=arr(R/path);stable &= np.max(np.abs(frame.astype(int)-target.astype(int)),axis=2)<=1
  w*=stable;assert (w>.1).sum()>350,(key,int((w>.1).sum()))
  (P/'masks').mkdir(exist_ok=True);Image.fromarray((w*255).astype('uint8')).save(P/'masks'/f'{key}.png')
  def polished(old):
   out=old.copy();out[:,:,:3]=np.clip(old[:,:,:3]*(1-w[:,:,None])+paint*w[:,:,None],0,255).astype('uint8');return out
  posed=polished(target);p=P/'poses'/f'{key}.png';p.parent.mkdir(exist_ok=True);Image.fromarray(posed).save(p)
  newpose=p.relative_to(R).as_posix()
  if key==h:data['headings'][h]['pose']=newpose
  else:
   a=key.rsplit('-',1)[0];data['actions'][a]['directions'][h]['pose']=newpose
   if h=='south':data['actions'][a]['pose']=newpose
  checks=0
  for clip in clips:
   if 'pose' in clip:clip['pose']=newpose
   paths=[];outdir=P/'frames'/clip['id'];outdir.mkdir(parents=True,exist_ok=True)
   for n,path in enumerate(clip['frameFiles']):
    old=arr(R/path);out=polished(old)
    assert np.array_equal(old[:,:,3],out[:,:,3]);assert np.array_equal(old[w==0],out[w==0]);checks+=1
    dest=outdir/f'{n:03}.png';Image.fromarray(out).save(dest,compress_level=3);paths.append(dest.relative_to(R).as_posix())
   clip['frameFiles']=paths
   # Only changed body atlases are repacked; existing cargo, effects and status stay intact.
   atlas=Image.new('RGBA',(2048,math.ceil(len(paths)/8)*256))
   for n,path in enumerate(paths):atlas.paste(Image.open(R/path),(n%8*256,n//8*256))
   ap=P/'atlases'/f"{clip['id']}.png";ap.parent.mkdir(exist_ok=True);temp=ap.with_suffix('.tmp.png');atlas.save(temp,compress_level=3);temp.replace(ap)
   clip['atlas']={'path':ap.relative_to(R).as_posix(),'columns':8,'rows':math.ceil(len(paths)/8),'frameCount':len(paths)}
  report.append({'pose':key,'registration':list(v),'fixedSurfacePixels':int((w>.1).sum()),'framesChecked':checks,'alphaAndOutsideMask':'identical'})
  x=gi%5*256;y=gi//5*300;draw.text((x+6,y+3),key,font=font,fill='white');im=Image.fromarray(posed);board.paste(im,(x,y+18),im)
  print(key,checks,'frames;',int((w>.1).sum()),'fixed pixels',flush=True)
 board.save(P/'all-polished-poses.png')
 data['surfacePolish']={'source':'polish/heading-polish-v2.png','method':'Imagegen painted surfaces registered and composited only onto stationary pixels. Original alpha, limbs, blades and timeline retained.','baselineManifest':'polish/manifest-before-polish.json','limits':'Shading refinement inside existing geometry; no new camera projection or world-size approval.'}
 data['sourceFiles'].append({'path':'polish/heading-polish-v2.png','sha256':hashlib.sha256((P/'heading-polish-v2.png').read_bytes()).hexdigest()})
 (P/'validation.json').write_text(json.dumps({'groups':report,'bodyFrames':sum(x['framesChecked'] for x in report),'status':'pass'},indent=2))
 temp=R/'manifest.tmp.json';temp.write_text(json.dumps(data,indent=2));temp.replace(R/'manifest.json')
if __name__=='__main__':main()
