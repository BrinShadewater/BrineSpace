from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'room-journey-v286';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();n=json.loads((o/'native-evidence.json').read_bytes());v=json.loads((o/'native_probe-validation.json').read_bytes());d=json.loads((o/'inputs.json').read_bytes());a=json.loads((o/'travel-analysis.json').read_bytes())
assert all(sha(r/f)==h for f,h in d['preLaunchSha256'].items())
assert n['checks']==2563 and n['failures']==0 and len(n['results'])==2
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
for route in n['results']:assert sorted(route['observedWalkSlots'])==list(range(49)) and route['freshSceneDiskResume'] and len(route['captures'])==6
for route in a['routes']:assert route['samples']==417 and route['sourceIndices']==list(range(49)) and route['maxDistancePhaseErrorSeconds']<1e-9
findings=['Latest garment studies displayed on actual prescribed dry west navigation/grid route in both gears; all49 slots consumed and2midroute fresh-scene disk resumes exact with candidate bank explicitly reinstalled.', 'Existing69world-unit stride:417moving samples per gear, phase equals accumulated root distance/69*1.68 within1.2e-14seconds. This validates distance coupling, not planted foot landmarks, anatomy or physical contact.', 'All12 room captures reviewed: bare full board; helmet entry/quarter/preresume and separate resume/arrival crop. Arrival directly jumps west carry to north unload; no newly authored turn. Camera/room tint differ after fresh scene; exact source restoration does not imply complete scene parity.', 'Normal bank remains unchanged. Full pickup/preparation/arrival lifecycle, authored turn join, autonomous scheduling/interruptions and title fresh-process Continue remain unproven.']
(o/'review-acceptance.json').write_text(json.dumps(dict(nativeChecks=2563,nativeFailures=0,actualRoutes=2,sourceSlotsPerRoute=49,freshSceneDiskResumes=2,reviewedRoomCaptures=12,reviewedBoards=['bare-room-review.png','helmet-room-review.png','helmet-resume-arrival-review.png'],travelSamplesPerGear=417,physicalFootContactAccepted=False,continuousVisualMotionReviewed=False,normalChanged=False,sourceAcceptance=False,fullGoalComplete=False,findings=findings),indent=2)+'\n')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();j=json.loads(old);j['latestActualRoomReview']=dict(version=286,file=(o/'review-acceptance.json').relative_to(r).as_posix(),selected=False);j['nextVisualRepair']='Latest49 traverses real room with existing69unit stride and2scratch disk restores; actual arrival still snaps west carry to north unload. Inspect/authored arrival-turn coverage and lifecycle join, track stance foot landmarks against moving root, then master grade/proportion/helmet and full family polish. Normal adoption unproven.';assert ledger.read_bytes()==old;ledger.write_text(json.dumps(j,indent=2)+'\n')
section='''### James latest49 actual room distance coupling and arrival join - October3,2026

V286 latest V285 paired49 artwork explicitly staged as carry-west with inherited
69world-unit stride on actual JamesNPC navigation/move/arrive/grid. Two prescribed
collision-clear96unit dry west workshop routes;2563checks0, all49 slots each gear.
Two fresh-scene midroute disk saves/restores exact actor/playback/clock/pause/source
with candidate bank explicitly reinstalled. Scratch APPDATA owner unchanged;
109frozen sources/runtime/program/manifest hashes stable. Normal bank unchanged.
417moving samples/gear trace foot root and source slot: player phase equals traveled
distance/69*1.68 within1.2e-14seconds. Last carry sample95.901855units; completion
is independently asserted after arrival. Distance coupling does not prove stance
foot support or moving anatomy. All12 room captures inspected; camera/tint change
across fresh scene remains, so exact source restore is not rendered-scene parity.

Actual arrival directly switches west carry to north unload. No authored arrival
turn exercised. Full pickup/preparation/arrival lifecycle, autonomous dispatch,
interruptions and title fresh-process Continue remain unproven. Existing source
coverage is not normal controller coverage. Do not promote by route checks alone.
Lesson: audit actual root-distance phase separately from foot contact and local
source playback. Trace near/far stance landmarks to assess sliding; preserve
perspective-consistent ground projections. Next arrival-turn coverage/join and
complete lifecycle, original-master material/proportion/helmet/contact, versioned
adoption and cross-family polish. Goal active/incomplete.
Handoff: character/james-west-carry-walk-keys-v1/room-journey-v286/HANDOFF.md.
'''
guides=record_guides(r,section,'### James latest full-cycle browser samples and alpha-sensitive master ruler')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James latest cargo travel

## Objective and acceptance
Full James master-matched set, full normal lifecycle and cross-family polish.

## Accepted decisions and constraints
Preserve masters, matte cloth, proportions/perspective/equipment. Wrench on belt,
tablet diagnostics, forward repair torch. Provisional sources remain unselected.

## Current state
Room-journey-v286 stages exact latest49 art on actual dry west NPC/grid route;
versioned manifests reuse69world-unit stride. Native probe, trace834samples,
analysis/12captures/review boards and acceptance report. Latest ledger and5guides
updated. No normal source/code selections changed.

## Verification
2563checks0,2routes,all49slots/gear,2fresh-scene scratch disk resumes with explicit
candidate reinstall.109frozen inputs stable, owner unchanged.417distance/phase
samples each, error<1.2e-14seconds.12native room captures visually inspected.
Physical stance contacts, full continuous visual motion and normal adoption unproven.

## Next action
Inspect existing arrival-turn coverage and author west carry to north unload join;
exercise full pickup/preparation/arrival lifecycle. Track near/far stance landmarks
against real root motion; whole master colour/proportions/helmet, interruptions,
checkpoint binding/Continue, finish coverage and full-library consistency/polish.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for f in o.rglob('*.png')];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(checks=2563,failures=0,routes=2,diskResumes=2,travelSamples=834,reviewedCaptures=12,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
