from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
families={
 'cargo':'character/veld-cargo-south-master-family-v1/bare-manifest.json',
 'start':'character/veld-carry-south-start-master-v1/bare-manifest.json',
 'gait':'character/veld-carry-south-master-proportions-v1/bare-manifest.json'}
idle_path='character/veld-cargo-south-master-family-v1/frames/bare/unload-south/006.png'
head_gain=np.array([.80,.89,.95]);cloth_gain=.93;cloth_offset=np.array([0,1,2]);metal_gain=.82
records={};refs={};checks=0
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def transform(a,ref):
 rgb=a[:,:,:3].astype(float);out=a.copy();y,x=np.where(a[:,:,3]>200);top=int(y.min());yy=np.indices(a.shape[:2])[0]
 # Fixed material transform across the family, never separate frame normalization.
 head=(a[:,:,3]>200)&(yy<top+20)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15)
 neutral=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(yy>=top+28)
 cloth=neutral&(rgb.mean(2)>20)&(rgb.mean(2)<125)
 metal=neutral&(rgb.mean(2)>=125)
 # Preserve central carried case and adjacent grip as authored hardware.
 protect=None
 if '/unload-south/' in ref:
  if ref.endswith('/000.png'):protect=(95,110,162,166)
  elif ref.endswith('/001.png'):protect=(95,165,161,195)
  elif ref.endswith('/002.png'):protect=(103,192,153,227)
 else:protect=(95,110,162,166)
 if protect:
  x0,y0,x1,y1=protect;cloth[y0:y1,x0:x1]=False;metal[y0:y1,x0:x1]=False
 out[head,:3]=(rgb[head]*head_gain).clip(0,255).astype('uint8')
 out[cloth,:3]=(rgb[cloth]*cloth_gain+cloth_offset).clip(0,255).astype('uint8')
 out[metal,:3]=(rgb[metal]*metal_gain).clip(0,255).astype('uint8')
 assert np.array_equal(out[:,:,3],a[:,:,3])
 changed=head|cloth|metal;assert np.array_equal(out[~changed],a[~changed])
 return out,top,int(changed.sum())
def export(ref):
 global checks
 if ref in refs:return refs[ref]
 src=R/ref[6:];original=np.array(Image.open(src).convert('RGBA'))
 if ref[6:]==idle_path:
  revised=original.copy();top=76;count=0
 else:revised,top,count=transform(original,ref)
 target=P/'frames/bare'/f'{len(refs):03}.png';target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(revised).save(target)
 equipped_ref=ref.replace('/bare/','/helmet/');equipped_src=R/equipped_ref[6:]
 assert equipped_src.exists(),equipped_src
 eq=np.array(Image.open(equipped_src).convert('RGBA'));helmet=revised.copy()
 # Preserve the original shell/head fitting box; grade the same body outside it.
 y,x=np.where(np.any(original!=eq,axis=2));box=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1))
 x0,y0,x1,y1=box;helmet[y0:y1,x0:x1]=eq[y0:y1,x0:x1]
 ht=P/'frames/helmet'/target.name;ht.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(helmet).save(ht)
 protected=np.zeros(original.shape[:2],bool);protected[y0:y1,x0:x1]=True
 assert np.array_equal(helmet[protected],eq[protected]);assert np.array_equal(helmet[~protected],revised[~protected])
 assert np.array_equal(helmet[:,:,3],eq[:,:,3]);checks+=4
 refs[ref]='res://'+target.relative_to(R).as_posix()
 records[ref]={'sourceSHA256':digest(src),'equippedSource':equipped_ref,'equippedSHA256':digest(equipped_src),'output':refs[ref],'outputSHA256':digest(target),'helmetOutputSHA256':digest(ht),'originalEquippedHeadBox':box,'top':top,'changedPixels':count,'originalIdleUnchanged':ref[6:]==idle_path}
 return refs[ref]
for family,path in families.items():
 data=json.loads((R/path).read_text(encoding='utf-8'))
 for state in data['states']:state['frameFiles']=[export(ref) for ref in state['frameFiles']]
 for gear in ['bare','helmet']:
  d=json.loads(json.dumps(data))
  if gear=='helmet':
   for state in d['states']:state['frameFiles']=[ref.replace('/bare/','/helmet/') for ref in state['frameFiles']]
  d.update(name='Veld South shared material study '+family+' '+gear,status='staged_material_study_not_installed')
  if 'floorPropStudy' in d:d['floorPropStudy']['canvas']='res://character/veld-cargo-south-master-family-v1/floor-case-canvas.png'
  (P/f'{family}-{gear}-manifest.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1792,900),'#202a30');draw=ImageDraw.Draw(board)
cargo=json.loads((P/'cargo-bare-manifest.json').read_text(encoding='utf-8'));row=next(s for s in cargo['states'] if s['id']=='unload-south')
old=json.loads((R/families['cargo']).read_text(encoding='utf-8'));oldrow=next(s for s in old['states'] if s['id']=='unload-south')
for i,(oref,nref) in enumerate(zip(oldrow['frameFiles'],row['frameFiles'])):
 for j,ref in enumerate([oref,nref,nref.replace('/bare/','/helmet/')]):
  im=Image.open(R/ref[6:]).convert('RGBA')
  if i>=3:im.alpha_composite(Image.open(R/'character/veld-cargo-south-master-family-v1/floor-case-canvas.png').convert('RGBA'))
  board.paste(im,(i*256,j*300+25),im);draw.text((i*256+3,j*300+4),['Previous','Shared study','Helmet study'][j]+' '+str(i),fill='white')
board.save(P/'paired-material-study.png')
record={'checks':checks,'failures':0,'sourceFrames':len(refs),'recipe':{'headRGBGain':head_gain.tolist(),'clothGain':cloth_gain,'clothOffset':cloth_offset.tolist(),'neutralMetalGain':metal_gain,'oneFixedTransform':True,'originalIdleUnchanged':True,'equippedHeadAndShellUnchanged':True},'records':records,'scope':'Staged shared South held/start/stop/gait/cargo material study. Whole body geometry/timing retained; original idle and equipped head untouched. Turn interior palettes, native/world/controller/save/ownership and full library remain pending.'}
(P/'registration.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':checks,'frames':len(refs),'failures':0}))
