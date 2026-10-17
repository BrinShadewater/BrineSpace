"""Admit only proven exact release drawings; retain all prior cue guards."""
from pathlib import Path
from PIL import Image
import json,hashlib
import numpy as np
H=Path(__file__).resolve().parent;R=H.parents[1];P=R/'character/krusher-animation-package-v8';OLD=R/'character/krusher-animation-package-v4';COLOUR=R/'character/krusher-coherent-bank-v2'
read=lambda p:json.loads(p.read_text());index=read(P/'package.json');oldindex=read(OLD/'package.json');colours={q['output']:q for q in read(COLOUR/'palette-validation.json')['records']};hashes={};proof=[]
def pose(root,idx,g):
 q=idx['states'][g+':unload-west'];mp=root/q['manifest'];s=next(s for s in read(mp)['states'] if s['id']=='unload-west');return np.array(Image.open(mp.parent/s['frameFiles'][4]).convert('RGBA')),q
for g in ['bare','helmet']:
 a,oq=pose(OLD,oldindex,g);b,nq=pose(P,index,g)
 finished=R/nq['sourceFrames'][4];palette=colours[finished.relative_to(COLOUR).as_posix()];raw=R/palette['source'];family=raw.parent.parent.parent;records=read(family/'revision.json')['records'];record=next(q for q in records if (family/q['output']).resolve()==raw.resolve())
 oldfamily=R/'character/krusher-cargo-family-v4';oldrecord=next(q for q in read(oldfamily/'revision.json')['records'] if q['output']==record['output'])
 assert np.array_equal(a,np.array(Image.open(oldfamily/oldrecord['output']).convert('RGBA')))
 oldmask=np.array(Image.open(oldfamily/oldrecord['mask']).convert('L'))>0;newmask=np.array(Image.open(family/record['mask']).convert('L'))>0;paint=np.array(Image.open(COLOUR/palette['mask']).convert('L'))>0
 allowed=oldmask|newmask|paint
 assert np.array_equal(a[~allowed],b[~allowed]),(g,'case/body outside declared head and cyan masks')
 assert np.array_equal(a[140:,:,3],b[140:,:,3]),(g,'case/body geometry')
 # Godot hashes the hexadecimal RGBA string, rather than raw RGBA bytes.
 digest=hashlib.sha256(b.tobytes().hex().encode()).hexdigest();hashes['' if g=='bare' else 'diving-helmet']=digest
 proof.append({'gear':g,'releaseIndex':4,'uniqueSourceState':record['state'],'uniqueSourceFrame':record['frame'],'sourceDrawing':raw.relative_to(R).as_posix(),'previousCueHash':hashlib.sha256(a.tobytes().hex().encode()).hexdigest(),'currentCueHash':digest,'outsideDeclaredHeadAndPaletteExact':True,'caseAndLowerBodyAlphaExact':True})
path=R/'character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd';text=path.read_text();constant='const KRUSHER_H7_CUE_HASHES='+json.dumps(hashes,separators=(',',':'))
if 'const KRUSHER_H7_CUE_HASHES=' not in text:
 text=text.replace('static var checked_cues:Dictionary={}',constant+'\nstatic var checked_cues:Dictionary={}')
 text=text.replace('or digest==KRUSHER_H4_CUE_HASHES.get(gear,"")','or digest==KRUSHER_H4_CUE_HASHES.get(gear,"") or digest==KRUSHER_H7_CUE_HASHES.get(gear,"")')
else:
 import re
 text=re.sub(r'const KRUSHER_H7_CUE_HASHES=.*',constant,text)
path.write_text(text)
(H/'floor-cue-proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({'provenCues':len(proof),'guard':'Two exact additional RGBA hashes; all earlier admissions and strict mismatched-cue rejection retained.'}))
