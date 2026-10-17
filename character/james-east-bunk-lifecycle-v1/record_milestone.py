from pathlib import Path
import json,hashlib,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'evidence.json').read_bytes());g=json.loads((P/'validate-validation.json').read_bytes())
assert e['complete'] and e['failures']==0 and g['exitCode']==0 and not g['timedOut'] and g['realProfileUnchanged']
inputs=json.loads((P/'inputs-before.json').read_bytes())
changed=[p for p,h in inputs.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert set(changed)=={'scripts/bill_npc.gd','scripts/branforth_npc.gd'},changed
(P/'input-change-evidence.json').write_text(json.dumps({'inputs':len(inputs),'changed':changed,'unchanged':len(inputs)-len(changed),'after':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in inputs}},indent=2))
note=f'''

## James actual East bunk Continue and interrupted exit — October 1, 2026

`character/james-east-bunk-lifecycle-v1` proves actual default authored unmirrored
East station-prop bunk at room rotation3, genuine fatigue chooser/clear approach,
automatic arrival, full entry/static sleep/exit, both prescribed initial gears.
Normal rest ends at fatigue55 with exactly one completion event. All30 selected
source references reviewed; six exact reverse/join/1840ms source checks pass.

Six actual scratch disk checkpoints during entry/sleep/exit restore into fresh
main scenes with exact actor/player/source/offset/clock/resources and paused
freeze. Actual power loss then completes visible return without a false event.
Baseline3780checks exposed two genuine failures: loss during an already active
life_get_up discarded stage/timer and snapped to standing. Complete baseline and
original captures retained in baseline-before-exit-fix. Initial camera left actor
offscreen; those captures establish no furniture visual acceptance.

Production fix: bill_npc optional retain_interrupted_rest_exit hook preserves the
existing get-up timer after service goal clears; branforth opts in only for active
special bunk exit. Safety precedence and cleared-goal reward suppression retained.
Fixture now observes settled room camera and checks actor visibility; corrected
chronological furniture/Continue boards reviewed. {e['checks']}checks0failures,
{len(e['records'])}native captures; engine0/no timeout, full owner profile unchanged.
39 of41 frozen source/controller inputs unchanged; only two named controllers
changed. No source art, masters, material, body ruler, furniture, owner layouts or
gear acquisition changed. Static bunk sleep is one source per gear, not breathing.

Scope excludes other room layouts/rotations, hazards/traffic, acquired gear and
continuous native video acceptance. Full James library and cross-family visual
acceptance remain incomplete. Next: remaining interrupted rest contexts and
full-family continuous/master material and proportion review.
'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    data=path.read_bytes()
    if b'## James actual East bunk Continue and interrupted exit' in data:continue
    updated=note.lstrip().encode()+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+note.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(updated)
    assert path.read_bytes()==data;os.replace(tmp,path)
(P/'HANDOFF.md').write_text(f'''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James actual East bunk lifecycle

## Objective and acceptance
Continue full James/master consistency work; full library acceptance incomplete.

## Accepted decisions and constraints
Keep matte selected masters, fixed rulers, belt wrench and current furniture.
Power loss during an authored return must finish that return without rest reward.

## Current state
Two narrow controller changes: bill_npc optional retention hook, branforth active
bunk-only opt-in. New actual lifecycle/Continue fixture and native review boards.
Archived complete failing baseline, original camera and both controller texts.
Five guides record outcome and reusable source/context evidence limits.

## Verification
Six source checks; {e['checks']}native checks0fail/{len(e['records'])}captures reviewed.
Two normal genuine chooser/approach/rest completions; six fresh actual disk
Continues and subsequent power interruptions. Exact pose/clock/pause/resources.
Strict scratch full owner fingerprint unchanged, terminal engine0/no timeout.
39/41 inputs unchanged; only two intended controllers differ. Actual default
East bunk q3 only, static sleep, prescribed gears, no continuous video proof.

## Next action
Remaining interrupted rest contexts and full-family continuous/master quality.
No commit/export requested. Preserve concurrent actor work and selected sources.
''')
print('Recorded actual East bunk fix and bounded visual/native evidence in five guides.')
