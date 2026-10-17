from pathlib import Path
import json
import numpy as np
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1]
p=json.loads((H/'packaging-checks.json').read_text());assert p['failures']==0 and p['nativeChecks']==195
bounds={}
for f in p['frameHashes']:
 a=np.array(Image.open(H/f));y,x=np.where(a[:,:,3]>20);b=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];bounds[f]={'canvasBounds':b,'pivotRelativeAt148':(np.array(b)-128).tolist(),'pivotRelativeAt82':((np.array(b)-128)*82/148).tolist()}
(H/'alpha-bounds-v1.json').write_text(json.dumps(dict(alphaThreshold=20,standingHeight=148,pivot=[128,128],frameBounds=bounds,scope='Measured frames only; world clearance not certified'),indent=2)+'\n',encoding='utf-8')
title='Veld west north cargo swimming turn pair staged — September30,2026'
body='''Third independent cargo quarter/reverse staged:4gearstates/24refs, fixed.22body/.07helmet rulers, explicit rear-head/case ownership, selected prone helmet construction, exact cargo endpoints and original800ms. Revised source fixes repeated early yaw and cardinal last pose.28bodyfit/16helmetfit/39package/195actual-player checks PASS; engine errors0, real profile changes0. Source/native148/82/54 and middle light browser sample reviewed; alpha bounds retained. E/S,S/W,W/N now12staged states/72refs. N/E,4halves,final controller/world journeys and remaining life/distress/recovery/death/full-set polish remain. [Handoff](../character/veld-swim-carry-turn-west-north-coherent-v1/FAMILY_HANDOFF.md), [review](http://127.0.0.1:8791/character/veld-swim-carry-turn-west-north-coherent-v1/?v=rear-master-v1). Runtime unchanged; full goal active.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
 q=R/rel;old=q.read_bytes()
 if title.encode() not in old:q.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Rear cargo yaw landmarks and case ownership — September30,2026

Rear cargo views can have no visible face: register explicit full cranial/bun
centers interpolated between selected endpoints, never a skin-pixel fallback or
per-frame silhouette size. Semantic case/grip exclusions keep pooled suit grade
from flattening cargo materials. Preserve raw head/hair except visible skin;
reuse independently authored prone skull views at a fixed atlas ruler and restore
foreground grips after helmet fitting. Inspect body/head/case axes together: a
numeric angle prompt can repeat early yaw or supply a cardinal pose as an interior.
Retain rejected sources and revise yaw before packaging. Bounds measurements and
native player clocks are separate from actual world-route clearance and motion
acceptance. Evidence: Veld west/north cargo FAMILY_HANDOFF.md.
'''
for q in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 if b'Rear cargo yaw landmarks and case ownership' not in q.read_bytes():
  with q.open('ab') as out:out.write(lesson.encode())
print('W/N milestone, alpha bounds and rear cargo lessons recorded.')
