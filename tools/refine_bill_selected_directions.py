from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path('character/bill-selected-directions-v2');P.mkdir(exist_ok=True)
reports={};tracks=[];original=json.loads(Path('character/crew-runtime-matte-v1/bill/manifest.json').read_text())
for direction,folder in [('south','bill-south-selected-loop-v1'),('north','bill-north-loop-v3')]:
 root=Path('character')/folder;m=json.loads((root/'manifest.json').read_text());s=m['states'][0];dest=P/direction;dest.mkdir(exist_ok=True);hashes={};bounds=[];delta=0
 for f in s['frameFiles']:
  im=Image.open(root/f).convert('RGBA');a=np.array(im)
  if direction=='south':
   rgb=a[:,:,:3].astype(float);luma=(rgb*[.2126,.7152,.0722]).sum(2,keepdims=True);y=np.indices(a.shape[:2])[0];factor=.95-.15*np.clip((y-48)/12,0,1);b=a.copy();b[:,:,:3]=np.clip(np.rint(luma+(rgb-luma)*factor[:,:,None]),0,255);b[a[:,:,3]==0]=a[a[:,:,3]==0];assert np.array_equal(a[:,:,3],b[:,:,3]);delta=max(delta,float(np.abs(((b[:,:,:3].astype(float)-rgb)*[.2126,.7152,.0722]).sum(2)).max()));im=Image.fromarray(b)
  else:
   scale=1.035;im=im.transform((184,184),Image.Transform.AFFINE,(1/scale,0,92*(1-1/scale),0,1/scale,172*(1-1/scale)),Image.Resampling.BICUBIC)
  out=dest/f;out.parent.mkdir(parents=True,exist_ok=True);im.save(out);hashes[f]=hashlib.sha256(out.read_bytes()).hexdigest();bounds.append(im.getbbox())
 s['provenance']=dict(source=folder,method='Fixed body chroma 80%, feather to 95% on head; alpha and poses preserved' if direction=='south' else 'Uniform 1.035 scale around fixed foot pivot (92,172), same transform every frame')
 (dest/'manifest.json').write_text(json.dumps(m,indent=2));(dest/'frame-hashes.json').write_text(json.dumps(hashes,indent=2));reports[direction]=dict(frames=len(hashes),clipped=sum(b[0]<=0 or b[1]<=0 or b[2]>=184 or b[3]>=184 for b in bounds),maxLumaDelta=delta,frameTimingUnchanged=True)
 tracks.append(dict(label=direction.title()+' - revised',files=[direction+'/'+f for f in s['frameFiles']],durations=s['frameDurationsMs']))
(P/'validation.json').write_text(json.dumps(reports,indent=2));print(reports)
# Keep east and west choices unchanged in the overview.
for direction,root in [('east',Path('character/bill-east-selected-loop-v1')),('west',Path('character/crew-runtime-matte-v1/bill'))]:
 m=json.loads((root/'manifest.json').read_text());s=next(s for s in m['states'] if s['id']=='walk-'+direction);tracks.append(dict(label=direction.title()+' - unchanged',files=['../'+str(root.relative_to('character')).replace('\\','/')+'/'+f for f in s['frameFiles']],durations=s['frameDurationsMs']))
tracks.sort(key=lambda t:['South','East','North','West'].index(t['label'].split()[0]))
import re
html=Path('character/bill-selected-directions-v1/index.html').read_text();html=re.sub(r'const tracks=.*?;let loaded=',lambda _: 'const tracks='+json.dumps(tracks)+';let loaded=',html);html=html.replace('Saved muted south and east selections, prepared north loop, and installed west. Review gait, repeat seams and colour consistency at gameplay sizes before installation.','South: 20% less body chroma, with a gentle 5% reduction on skin and hair. North: 3.5% larger around the fixed foot pivot. East and west unchanged.').replace('Exact copied frames. No new generation or colour changes. East and south preserve source timing; north retains its previously prepared timing. Runtime unchanged.','Fixed treatments across every frame; timing and poses retained. Runtime unchanged.');(P/'index.html').write_text(html)
