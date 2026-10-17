from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'finish-priority-review-evidence.json').read_text());v=e['validation'];assert v['passed'] and len(e['boards'])==10
note=f'''## Bill finite-exit priority takeover audit — October 2, 2026

Staged finish_actor/player unchanged; new actual-main priority fixture includes
normal room_flooding.step_crew before controller update.20cases: both gears,
before/after source release, actual fire refresh, room water/air medium selection,
public gear change, mortality and controlled placed-room/occupied removal with
topology rebuild. Each removal starts a fresh main scene. Exit clears immediately;
15future ticks cannot resurrect it or invent/move released floor case. Removal
drops owning room record; retained room canvas is absent. No demolition-UI claim.

{e['checks']}native checks0fail, engine0/{v['seconds']}s, all2931owner non-log files
unchanged under scratch APPDATA. All40presentations/10boards viewed,80original
source-room files copied unchanged; two raw flooded replacement sources viewed.
Gear/death/fire takeover preserves matching source family in sampled views; death
is initial fall/fire is dispatch, not complete fall/escape. Flood overlays obscure
Bill: source admission does not prove native visibility, contact or matte grade.
Bare removed room exposes Bill to space, causing real death/run-report backdrop;
those after-images do not prove visual disappearance, though canvas absence is
checked. No normal selection, ordinary exit Continue or continuous-film acceptance.
Helmeted removal still shows Bill through global actor fallback outside the removed
room; retained-canvas absence does not prove global actor disappearance. Outside
medium/pose/contact remains unaccepted and needs separate native review.

First interval FAILED flood checks20failures/48.83s: fixture skipped world water/
air update, kept dry mode and allowed unfinished exit to release case. Failed
script/log/report/20captures retained. Fixture now calls actual step_crew before
actor update, preserving strict guards; candidate/production code unchanged.
Second interval962checks0fail/54.72s but reused scene let bare-removal run report
obscure later captures. Full script/log/report/records/80captures retained. Final
fresh-removal fixture prevents cross-case overlay contamination. Broad hashes
post-run, not prelaunch frozen. Normal gameplay/failure conditions retained.

Lesson: callers select movement medium before actor animation logic; isolated
controller tests cannot certify flooding without that world boundary. Actual
outside exposure can legitimately conclude a fixture run; give destructive cases
fresh scenes and report frozen result backdrops separately from live room drawing.
Native overlays can hide valid sprites; green texture/priority checks do not close
visual visibility. Next bound ordinary exit checkpoint/Continue, flood visibility,
early held-case priority disposition and continuous idle join/shared-room lifetime,
then normal admission/remaining full Bill set and master/grade consistency polish.
Goal active/incomplete. Review:character/bill-floor-case-north-v1/
finish-priority-review.html; FINISH_PRIORITY_HANDOFF.md. No commit/export.

'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 old=path.read_text(encoding='utf-8');assert note.splitlines()[0] not in old;path.write_text(note+old,encoding='utf-8')
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 with path.open('a',encoding='utf-8') as f:f.write('\n\n'+note)
e['boardsViewed']=10;e['rawFloodSourcesViewed']=2;e['visibilityAcceptance']={'flood':False,'bareRemovedResultBackdrop':False};e['postRunInputs']={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'finish_actor.gd',P/'finish_player.gd',R/'tests/test_bill_floor_case_finish_priority_v1.gd',R/'scripts/room_flooding.gd']}
(P/'finish-priority-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
(P/'FINISH_PRIORITY_HANDOFF.md').write_text(f'''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill finite-exit priorities

## Objective and acceptance
Full Bill set matching master/style/perspective/stature/proportions/matte grade,
then full cross-family consistency and polish. Goal active and incomplete.

## Accepted decisions and constraints
Preserve original art, normal gameplay/failures and production selection. Ordinary
finite exit must yield immediately to priority. World medium update precedes actor.

## Current state
Priority fixture/runner/review builder,10boards and80unchanged source-room captures.
Candidate actor/player unchanged.20cases include real fire/flood/gear/death and
controlled room ownership removal/topology. Four removal cases use fresh main scenes.

## Verification
{e['checks']}native checks0fail/20cases/{v['seconds']}s/engine0, owner2931non-log
files unchanged.15future ticks per case.40presentations/10boards +2raw flood sources
viewed. Flood overlays obscure Bill; bare removal causes genuine exterior death and
run-report frozen backdrop. Those views do not prove pose visibility/disappearance.
Helmeted removal renders Bill globally outside the absent room; outside medium and
pose/contact remain unaccepted. The canvas guard does not assert global invisibility.
Initial failed skipped-medium interval and second technical-green but overlay-
contaminated interval retained independently. No assertion/candidate changes.

## Next action
Detached finish-exit actor/player/source/clock checkpoint binding and ordinary disk/
fresh-main Continue. Diagnose native flood visibility, early held-case disposition,
shared-room floor lifetime and continuous idle join. Candidate remains unselected;
remaining full Bill families/master/color/proportion polish still open.
''',encoding='utf-8')
print('Priority milestone recorded with technical/visibility limits; pipeline/bible/skills updated.')
