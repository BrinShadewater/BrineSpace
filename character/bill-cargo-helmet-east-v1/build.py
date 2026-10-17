"""Package generated pose-specific equipment over approved, unchanged cargo bodies."""
from pathlib import Path
import json,hashlib,copy
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;BARE=HERE.parent/'bill-cargo-east-coherent-v1'
AUTHORITY=HERE.parent/'bill-equipped-east-selected-v1'

def main():
 cells=json.loads((HERE/'source-cells.json').read_text());sheet=Image.open(HERE/'sources/helmet-pose-sheet.png').convert('RGBA');assert sheet.size==(1536,1024)
 selected=json.loads((AUTHORITY/'manifest.json').read_text());idle_state=next(s for s in selected['states'] if s['id']=='idle-east')
 idle=Image.open(AUTHORITY/idle_state['frameFiles'][0]).convert('RGBA');ia=np.array(idle);yy,xx=np.indices(ia.shape[:2]);hy,hx=np.where((ia[:,:,3]>180)&(yy<60))
 template_box=[int(hx.min()),int(hy.min()),int(hx.max()+1),60];template=idle.crop(template_box)
 # Frozen equipment dimensions/grade from selected idle, not pose bounding height.
 ref_rgb=ia[:,:,:3].astype(float);neutral=(ia[:,:,3]>180)&(yy<55)&((ref_rgb.max(2)-ref_rgb.min(2))<25)
 quantiles=[0,.1,.35,.5,.7,.9,1];target=np.quantile(ref_rgb.mean(2)[neutral],quantiles)
 first=np.array(sheet.crop((0,0,256,256)));gy,gx=np.where(first[:,:,3]>180);top=int(gy.min());grid_y,grid_x=np.indices((256,256))
 sy,sx=np.where((first[:,:,3]>180)&(grid_y<top+24));box=[int(sx.min()-2),top,int(sx.max()+3),top+47]
 scale=(template.width/(box[2]-box[0]),template.height/47)
 first_rgb=first[:,:,:3].astype(float);valid=(first[:,:,3]>180)&(grid_y<top+47)&((first_rgb.max(2)-first_rgb.min(2))<25)
 curve=np.quantile(first_rgb.mean(2)[valid],quantiles);curve,ix=np.unique(curve,return_index=True);target=target[ix]
 ref_skin=(ia[:,:,3]>180)&(yy<55)&(xx>90)&(ref_rgb[:,:,0]>ref_rgb[:,:,1]+8)&(ref_rgb[:,:,0]>ref_rgb[:,:,2]+15)&(ref_rgb.mean(2)>55)
 src_skin=(first[:,:,3]>180)&(grid_y<top+47)&(grid_x>(box[0]+box[2])/2)&(first_rgb[:,:,0]>first_rgb[:,:,1]+15)&(first_rgb[:,:,0]>first_rgb[:,:,2]+25)&(first_rgb.mean(2)>55)
 skin_gain=np.clip(np.median(ref_rgb[ref_skin],axis=0)/np.median(first_rgb[src_skin],axis=0),.75,1.05)
 manifest=copy.deepcopy(json.loads((BARE/'manifest.json').read_text()));manifest.update(name='Bill east cargo with fitted shared helmet',status='owner_visual_accepted_staged_2026_09_30_equipment_v1',equipment='diving-helmet');states={s['id']:s for s in manifest['states']};hashes={};registrations=[];images=[]
 for cell in cells:
  i=cell['cell'];original=Image.open(BARE/cell['file']).convert('RGBA');a=np.array(original);y,x=np.where(a[:,:,3]>180);by=int(y.min())
  rgb0=a[:,:,:3].astype(float);warm=(a[:,:,3]>180)&(grid_y<by+18)&(rgb0[:,:,0]>rgb0[:,:,1]+3)&(rgb0[:,:,0]>rgb0[:,:,2]+5)
  labels,n=label(warm);parts=[]
  for ident in range(1,n+1):
   py,px=np.where(labels==ident)
   if len(px)>3:parts.append((float(px.mean()),py,px))
  _,head_y,head_x=max(parts,key=lambda p:p[0]);center=(head_x.min()+head_x.max())/2
  raw=np.array(sheet.crop(((i%6)*256,(i//6)*256,(i%6+1)*256,(i//6+1)*256)));ry,rx=np.where(raw[:,:,3]>180);rtop=int(ry.min())
  rhead_y,rhead_x=np.where((raw[:,:,3]>180)&(grid_y<rtop+24));x0=int(rhead_x.min()-2);x1=int(rhead_x.max()+3)
  head=Image.fromarray(raw).crop((x0,rtop,x1,rtop+47));p=np.array(head);rgb=p[:,:,:3].astype(float)
  # Extract shell/visor/neck only: the generated shoulder patch must never
  # ride over the authored moving shoulder. Same shell contour per pose.
  mask=Image.new('L',head.size);w=head.width
  ImageDraw.Draw(mask).polygon([(0,0),(w,0),(w,47),(w*.80,47),(w*.52,43),(w*.28,36),(w*.14,29),(0,22)],fill=255)
  local_y,local_x=np.indices(p.shape[:2]);patch=(rgb[:,:,0]>rgb[:,:,1]*1.3)&(rgb[:,:,0]>rgb[:,:,2]*1.3)&(local_x<w*.55)&(local_y>24)
  p[:,:,3]=np.minimum(p[:,:,3],np.array(mask));p[patch]=0
  spread=rgb.max(2)-rgb.min(2);weight=np.clip((25-spread)/15,0,1)
  lamp=(rgb.mean(2)>175)&(np.indices(p.shape[:2])[0]<12);weight[lamp]=0
  mapped=np.interp(rgb.mean(2),curve,target);tone=np.stack([mapped+.7,mapped,mapped-.5],2)
  p[:,:,:3]=np.clip(rgb*(1-weight[:,:,None])+tone*weight[:,:,None],0,255).astype('uint8')
  skin=(local_x>w*.5)&(rgb[:,:,0]>rgb[:,:,1]+15)&(rgb[:,:,0]>rgb[:,:,2]+25)&(rgb.mean(2)>55)
  p[skin,:3]=np.clip(rgb[skin]*skin_gain,0,255).astype('uint8')
  head=Image.fromarray(p).resize((round(head.width*scale[0]),round(head.height*scale[1])),Image.Resampling.LANCZOS)
  dest=(round(center-head.width/2),by-5);cutoff=by+22
  # Above the neck there are no case/limb pixels. Remove original hair/face;
  # retain authored shoulders outside the helmet and every lower-body pixel.
  erase=(grid_y<cutoff)&(grid_x>=head_x.min()-3)&(grid_x<=head_x.max()+3)
  a[erase]=0;result=Image.fromarray(a);result.alpha_composite(head,dest)
  protected_y=max(cutoff,dest[1]+head.height)
  if i in [0,22]:
   # Exact accepted idle head for empty-handed endpoints; same body/case below.
   b=np.array(original);b[:112]=0;result=Image.fromarray(b);pad=Image.new('RGBA',(256,256));pad.alpha_composite(idle,(36,52));pad_a=np.array(pad);pad_a[112:]=0;result.alpha_composite(Image.fromarray(pad_a));protected_y=112
  file=HERE/cell['file'];file.parent.mkdir(parents=True,exist_ok=True);result.save(file);hashes[cell['file']]=hashlib.sha256(file.read_bytes()).hexdigest();images.append(result)
  registrations.append({'cell':i,'state':cell['state'],'file':cell['file'],'sourceHeadBox':[x0,rtop,x1,rtop+47],'helmetPosition':list(dest),'bareHeadCenter':float(center),'protectedBodyFromY':protected_y,'originalBodySha256':hashlib.sha256((BARE/cell['file']).read_bytes()).hexdigest()})
 for s in states.values():s['provenance']='approved bare cargo body/case; generated pose-specific shared helmet/neck only; frozen idle-calibrated equipment scale/grade'
 manifest['strideDistanceCells']={'carry':0.12}
 for name,data in [('manifest.json',manifest),('frame-hashes.json',hashes),('helmet-registration.json',{'authority':str(AUTHORITY.relative_to(HERE.parent)),'templateBox':template_box,'scale':list(scale),'curveInput':curve.tolist(),'curveOutput':target.tolist(),'skinGain':skin_gain.tolist(),'frames':registrations})]:
  (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
 out=Image.new('RGB',(1536,1024),(34,48,56));draw=ImageDraw.Draw(out)
 for i,im in enumerate(images):out.paste(im,((i%6)*256,(i//6)*256),im);draw.text(((i%6)*256+4,(i//6)*256+4),str(i),fill='white')
 out.save(HERE/'contact-sheet.png');print('Equipped east cargo:23 references;original body/case pixels preserved below fitted neck')

if __name__=='__main__':main()
