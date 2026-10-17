from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
package=json.loads((P/'packaging-validation.json').read_text());native=json.loads((P/'native-staged-validation.json').read_text());phase=json.loads((P/'phase-evidence.json').read_text());phase_run=json.loads((P/'native-phases-validation.json').read_text())
assert package['passed'] and package['statesPerMode']==12
assert native['exitCode']==0 and native['realProfileUnchanged']
assert phase['failures']==0 and len(phase['results'])==4 and phase_run['exitCode']==0 and phase_run['realProfileUnchanged']
def atomic(path,fn):
 before=path.read_bytes();after=fn(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
 tmp.replace(path)
note='''### James underwater salvage, pickup and cargo staged - 2026-09-30

Twelve directional states /72 references per mode are staged in
character/james-water-cargo-family-v1; runtime selection remains unchanged.
Independent source bodies, common256x276 canvas/p128,148px physical ruler,
one cranial source scale/facing and uniform material gains. Exact salvage0 to
pickup0 and pickup5 to carry0 joins; loops close on exact neutral. Retained840ms
salvage/carry and520ms simulation-driven pickup clocks, only swim-carry stride
.16 added by this pack. Wrench remains on belt; salvage uses forward blowtorch,
pickup stows it and reaches for graphite case. West downward-aiming source3
excluded explicitly. Helmets reuse accepted prone donor4 at fixed shell scale;
body pixels outside recorded owned-head bounds remain exact.

North full-sheet repairs kept copying the overly upright first source. Isolate
the actual prone master as the only geometry reference; its22px skull width and
82px skull-to-heels projection establish the pitch ruler. V5 now provides compact
rear swimming anatomy and visible loose-case reach/grasp. Preserve rejectedv3,
candidatev4 and selectedv5, original prompts and native source paths. Never hide
pitch errors by resizing each frame to a common bounding-box height.

712 packaging and1581 standalone native playback/render checks PASS; both82px
native contact boards reviewed.183 controlled helmet exterior phase checks PASS:
actual expedition advance, normal grid with candidate manifest injected, six
pickup slots, cosmetic-clock pause, one load committed at completion, no delivery
before safe return, recall cancels uncommitted pickup, short exterior movement.
32 captures reviewed,12 actor-on/off checks. Fixture begins in injected salvage,
not actual dispatch or a complete airlock journey. Bare water sprites are verified
in the standalone player; actual exterior medium correctly requires helmet gear.
Fixture errors (wrong visual-clock field, bare exterior assumption, unsettled
first viewport) preserved before repair; no gameplay changes. Real profile
unchanged in all reports. No owner acceptance or full-route/turn-clearance claim.

Next:12 independently authored swim-carry turns using these exact cargo endpoints,
then combined clearance/installed loader and movement checks before selection.
40 retained runtime states remain until installation; full-set polish active.
See docs/JAMES_WATER_CARGO_STAGING_HANDOFF_2026-09-30.md and family/review.gif.
'''
(P/'selection.json').write_text(json.dumps(dict(status='staged_native_reviewed_installation_pending',runtimeInstalled=False,statesPerMode=12,refsPerMode=72,sourceReview='All four registered/paired contacts and native82px boards viewed; northv5 replaces overly upright source',phaseScope=phase['scope'],packagingChecks=package['checks'],phaseChecks=phase['checks'],fullSetComplete=False,next='Create matching cargo turns, derive combined clearance, installed validation and selection'),indent=2)+'\n')
headline='''## James underwater cargo family staged — September 30, 2026

Salvage, pickup and swim-carry now have four directional source packs in both
bare and helmet modes,144 staged references. North remade from isolated prone
master to correct projected body length.712 packaging,1581 native playback and
183 controlled helmet expedition phase checks PASS; native previews and32 phase
captures reviewed. Real profile unchanged. Runtime selection remains unchanged;
matching12 cargo turns and combined clearance/installed checks are next.
40 retained runtime states remain. Owner acceptance and full-set polish pending.
See [handoff](JAMES_WATER_CARGO_STAGING_HANDOFF_2026-09-30.md).

'''
atomic(R/'docs/CURRENT_STATUS.md',lambda b:headline.encode('utf-8')+b if b'## James underwater cargo family staged' not in b else b)
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 atomic(path,lambda b:b if b'### James underwater salvage, pickup and cargo staged' in b else b+b'\n\n'+note.encode('utf-8'))
handoff='''# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James underwater cargo staging

## Objective and acceptance
Complete James's full animation set with master style, scale and perspective;
then cross-family polish. This milestone stages salvage/pickup/carry; goal active.

## Accepted decisions and constraints
Matte master materials, fixed per-source anatomy scale, forward blowtorch for
salvage, belt wrench fixed, two-hand graphite case pickup/carry. Bare/helmet
coverage separate from owner acceptance. Reversible continuation authorized.

## Current state
Four james-water-cargo-{direction}-v1 packs, family scripts/manifests/review.gif,
12states/72refs per mode. Northv5 selected for staging after v3/v4 rejected for
body projection; v1/v2 preserved. Cranial proxies explicitly labelled, fixed
scales E25/43,S25/55,W25/44,N22/55. Existing prone helmet donor4 fitted without
editing body pixels beyond recorded head region. Shared runtime selection untouched.
Pipeline,bible,continuation and repo/installed crew-consistency notes updated.

## Verification
712 packaging;1581 standalone native playback/render;183 controlled helmet
expedition phase checks PASS. Two82px boards and32 normal-grid phase captures
reviewed; twelve actor-on/off checks. Actual pickup clocks, cargo commit and recall
branches exercised from injected salvage states, short exterior move; not actual
dispatch, a full airlock journey, collision/turn proof or installed loader checks.
Real owner profile unchanged. Failed fixture evidence retained. No commit/export.

## Next action
Create12 matching swim-carry-turn states from exact staged carry endpoints;
preserve retained clocks, then combined alpha clearance and actual installed
loader/movement proof before selecting. Runtime still has40retained states.
Then distress/recover/deaths and cross-family anatomy/material/motion polish.
Known non-east swim-to-activity stop-facing snap and water readability pending.
'''
(R/'docs/JAMES_WATER_CARGO_STAGING_HANDOFF_2026-09-30.md').write_text(handoff,encoding='utf-8')
print('Recorded staged12-state milestone; runtime unchanged; full-set goal active')
