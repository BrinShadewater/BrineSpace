from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
for name in ['native-installed','native-installed-routes']:
 report=json.loads((P/(name+'-validation.json')).read_bytes());assert report['exitCode']==0 and report['realProfileUnchanged']
route=json.loads((P/'installed-route-evidence.json').read_bytes());assert route['failures']==0 and len(route['results'])==24
assert all(s['entered'] and s['completed'] for s in route['results'])
assert sum(len(s['captures']) for s in route['results'])==184
def atomic(path,fn):
 before=path.read_bytes();after=fn(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
 tmp.replace(path)
def append(path,text):
 block=text.encode()
 atomic(path,lambda b:b if block.split(b'\n')[1] in b else b.rstrip()+b'\n'+block+b'\n')
milestone='''
### James ordinary swimming turns installed - 2026-09-30

Twelve ordinary water turns now use four independent quarter source sheets,
with exact installed directional swim endpoints, fixed source anatomical scales,
uniform endpoint material gains and source-authored shared helmet heads. Three
body repairs are preserved alongside their originals; original helmet donors are
reused explicitly because generation did not preserve their pixels exactly.
Eight quarter/reverse states contain six poses,520ms. Four half turns compose
exact quarter donors with the duplicate joint merged:11 poses,680ms. Durations
come from the retained arrays;45+60+65+65+60+45 is340ms, not300ms. No dry-turn
clock substitution, per-pose height normalization or mirrored artwork.
Installed184 selected references across both modes.1146 packaging,2780 actual
installed loader/playback and2581 installed movement/clearance checks PASS.
24 explicitly authored collision-checked two-leg in-room paths use actual NPC
move, normal grid selection and lazy-loaded installed clearance; all184 pose
references rendered,344 turn envelope samples clear,24 actor-on/off checks.
Fresh native82px and flooded-room contacts reviewed; water tint remains dark,
so readability belongs in cross-family polish. These authored paths do not prove
pathfinder-generated cross-room turns, every room layout, exterior or traffic.
Both scratch reports confirm the real profile unchanged. Owner acceptance pending.
Ordinary water turns replace12 retained states;40 bare states remain. Continue
swim cargo turns, swim cargo/pickup, salvage/distress/recovery/death, then full-set
cross-family polish. Non-east swim->activity stop-facing snap remains pending.
See docs/JAMES_WATER_TURNS_HANDOFF_2026-09-30.md and
character/james-water-turn-family-v1/review.gif. Full-set goal remains active.
'''
for path in [R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:append(path,milestone)
status='''## James ordinary swimming turns installed - 2026-09-30

12 states/92 references per mode installed with exact swim endpoints, independent
quarters, fixed anatomy/material scales and shared-helmet head ownership. Quarter
clocks520ms; half clocks680ms,11 exact donor poses with summed90ms middle hold.
1146 packaging,2780 installed loader/playback and2581 installed movement checks
PASS.24 explicitly authored collision-checked two-leg paths exercised actual NPC
move and normal grid/lazy clearance, all184 pose references rendered;344 sampled
turn envelopes clear. Fresh flooded native contacts reviewed, real profile unchanged.
This is not all-layout/pathfinder/exterior/traffic proof; owner acceptance pending.
40 retained bare states remain. Swim cargo turns/cargo/pickup and salvage/distress/
recovery/death are next, followed by cross-family polish. Dark water readability
and non-east activity stop-facing snap remain polish items. Full-set goal active.
See docs/JAMES_WATER_TURNS_HANDOFF_2026-09-30.md and family/review.gif.

'''.encode()
atomic(R/'docs/CURRENT_STATUS.md',lambda b:b if status.split(b'\n')[0] in b else status+b)
handoff='''# James ordinary swimming turns handoff

Updated:2026-09-30 · Project:C:/Users/Alex/Documents/Brine Space · Task:James full animation set

## Objective and acceptance
Continue the full James set against the accepted masters, then cross-family
consistency/polish. Ordinary water-turn milestone is installed, owner review pending.
Full-set goal is active; no claim of complete coverage or owner acceptance.

## Accepted decisions and constraints
Preserve installed swim endpoints byte-exactly, matte neutral graphite and muted
gold, belt wrench, fixed physical source density and35-degree camera. Independent
views, no mirroring or per-pose height normalization. Four independent source
sheets plus three preserved body repairs; original helmet donors reused explicitly.
Quarter520ms and half680ms clocks derive from retained arrays, not dry turns.

## Current state
`character/james-water-turn-family-v1/` owns manifests, reproducible build/extract,
verification, selected-alpha clearance, source records, route fixtures and previews.
Four `james-water-turn-{east-south,south-west,west-north,north-east}-v1/` folders
preserve references, original/v2 sources, prompts/origins, crops and registered frames.
Bare/helmet manifests select12 states/92 refs each,256x276/pivot128,128/standing148.
Four half turns reuse exact quarter PNGs with a shared pose merged into90ms hold.
`scripts/grid_canvas.gd`, `character/ACTIVE_ASSETS.json` and the Branforth root
clearance select these clips. Only transition bounds union was expanded; swim,
tread and unrelated action profiles preserved. Registry/docs/skills writes atomic.
Coverage ledger refresh follows. Remaining retained bare states:40.

## Verification
1146 packaging checks PASS;2782 staged and2780 actual installed loader/clock/pause/
seam checks PASS.2579 staged and2581 installed movement checks PASS.24 authored
collision-checked two-leg paths, actual NPC.move, normal grid selector and installed
lazy clearance, both modes/all12 turns. All184 pose references captured;344 actual
turn envelope samples clear navigation blockers.24 actor-on/off visibility checks.
Native82px contacts and all four fresh installed route boards reviewed;144 selected
route contact samples shown, report captures184 authoritative. All scratch validation
reports confirm unchanged owner profile. Paths are explicit in-room fixtures,
not pathfinder-generated cross-room routes or proof of all layouts/exterior/traffic.
No gameplay/controller changes, release export, commit or push.
One packaging assertion originally mis-totalled retained halves as600ms; corrected
to actual680ms from authoritative arrays. Actual playback was always680ms.
Dark flooded-room tint reduces contrast; assess with the other water animations
in polish rather than brightening source art. Source anatomy remains owner review
pending; technical checks do not establish visual acceptance.

## Next action
Continue12 retained swim-carry turns, then swim-carry/pickup4 each, salvage,
distress,recover-air and two death families4 each. Preserve installed ordinary
water turns as body-angle reference; keep cargo physically coherent and exact
directional cargo endpoints. After remaining40 states, cross-family style/motion
polish, including non-east swim->activity stop-facing snap and underwater contrast.
Commands:build.py,verify.py,derive_clearance.py,prepare_routes.py/prepare_installed.py,
scratch wrapper `character/james-shared-helmet-actions-south-v1/run_validation.py`.
Use family selection.json as current installed status; do not rerun old water
record_packaging.py, which belongs to its staged milestone.
'''
(R/'docs/JAMES_WATER_TURNS_HANDOFF_2026-09-30.md').write_text(handoff,encoding='utf-8')
atomic(P/'selection.json',lambda b:(json.dumps(dict(json.loads(b),installedRuntimeVerification='native-installed-validation.json',installedRouteVerification='native-installed-routes-validation.json',installedRouteEvidence='installed-route-evidence.json',routeVisualReview='All four fresh installed route boards viewed; dark flooded overlay retained; source-native82px contacts reviewed'),indent=2)+'\n').encode())
audit=R/'character/james-animation-coverage-2026-09-30/audit.py'
atomic(audit,lambda b:b.replace(b'Current next work: water turns/carry/pickup, then salvage/distress/recovery/death.',b'Current next work: swim cargo turns/carry/pickup, then salvage/distress/recovery/death. All12 ordinary swimming turns installed in both modes; exact endpoints,520ms quarters/680ms halves and24 authored in-room turn paths reviewed.'))
print('Recorded installed water-turn milestone, scoped proof, source lessons and40-state continuation')
