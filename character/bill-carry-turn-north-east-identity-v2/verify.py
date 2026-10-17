from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parents[1];reg=json.loads((P/'registration.json').read_text());frozen=json.loads((P/'frozen-bindings.json').read_text());checks=[]
def check(ok,name):
 assert ok,name
 checks.append(name)
for c in reg['calibration']:
 source=Image.open(P/f"sources/calibration-{c['gear']}-neutral.png");target=Image.open(R/c['targetFile'])
 check(source.height==c['sourceNeutralBox'][3]-c['sourceNeutralBox'][1],'Complete recorded calibration component')
 check(list(target.size)==c['targetSize'],'Accepted native head component dimensions')
 check(abs(c['scale']-target.height/source.height)<1e-12,'One master-calibrated component ruler per sheet')
for d in reg['donors']:
 check(d['scale']==reg['scales'][d['gear']],'One frozen source ruler for all four interior heads per sheet')
 check(hashlib.sha256((P/f"sources/{d['gear']}-v1.png").read_bytes()).hexdigest()==d['rawSha256'],'Generated sources unchanged')
for row in reg['frames']:
 old=np.array(Image.open(R/row['originalBare'][6:]).convert('RGBA'));out=np.array(Image.open(R/row['output'][6:]).convert('RGBA'))
 check(hashlib.sha256((R/row['originalBare'][6:]).read_bytes()).hexdigest()==row['originalBareSha256'],'Original authored bare bodies unchanged')
 if row['endpoint']:
  direction='north' if row['frame']==0 else 'east';check(np.array_equal(out,np.array(Image.open(R/frozen['endpoints'][row['gear']][direction][6:]).convert('RGBA'))),'Exact current static held cardinal endpoint');continue
 h=Image.open(P/f"sources/component-{row['gear']}-{row['frame']:03}.png").convert('RGBA');plane=Image.new('RGBA',(256,256));plane.alpha_composite(h,tuple(row['position']));ha=np.array(plane);erase=np.array(Image.open(P/row['eraseMask']))>0;region=erase|(ha[:,:,3]>0)
 check(np.array_equal(out[~region],old[~region]),'Original body/case/feet/suit detail exact outside head fit')
 base=old.copy();base[erase]=0;expected=Image.fromarray(base);expected.alpha_composite(h,tuple(row['position']));check(np.array_equal(out,np.array(expected)),'Exact recorded component composition')
 labs,_=label(out[:,:,3]>160);counts=np.bincount(labs.ravel());counts[0]=0;head=ha[:,:,3]>200;check(float((labs[head]==counts.argmax()).mean())>.98,'Head connected to original torso')
for gear,name in [('bare','bare-manifest.json'),('helmet','helmet-manifest.json')]:
 m=json.loads((P/name).read_text());old=json.loads((R/frozen['turn'][gear]['manifest']).read_text())
 check(m['pivot']==[128,224] and m['standingHeight']==148,'Same native foot/density metadata')
 for st in m['states']:
  before=next(x for x in old['states'] if x['id']==st['id']);check(st['frameDurationsMs']==before['frameDurationsMs'] and st['loop']==before['loop'],'Original source clock')
  check(st['facings']==before['facings'],'Original directional source metadata')
 check(m['states'][0]['frameFiles']==m['states'][1]['frameFiles'][::-1],'Exact reverse without mirroring')
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':len(checks),'scope':'Frozen source ruler/pixels, protected original bodies/case, exact current endpoints, recorded connected component fit and source clocks/reverse;visual separate'},indent=2)+'\n');print(str(len(checks))+' package checks pass')
