from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1];cargo=P.parent/'james-water-cargo-family-v1'
def atomic(path,fn):
 before=path.read_bytes();after=fn(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
 tmp.replace(path)
for folder,names in [(P,['native-installed','native-installed-routes']),(cargo,['native-installed','native-installed-phases'])]:
 for name in names:
  m=json.loads((folder/(name+'-validation.json')).read_bytes());assert m['exitCode']==0 and m['realProfileUnchanged']
route=json.loads((P/'installed-route-evidence.json').read_bytes());assert route['failures']==0 and len(route['results'])==24
samples=sum(s['envelopeSamples'] for s in route['results'])
note='''### James underwater cargo and turns installed — September 30, 2026

The cargo family and four independent quarter-turn sources now replace24 retained
states: salvage, swim-pickup, swim-carry and12 cargo turns.72 cargo plus92 turn
references per mode,328 total;256x276,pivot128,standing148 physical density.
Installed owner review pending; full set and cross-family polish incomplete.

Body repairs ES/WN v2 preserve exact v1 helmet donors. SW/NE v2 correct retained
guide yaw errors and select their matching v2 heads. Source files, original prompts,
origins, previous crops and extraction audits remain. Fixed turn sheet rulers:
ES25/76,SW25/70,WN25/63,NE25/65; use an oblique skull against the matching master,
not the first rear pose to normalize an entire sheet. ES goggles now persist near
the South endpoint. Manual rear-crown proxies are documented, not measured shoulders.
No pose-by-pose height fit, mirroring or procedural replacement of authored limbs.

Cargo pickup retains520ms simulation clock; carry/salvage retain840ms loops.
Cargo quarters retain800ms, composed half turns680ms with merged90ms join hold.
Exact straight cargo endpoints, reverse donors and rigid case seams preserved.
Half/quarter angular speed mismatch remains a full-set timing review item.

712 cargo and1162 turn packaging checks PASS.1580 cargo/2780 turn installed loader
and playback checks PASS.2916 staged and2918 installed route checks PASS:24 authored
collision-checked two-leg flooded-room paths, actual NPC move, normal grid and actual
lazy selected life cargo-turn clearance; all184 turn refs,456 alpha samples reviewed.
The turn gate uses CrewLife.clearance.life cargo-turn-* rather than actions transition-*.
Union actual alpha into life cargo-turn-*; preserve ordinary swim/tread/transition
profiles. Cargo action envelopes also retain conservative existing bounds.

182 installed phase checks PASS: controlled injected helmet exterior salvage,
six pickup slots, pause, one-load commit, exact carry join, short exterior movement,
recall cancellation.32 native captures reviewed. This is not dispatch or a complete
airlock/return/delivery journey, pathfinder-generated routing, all layouts or traffic.
Real owner profile unchanged in all successful scratch-native runs.

Four installed turn route boards and82px body/equipment contacts reviewed. Native
95%-flooded room tint still makes crew dark; preserve material identity and revisit
readability in cross-family polish. Remaining16 states are four directions each of
swim-distress,recover-air,death-ground,death-water. Runtime coverage173 bare3196slots,
171helmet3172slots. Registry coverage does not establish owner acceptance.
See docs/JAMES_WATER_CARGO_HANDOFF_2026-09-30.md. No commit or export.
'''
headline='''## James underwater cargo and turns installed — September 30, 2026

24 states now use independent masters-matched sources, with refined turn anatomy,
fixed skull rulers and preserved helmet donors. Actual loader,24 moving cargo paths
and controlled salvage/pickup/recall checks PASS; scratch owner profile unchanged.
Native contacts reviewed.16 distress/recovery/death states remain, then full-set
material/anatomy/timing/readability polish. Installed owner review pending.
See [handoff](JAMES_WATER_CARGO_HANDOFF_2026-09-30.md).

'''
atomic(R/'docs/CURRENT_STATUS.md',lambda b:b if headline.encode() in b else headline.encode()+b)
for file in [R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 atomic(file,lambda b:b if note.encode() in b else b+b'\n\n'+note.encode())
handoff='''# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James underwater cargo integration

## Objective and acceptance
Continue full James animation replacement and cross-family polish. This milestone
installs cargo/activity/turn families; owner visual acceptance remains pending.

## Accepted decisions and constraints
Matte masters, fixed source skull rulers, sensible compact limbs, rigid case in
both hands, wrench on belt, forward blowtorch for salvage. Exact destination carry
seams and retained gameplay clocks. No per-pose height fitting or mirrored yaw.

## Current state
character/james-water-cargo-family-v1 and james-water-cargo-turn-family-v1 installed
through scripts/grid_canvas.gd and character/ACTIVE_ASSETS.json. Clearance action
cargo/salvage envelopes and life cargo-turn profiles union actual selected alpha;
ordinary swim/tread/transition profiles preserved.24states/328refs in both modes.
ES/WN bodyv2 preservev1 helmets, SW/NE fullv2 correct yaw. Reviewed configs/builders
protected against accidental regeneration/reset. Source revisions and prompts retained.
Pipeline,bible,continuation and maintained/installed crew-consistency skill updated.

## Verification
712 cargo and1162 turn package checks PASS;1580 cargo and2780 turn installed player
checks PASS;2916 staged/2918 installed moving route checks PASS,24 authored two-leg
flooded-room paths,184turn refs,456 alpha samples.182 installed controlled exterior
salvage/pickup/recall checks PASS,32 reviewed captures; real owner profile unchanged.
Native82px contacts and four fresh installed route boards reviewed. Not all layouts,
pathfinder/traffic/exterior-turn proof, dispatch or full airlock delivery proof.

## Next action
Replace16 remaining states:swim-distress,recover-air,death-ground,death-water each
four directions, then cross-family material/anatomy/timing/readability polish.
Revisit cargo680ms halves versus800ms quarters, water arrival stop-facing snap,
flooded tint, helmet/case occlusion, compact legs and prior furniture journey limits.
Coverage173bare3196slots/171helmet3172slots,16retained; full goal remains active.
No jobs running, commit, export or full-set acceptance.
'''
(R/'docs/JAMES_WATER_CARGO_HANDOFF_2026-09-30.md').write_text(handoff,encoding='utf-8')
for name in ['JAMES_WATER_CARGO_STAGING_HANDOFF_2026-09-30.md','JAMES_WATER_CARGO_TURNS_STAGING_HANDOFF_2026-09-30.md']:
 atomic(R/'docs'/name,lambda b:b if b'Installation supersedes this staged snapshot' in b else b'Installation supersedes this staged snapshot: see JAMES_WATER_CARGO_HANDOFF_2026-09-30.md. Earlier evidence below retains its original scope.\n\n'+b)
atomic(cargo/'build.py',lambda b:b.replace(b"status='staged_visual_review_pending'",b'status=STATUS'))
for folder in [cargo,P]:
 selection=json.loads((folder/'selection.json').read_bytes());selection.update(visualReview='Native82px contacts, installed movement/phase contacts reviewed; owner review pending',installedChecks='See JAMES_WATER_CARGO_HANDOFF_2026-09-30.md')
 (folder/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
for d in ['east','south','west','north']:
 folder=P.parent/('james-water-cargo-'+d+'-v1')
 for mode in ['bare','helmet']:
  def status(b):
   m=json.loads(b);m['status']='installed_owner_review_pending';return (json.dumps(m,indent=2)+'\n').encode()
  atomic(folder/(mode+'-manifest.json'),status)
print('Recorded installed milestone;16 states and full-set polish remain. Alpha samples:',samples)
