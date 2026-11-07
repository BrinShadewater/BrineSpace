from pathlib import Path
from collections import deque
from PIL import Image
import numpy as np, hashlib, json
root=Path(__file__).parent
records=[]
for state in ['occupied','empty']:
 source=root/f'{state}-source.png'
 im=Image.open(source).convert('RGBA'); a=np.array(im)
 if state=='occupied':
  # Generated alpha includes a soft exterior halo; preserve the solid silhouette.
  a[:,:,3]=np.where(a[:,:,3]>=200,255,0)
 else:
  rgb=a[:,:,:3].astype(int); eligible=(rgb.min(2)>175)&((rgb.max(2)-rgb.min(2))<24)
  h,w=eligible.shape; seen=np.zeros((h,w),bool); q=deque()
  for x,y in [(x,y) for x in range(w) for y in [0,h-1]]+[(x,y) for y in range(h) for x in [0,w-1]]:
   if eligible[y,x] and not seen[y,x]:seen[y,x]=True;q.append((x,y))
  while q:
   x,y=q.popleft()
   for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if 0<=nx<w and 0<=ny<h and eligible[ny,nx] and not seen[ny,nx]:seen[ny,nx]=True;q.append((nx,ny))
  a[seen,3]=0
 # Same canvas / same registration, half-size nearest sampling, no independent crop.
 out=root/f'{state}.png';Image.fromarray(a).resize((512,768),Image.Resampling.NEAREST).save(out)
 records.append({'state':state,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source_size':im.size,'output_size':[512,768]})
# Register both states to the generated empty machine's shared exterior silhouette.
# This strips the occupied source's opaque halo without altering any interior art.
occupied=Image.open(root/'occupied.png'); empty=Image.open(root/'empty.png')
occupied.putalpha(empty.getchannel('A')); occupied.save(root/'occupied.png')
records[0]['output_sha256']=hashlib.sha256((root/'occupied.png').read_bytes()).hexdigest()
(root/'manifest.json').write_text(json.dumps({'department':'Android servicing / engineering','condition':'powered-down derelict; localized wear','camera':'south-facing elevated orthographic','host':'recovered cryo shell, dedicated charging wreck subtype','canvas_registration':{'source_size':[1024,1536],'ground_pivot':[512,1435],'visible_width':684},'cleanup':'occupied alpha>=200; empty edge-connected neutral >175, chroma<24; shared 0.5 nearest resize','records':records},indent=2))
