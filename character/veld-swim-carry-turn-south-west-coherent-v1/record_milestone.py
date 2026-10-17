from pathlib import Path
import json
H=Path(__file__).resolve().parent;R=H.parents[1]
p=json.loads((H/'packaging-checks.json').read_text());assert p['failures']==0 and p['nativeChecks']==195
title='Veld south west cargo swimming turn pair staged — September30,2026'
body='''Second independent paired cargo quarter/reverse staged:4gearstates/24refs, frozen.21body ruler/shared grade, retained canonical yaw helmets, exact south/west cargo endpoints, original800ms.24bodyfit/16helmetfit/39package/195native PASS; profiles unchanged. Source/body/head/native148/82/54 and near-west light browser comparison reviewed. E/S and S/W now8staged turn gearstates/48refs. Both review pages now finite same-clock forward/reverse with source/destination masters; E/S middle light sample reviewed, artwork unchanged. W/N,N/E,4halves, envelopes/final controller/world journeys and remaining distress/recovery/death/life/full-set polish remain. [Handoff](../character/veld-swim-carry-turn-south-west-coherent-v1/FAMILY_HANDOFF.md), [review](http://127.0.0.1:8791/character/veld-swim-carry-turn-south-west-coherent-v1/?v=finite-master-v1). Full goal active.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
 q=R/rel;old=q.read_bytes()
 if title.encode() not in old:q.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Finite cargo turn review — September30,2026

Review finite turn clips with replay, exact phase scrubbing, both directions and
a destination hold. A repeating GIF jumps from the final direction back to the
first and can masquerade as a turn seam defect. Keep export playback separate
from an actual watched-motion claim. Pair both gear modes on one clock and show
source/destination masters at the same physical canvas ruler; examine pose bulk,
case size/grip, attached sleeves and anatomical tool sides through projection.
Measured endpoint face anchors register the orbit, not per-frame bounding-box
normalization. Evidence: Veld cargo south/west FAMILY_HANDOFF.md.
'''
for q in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 if b'Finite cargo turn review' not in q.read_bytes():
  with q.open('ab') as f:f.write(lesson.encode())
print('S/W milestone and finite motion-review lesson recorded.')
