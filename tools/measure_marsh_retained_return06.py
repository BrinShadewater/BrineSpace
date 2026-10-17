from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
root=Path.cwd();b=root/'character/marsh-retained-gesture-material-v1';o=b/'east-return06-unselected'
load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
new=load(o/'manifest.json')['states'][0];old=load(b/'east04-unselected/manifest.json')['states'][0]
seq=[Image.open(root/p.removeprefix('res://')).convert('RGBA') for p in new['frameFiles']]
seq[0].save(o/'gesture.apng',format='PNG',save_all=True,append_images=seq[1:],duration=[150]*6,loop=1,disposal=0,blend=0)
ap=Image.open(o/'gesture.apng');assert ap.n_frames==6
for i,im in enumerate(seq):
 ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==150
metrics={}
for name,state in [('prior04',old),('return06',new)]:
 masks=[np.array(Image.open(root/p.removeprefix('res://')).convert('RGBA'))[58:121,:,3]>80 for p in state['frameFiles']]
 metrics[name]={'fixedRowBand':[58,121],'alphaThreshold':80,'adjacentChangedAlphaPixels':[int(np.count_nonzero(a!=c)) for a,c in zip(masks,masks[1:])]}
metrics['scope']='Fixed torso/arm row-band silhouette change, includes body edges and registration; not tracked glove centers or perceived motion/smoothness proof.'
(o/'transition-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
print(json.dumps(metrics))
