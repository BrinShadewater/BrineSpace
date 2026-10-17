"""Record observed route coverage and visual findings separately from assertions."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-carry-short-route-audit-v1'
d=json.loads((O/'records.json').read_text(encoding='utf-8'));v=json.loads((O/'validation.json').read_text(encoding='utf-8'))
provenance=json.loads((P/'short-route-capture-provenance.json').read_text(encoding='utf-8'))
assert v['passed'] and d['failures']==0 and len(d['records'])==8
directions=sorted({s['direction'] for r in d['records'] for s in r['samples']})
phases=sorted({s['phase'] for r in d['records'] for s in r['samples']})
evidence={'validation':v,'records':d,'reviewer':'Codex agent','visualReview':'All eight route boards reviewed against registered source thumbnails. Captured head/helmet, matte suit detail, stature and carried case remain coherent. Completed idle loses the floor case: known unresolved disposition, not full lifecycle acceptance. Static samples do not establish continuous foot support or loop smoothness.','directionsObserved':directions,'phasesObserved':phases,'sourceSelectionChanged':False,'scope':d['scope'],'inputSnapshot':'Post-run only; broader dependency freeze not claimed.'}
evidence['captureProvenance']=provenance
(P/'short-route-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
files=['scripts/bill_carry_player.gd','scripts/bill_carry_npc.gd','scripts/bill_carry_checkpoint.gd','scripts/crew_sprite_player.gd','tests/test_bill_carry_short_route_audit_v1.gd','tools/run_bill_carry_short_route_audit_v1_validation.py']
prior=json.loads((P/'version-input-hashes.json').read_text(encoding='utf-8'))
files+= [k for k in prior if '/frames/' in k or k.endswith('manifest.json')]
hashes={k:hashlib.sha256((R/k).read_bytes()).hexdigest() for k in sorted(set(files))}
(P/'short-route-input-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
section=f'''## Bill actual workshop-generated carrying routes — October 2, 2026

Normal selected Bill actor/player completes all4workshop rotations/both gears,
8routes from prescribed actual service stations. Workshop's generated cargo path
retained; no lane replacement, art/player/controller/gameplay/geometry edits.
{d['checks']}native checks/0fail, engine0/{v['seconds']}s, all{v['realProfileFileCount']}owner non-log
files unchanged under scratch APPDATA. Full initial-foot-to-waypoint distance
recorded, not just final waypoint gap. Observed display directions:{','.join(directions)};
phases:{','.join(phases)}. Per-tick source presence, paired checkpoint admission,
planted turns/arrival and program cleanup verified. Source/native room capture
pairs retained; all8registered route boards visually reviewed. Captured master
stature, matte suit, head/helmet and cargo remain coherent. Completed idle loses
the floor crate; disposition remains unresolved. Static samples do not certify
continuous support, glide or motion smoothness. Paused world/actor60Hz stepping;
prescribed service dispatch, not natural chooser/approach or traffic coverage.
No prelaunch broad input freeze; post-run hashes retained. Full goal incomplete.
Initial13097check/188.77s interval repeated rotation0 because free placement forces
zero. Original logs/records/captures retained. Corrected fixture explicitly sets
fixture room rotation and asserts actual resolved layout quarter; production
placement rules unchanged. Technical green did not establish rotation coverage.
Seven bare rotation0pairs use retained initial-run actual rotation0captures after
stale cleanup lost six pairs and one source file; exact phase/direction/root/state/
key/entry records match. Other59pairs are corrected-run captures. Provenance saved
separately. Final runner's screenshot check did not require every source file;
functional12351guard pass is distinct from capture-retention completeness.
Next carry interruption/put-down/floor-case lifecycle, remaining equipment/actions
and continuous cross-family master/grade polish. Review: character/
bill-carry-start-south-v2/short-route-review.html; SHORT_ROUTE_HANDOFF.md.

'''
for file in [R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 s=file.read_text(encoding='utf-8')
 if section.splitlines()[0] not in s:file.write_text(section+s,encoding='utf-8')
lesson='''
## Measure complete generated cargo routes — October 2, 2026

Measure from the actual actor foot to the first generated waypoint, then each
successive segment. A32unit final waypoint gap can conceal a272unit total route.
Assert the actual resolved layout quarter: free fixture placement deliberately
forces rotation0 even when selected_rotation differs. Retain a mistaken interval
and correct fixture setup rather than changing normal placement behavior.
Retain generated paths across actual room rotations; long prescribed lanes prove
different coverage. Record observed directions and phases rather than declaring
all-cardinal coverage from four room rotations. Native captures, planted-root and
checkpoint checks do not prove continuous foot support or cargo disposition.
Bill's8selected workshop routes pass technical guards and captured style review;
the floor case still disappears at completed idle. Treat that as unresolved
lifecycle work, not a successful put-down. Preserve owner geometry and record
prescribed service dispatch separately from natural chooser/traffic.
Evidence: character/bill-carry-start-south-v2/short-route-evidence.json.
'''
for file in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 s=file.read_text(encoding='utf-8')
 if lesson.splitlines()[1] not in s:file.write_text(s+lesson,encoding='utf-8')
handoff=f'''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill generated cargo routes

## Objective and acceptance
Full master-matched Bill animation set and subsequent full cross-family polish.
This audit advances actual route/contact evidence; full objective incomplete.

## Accepted decisions and constraints
Normal current South3/North2 selection retained. Original room geometry and
generated cargo paths preserved; scratch APPDATA. No commit/export.

## Current state
Added short-route native test/paired UID, runner, preparation/review/evidence
helpers. Eight route boards and original native source/room captures retained.
No production scripts or raster changes. Current status/pipeline/bible/skill
references updated with complete-route measurement and evidence-scope lesson.

## Verification
{d['checks']}checks0fail/{v['seconds']}s/engine0; all{v['realProfileFileCount']}owner non-log files unchanged.
4workshop rotations/both gears from prescribed service dispatch, generated path
unchanged. Observed directions:{','.join(directions)}. Source presence, checkpoint,
planted turns/arrival and completion cleanup verified. All8static native route
boards reviewed; captured size, head/helmet, matte detail and held cargo coherent.
Completed idle drops floor case visibility. No continuous contact/film, natural
chooser/approach/traffic claim. Hashes post-run; broad freeze not established.
Seven bare rotation0pairs use retained earlier actual rotation0captures guarded
by exact pose/root/entry records after stale-cleanup loss; other59pairs current.
short-route-capture-provenance.json records intervals; prior repeated-rotation
run is retained and does not establish all4rotation coverage.

## Next action
Complete source-bound interrupted carrying/put-down return and floor-case
disposition; test actual service loss and Continue. Remaining equipment/actions,
continuous contact and full cross-family motion/master/color polish stay open.
'''
(P/'SHORT_ROUTE_HANDOFF.md').write_text(handoff,encoding='utf-8')
print('Recorded actual directions:',directions,'phases:',phases)
