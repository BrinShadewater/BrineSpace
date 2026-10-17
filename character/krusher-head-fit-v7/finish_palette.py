"""Create a final colour layer over validated poses, preserving all head/prop masks."""
from pathlib import Path
from PIL import Image
import json,copy,hashlib
import numpy as np
H=Path(__file__).resolve().parent;R=H.parents[1];O=R/'character/krusher-coherent-bank-v2';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
index=read(H/('source-bank-index.json' if (H/'source-bank-index.json').exists() else 'candidate-bank-index.json'));protected={}
for folder in set(p[6:].rsplit('/',1)[0] for paths in index['candidatePacks'].values() for p in paths):
 root=R/folder
 revision=root/'revision.json'
 if not revision.exists():continue
 for q in read(revision).get('records',[]):
  if not q.get('mask'):continue
  mask=np.array(Image.open(root/q['mask']).convert('L'))>0
  d=q.get('details',{})
  # Allowed edit windows also contain restored shoulder hardware and distant
  # body pixels in padded recovery aliases. Protect the authored head itself,
  # rather than treating that whole old edit window as skin.
  if d.get('headSource') and d.get('paste'):
   head=Image.open(R/d['headSource'].removeprefix('res://')).convert('RGBA')
   layer=Image.new('RGBA',(mask.shape[1],mask.shape[0]));layer.alpha_composite(head,tuple(d['paste']))
   mask=np.array(layer)[:,:,3]>0
  fg=d.get('foregroundMask')
  if fg:
   path=R/fg.removeprefix('res://')
   if path.is_file():mask|=np.array(Image.open(path).convert('L'))>0
  protected[(root/q['output']).resolve()]=mask
cache={};records=[];outindex={'candidatePacks':{'bare':[],'helmet':[]}}
for gear,paths in index['candidatePacks'].items():
 for number,path in enumerate(paths):
  mp=R/path[6:];m=read(mp)
  for s in m['states']:
   files=[]
   for rel in s['frameFiles']:
    src=(R/rel[6:] if rel.startswith('res://') else mp.parent/rel).resolve()
    if src not in cache:
     a=np.array(Image.open(src).convert('RGBA'));out=a.copy();mask=protected.get(src,np.ones(a.shape[:2],bool))
     r,g,b=[a[:,:,i].astype(float) for i in range(3)]
     # Some original suit lettering is yellow-green (G slightly above R).
     # Include that observed accent range while keeping cyan panels out.
     paint=(a[:,:,3]>0)&~mask&(r>g*.85)&(r<g*1.85)&(g>b*1.12)&(g>32)
     lum=(r*.2126+g*.7152+b*.0722)/145
     colour=np.clip(lum[:,:,None]*np.array([82,124,128]),0,190).astype('uint8')
     out[paint,:3]=colour[paint]
     assert np.array_equal(a[:,:,3],out[:,:,3]) and np.array_equal(a[~paint],out[~paint])
     assert np.array_equal(a[mask],out[mask])
     # New colours must be blue/cyan; no unaffected RGB or alpha is rewritten.
     assert np.all(out[paint,0]<=out[paint,1]) and np.all(out[paint,1]<=out[paint,2])
     digest=sha(out.tobytes()+str(out.shape).encode());dst=O/'frames'/(digest+'.png');dst.parent.mkdir(exist_ok=True)
     if not dst.exists():Image.fromarray(out).save(dst)
     maskfile=O/'palette-masks'/(digest+'.png');maskfile.parent.mkdir(exist_ok=True);Image.fromarray(paint.astype('uint8')*255).save(maskfile)
     cache[src]='res://'+dst.relative_to(R).as_posix()
     records.append({'source':src.relative_to(R).as_posix(),'sourceHash':sha(src.read_bytes()),'output':dst.relative_to(O).as_posix(),'outputHash':sha(dst.read_bytes()),'mask':maskfile.relative_to(O).as_posix(),'recolouredPixels':int(paint.sum()),'protectedPixels':int(mask.sum())})
    files.append(cache[src])
   s['frameFiles']=files
  dest=O/'packs'/f'{gear}-{number:02d}.json';dest.parent.mkdir(exist_ok=True);dest.write_text(json.dumps(m,indent=2)+'\n')
  outindex['candidatePacks'][gear].append('res://'+dest.relative_to(R).as_posix())
(H/'source-bank-index.json').write_text(json.dumps(index,indent=2)+'\n')
(O/'candidate-bank-index.json').write_text(json.dumps(outindex,indent=2)+'\n')
(O/'palette-validation.json').write_text(json.dumps({'checks':len(records)*4,'errors':[],'method':'Approved luminance-preserving matte cyan mapping outside recorded head/foreground masks; alpha, geometry and all other pixels exact. Canonical poses remain byte/pixel exact.','records':records},indent=2)+'\n')
print(json.dumps({'sourceImages':len(records),'recolouredImages':sum(q['recolouredPixels']>0 for q in records),'recolouredPixels':sum(q['recolouredPixels'] for q in records),'checks':len(records)*4}))
