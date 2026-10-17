from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
pack=json.loads((P/'packaging-validation.json').read_text());native=json.loads((P/'native-staged-validation.json').read_text())
assert pack['passed'] and native['exitCode']==0 and native['realProfileUnchanged']
def atomic(path,fn):
 before=path.read_bytes();after=fn(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
 tmp.replace(path)
note='''### James underwater cargo turn auditions - 2026-09-30

Four independent quarter sheets stage12 states/92refs per mode, with exact
staged cargo endpoints, exact reverse and composed11-pose half turns. Retained
cargo quarters are800ms, halves680ms; ordinary swimming quarters are520ms.
Do not infer cargo clocks from ordinary swimming or silently substitute dry clocks.
The differing quarter/half angular speeds remain a cross-family timing review item.
1146 package and2782 standalone native playback/render checks PASS, real profile
unchanged; native82px bare/helmet boards reviewed. Runtime remains unchanged.

Retained geometry guides are not valid yaw ground truth. The first south-west
and north-east sources copied opposite diagonals from those guides. V2 remakes
use actual endpoints only and explicit case/feet positions: SW case lower-left,
feet upper-right; NE case upper-right,feet lower-left. Independent matching helmet
heads remade too; use current v2 head donors, never the rejected v1 donors. All
originals, prompts and source-crop audits preserved. Source5 helmet accidentally
drawn on SW body is unused because endpoints come from exact staged cargo PNGs.

Fixed cranial scales E-S25/76,S-W25/75,W-N25/63,N-E22/75 are auditions, not
accepted anatomy. Two rear-cranium proxies corrected manually. The native boards
still show compressed intermediate legs and some skull/material variation relative
to endpoints; source repairs and fixed ruler recalibration required before selection.
No per-pose bounding-box resizing or pixel stretching to hide anatomy changes.
Bare goggles consistency around south and helmet/case occlusion also need review.
Then derive combined24-state cargo/turn clearance and prove actual installed
movement/phase selection.328 combined staged refs across both modes;40 retained
runtime states still remain. Full-set goal active, no commit or export.
See docs/JAMES_WATER_CARGO_TURNS_STAGING_HANDOFF_2026-09-30.md.
'''
(P/'selection.json').write_text(json.dumps(dict(status='staged_anatomy_refinement_required',runtimeInstalled=False,statesPerMode=12,refsPerMode=92,packagingChecks=1146,nativeChecks=2782,visualReview='Both82px native contacts viewed; yaw repaired but leg compression/skull/material matching still need refinement',ownerAccepted=False,fullSetComplete=False,next='Repair interior anatomy against cargo masters, then combined clearance/installed movement'),indent=2)+'\n')
headline='''## James cargo turn candidates — September 30, 2026

Four independently authored quarter sources stage12 cargo-turn states in both
modes,184 references, exact staged carry endpoints and exact reverse/half joins.
Opposite-diagonal errors from retained guides corrected with explicit SW/NE
remakes.1146 packaging and2782 native playback/render checks PASS; real profile
unchanged. Native review still finds compressed intermediate legs and skull/material
variation, so source refinement precedes combined cargo/turn installation.
Runtime selection unchanged;40 retained states remain. Full animation goal active.
See [handoff](JAMES_WATER_CARGO_TURNS_STAGING_HANDOFF_2026-09-30.md).

'''
atomic(R/'docs/CURRENT_STATUS.md',lambda b:headline.encode()+b if b'## James cargo turn candidates' not in b else b)
for path in [R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 atomic(path,lambda b:b if b'### James underwater cargo turn auditions' in b else b+b'\n\n'+note.encode())
(R/'docs/JAMES_WATER_CARGO_TURNS_STAGING_HANDOFF_2026-09-30.md').write_text('''# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James cargo-turn auditions

## Objective and acceptance
Complete full James animation set and cross-family polish. This batch adds
cargo-turn candidates; full goal remains active and runtime unchanged.

## Accepted decisions and constraints
Exact cargo endpoints, matte masters, fixed source anatomy ruler, compact legs,
two-handed rigid case and belt wrench. Source review and owner acceptance separate.

## Current state
Four james-water-cargo-turn-{pair}-v1 source packs, family scripts/manifests,
native contacts/review.gif.12states/92refs per mode,256x276,p128,standing148.
SW/NEv2 correct wrong diagonals from retained guides; v1 bodies/heads preserved.
Current v2 heads deliberately selected. Pipeline,bible,continuation,skill updated.

## Verification
1146 package and2782 standalone native playback/render checks PASS.
Exact staged carry endpoints, reverse/composition, clocks and paused playback;
82px bare/helmet contacts reviewed, real profile unchanged. Quarters800ms,
halves680ms retained. No installed loader, route/clearance or owner acceptance.

## Next action
Repair compressed intermediate legs, skull/material drift and bare goggles around
south; review helmet/case occlusion. Fixed scale auditions in anatomy-config.json
are provisional, not validated anatomy. build.py reads that file; prepare_build.py
resets its estimates, so preserve deliberate refinements when updating the template.
Then combined cargo family/turn clearance, actual movement/installed selection.
40 runtime states retained;24 staged replacements pending, then16 life/death states
and full-set polish. No commit/export; no jobs still running.
''',encoding='utf-8')
print('Recorded cargo-turn auditions; anatomy refinement remains before installation')
