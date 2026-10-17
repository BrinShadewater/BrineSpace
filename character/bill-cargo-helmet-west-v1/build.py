"""Fit the exact accepted west head/helmet to approved cargo motion."""
from pathlib import Path
import json,hashlib,copy
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;BARE=HERE.parent/'bill-cargo-west-coherent-v1'
AUTHORITY=HERE.parent/'bill-equipped-west-selected-v1'

def main():
 cells=json.loads((HERE/'source-cells.json').read_text())
 selected=json.loads((AUTHORITY/'manifest.json').read_text());idle_state=next(s for s in selected['states'] if s['id']=='interact-west')
 idle=Image.open(AUTHORITY/idle_state['frameFiles'][0]).convert('RGBA');idle=idle.crop((36,52,220,236));ia=np.array(idle);yy,xx=np.indices(ia.shape[:2]);hy,hx=np.where((ia[:,:,3]>180)&(yy<60))
 template_box=[int(hx.min()),int(hy.min()),int(hx.max()+1),60];template=idle.crop(template_box)
 grid_y,grid_x=np.indices((256,256))
 canonical_head=idle.crop((74,20,114,60));ca=np.array(canonical_head);cy,cx=np.indices(ca.shape[:2]);rgb=ca[:,:,:3].astype(float)
 # Exclude the idle shoulder patch from this equipment resource.
 contour=Image.new('L',(40,40));ImageDraw.Draw(contour).polygon([(0,0),(40,0),(40,27),(34,33),(26,37),(18,40),(0,40)],fill=255)
 ca[:,:,3]=np.minimum(ca[:,:,3],np.array(contour));patch=(cx>20)&(cy>24)&(rgb[:,:,0]>rgb[:,:,1]*1.3)&(rgb[:,:,0]>rgb[:,:,2]*1.3);ca[patch]=0
 canonical_head=Image.fromarray(ca);canonical_head.save(HERE/'sources/canonical-head.png')
 first_bare=np.array(Image.open(BARE/cells[0]['file']));fy,fx=np.where(first_bare[:,:,3]>180);reference_top=int(fy.min());frgb=first_bare[:,:,:3].astype(float)
 warm0=(first_bare[:,:,3]>180)&(grid_y<reference_top+18)&(frgb[:,:,0]>frgb[:,:,1]+3)&(frgb[:,:,0]>frgb[:,:,2]+5)
 ls,n=label(warm0);parts0=[]
 for ident in range(1,n+1):
  py,px=np.where(ls==ident)
  if len(px)>3:parts0.append((float(px.mean()),px))
 _,px=min(parts0,key=lambda p:p[0]);reference_center=(px.min()+px.max())/2
 angles=[0,5,10,15,20,20,20,15,10,5,0,0]
 manifest=copy.deepcopy(json.loads((BARE/'manifest.json').read_text()));manifest.update(name='Bill west cargo with fitted shared helmet',status='owner_visual_accepted_staged_2026_09_30_head_lock_v2',equipment='diving-helmet');states={s['id']:s for s in manifest['states']};hashes={};registrations=[];images=[]
 for cell in cells:
  i=cell['cell'];original=Image.open(BARE/cell['file']).convert('RGBA');a=np.array(original);y,x=np.where(a[:,:,3]>180);by=int(y.min())
  rgb0=a[:,:,:3].astype(float);warm=(a[:,:,3]>180)&(grid_y<by+18)&(rgb0[:,:,0]>rgb0[:,:,1]+3)&(rgb0[:,:,0]>rgb0[:,:,2]+5)
  labels,n=label(warm);parts=[]
  for ident in range(1,n+1):
   py,px=np.where(labels==ident)
   if len(px)>3:parts.append((float(px.mean()),py,px))
  _,head_y,head_x=min(parts,key=lambda p:p[0]);center=(head_x.min()+head_x.max())/2
  # Canonical accepted head/helmet, translated and tilted around its neck.
  # Every pose starts from this same original; no generated face or shell pixels.
  angle=angles[i] if i<12 else 0
  dx=round(center-reference_center);dy=by-reference_top
  head_canvas=Image.new('RGBA',(96,96));head_canvas.alpha_composite(canonical_head,(22,13))
  head_canvas=head_canvas.rotate(angle,resample=Image.Resampling.BICUBIC)
  dest=(136+dx-48,107+dy-48);cutoff=by+25
  erase=(grid_y<cutoff)&(grid_x>=head_x.min()-3)&(grid_x<=head_x.max()+3)
  a[erase]=0;result=Image.fromarray(a);result.alpha_composite(head_canvas,dest)
  visible=np.array(head_canvas)[:,:,3];vy,vx=np.where(visible>0)
  protected_y=max(cutoff,dest[1]+int(vy.max())+1)
  if i==0:
   # Keep the previous exact accepted empty-handed endpoint.
   b=np.array(original);b[:112]=0;result=Image.fromarray(b);pad=Image.new('RGBA',(256,256));pad.alpha_composite(idle,(36,52));pad_a=np.array(pad);pad_a[112:]=0;result.alpha_composite(Image.fromarray(pad_a));protected_y=112
  file=HERE/cell['file'];file.parent.mkdir(parents=True,exist_ok=True);result.save(file);hashes[cell['file']]=hashlib.sha256(file.read_bytes()).hexdigest();images.append(result)
  registrations.append({'cell':i,'state':cell['state'],'file':cell['file'],'canonicalHeadBox':[110,72,150,112],'helmetPosition':list(dest),'angleDegrees':angle,'neckAnchor':[136+dx,107+dy],'bareHeadCenter':float(center),'protectedBodyFromY':protected_y,'originalBodySha256':hashlib.sha256((BARE/cell['file']).read_bytes()).hexdigest()})
 # West unload is exactly the reverse fitted pickup, with its own timings.
 pickup=states['pickup-west']['frameFiles'];unload=states['unload-west']['frameFiles']
 for j,(source,dest) in enumerate(zip(reversed(pickup),unload)):
  path=HERE/dest;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((HERE/source).read_bytes());hashes[dest]=hashlib.sha256(path.read_bytes()).hexdigest()
  record=copy.deepcopy(registrations[11-j]);record.update(cell=18+j,state='unload-west',file=dest,originalBodySha256=hashlib.sha256((BARE/dest).read_bytes()).hexdigest());registrations.append(record)
 for s in states.values():s['provenance']='approved bare cargo body/case; exact accepted west idle head/helmet; pose translation and neck rotation only'
 manifest['strideDistanceCells']={'carry':0.12}
 for name,data in [('manifest.json',manifest),('frame-hashes.json',hashes),('helmet-registration.json',{'authority':str(AUTHORITY.relative_to(HERE.parent)),'templateBox':template_box,'selectedHeadMethod':'canonical accepted pixels;no source grade applied','canonicalHeadSha256':hashlib.sha256((HERE/'sources/canonical-head.png').read_bytes()).hexdigest(),'frames':registrations})]:
  (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
 out=Image.new('RGB',(1536,1024),(34,48,56));draw=ImageDraw.Draw(out)
 for i,im in enumerate(images):out.paste(im,((i%6)*256,(i//6)*256),im);draw.text(((i%6)*256+4,(i//6)*256+4),str(i),fill='white')
 out.save(HERE/'contact-sheet.png');print('Equipped west cargo:30 references;original body/case pixels preserved below fitted neck')

if __name__=='__main__':main()
