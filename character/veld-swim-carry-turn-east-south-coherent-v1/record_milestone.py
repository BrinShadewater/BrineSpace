from pathlib import Path
import json
H=Path(__file__).resolve().parent;R=H.parents[1]
p=json.loads((H/'packaging-checks.json').read_text());assert p['failures']==0 and p['nativeChecks']==195
title='Veld east south cargo swimming turn pair staged — September30,2026'
body='''First paired cargo quarter/reverse now master-joined:4gearstates/24refs, original800ms, shared.24body ruler/grade and selected ordinary-turn helmet components. Repaired third yaw prevents near-repeated middle angles; tightened head erasure preserves warm-tinted harness and case foreground.24barefit/16helmetfit/39package/195native PASS, owner files unchanged. Source/native148/82/54/body/master/helmet boards reviewed; full-speed/reverse dark/light review pending. Runtime/registry/clearance unchanged. Other quarters,4halves, final controller/world envelopes/journeys and remaining distress/recovery/death/life/full-set polish remain. [Handoff](../character/veld-swim-carry-turn-east-south-coherent-v1/FAMILY_HANDOFF.md), [review](http://127.0.0.1:8791/character/veld-swim-carry-turn-east-south-coherent-v1/). Full goal active.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
 q=R/rel;old=q.read_bytes()
 if title.encode() not in old:q.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Cargo yaw pacing and warm hardware protection — September30,2026

Numeric turn-angle prompts do not prove angular progress. Inspect head/torso/hip
axis across the atlas; nearby middle angles caused a visual stall in Veld cargo
E/S source1. Select only the targeted revised cell and preserve original others,
source hashes and rejected board. Exact endpoint pixels still do not prove pacing.
Reused shared helmet heads need fresh fit to cargo arms and case. Broad warm-head
erasure also classified warm silver harness pixels; restrict connected brown/skin
support and inspect the collar/harness alpha, not just outside-mask equality.
Keep case/glove foreground and grade once from raw sources. Evidence:
character/veld-swim-carry-turn-east-south-coherent-v1/FAMILY_HANDOFF.md.
'''
for q in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 if b'Cargo yaw pacing and warm hardware protection' not in q.read_bytes():
  with q.open('ab') as f:f.write(lesson.encode())
print('Cargo E/S milestone and source/helmet lessons recorded.')
