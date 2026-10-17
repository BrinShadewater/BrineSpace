from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1];B=R/'character/krusher-style-neck-bank-v1';OLD=R/'character/krusher-animation-package-v8';read=lambda p:json.loads(p.read_text());rev=read(B/'revision.json');checks=0
assert len(rev['records'])==3486 and not rev['attachmentFindings']
for q in rev['records']:
 p=B/q['output'];a=np.array(Image.open(OLD/q['source']).convert('RGBA'));b=np.array(Image.open(p).convert('RGBA'));m=np.array(Image.open(B/q['mask']).convert('L'))>0
 assert hashlib.sha256(p.read_bytes()).hexdigest()==q['outputHash'];assert hashlib.sha256((OLD/q['source']).read_bytes()).hexdigest()==q['sourceHash'];assert a.shape==b.shape;assert np.array_equal(a[~m],b[~m]);checks+=4
 if q['gear']=='helmet':assert np.array_equal(a[:,:,3],b[:,:,3]);checks+=1
 if 'primaryHeadAttached' in q:assert q['primaryHeadAttached'];checks+=1
report={'checks':checks,'sourceDrawings':3486,'changedDrawings':sum(q['changedPixels']>0 for q in rev['records']),'attachmentFindings':rev['attachmentFindings'],'outsideHeadNeckMasksExact':True,'allHelmetAlphaExact':True,'errors':[]};(H/'bank-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
