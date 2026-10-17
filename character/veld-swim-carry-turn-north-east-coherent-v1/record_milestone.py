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
title='Veld north east cargo swimming turn pair staged — September30,2026'
body='''Fourth independent cargo quarter/reverse staged:4gearstates/24refs,fixed.22body/.083helmet rulers,explicit full-head/case ownership,selected prone helmet construction and exact cargo endpoints,original800ms.28bodyfit/16helmetfit/39package/195actual-player checks PASS;engine errors0,real profile changes0. Source/native148/82/54 and near-east light browser sample reviewed;alpha bounds retained. All4cargoquarter pairs now16staged states/96refs. Original cargo halves confirmed12refs/680ms,not ordinary1040ms or2×quarter800ms. Derive4halves,consolidate,finalcontroller/worldjourneys,then remaining life/distress/recovery/death/full-set polish. [Handoff](../character/veld-swim-carry-turn-north-east-coherent-v1/FAMILY_HANDOFF.md),[review](http://127.0.0.1:8791/character/veld-swim-carry-turn-north-east-coherent-v1/?v=master-cargo-v1). Runtime unchanged;full goal active.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
 q=R/rel;old=q.read_bytes()
 if title.encode() not in old:q.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Cargo material priority and independent turn clocks — September30,2026

Explicit head/case rectangles can overlap at warm silver cuffs. Make semantic
case/grip ownership override skin RGB thresholds and assert those pixels remain
unchanged; narrow boundaries after inspecting the unscaled source. Measure exact
selected endpoint head positions rather than assuming opposite heads occupy
symmetric canvas coordinates. Numeric border checks cannot detect an anchor error.
Cargo half-turn contracts differ from both ordinary swim halves and cargo quarters:
Veld selected legacy cargo halves are12refs/680ms,quarters6refs/800ms. Read their
actual metadata before deriving frames; exact joins alone do not certify pacing.
Evidence: Veld north/east cargo FAMILY_HANDOFF.md.
'''
for q in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 if b'Cargo material priority and independent turn clocks' not in q.read_bytes():
  with q.open('ab') as out:out.write(lesson.encode())
print('N/E milestone, measured bounds and material/timing lessons recorded.')
