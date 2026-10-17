from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
for name in ['native-staged-behaviour','native-installed','native-installed-behaviour','native-restore']:
    v=json.loads((P/(name+'-validation.json')).read_text());log=(P/(name+'.log')).read_text(errors='replace')
    assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'],name
    assert 'SCRIPT ERROR:' not in log and '\nERROR:' not in log,(name,'engine log errors')
assert json.loads((P/'package-verification.json').read_text())['checks']==82
assert json.loads((P/'restore-evidence.json').read_text())['checks']==52
def atomic(path,fn):
    before=path.read_bytes() if path.exists() else b'';after=fn(before)
    if before==after:return
    tmp=path.with_name(path.name+'.west-death.tmp');tmp.write_bytes(after)
    if (path.read_bytes() if path.exists() else b'')!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
    tmp.replace(path)
def selection(b):
    m=json.loads(b);m.update(packageChecks=82,stagedMortalityChecks=72,installedPlayerChecks=62,installedMortalityChecks=71,diskRestoreChecks=52,
                           sourceReview='Six paired poses,82px comparison,12 final native mortality captures,2 restored terminal captures and four-direction death-water master page reviewed',
                           bootReach={'selectedEntry':199,'oldMax':221,'newMax':205,'units':'native pixels at common114px cranial anchor'})
    m['pending']=['Workstation-specific facing transitions','Full furniture/meal/equipment/exterior journeys','Owner and full-set acceptance'];return (json.dumps(m,indent=2)+'\n').encode()
atomic(P/'selection.json',selection)
note='''### James West water death projected-limb polish — September30,2026

Skull matching alone does not prove thigh/shin projection. Independently authored
v3 water-death poses still lengthened boots behind the selected swim; v4 source
edit uses depth/knee foreshortening to shorten that span without whole-body or
per-pose resizing. Fixed25/60 cranial ruler,common114px head anchor: selected
entry boot ends at199px; previous max221px,new max205px. Arms lower smoothly,
shared helmets retain recorded pitch/owned head edits; finite clocks unchanged.
Raw sources,prompts,origins and rejected candidate retained.

82 package,72 candidate mortality,62 installed player,71 final installed mortality
and52 disk-restore checks PASS. Two flooded West gear cases,12 final normal-grid
captures and2 restored-terminal captures reviewed. Actual controlled
RoomFlooding.kill accounting/chooser/pause/terminal hold and four real scratch
RunSave write/read/restore phases(mid3/final5,both modes) verified. No oxygen
depletion journey/all-layout claim. Profile unchanged and final engine logs clean.
An initial nominal62-check PASS also logged a dependency parse failure: Moonbay
center arithmetic needed explicit Vector2 because distance is a Variant from an
array. One-line typing fix preserved geometry; failed logs retained, affected
installed checks rerun clean. Exit0/check totals alone never certify a clean run.
See docs/JAMES_WEST_WATER_DEATH_POLISH_HANDOFF_2026-09-30.md;goal active.
'''
for path in [R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    atomic(path,lambda b:b if note.encode() in b else b+b'\n\n'+note.encode())
headline='''## James West water death limb projection repaired — September30,2026

Paired West water death now keeps compact swim-master leg projection as arms
relax.82 package/62 installed player/71 actual mortality/52 disk-restore checks
PASS;12 final native poses and2 restored terminals reviewed. Profile unchanged;
final logs clean after one-line Moonbay type fix. [Handoff](JAMES_WEST_WATER_DEATH_POLISH_HANDOFF_2026-09-30.md).
Workstation-facing and complete life/exterior journeys remain;James goal active.

'''
atomic(R/'docs/CURRENT_STATUS.md',lambda b:b if headline.encode() in b else headline.encode()+b)
handoff='''# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James West water death limb polish

## Objective and acceptance
Full James master matching and cross-family consistency/motion polish.
Local paired West water death revision installed for owner review;goal active.

## Accepted decisions and constraints
Matte graphite/ochre,small boots,compact projected legs matching selected swim,
same left camera/skull/torso density. Source-authored foreshortening, no mirrored
art/limb splices/per-pose silhouette scaling. Exact selected swim entry; finite
clock/shared-helmet pitch and other death states unchanged.

## Current state
character/james-west-water-death-polish-v1 paired one-state6refs per mode pack
selected through literal grid_canvas paths and ACTIVE_ASSETS registry. Source
water-v4 and exact prompts/origins retained in james-death-west-v1;v3 rejected.
One fixed25/60 skull ruler. Bootsmax205vs selected entry199 and prior221px.
Builder/82-check verifier/native/review/install/record helpers reproducible.
rooms/large-rooms/moonbay.gd center gets explicit Vector2 for Variant array
distance arithmetic; no collision geometry change. Pipeline,bible,continuation,
canonical+installed skill lessons and review ledger updated.

## Verification
82 package PASS,72 staged controlled mortality PASS. Final clean installed62
player/71 actual mortality/52 disk-restore checks PASS.12 final normal-grid
poses and2 restored terminal captures reviewed;updated four-direction
death-water master page reviewed. Mid3/final5 checkpoint phases,bare/helmet,
actual scratch writes/reads/restores preserve pixels,clock,pause,terminal hold.
Owner profile unchanged each wrapper. Earlier nominal62-check run had dependency
parse errors despite exit0;failed logs retained,typing fix and clean reruns replace
that evidence. Native fixtures use clear actual room nodes; not real oxygen
depletion,all furniture/traffic/exterior or legacy checkpoint acceptance.

## Next action
Prove workstation-specific facing changes and full furniture/meal/equipment
journeys,then exterior dispatch/airlock/dewatering/salvage/cargo-return handoffs.
Continue complete motion/material comparisons;344 selected clips/41 families
and representative review are coverage,not full-set acceptance. No live processes.
'''
atomic(R/'docs/JAMES_WEST_WATER_DEATH_POLISH_HANDOFF_2026-09-30.md',lambda b:handoff.encode())
path=R/'character/james-animation-coverage-2026-09-30/consistency-review/review-ledger.json'
def ledger(b):
    m=json.loads(b);m['remaining']=[x for x in m['remaining'] if x!='West water death projected limb-length seam']
    item='West water death projected thigh/shin span matched to selected swim'
    if item not in m['corrected']:m['corrected'].append(item)
    m['westWaterDeathRevision']=dict(pack='character/james-west-water-death-polish-v1',installedMortalityChecks=71,diskRestoreChecks=52,finalNativeCapturesReviewed=14,ownerReviewPending=True);return (json.dumps(m,indent=2)+'\n').encode()
atomic(path,ledger)
print('Installed West water death polish recorded; clean62/71/52native evidence; full James goal active')
