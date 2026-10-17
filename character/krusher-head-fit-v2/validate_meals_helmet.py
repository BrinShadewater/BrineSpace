from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2]
def read(p):return json.loads(p.read_text())
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pad(a):
 out=Image.new('RGBA',(256,256));out.alpha_composite(Image.fromarray(a),(36,52));return np.array(out)
can=R/'character/krusher-james-canonical-v5'
idle={}
for g in ['bare','helmet']:
 for s in read(can/(g+'-manifest.json'))['states']:
  if s['id'].startswith('idle-'):idle[g,s['id'][5:]]=pad(rgba(can/s['frameFiles'][0]))
for family,names in [('meal-family',['bare-manifest.json','helmet-manifest.json']),('helmet-transition',['manifest.json']),('meal-service',['bare-manifest.json'])]:
 old=R/f'character/krusher-{family}-v1';P=R/f'character/krusher-{family}-v2';checks=0;slots=0;joins=0
 for name in names:
  a=read(old/name);b=read(P/name)
  assert {k:v for k,v in a.items() if k!='states'}=={k:v for k,v in b.items() if k!='states'};checks+=1
  assert len(a['states'])==len(b['states']);checks+=1
  for os,ns in zip(a['states'],b['states']):
   assert os==ns;checks+=1
   for frame in ns['frameFiles']:
    image=Image.open(P/frame);assert image.size==(b['frameWidth'],b['frameHeight']);checks+=1;slots+=1
   if family=='meal-family' and name.startswith('helmet'):
    d=ns['id'].rsplit('-',1)[1]
    for f in [ns['frameFiles'][0],ns['frameFiles'][-1]]:
     assert np.array_equal(rgba(P/f),idle['helmet',d]);checks+=1;joins+=1
   if family=='meal-service' and ns['id'].startswith('meal-return-'):
    d=ns['id'].rsplit('-',1)[1];assert np.array_equal(rgba(P/ns['frameFiles'][-1]),idle['bare',d]);checks+=1;joins+=1
 if family=='helmet-transition':
  m=read(P/'manifest.json');equip=m['states'][0];remove=m['states'][1]
  for s in [equip,remove]:
   for f,i in zip(s['frameFiles'],s['sourcePoseIndices']):
    assert np.array_equal(rgba(P/f),rgba(P/equip['frameFiles'][i]));checks+=1
   for i,g in [(0,'bare'),(11,'helmet')]:
    f=s['frameFiles'][s['sourcePoseIndices'].index(i)];assert np.array_equal(rgba(P/f),idle[g,'east']);checks+=1;joins+=1
 for q in read(P/'revision.json')['records']:
  source=R/q['source'][6:];out=P/q['output'];before=rgba(source);after=rgba(out);mask=np.array(Image.open(P/q['mask']))>0
  assert sha(source)==q['sourceHash'] and sha(out)==q['outputHash'];checks+=1
  assert np.array_equal(before[~mask],after[~mask]);checks+=1
  if family=='meal-family':
   if q['details']['gear']=='helmet':assert np.array_equal(before[:,:,3],after[:,:,3]);checks+=1
   else:
    oldq=next(z for z in read(old/'provenance.json')['records'] if z['output']==q['output']);fg=np.array(Image.open(old/oldq['foregroundMask']))>0
    assert np.array_equal(before[fg],after[fg]);assert np.array_equal(before[141:],after[141:]);checks+=2
  if family=='helmet-transition':
   assert np.array_equal(before[138:],after[138:]);checks+=1
   if q['details']['pose']>=5:assert np.array_equal(before[:,:,3],after[:,:,3]);checks+=1
  if family=='meal-service':assert np.array_equal(before,after);checks+=1
 result={'checks':checks,'errors':[],'slots':slots,'exactCanonicalJoins':joins,'scope':'Exact original root/state metadata, source hashes, all pose canvases, head masks, meal foreground/body protection, helmet alpha, equipment reversal and canonical idle joins. No world acceptance.'}
 (P/'independent-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'family':family,**result}))
 # Reuse existing native-pose replay builder and make its referenced sheets current.
 (P/'build_review.py').write_text((old/'build_review.py').read_text())
 if family=='meal-family':
  for g in ['bare','helmet']:shutil.copyfile(P/(g+'-manifest-head-fit-sheet.png'),P/(g+'-sheet.png'))
 elif family=='helmet-transition':shutil.copyfile(P/'manifest-head-fit-sheet.png',P/'contact-sheet.png')
 else:shutil.copyfile(P/'bare-manifest-head-fit-sheet.png',P/'new-poses-sheet.png')
