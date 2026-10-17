from pathlib import Path
import json,hashlib,re
import numpy as np
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1];P=R/'character/krusher-animation-package-v9';OLD=R/'character/krusher-animation-package-v8';B=R/'character/krusher-style-neck-bank-v1'
read=lambda p:json.loads(p.read_text());index=read(P/'package.json');old=read(OLD/'package.json');records={r['output']:r for r in read(B/'revision.json')['records']};hashes={};proof=[]
def pose(root,idx,g):
 q=idx['states'][g+':unload-west'];mp=root/q['manifest'];s=next(s for s in read(mp)['states'] if s['id']=='unload-west');return np.array(Image.open(mp.parent/s['frameFiles'][4]).convert('RGBA')),q
for g in ['bare','helmet']:
 a,oq=pose(OLD,old,g);b,nq=pose(P,index,g);record=records[Path(nq['sourceFrames'][4]).relative_to(B.relative_to(R)).as_posix()];mask=np.array(Image.open(B/record['mask']).convert('L'))>0
 assert np.array_equal(a[~mask],b[~mask]);assert np.array_equal(a[140:],b[140:])
 digest=hashlib.sha256(b.tobytes().hex().encode()).hexdigest();hashes['' if g=='bare' else 'diving-helmet']=digest
 proof.append({'gear':g,'releaseIndex':4,'oldHash':hashlib.sha256(a.tobytes().hex().encode()).hexdigest(),'currentHash':digest,'outsideHeadNeckMaskExact':True,'caseAndLowerBodyRgbaExact':True})
p=R/'character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd';s=p.read_text();constant='const KRUSHER_STYLE_CUE_HASHES='+json.dumps(hashes,separators=(',',':'))
if 'const KRUSHER_STYLE_CUE_HASHES=' not in s:
 s=s.replace('static var checked_cues:Dictionary={}',constant+'\nstatic var checked_cues:Dictionary={}')
 s=s.replace('or digest==KRUSHER_H7_CUE_HASHES.get(gear,"")','or digest==KRUSHER_H7_CUE_HASHES.get(gear,"") or digest==KRUSHER_STYLE_CUE_HASHES.get(gear,"")')
else:s=re.sub(r'const KRUSHER_STYLE_CUE_HASHES=.*',constant,s)
p.write_text(s);(H/'floor-cue-proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({'provenCues':2,'caseAndLowerBodyRgbaExact':True}))
