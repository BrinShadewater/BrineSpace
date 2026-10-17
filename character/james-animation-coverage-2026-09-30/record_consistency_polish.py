"""Record the reviewed milestone only after installed evidence reaches PASS."""
from pathlib import Path
import json

P=Path(__file__).resolve().parent
R=P.parents[1]
air=R/'character/james-air-family-v1'
death=R/'character/james-death-family-v1'
turn=R/'character/james-water-cargo-turn-family-v1'
def read(p):return json.loads(p.read_text())
for folder,names in [(air,['native-north-polish','native-north-polish-behaviour']),
                     (death,['native-restore']),
                     (turn,['native-installed','native-installed-routes'])]:
    for name in names:
        v=read(folder/(name+'-validation.json'))
        assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'], (folder,name)
for folder in [air,turn]:assert read(folder/'packaging-validation.json')['passed']
restore=read(death/'restore-evidence.json')
assert restore['checks']==402 and restore['failures']==0 and len(restore['results'])==32
assert all(r['actualDiskRestore'] for r in restore['results'])
routes=read(turn/'installed-route-evidence.json')
assert routes['failures']==0 and len(routes['results'])==24
assert all(r['completed'] for r in routes['results'])
samples=sum(r['envelopeSamples'] for r in routes['results'])
assert read(turn/'frame-hashes.json')==read(turn/'before-half-turn-timing-polish/frame-hashes.json')
diagnostics=read(P/'consistency-review/diagnostics.json')
families=sorted(p.name.removesuffix('-page-0.png') for p in (P/'consistency-review').glob('*-page-0.png'))
assert len(families)==41 and diagnostics['sampledClips']==344
ledger=dict(date='2026-09-30',scope='Visual inspection of first/middle/final selected poses in both modes, fixed 82px standing scale, all pages including 12-state turn families; not every-frame motion or full journey acceptance.',familiesReviewed=families,
    dryTurnHeight=dict(measurements='turn-height-review/measurements.json',allSlotsMeasured=True,uniqueFullPoseBoardsReviewed=['east-south','north-east','north-west','south-west','east-west','north-south'],bareHeightRange=[147,149],bareMasterHeightRange=[147,148],rearHelmetMasterHeight=150,sideHelmetMasterHeight=156,perPoseResizing=False),
    corrected=['North dry recovery slim long legs/close stance with master-only v3 source','Underwater cargo half clock composed from two quarters:680 to1600ms,quarter800 retained,all pose hashes unchanged','Review water boards include actual alpha bounds around pivot','Route fixture checks cargo-turn life keys rather than equality with a historical whole profile'],
    remaining=['Full motion/material/transition review across families','North ordinary water tread/start/stop boot proportions','West water death projected limb-length seam','Actual non-East activity arrival facing continuity','North neutral sleep breathing','Full furniture/meal/equipment/exterior dispatch-airlock-cargo-return handoffs','Owner and release acceptance'])
(P/'consistency-review/review-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
timing=dict(status='installed_owner_review_pending',quarterMs=800,halfMs=1600,previousHalfMs=680,allPoseFileHashesUnchanged=True,packagingChecks=1162,installedPlayerChecks=2804,installedRouteChecks=routes['checks'],routes=24,envelopeSamples=samples,scope=routes['scope'])
(turn/'timing-polish.json').write_text(json.dumps(timing,indent=2)+'\n')

selection=read(turn/'selection.json')
selection.update(packagingChecks=1162,nativeChecks=2804,
    quarterMs=800,halfMs=1600,
    installedRouteChecks=routes['checks'],
    next='Full motion/arrival-facing and exterior dispatch-airlock-cargo-return handoff polish',
    installedChecks='See JAMES_CONSISTENCY_HANDOFF_2026-09-30.md and timing-polish.json')
(turn/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
selection=read(air/'selection.json')
selection.update(northRecoveryPolish=dict(source='james-air-north-v1/recover-source-v3.png',
    ruler='22/102',packagingChecks=528,installedPlayerChecks=1044,
    actualNorthBehaviourChecks=119,cases=2,captures=24),
    next='Full motion/arrival-facing and complete low-air travel handoff polish')
(air/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')

def atomic(file,fn):
    before=file.read_bytes();after=fn(before)
    if before==after:return
    tmp=file.with_name(file.name+'.james.tmp');tmp.write_bytes(after)
    if file.read_bytes()!=before:
        tmp.unlink();raise RuntimeError('Concurrent edit '+str(file))
    tmp.replace(file)

note=f'''### James consistency polish milestone — September 30, 2026

Latest evidence supersedes the previous North recovery and disk-phase pending
items. North dry recovery uses master-only recover-source-v3.png, six owned
crops, fixed cranial ruler22/102, slimmer long legs and close planted boots.
Other facing sources/distress unchanged.528 package,1044 installed player and119
actual North low-air/recovery checks PASS, two modes/two cases/24 native captures.

Full checkpoints already preserve crew playback and visual time separately from
NPC snapshots.402 checks prove32 disk write/read/restore phases:4 facings, ground/
water, bare/helmet, mid-collapse and final hold.16 restored terminal native captures
reviewed. No death/save gameplay change. Capture fixture deliberately requests
the target camera and waits for observable centre; deferred CORE focus otherwise
overwrites raw scroll changes and produces a misleading empty crop.

All41 family first/middle/final boards now reviewed against selected masters in
both modes. Fixed82px equivalent boards are comparative source evidence, not
native motion/journey proof. Water origins differ from boot contacts: retain full
alpha bounds around the declared pivot;240px review rows corrected clipping.
All24 dry turn clips/184 slots measured: bare147–149 versus masters147–148px.
Four unique quarter and two unique half full-pose boards reviewed. Rear helmet
master150px versus side156px is projected camera anatomy; avoid forcing all
orientations to identical outer height or resizing individual poses.

Underwater cargo halves formerly680ms against800ms quarters. Builder now composes
the two quarter clocks, preserving both exact shared endpoint holds:1600ms half.
Every pose file hash unchanged.1162 package,2804 installed player and{routes['checks']}
installed route checks PASS:24 authored collision-checked two-leg paths,
{samples} actual alpha samples, all184 slots. Initial route run failed only historical
whole-life-profile equality after newer AIR additions; preserved failure evidence,
compare the eight cargo-turn keys explicitly, rerun PASS. No live clearance change.
All native tests scratch APPDATA and owner profiles unchanged.

Source coverage remains173bare/171helmet,zero retained states. Full motion,
material/anatomy joins, non-East arrival facing, North water boots and sleep
breathing, side-water death proportions, furniture/meal/equipment/exterior travel
handoffs and owner/release acceptance remain open. Goal active.
See docs/JAMES_CONSISTENCY_HANDOFF_2026-09-30.md and
character/james-animation-coverage-2026-09-30/consistency-review/review-ledger.json.
'''
headline='''## James consistency polish: master height, North recovery and cargo turn pace — September 30, 2026

All41 family representative boards reviewed; full motion/handoffs remain open.
All dry turn slots measured:147–149px bare versus147–148px masters. North dry
recovery remade with close planted boots/longer slim legs;528/1044/119 checks PASS.
Death phase restoration proved across32 disk checkpoint cases,402 checks PASS.
Underwater cargo halves now1600ms from two800ms quarters; pose pixels unchanged,
installed playback and24 authored routes PASS. Owner profiles unchanged.
See [polish handoff](JAMES_CONSISTENCY_HANDOFF_2026-09-30.md). Goal remains active.

'''
atomic(R/'docs/CURRENT_STATUS.md',lambda b:b if headline.encode() in b else headline.encode()+b)
for file in [R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    atomic(file,lambda b:b if note.encode() in b else b+b'\n\n'+note.encode())
latest=b'\n\nLatest polish supersedes the pending North dry recovery, cargo half-clock and disk-restored death-phase items here. See JAMES_CONSISTENCY_HANDOFF_2026-09-30.md; prior checks retain their dated scope.\n'
for name in ['JAMES_AIR_HANDOFF_2026-09-30.md','JAMES_DEATH_HANDOFF_2026-09-30.md','JAMES_WATER_CARGO_HANDOFF_2026-09-30.md']:
    file=R/'docs'/name
    if file.exists():atomic(file,lambda b:b if latest in b else b+latest)
handoff=f'''# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James full-set consistency polish

## Objective and acceptance
Continue all James animations, then master/style/material/anatomy/motion and
cross-family handoff consistency. Zero retained source states is coverage only.
Goal active; current changes installed_owner_review_pending.

## Accepted decisions and constraints
Matte neutral masters, anatomically correct belt wrench, diagnostics tablet,
forward repair/construction torch, independent facings and fixed source rulers.
Preserve exact selected joins and authored leg continuity; no per-pose height fit.
Native probes use scratch APPDATA and fingerprint the owner's real profile.

## Current state
North dry recovery source/crops/anatomy config in james-air-north-v1 and shared
family rebuilt. Fixed22/102 ruler; slimmer close stance. Distress/other facings
unchanged. Water cargo turn builder/verify/paired manifests now compose halves
from their two800ms quarters:1600ms, previously680ms. All pose hashes unchanged.
Route fixture checks eight actual cargo-turn keys after later AIR additions.
Death disk-restore fixture/capture camera corrected; no save/gameplay change.
Coverage review scripts,41-family ledger and dry all-slot height boards added.
Pipeline/bible/continuation and canonical+installed skills updated.

## Verification
North528 package/1044 installed player/119 actual controlled recovery checks PASS;
two modes/two North cases/24 captures visually reviewed. Death402 checks prove32
actual disk-restored mid/final phases,16 terminal captures reviewed. Cargo timing
1162 package/2804 installed player/{routes['checks']} installed route checks PASS;
24 authored two-leg in-room paths,184slots/{samples} alpha samples. Initial route
scope assertion failed against old whole-life profile; preserved report, narrowed
to exercised cargo-turn keys, rerun PASS. Every scratch owner profile unchanged.
All41 family first/middle/final boards reviewed at fixed82px equivalent scale;
not all-frame motion or runtime proof. All184 dry turn slots measured147–149px
bare vs147–148px masters. Four unique quarter/two half full-pose boards reviewed;
rear helmet150px vs side156px follows master camera projection.

## Next action
Check full actual motion and joins. Review North ordinary water boot proportions,
West water death projected limb length, non-East activity arrival facing and North
sleep breathing. Prove furniture/meal/equipment and complete exterior cargo/airlock
journeys. Owner/export acceptance remains separate. No process remains after PASS.
'''
file=R/'docs/JAMES_CONSISTENCY_HANDOFF_2026-09-30.md'
if file.exists():atomic(file,lambda b:handoff.encode())
else:file.write_text(handoff)
print(f'Polish milestone recorded;41 families sampled,24 cargo routes/{samples} alpha samples; goal active')
