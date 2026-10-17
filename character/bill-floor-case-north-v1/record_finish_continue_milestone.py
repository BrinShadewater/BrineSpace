from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'finish-continue-review-evidence.json').read_text());v=e['validation'];unit=json.loads((R/'output/bill-floor-case-finish-plan-v1/validation.json').read_text());guard=json.loads((R/'output/bill-floor-case-finish-admission-v1/validation.json').read_text());assert v['passed'] and unit['passed'] and guard['passed']
note=f'''## Bill staged finite-exit checkpoint and fresh Continue — October 2, 2026

finish_plan schema now binds remaining exact authored clock/rows to finish1/case4;
finish_sources locks all28decoded North unload RGBA sources. Actor/player snapshot
markers pair finite exit, gear, source bank, saved clock, contact foot/owning room
and released floor payload. finish_checkpoint admits detached full state/source
before ordinary RunSave station restore, then explicitly rebinds candidate actor/
player. Source-version banks contain only gait/start subsets; shared unload sources
stay in common frames. Normal production selection/save validator/art unchanged.

933headless finite-plan checks0fail/6.05s. {e['checks']}native checks0fail/6actual disk/
fresh-main restores, engine0/{v['seconds']}s: both gears early/pre-release/released
ordinary service-loss exit. Exact immediate source/root/clock/floor, pause and40
future actor/player/source/case ticks match through ordinary activity resumption.
Ten malformed pairing/clock/gear/row/room/foot/floor cases plus altered shared
source per restore reject atomically before live state mutation. All12native
presentations/2boards viewed;24original source-room captures copied unchanged.
Registered head/helmet/body/matte appearance retained; static pairs do not prove
continuous idle/contact polish. Current selected source bank only; older retained
bank variants, Title/new-process and normal admission remain unverified here.

Final20headless real-disk admission checks0fail/{guard['seconds']}s/engine0: missing/
shifted released case, pre-start clock, malformed actor/player exit shapes and
numeric/null version markers reject before any mutable scene access. Legacy fields
absent stays admitted. This final rejection-only typed-marker correction follows
the native interval; valid string-marked restore behavior unchanged. All2931owner
non-log files unchanged in every scratch-profile interval. Input disk SHA retained;
wider controller/code hashes post-run, not prelaunch freeze.

First Continue interval SCRIPT ERROR/170.94s: corruption fixture wrongly looked
for shared unload in partial version bank. Exact errored fixture process stopped;
script/log/report/capture pair retained. Corrected shared frame-table corruption
test passes without weakening source guard. First extra-admission interval logged
int-vs-String comparison error/6.03s despite engine0. Failed guards/log/report/input
hash retained; actor/player/wrapper now type-check version markers before compare.
Errors invalidate a green exit code. No repeated native run for this rejection-only
fix; final real-disk schema/rejection check passes cleanly.

Lesson: preserve full paired metadata and canonical loaded sources before mutating
station state; a finite clock must not restore onto a different body/helmet bank.
Clone common frames and apply versioned subsets, rather than assuming each bank is
a whole library. Typed malformed-save tests catch script errors that process exit
status alone misses. Next flood/global-fallback visibility, early held-case priority
disposition, shared-room lifetime, older-bank/native continuous joins and normal
guarded admission, then remaining full Bill families and cross-master style/polish.
Goal active/incomplete. Review:character/bill-floor-case-north-v1/
finish-continue-review.html; FINISH_CONTINUE_HANDOFF.md. No commit/export.

'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 old=path.read_text(encoding='utf-8');assert note.splitlines()[0] not in old;path.write_text(note+old,encoding='utf-8')
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 with path.open('a',encoding='utf-8') as f:f.write('\n\n'+note)
e['boardsViewed']=2;e['unitValidation']=unit;e['finalAdmissionValidation']=guard;e['nativePrecedesFinalTypedRejectionGuard']=True;e['postRunInputs']={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'finish_actor.gd',P/'finish_player.gd',P/'finish_plan.gd',P/'finish_sources.gd',P/'finish_checkpoint.gd',R/'tests/test_bill_floor_case_finish_continue_v1.gd',R/'tests/test_bill_floor_case_finish_admission_v1.gd']}
(P/'finish-continue-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
(P/'FINISH_CONTINUE_HANDOFF.md').write_text(f'''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill finite-exit Continue

## Objective and acceptance
Full Bill animation set matching masters/style/perspective/stature/proportions/matte
grade, then full cross-family consistency/polish. Goal active and incomplete.

## Accepted decisions and constraints
Original art and normal production selection preserved. Explicit staged wrapper
must admit whole paired metadata and canonical sources before any station mutation.
Keep normal source-version behavior and ordinary RunSave disk/station restore.

## Current state
Updated finish_plan/actor/player, new finish_sources+UID and finish_checkpoint+UID,
six-case Continue fixture/runner, real-disk admission fixture/runner and review.
Two boards/24unchanged source-room captures. All28decoded source locks; no raster edits.

## Verification
933headless finite-plan;{e['checks']}native/6disk-fresh-main/40future updates each;
20final real-disk malformed/legacy admission checks pass. Owner2931non-log files
unchanged in each scratch interval. All12native presentations/2boards viewed.
Native interval precedes final rejection-only version-marker type guards. First
shared-bank fixture error and typed-marker guard error retained independently.
Current source bank only, fixture-selected candidate; no normal/Title/new-process
admission or continuous motion acceptance. Terminal stance remains unresolved.

## Next action
Diagnose flood occlusion/global fallback outside removed room, early held-case
priority disposition and shared-room floor lifetime. Validate older source banks,
native continuous join and normal guarded admission. Remaining Bill families and
full-library master/grade/proportion consistency/polish still open. No commit/export.
''',encoding='utf-8')
print('Finite-exit Continue milestone recorded; pipeline/bible/maintained and installed skill updated.')
