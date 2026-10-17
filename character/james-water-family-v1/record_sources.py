from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
def atomic(path,fn):
 before=path.read_bytes();after=fn(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
 tmp.replace(path)
entry='''## James independent water sources staged - 2026-09-30

Four independently generated18-pose tread/swim/start sheets saved with exact prompts,
originals, body crops, contracts and fixed-scale anatomy auditions. Grayscale older
motion guides used separately from master identity/material references. North v2
corrects overlong axial prone bodies; four new rear-facing start interiors saved
separately, still pending torso/pitch matching to the loop. Initial cranium-ruler
scales E.5/S.480769/W.471698/N.468085; bent-knee heights do not set scale.
No water runtime change or owner acceptance. Material grade, anatomical review,
shoulder/head registration, shared endpoints/helmets, selected-pixel clearance and
actual water routes remain before installation. Target16 paired states; current
inventory still68 retained bare. Full-set and later cross-set polish remain active.
See docs/JAMES_WATER_HANDOFF_2026-09-30.md and james-water-*/anatomy-audition.png.

'''
lesson='''

### James water source anatomical auditions - 2026-09-30

Separate a grayscale retained stroke/registration guide from the actual identity
and material master: old axial water bodies can be vertically stretched and their
launch poses enlarged. Foreshorten the prone body in depth through authored pose,
keeping physical head/shoulder/boot widths. Do not normalize the entire swimmer's
height or shrink its head to fix perspective. Bent tread knees invalidate a
crown-to-sole scale ruler; inspect a named cranial/torso landmark instead. A
cranial-width audition alone does not prove torso/limb proportion matching.
North loops can improve while start interiors still yaw or wave one arm. Check
these separately; independently redraw the failed interiors, then compare physical
neck/backpack/limb mass to both endpoints before selecting. Document audit canvas
bottom alignment separately from real world shoulder registration. Named source
caps, extraction counts and contact boards are production evidence, not runtime
or motion acceptance. Evidence: docs/JAMES_WATER_HANDOFF_2026-09-30.md.
'''
for rel,text,prepend in [('docs/CURRENT_STATUS.md',entry,True),('docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',entry,False),('docs/ASSET_PIPELINE_AND_WORKFLOW.md',lesson,False),('docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',lesson,False),('skills/brinespace-character-pipeline/references/crew-consistency.md',lesson,False)]:
 path=R/rel;marker=(entry if text==entry else lesson).strip().splitlines()[0].encode()
 if marker not in path.read_bytes():atomic(path,lambda b,t=text.encode(),p=prepend:t+b if p else b+t)
path=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if b'### James water source anatomical auditions - 2026-09-30' not in path.read_bytes():atomic(path,lambda b:b+lesson.encode())
path=P/'selection.json'
def selected(b):
 m=json.loads(b)
 if m.get('status')!='source_anatomy_audition_pending':return b
 m['northStartInteriors']='../james-water-north-v1/source-start-interiors-v3.png';m['northStartInteriorsStatus']='pending neck/backpack/leg scale and pitch continuity to both endpoints';m['pending'][0]='Select or refine north start interiors after anatomical review';return (json.dumps(m,indent=2)+'\n').encode()
atomic(path,selected)
print('Water source milestone and pending full-set work recorded')
