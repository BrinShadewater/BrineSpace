from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;m=json.loads((P/'catalog.json').read_text());sheet=np.array(Image.open(P/'base-family-comparison.png').convert('RGB'));errors=[];checks=0
def check(ok,label):
    global checks
    checks+=1
    if not ok:errors.append(label)
for path,digest in m['sourceHashes'].items():check(hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,'source changed: '+path)
for record in m['records']:
    source=Image.open(R/record['source']).convert('RGBA').resize(tuple(record['tileSize']),Image.Resampling.NEAREST);expected=Image.new('RGBA',source.size,'#272b2e');expected.alpha_composite(source);alpha=np.array(source)[:,:,3]>0
    x,y=record['tileXY'];w,h=record['tileSize'];crop=sheet[y:y+h,x:x+w]
    check(crop.shape==(h,w,3),'tile bounds')
    # Captions occupy transparent padding beside the boots. Compare every source
    # pixel with nonzero alpha, including inherited faint markers and fringes.
    check(np.array_equal(crop[alpha],np.array(expected.convert('RGB'))[alpha]),'source character pixels exact: '+record['family']+'/'+record['direction'])
    check(record['canvas']==[184,184] and record['pivot']==[92,172] and record['standingHeight']==148,'shared standing profile')
check(len(m['records'])==16 and len({(r['family'],r['direction']) for r in m['records']})==16,'four directions for each family')
result={'checks':checks,'errors':errors,'scope':'Read-only source catalog, selected Marsh manifest order, standing metadata and unmodified source character pixels; no animation or head-fitting acceptance'};(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(bool(errors))
