from pathlib import Path
from PIL import Image
import json
P=Path(__file__).resolve().parent;R=P.parents[2];checks=0
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text());lo=m['states'][1];up=m['states'][2]
 refs=lo['frameFiles']+[lo['frameFiles'][-1]]+up['frameFiles']+[up['frameFiles'][-1]];holds=lo['frameDurationsMs']+[600]+up['frameDurationsMs']+[600]
 ims=[Image.open(R/f[6:]).convert('RGBA') for f in refs]
 ims[0].save(P/f'{gear}-kneel-rise-preview.png',save_all=True,append_images=ims[1:],duration=holds,loop=0,disposal=0,blend=0)
 for state in m['states']+[dict(id='kneel-rise-preview',frameFiles=refs,frameDurationsMs=holds)]:
  groups=[]
  for ref,hold in zip(state['frameFiles'],state['frameDurationsMs']):
   im=Image.open(R/ref[6:]).convert('RGBA')
   if groups and im.tobytes()==groups[-1][0].tobytes():groups[-1][1]+=hold
   else:groups.append([im,hold])
  ap=Image.open(P/f'{gear}-{state["id"]}.png');assert ap.n_frames==len(groups);checks+=1
  for i,(im,hold) in enumerate(groups):
   ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes();assert ap.info['duration']==hold;checks+=2
(P/'APNG_REVIEW.json').write_text(json.dumps(dict(checks=checks,failures=0,allSourceSlots=142,lowerAndRiseSlots=57,lowerAndRiseDurationMs=1000,previewDurationMs=3200,previewHoldsNotExamination=True),indent=2)+'\n')
print('Grouped APNG checks:',checks)
