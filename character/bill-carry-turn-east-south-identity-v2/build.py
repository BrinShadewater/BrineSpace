"""Fit new authored front-quarter identity over frozen accepted turn bodies."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_fill_holes,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
frozen=json.loads((P/'frozen-bindings.json').read_text());scale=148/352
Y,X=np.indices((256,256));heads={};donors=[];records=[];outputs={g:[] for g in ['bare','helmet']}
# One frozen ruler from the complete generated east neutral:352source pixels to148native.
# Original bodies/cases are retained. Complete source0 establishes the fixed full figure ruler.
for gear in outputs:
 raw=np.array(Image.open(P/f'sources/{gear}-v1.png').convert('RGBA'))
 for i in range(1,5):
  a=raw[i//3*512:(i//3+1)*512,i%3*512:(i%3+1)*512].copy();rgb=a[:,:,:3].astype(float);y,x=np.indices(a.shape[:2]);labs,_=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;body=labs==counts.argmax();by,bx=np.where(body);top=int(by.min())
  crown=body&(y<top+12);cy,cx=np.where(crown);axis=float((cx.min()+cx.max())/2)
  if gear=='bare':
   mask=body&(x>=axis-40)&(x<axis+40)&(y<top+65)&(rgb[:,:,0]>rgb[:,:,1]*1.035)&(rgb[:,:,0]>rgb[:,:,2]*1.05)
   mask=(binary_dilation(binary_fill_holes(mask),iterations=1)| (body&(y<top+24)))&(a[:,:,3]>0)&(x>=axis-40)&(x<axis+40)&(y<top+65)
   mask&=~((rgb.max(2)-rgb.min(2)<12)&(y>=top+28))
  else:mask=binary_dilation(body,iterations=1)&(a[:,:,3]>0)&(x>=axis-54)&(x<axis+54)&(y<top+85)
  yy,xx=np.where(mask);box=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];a[~mask]=0;h=Image.fromarray(a).crop(box);h=h.resize((round(h.width*scale),round(h.height*scale)),Image.Resampling.LANCZOS)
  heads[gear,i]=h;donors.append({'gear':gear,'cell':i,'box':box,'scale':scale,'headAxis':(axis-box[0])*scale,'componentSize':list(h.size),'rawSha256':hashlib.sha256((P/f'sources/{gear}-v1.png').read_bytes()).hexdigest()})
# One shared material calibration across all intermediate heads; no per-frame exposure.
master_bare=[np.array(Image.open(R/frozen['endpoints']['bare'][d][6:]).convert('RGBA')) for d in ['east','south']]
master_gear=[np.array(Image.open(R/frozen['endpoints']['helmet'][d][6:]).convert('RGBA')) for d in ['east','south']]
def material(a,kind,source=False):
 rgb=a[:,:,:3].astype(float);y,x=np.indices(a.shape[:2]);opaque=a[:,:,3]>180
 if source:
  top=int(np.where(opaque)[0].min());roi=opaque&(y<top+14)
 else:
  top=int(np.where(opaque)[0].min());roi=opaque&(y>=top)&(y<top+14)&(x>100)&(x<156)
 if kind=='hair':return roi&(rgb[:,:,0]>rgb[:,:,2]*1.05)&(rgb.mean(2)<90)
 if kind=='skin':return opaque&(y<top+30)&(rgb[:,:,0]>rgb[:,:,1]+12)&(rgb[:,:,0]>rgb[:,:,2]+15)&(rgb.mean(2)>70)&((x>100)&(x<156) if not source else True)
 return opaque&(y<top+(45 if not source else 100))&(rgb.max(2)-rgb.min(2)<22)&((x>100)&(x<156) if not source else True)
gains={}
for kind in ['hair','skin','shell','helmet_skin']:
 gear='helmet' if kind in ['shell','helmet_skin'] else 'bare';master=master_gear if gear=='helmet' else master_bare
 target=np.concatenate([a[:,:,:3][material(a,'skin' if kind=='helmet_skin' else kind)] for a in master]);src=np.concatenate([np.array(heads[gear,i])[:,:,:3][material(np.array(heads[gear,i]),'skin' if kind=='helmet_skin' else kind,True)] for i in range(1,5)])
 assert len(target) and len(src),(kind,len(target),len(src));gains[kind]=(np.median(target,axis=0)/np.median(src,axis=0)).tolist()
for gear in outputs:
 for i in range(1,5):
  a=np.array(heads[gear,i]);rgb=a[:,:,:3].astype(float)
  for kind in (['shell','helmet_skin'] if gear=='helmet' else ['hair','skin']):
   mask=material(a,'skin' if kind=='helmet_skin' else kind,True);a[mask,:3]=np.clip(rgb[mask]*gains[kind],0,255).astype('uint8')
  heads[gear,i]=Image.fromarray(a)
(P/'material-grade.json').write_text(json.dumps({'fixedGains':gains,'scope':'one pooled master-relative hair/skin/shell grade;all4source heads pergear,not perpose exposure'},indent=2)+'\n')
for i,barefile in enumerate(frozen['turn']['bare']['sourceFiles']):
 old=Image.open(R/barefile[6:]).convert('RGBA');a=np.array(old);rgb=a[:,:,:3].astype(float);top=int(np.where(a[:,:,3]>180)[0].min());crown=(a[:,:,3]>180)&(Y<top+8);cy,cx=np.where(crown);axis=float((cx.min()+cx.max())/2)
 warm=(a[:,:,3]>0)&(X>=axis-18)&(X<axis+18)&(Y>=top)&(Y<top+31)&(rgb[:,:,0]>rgb[:,:,1]*1.035)&(rgb[:,:,0]>rgb[:,:,2]*1.05)
 erase=(binary_dilation(binary_fill_holes(warm),iterations=1)|((Y>=top-2)&(Y<top+14)))&(a[:,:,3]>0)&(X>=axis-18)&(X<axis+18)&(Y>=top-2)&(Y<top+31)
 erase&=~((rgb.max(2)-rgb.min(2)<12)&(Y>=top+14))
 strong=warm&(a[:,:,3]>180);neck=int(np.where(strong)[0].max());base=a.copy();base[erase]=0
 for gear in outputs:
  if i in [0,5]:
   direction='east' if i==0 else 'south';src=frozen['endpoints'][gear][direction];out=Image.open(R/src[6:]).convert('RGBA');position=None
  else:
   h=heads[gear,i];rec=next(d for d in donors if d['gear']==gear and d['cell']==i);hy,hx=np.where(np.array(h)[:,:,3]>180);position=[round(axis-rec['headAxis']),neck+(5 if gear=='helmet' else 0)-int(hy.max())]
   out=Image.fromarray(base);out.alpha_composite(h,tuple(position));h.save(P/f'sources/component-{gear}-{i:03}.png')
  f=P/f'frames/{gear}/carry-turn-east-south/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);out.save(f);outputs[gear].append('res://'+f.relative_to(R).as_posix())
  mf=P/f'sources/erase-{i:03}.png';Image.fromarray(erase.astype('uint8')*255).save(mf)
  records.append({'gear':gear,'frame':i,'originalBare':barefile,'originalBareSha256':hashlib.sha256((R/barefile[6:]).read_bytes()).hexdigest(),'output':outputs[gear][-1],'endpoint':i in [0,5],'position':position,'eraseMask':mf.relative_to(P).as_posix(),'headAxis':axis,'neckY':neck})
for gear in outputs:
 original=json.loads((R/frozen['turn'][gear]['manifest']).read_text());m={k:v for k,v in original.items() if k!='states'};m.update(name='Bill East/South authored quarter identity candidate',status='staged_visual_review',states=[])
 for key,files in [('carry-turn-east-south',outputs[gear]),('carry-turn-south-east',outputs[gear][::-1])]:
  st=copy.deepcopy(next(s for s in original['states'] if s['id']==key));st['frameFiles']=files;st['provenance']='New authored front-quarter identity at one frozen ruler over original bare bodies/cases;exact current cardinal held endpoints;reverse derived,never mirrored';m['states'].append(st)
 (P/('bare-manifest.json' if gear=='bare' else 'helmet-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
(P/'registration.json').write_text(json.dumps({'scale':scale,'ruler':'complete generated bare source0 east stature352px ->native148;all eight heads share this ruler','sourceScope':'new heads only;generated body changes and halos excluded','donors':donors,'frames':records},indent=2)+'\n')
board=Image.new('RGB',(1536,1536),(34,52,62));dr=ImageDraw.Draw(board)
for row,gear in enumerate(outputs):
 for i,f in enumerate(outputs[gear]):
  im=Image.open(R/f[6:]).convert('RGBA');board.paste(im,(i*256,row*768),im);crop=im.crop((100,65,160,125)).resize((240,240),Image.Resampling.NEAREST);board.paste(crop,(i*256,row*768+300),crop);dr.text((i*256+3,row*768+560),gear+' '+str(i),fill='white')
board.save(P/'candidate-review.png');print('Staged24reference paired quarter;12unique poses;native body protected;not installed')
