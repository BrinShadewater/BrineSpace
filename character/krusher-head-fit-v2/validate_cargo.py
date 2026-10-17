from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];P=R/'character/krusher-cargo-family-v2';old=R/'character/krusher-cargo-family-v1';checks=0;joins=[];slots=0
def read(p):return json.loads(p.read_text())
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for q in read(P/'revision.json')['records']:
 a=rgba(R/q['source'][6:]);b=rgba(P/q['output']);mask=np.array(Image.open(P/q['mask']))>0
 assert sha(R/q['source'][6:])==q['sourceHash'];assert sha(P/q['output'])==q['outputHash'];checks+=2
 assert b.shape==(256,256,4);checks+=1
 assert np.array_equal(a[~mask],b[~mask]);checks+=1
 assert np.array_equal(a[q['protectedFromRow']:],b[q['protectedFromRow']:]);checks+=1
 if q['gear']=='helmet':assert np.array_equal(a[:,:,3],b[:,:,3]);checks+=1
 if q['details'].get('rearQuarterVisibleFace'):
  yy,xx=np.indices(mask.shape);x0,y0,x1,y1=q['details']['protectedVisorAperture'];roi=(xx>=x0)&(xx<x1)&(yy>=y0)&(yy<y1)
  assert not np.any(mask&~roi);checks+=1
  assert sha(R/q['details']['faceSource'][6:])==q['details']['faceSourceHash'];checks+=1
for g in ['bare','helmet']:
 om=read(old/(g+'-manifest.json'));nm=read(P/(g+'-manifest.json'));assert om==nm;checks+=1
 states={s['id']:s for s in nm['states']};pairs=[]
 for s in nm['states']:
  for f in s['frameFiles']:assert Image.open(P/f).size==(256,256);checks+=1;slots+=1
 for d in ['south','east','north','west']:pairs.extend([('pickup-'+d,-1,'carry-'+d,0),('carry-'+d,0,'unload-'+d,0)])
 for key in states:
  if key.startswith('carry-turn-'):
   start,end=key.split('-')[-2:];pairs.extend([('carry-'+start,0,key,0),(key,-1,'carry-'+end,0)])
 for left,li,right,ri in pairs:
  a=states[left]['frameFiles'][li];b=states[right]['frameFiles'][ri];old_equal=np.array_equal(rgba(old/a),rgba(old/b));new_equal=np.array_equal(rgba(P/a),rgba(P/b))
  assert not old_equal or new_equal;checks+=1;joins.append({'gear':g,'from':left,'to':right,'oldEqual':bool(old_equal),'newEqual':bool(new_equal)})
 profile=R/'character/krusher-cargo-settle-profile-v2'/(g+'-manifest.json');m=read(profile);previous=read(R/'character/krusher-cargo-settle-profile-v1'/(g+'-manifest.json'))
 assert {k:v for k,v in m.items() if k!='states'}=={k:v for k,v in previous.items() if k!='states'};checks+=1
 for s,t in zip(m['states'],previous['states']):
  assert {k:v for k,v in s.items() if k!='frameFiles'}=={k:v for k,v in t.items() if k!='frameFiles'};checks+=1
  for f,want in zip(s['frameFiles'],states[s['id']]['frameFiles']):assert np.array_equal(rgba(R/f[6:]),rgba(P/want));checks+=1
 assert 'textureFilter' not in m;checks+=1
result={'checks':checks,'errors':[],'slots':slots,'joins':joins,'exactSharedJoins':sum(q['oldEqual'] for q in joins),'scope':'Exact previous manifests/stride/timing/state flags, all PNGs/hash stability, head mask and cargo/lower body protection, helmet alpha,64join comparisons, original nearest West settle profile retargeted to revised whole paths. No release cue/save or world lifecycle acceptance.'}
(P/'independent-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['joins','scope']}))
