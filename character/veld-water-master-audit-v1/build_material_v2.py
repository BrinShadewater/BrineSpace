"""One immutable-source water material pass; exact helmet/head protection."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OUT=ROOT/'character/veld-water-material-v2';OUT.mkdir(exist_ok=True);cov=json.loads((ROOT/'character/veld-consistency-audit-v2/coverage.json').read_text());WEIGHTS=np.array([.2126,.7152,.0722]);pairs=[]
def pixels(path):return np.array(Image.open(path).convert('RGBA'))
def cloth(a):
 rgb=a[:,:,:3].astype(float);lum=rgb@WEIGHTS
 return (a[:,:,3]>0)&(np.ptp(rgb,axis=2)<30)&(rgb[:,:,0]<=rgb[:,:,1]+12)&(lum>10)&(lum<135)
def bare_source(key):return cov['selected']['bare'][key]
tread_records={(r['state'],r['slot']):r for r in json.loads((HERE/'tread-fit-checks.json').read_text())['records']}
side_records={(r['state'],r['slot']):r for r in json.loads((HERE/'side-swim-checks.json').read_text())['records']}
axial_records={('swim-'+r['direction'],r['slot']):r for r in json.loads((HERE/'axial-swim-checks.json').read_text())['records']}
def head_protection(key,i,shape):
 yy,xx=np.indices(shape);protected=np.zeros(shape,bool)
 def rect(box):
  x,y,w,h=box;return (xx>=x)&(xx<x+w)&(yy>=y)&(yy<y+h)
 if key.startswith('tread'):
  r=tread_records[key,i];protected|=rect([*r['position'],*r['headSize']]);x,y,right,bottom=r['clearBox'];protected|=rect([x,y,right-x,bottom-y])
 elif key in ['swim-east','swim-west']:
  r=side_records[key,i];ow,oh=34,38;pivot=np.array([ow*.5,oh*.85]);center=np.array(r['offset'])+pivot;t=np.deg2rad(r['rotationDegrees']);c,s=np.cos(t),np.sin(t);dx,dy=xx+.5-center[0],yy+.5-center[1];sx=dx*c+dy*s+pivot[0];sy=-dx*s+dy*c+pivot[1];protected|=(sx>=0)&(sx<ow)&(sy>=0)&(sy<oh);protected|=rect(r['clearRect'])
 else:
  r=axial_records[key,i];size=Image.open(HERE/f'fitted-{key}-head.png').size;protected|=rect([*r['position'],*size]);x,y,right,bottom=r['clear'];protected|=rect([x,y,right-x,bottom-y])
 return protected
for action in ['tread','swim']:
 for dr in ['north','east','south','west']:
  key=action+'-'+dr;b=bare_source(key);path=HERE/('tread-helmet-manifest.json' if action=='tread' else f'swim-{dr}-helmet-manifest.json');m=json.loads(path.read_text());state=next(s for s in m['states'] if s['id']==key)
  for i,file in enumerate(b['files']):
   bp=ROOT/file;hp=HERE/state['frameFiles'][i];ba=pixels(bp);ha=pixels(hp);same=np.all(ba==ha,axis=2);headmask=head_protection(key,i,ba.shape[:2]);mask=cloth(ba)&same&~headmask
   pairs.append({'key':key,'slot':i,'bare':bp,'helmet':hp,'ba':ba,'ha':ha,'mask':mask,'headmask':headmask})
# Compare opaque source cloth only; one curve across all48 old loop poses.
samples=np.concatenate([p['ba'][p['mask']&(p['ba'][:,:,3]>200),:3] for p in pairs]).astype(float)
refs=[];reference_files=[]
for dr in ['north','east','south','west']:
 path=ROOT/cov['selected']['bare']['idle-'+dr]['files'][0];a=pixels(path);mask=cloth(a)&(a[:,:,3]>200);mask[:60]=False;refs.append(a[mask,:3]);reference_files.append({'file':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
ref=np.concatenate(refs).astype(float);percentiles=[0,10,25,50,75,90,100];source_knots=np.percentile(samples@WEIGHTS,percentiles);target_knots=np.percentile(ref@WEIGHTS,percentiles)
source_knots=np.r_[0,source_knots,160,255];target_knots=np.r_[0,target_knots,160,255]
# Master near-neutral hue offsets at fixed brightness bins. Preserve detail within ramp.
bins=np.array([0,20,40,60,80,100,125,160,200,255]);offsets=[];rl=ref@WEIGHTS
for value in bins:
 take=ref[np.abs(rl-value)<12];offsets.append(np.median(take-(take@WEIGHTS)[:,None],axis=0) if len(take)>10 else [0,0,0])
offsets=np.array(offsets);checks=0;records=[]
for pair in pairs:
 mask=pair['mask'];before=pair['ba'];rgb=before[:,:,:3].astype(float);lum=rgb@WEIGHTS;target=np.interp(lum,source_knots,target_knots);new=np.stack([target+np.interp(target,bins,offsets[:,c]) for c in range(3)],axis=-1);new=np.rint(new).clip(0,255).astype('uint8')
 for variant,original in [('bare',pair['ba']),('helmet',pair['ha'])]:
  after=original.copy();after[mask,:3]=new[mask];assert np.array_equal(after[:,:,3],original[:,:,3]);checks+=1;assert np.array_equal(after[~mask],original[~mask]);checks+=1;assert np.array_equal(after[pair['headmask']],original[pair['headmask']]);checks+=1
  file=f'frames/{variant}/{pair["key"]}/{pair["slot"]:03}.png';(OUT/file).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(after).save(OUT/file)
  records.append({'key':pair['key'],'slot':pair['slot'],'variant':variant,'source':pair[variant].relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(pair[variant].read_bytes()).hexdigest(),'changedPixels':int(np.count_nonzero(np.any(after[:,:,:3]!=original[:,:,:3],axis=2))),'protectedHeadAndEquipment':True})
for variant in ['bare','helmet']:
 for action in ['tread','swim']:
  directions=['north','east','south','west'];groups=[directions] if action=='tread' else [[d] for d in directions]
  for dirs in groups:
   source=ROOT/bare_source(action+'-'+dirs[0])['manifest'];m=json.loads(source.read_text());states=[]
   for dr in dirs:
    key=action+'-'+dr;s=next(s for s in m['states'] if s['id']==key).copy();s['frameFiles']=[f'frames/{variant}/{key}/{i:03}.png' for i in range(6)];states.append(s)
   m.update(name='Veld water material '+action+' '+variant,states=states,status='staged_master_material_pending_visual_review')
   name=f'tread-{variant}-manifest.json' if action=='tread' else f'swim-{dirs[0]}-{variant}-manifest.json';(OUT/name).write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
 # Transition interiors already have source-wide master grade; retain, replace endpoints only.
 m=json.loads((HERE/f'east-transition-{variant}-manifest.json').read_text())
 for state in m['states']:
  for i,file in enumerate(state['frameFiles']):
   original=pixels(HERE/file);after=original
   if i in [0,5]:
    loop=('tread' if (state['id']=='swim-start-east' and i==0) or (state['id']=='swim-stop-east' and i==5) else 'swim');pivot=[92,70] if loop=='tread' else [122,88];im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(OUT/f'frames/{variant}/{loop}-east/000.png'),(128-pivot[0],128-pivot[1]));after=np.array(im)
   else:assert np.array_equal(original,after);checks+=1
   target=f'frames/{variant}/{state["id"]}/{i:03}.png';(OUT/target).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(after).save(OUT/target);state['frameFiles'][i]=target
 m.update(name='Veld material-consistent east swim transitions '+variant,status='staged_master_material_pending_visual_review');(OUT/f'east-transition-{variant}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
result={'checks':checks,'failures':0,'sourceLumaKnots':source_knots.tolist(),'targetLumaKnots':target_knots.tolist(),'masterHueBins':bins.tolist(),'masterHueOffsets':offsets.tolist(),'referenceFiles':reference_files,'records':records,'nativeHeadEquipmentPixelsUnchanged':True,'geometryAlphaUnchanged':True,'transitionInteriorsUnchanged':True,'installed':False}
(OUT/'material-checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
contact=Image.new('RGBA',(800,8*220),'#202a30');draw=ImageDraw.Draw(contact)
for row,(action,dr) in enumerate([(a,d) for a in ['tread','swim'] for d in ['north','east','south','west']]):
 key=action+'-'+dr;draw.text((8,row*220+4),key,fill='white')
 for col,variant in enumerate(['master','before','after']):
  if variant=='master':s=cov['selected']['helmet']['idle-'+dr];path=ROOT/s['files'][0];pivot=s['pivot'];py=195
  else:s=bare_source(key);path=(HERE if variant=='before' else OUT)/f'frames/helmet/{key}/003.png';pivot=s['pivot'];py=100
  im=Image.open(path);contact.alpha_composite(im,(col*265+132-round(pivot[0]),row*220+py-round(pivot[1])));draw.text((col*265+8,row*220+24),variant,fill='#c8d6dc')
contact.save(OUT/'material-master-comparison.png');print(f'{checks} head/equipment/alpha and retained-interior checks pass;20 staged states,120 frame files.')
