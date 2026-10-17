from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent
A=R/'character/krusher-animation-package-v11';B=R/'character/krusher-animation-package-v12'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
a=read(A/'package.json');b=read(B/'package.json');q=read(H/'face-validation.json')
assert set(a['states'])==set(b['states']);holds=0;changes=0
for key,v in a['states'].items():
 ma=read(A/v['manifest']);mb=read(B/b['states'][key]['manifest']);ident=key.split(':',1)[1]
 sa=next(s for s in ma['states'] if s['id']==ident);sb=next(s for s in mb['states'] if s['id']==ident)
 assert {k:v for k,v in ma.items() if k!='states'}=={k:v for k,v in mb.items() if k!='states'}
 assert {k:v for k,v in sa.items() if k!='frameFiles'}=={k:v for k,v in sb.items() if k!='frameFiles'}
 assert len(sa['frameFiles'])==len(sb['frameFiles']);holds+=len(sa['frameFiles'])
 for x,y in zip(sa['frameFiles'],sb['frameFiles']):
  pa=(A/v['manifest']).parent/x;pb=(B/b['states'][key]['manifest']).parent/y
  aa=np.array(Image.open(pa).convert('RGBA'));bb=np.array(Image.open(pb).convert('RGBA'))
  assert aa.shape==bb.shape and np.array_equal(aa[:,:,3],bb[:,:,3])
  if not np.array_equal(aa,bb):
   changes+=1;mask=np.array(Image.open(H/'masks'/pa.name))>0
   assert not np.any(np.any(aa!=bb,axis=2)&~mask)
for path,meta in b['files'].items():
 raw=(B/path).read_bytes();assert hashlib.sha256(raw).hexdigest()==meta['sha256'] and len(raw)==meta['bytes']
assert holds==8058 and changes==144 and len(b['states'])==586 and len(b['files'])==3486
report={'states':586,'holds':holds,'indexedPng':3486,'changedHolds':changes,'changedStates':q['states'],'changedDrawings':q['drawings'],'timingPivotDimensionsExact':True,'alphaExact':True,'outsideFaceMasksExact':True,'indexedHashesExact':True,'failures':0}
(H/'package-validation.json').write_text(json.dumps(report,indent=2));(B/'verification/package-validation.json').write_text(json.dumps(report,indent=2));print(report)
