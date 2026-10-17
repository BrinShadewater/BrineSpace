from pathlib import Path
import json,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];OLD=R/'character/james-seated-family-v1'
pack=json.loads((P/'helmet-manifest.json').read_text());old=json.loads((OLD/'helmet-manifest.json').read_text());reg=json.loads((P/'registration.json').read_text());checks=0;failures=[]
def check(ok,label):
 global checks
 checks+=1
 if not ok:failures.append(label)
for s in pack['states']:
 previous=next(x for x in old['states'] if x['id']==s['id'])
 for field in previous:
  if field not in ['frameFiles','provenance']:check(s.get(field)==previous[field],s['id']+' '+field)
for t in reg['records']:
 a=np.array(Image.open(t['old']).convert('RGBA'));b=np.array(Image.open(P/t['output']).convert('RGBA'));mask=np.ones(a.shape[:2],bool);x0,y0,x1,y1=t['headROI'];mask[y0:y1,x0:x1]=False
 check(np.array_equal(a[mask],b[mask]),t['output']+' exact body outside head ROI')
 check(b.shape==a.shape,t['output']+' canvas')
 check(t['fixedScale']==reg['fixedScale'],t['output']+' frozen source ruler')
 if t['endpointExact']:check(np.array_equal(a,b),t['output']+' exact shared neutral')
check(len(reg['records'])==18,'three reading states18refs')
(P/'packaging-validation.json').write_text(json.dumps({'checks':checks,'failures':failures,'scope':'Three helmet reading states only: exact original metadata/clock and body outside recorded head ROI, exact neutral0/5, fixed whole-figure ruler. Does not prove gaze quality, native furniture or natural motion.'},indent=2)+'\n');print(json.dumps({'checks':checks,'failures':failures}));raise SystemExit(bool(failures))
