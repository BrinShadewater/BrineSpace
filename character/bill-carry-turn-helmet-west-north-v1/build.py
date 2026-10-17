"""Fit one authored rotating helmet family to the approved planted cargo pivot."""
from pathlib import Path
import copy, hashlib, json
import numpy as np
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
BARE=HERE.parent/'bill-carry-turn-west-north-v1'
ENDS=[HERE.parent/'bill-cargo-helmet-west-v1/frames/pickup-west/011.png', HERE.parent/'bill-cargo-helmet-north-v1/frames/pickup-north/011.png']

def anchor(im):
 a=np.array(im); y,x=np.where(a[:,:,3]>180); top=int(y.min())
 hy,hx=np.where((a[:,:,3]>180)&(np.indices(a.shape[:2])[0]<top+8))
 return top,float((hx.min()+hx.max())/2)

def main():
 sheet=Image.open(HERE/'sources/helmet-west-north-v2.png').convert('RGBA');sw,sh=sheet.size
 heads=[];boxes=[]
 for i in range(6):
  cell=sheet.crop((i*sw//6,0,(i+1)*sw//6,sh));box=cell.getchannel('A').point(lambda x:255 if x>160 else 0).getbbox()
  boxes.append(box);heads.append(cell.crop((box[0]-2,box[1]-2,box[2]+2,box[3]+2)))
 barepack=json.loads((BARE/'manifest.json').read_text(encoding='utf-8')); files=barepack['states'][0]['frameFiles']
 bare=[Image.open(BARE/f).convert('RGBA') for f in files];ends=[Image.open(p).convert('RGBA') for p in ENDS]
 # One family-wide scale, derived once from both canonical cardinal helmets.
 endpoints=[np.array(im) for im in ends];q=[.05,.15,.35,.5,.7,.9,.98]
 ref=[];src=[]
 for a in endpoints:
  y,x=np.indices(a.shape[:2]);rgb=a[:,:,:3].astype(float)
  mask=(a[:,:,3]>180)&(y<95)&((rgb.max(2)-rgb.min(2))<25)
  ref.extend(rgb.mean(2)[mask].tolist())
 for h in heads:
  a=np.array(h);rgb=a[:,:,:3].astype(float);mask=(a[:,:,3]>160)&((rgb.max(2)-rgb.min(2))<25)
  src.extend(rgb.mean(2)[mask].tolist())
 curve,ix=np.unique(np.quantile(src,q),return_index=True);target=np.quantile(ref,q)[ix]
 reference=endpoints[0];rr=reference[:,:,:3].astype(float);ry,rx=np.indices(reference.shape[:2])
 skin_ref=(reference[:,:,3]>180)&(ry<98)&(rx<130)&(rr[:,:,0]>rr[:,:,1]+12)&(rr[:,:,0]>rr[:,:,2]+20)&(rr.mean(2)>50)
 src_skin=[]
 for h in heads[:3]:
  a=np.array(h);rgb=a[:,:,:3].astype(float);sy,sx=np.indices(a.shape[:2]);mask=(a[:,:,3]>160)&(sx<h.width*.45)&(sy>h.height*.2)&(rgb[:,:,0]>rgb[:,:,1]+12)&(rgb[:,:,0]>rgb[:,:,2]+20)&(rgb.mean(2)>50)
  src_skin.extend(rgb[mask].tolist())
 skin_gain=np.clip(np.median(rr[skin_ref],axis=0)/np.median(src_skin,axis=0),.6,1.05)
 scale_y=42/np.mean([boxes[i][3]-boxes[i][1] for i in [0,5]])
 scale_x=40/np.mean([boxes[i][2]-boxes[i][0] for i in [0,5]])
 offsets=[anchor(ends[i])[1]-anchor(bare[i*5])[1] for i in range(2)]
 tops=[anchor(im)[0] for im in ends];results=[ends[0]];records=[]
 yy,xx=np.indices((256,256))
 for i in range(1,5):
  # Approved body frame1 is already rear-oblique. Discard the more frontal
  # source angle rather than letting Bill's face turn separately from his chest.
  source_cell={1:2,2:3,3:3,4:4}[i]
  h=heads[source_cell];p=np.array(h);rgb=p[:,:,:3].astype(float);spread=rgb.max(2)-rgb.min(2)
  weight=np.clip((25-spread)/15,0,1);mapped=np.interp(rgb.mean(2),curve,target)
  weight[(rgb.mean(2)>185)&(np.indices(p.shape[:2])[0]<60)]=0
  tone=np.stack([mapped+.7,mapped,mapped-.5],axis=2)
  p[:,:,:3]=np.clip(rgb*(1-weight[:,:,None])+tone*weight[:,:,None],0,255).astype('uint8')
  ly,lx=np.indices(p.shape[:2]);skin=(p[:,:,3]>0)&(lx<h.width*.45)&(ly>h.height*.2)&(rgb[:,:,0]>rgb[:,:,1]+12)&(rgb[:,:,0]>rgb[:,:,2]+20)&(rgb.mean(2)>50)
  p[skin,:3]=np.clip(rgb[skin]*skin_gain,0,255).astype('uint8')
  sx,sy=scale_x,scale_y
  h=Image.fromarray(p).resize((round(h.width*sx),round(h.height*sy)),Image.Resampling.LANCZOS)
  top,center=anchor(bare[i]);t=i/5
  # Crown follows actual authored head movement; offset follows approved cardinal fits.
  head_top=round(tops[0]*(1-t)+tops[1]*t+top-(anchor(bare[0])[0]*(1-t)+anchor(bare[-1])[0]*t))
  pos=(round(center+offsets[0]*(1-t)+offsets[1]*t-h.width/2),head_top)
  a=np.array(bare[i]);erase=(yy<top+25)&(xx>=center-19)&(xx<=center+19);a[erase]=0
  result=Image.fromarray(a);result.alpha_composite(h,pos);protected=max(top+25,pos[1]+h.height)
  assert np.array_equal(np.array(result)[protected:],np.array(bare[i])[protected:])
  results.append(result);records.append({'frame':i,'source':'helmet-west-north-v2.png','sourceCell':source_cell,'sourceBox':list(boxes[source_cell]),'helmetPosition':list(pos),'helmetSize':list(h.size),'protectedBodyFromY':protected})
 results.append(ends[1]);manifest=copy.deepcopy(barepack)
 manifest.update(name='Bill helmeted west/north planted carry turn',equipment='diving-helmet',status='staged_owner_visual_review')
 hashes={}
 for index,state in enumerate(manifest['states']):
  images=results if index==0 else list(reversed(results))
  state['provenance']='approved bare planted body; authored west/rear helmet source; exact equipped neutral endpoints; reverse derived without mirroring'
  for file,im in zip(state['frameFiles'],images):
   path=HERE/file;path.parent.mkdir(parents=True,exist_ok=True);im.save(path);hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest()
 for name,data in [('manifest.json',manifest),('frame-hashes.json',hashes),('helmet-registration.json',{'source':'sources/helmet-west-north-v2.png','selectedCells':[2,3,3,4],'omittedSourceCells':[0,1,5],'unselectedSource':'sources/helmet-west-north-v1.png','scale':[scale_x,scale_y],'curveInput':curve.tolist(),'curveOutput':target.tolist(),'skinGain':skin_gain.tolist(),'endpointAuthorities':[p.relative_to(HERE.parent).as_posix() for p in ENDS],'frames':records})]:
  if name=='helmet-registration.json':
   data['sourceHashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE/'sources').glob('*.png')}
  (HERE/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 review=Image.new('RGB',(1536,512),(29,43,51));draw=ImageDraw.Draw(review)
 for i,im in enumerate(results):
  review.paste(im,(i*256,0),im);draw.text((i*256+8,8),str(i),fill='white')
  sample=im.resize((512,512),Image.Resampling.NEAREST);review.paste(sample.crop((170,125,342,235)),(i*256+42,300))
 review.save(HERE/'contact-sheet.png')
 gameplay=Image.new('RGB',(600,360));draw=ImageDraw.Draw(gameplay)
 for row,(bg,height) in enumerate([((29,43,51),82),((218,225,224),82),((29,43,51),54),((218,225,224),54)]):
  draw.rectangle((0,row*90,600,row*90+89),fill=bg)
  for i,im in enumerate(results):
   s=height/148;sample=im.resize((round(256*s),round(256*s)),Image.Resampling.LANCZOS);gameplay.paste(sample,(i*100+50-round(128*s),row*90+87-round(224*s)),sample)
 gameplay.save(HERE/'gameplay-review.png')
 print('Built helmet west/north and reverse:12 references,6 poses;fixed scale/grade;protected body equality.')

if __name__=='__main__':main()
