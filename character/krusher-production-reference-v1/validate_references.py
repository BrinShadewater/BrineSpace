from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
m=json.loads((P/'reference-manifest.json').read_text());errors=[];checks=0
def check(ok,label):
    global checks
    checks+=1
    if not ok:errors.append(label)
for path,digest in m['sourceHashes'].items():check(hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,'source unchanged: '+path)
for tile in m['tiles']:
    source=Image.open(R/tile['source']).convert('RGBA').resize(tuple(tile['size']),Image.Resampling.NEAREST if tile['filter']=='nearest' else Image.Resampling.LANCZOS)
    expected=Image.new('RGBA',source.size,'#272b2e');expected.alpha_composite(source)
    x,y=tile['xy'];w,h=tile['size'];sheet=Image.open(P/tile['sheet']).convert('RGB')
    check(x>=0 and y>=0 and x+w<=sheet.width and y+h<=sheet.height,'tile within sheet')
    check(np.array_equal(np.array(sheet.crop((x,y,x+w,y+h))),np.array(expected.convert('RGB'))),'sprite tile exact: '+tile['source'])
result={'checks':checks,'errors':errors,'scope':'Source preservation and deterministic sprite tiles; visual sheet quality reviewed separately.'};(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(bool(errors))
