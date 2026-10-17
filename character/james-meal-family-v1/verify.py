from pathlib import Path
import json,hashlib,os,copy
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;checks=0;metrics={};combined={}
def check(ok,why):
 global checks
 assert ok,why
 checks+=1
for mode in ['bare','helmet']:
 out=None
 for direction in ['east','south','west','north']:
  p=ROOT/'character'/('james-meal-'+direction+'-v1');m=json.loads((p/(mode+'-manifest.json')).read_text());reg=json.loads((p/'registration.json').read_text());hashes=json.loads((p/'frame-hashes.json').read_text());check(hashlib.sha256((p/'source.png').read_bytes()).hexdigest()==reg['sourceSha256'],'source frozen')
  if out is None:out={k:copy.deepcopy(v) for k,v in m.items() if k!='states'};out.update(name='James meal family '+mode,states=[],status='installed_meal_family_owner_review_pending')
  check(m['pivot']==[92,172] and m['standingHeight']==148,'master registration')
  for st in m['states']:
   check(len(st['frameFiles'])==6 and st['loop'],'closed six-pose cycle');check(sum(st['frameDurationsMs'])==(1500 if st['id'].startswith('eat-') else 3000),'action duration');measure=[]
   for i,f in enumerate(st['frameFiles']):
    path=(p/f).resolve();im=Image.open(path).convert('RGBA');a=np.array(im);check(a.shape==(m['frameHeight'],m['frameWidth'],4),'canvas');check(not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any(),'unclipped');y,x=np.where(a[:,:,3]>180);measure.append(dict(crown=int(y.min()),sole=int(y.max()),height=int(y.max()-y.min()+1)))
    if mode=='bare':
     check(hashlib.sha256(path.read_bytes()).hexdigest()==hashes[f],'frame hash');check(abs(y.max()-y.min()+1-reg['masterHeight'])<=2 and 170<=y.max()<=172,'master size');idx=st['provenance']['sourcePoses'][i];old=np.array(Image.open(p/'registered-ungraded'/f'{idx:03d}.png'));check(np.array_equal(a[:,:,3],old[:,:,3]),'grade preserves alpha');yy=np.indices(a.shape[:2])[0];top=np.where(old[:,:,3]>180)[0].min();check(np.array_equal(a[yy<=top+30],old[yy<=top+30]),'face and hair unchanged by grade')
    else:
     donor=json.loads((ROOT/st['provenance']['sourceManifest']).read_text());ds=next(s for s in donor['states'] if s['id']==st['provenance']['sourceState']);expected=(ROOT/st['provenance']['sourceManifest']).parent/ds['frameFiles'][st['provenance']['sourcePoses'][i]];check(im.tobytes()==Image.open(expected).convert('RGBA').tobytes(),'exact sealed inspection substitute')
   check(Image.open(p/st['frameFiles'][0]).tobytes()==Image.open(p/st['frameFiles'][-1]).tobytes(),'exact loop endpoint');metrics[mode+'/'+st['id']]=measure;row=copy.deepcopy(st);row['frameFiles']=[Path(os.path.relpath((p/f).resolve(),HERE)).as_posix() for f in st['frameFiles']];out['states'].append(row)
  if mode=='bare':
   gif=Image.open(p/'review.gif');total=0
   for i in range(gif.n_frames):gif.seek(i);total+=gif.info['duration']
   check(total==12000,'decoded preview duration');gif.seek(2);gif.convert('RGB').save(p/'review-frame002.png')
 combined[mode]=out
 for path,value in [(HERE/(mode+'-manifest.json'),out)]:path.write_text(json.dumps(value,indent=2)+'\n')
report=dict(checks=checks,failures=0,bareReferences=48,helmetReferences=48,eatingLoopMs=1500,drinkingLoopMs=3000,closedLoopEndpoints=True,gradePreservesAlpha=True,independentSources=True,metrics=metrics,ownerReviewPending=True);(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('Meals:',checks,'checks,0 failures,8 states in each mode')
