from pathlib import Path
import json, os, uuid
P=Path(__file__).resolve().parent; R=P.parents[1]
e=json.loads((P/'evidence.json').read_bytes()); guard=json.loads((P/'validate-validation.json').read_bytes())
assert e['complete'] and e['failures']==0 and len(e['cases'])==8
assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
note='''

## James ordinary berth rotation review — October 1, 2026

`character/james-berth-rotation-motion-v1`: eight actual normal chooser, clear
approach, automatic arrival and full ordinary rest journeys, four crew_hab room
rotations and both prescribed initial gears. 20489 checks pass; all18 rest slots
selected per case, fixed navigation contact/facing/gear, one completion, fatigue
100->55. No arrival heading discontinuity observed. 248 chronological native
source-change captures reviewed across eight boards, including repeated breathing.
Standing return and captured material continuity look consistent; not continuous
native-video acceptance. 171 frozen source/manifest/controller inputs unchanged.
Engine0/no timeout; strict scratch APPDATA owner fingerprint unchanged.

Important scope: retained authored crew_hab view with no Studio overrides keeps
the same North berth geometry for all room rotations; these are not four distinct
furniture orientations. Initial room/foot/needs/gear resets are prescribed.
No new art or gameplay changes. Special East station-prop bunk, other layouts,
gear acquisition, disk Continue and traffic/hazards are outside this fixture.
Source South reclining faces still appear fuller than standing masters; anatomy
and perspective review remains open. Full James consistency goal remains active.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=path.read_bytes()
    if b'## James ordinary berth rotation review' in data: continue
    new=note.lstrip().encode()+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+note.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp'); tmp.write_bytes(new); os.replace(tmp,path)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James ordinary berth rotation

## Objective and acceptance
Continue full James animation and master consistency work; full goal active.

## Accepted decisions and constraints
Matte neutral masters, stable anatomy/head, genuine normal furniture service.
Existing reversible authorization; scratch APPDATA and strict owner guard.

## Current state
New validate.gd/.uid, runner, frozen inputs, evidence, 248 native captures,
eight chronological boards and compact native-key-poses.png. No production or
art changes. Five current pipeline/bible/skill guides record this milestone.

## Verification
20489 native checks, zero failures, eight ordinary full journeys, all18 slots
per case, fatigue55 and one completion. All eight boards reviewed. 171 frozen
inputs unchanged. Engine0/no timeout; owner profile unchanged. Retained North
bed geometry identical across room rotations, not distinct furniture facings.
No special East bunk, Continue, gear acquisition or continuous video proof.

## Next action
Compare South reclining head anatomy/perspective against masters; fuller face
remains unresolved. Continue actual distinct furniture layouts and cross-family
quality review. Validation session54676 completed; no native job left running.
''')
print('Berth milestone recorded; full goal remains active.')
