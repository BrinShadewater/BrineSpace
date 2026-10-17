from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'full-gait-review-v173';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((o/'native-evidence.json').read_bytes());v=json.loads((o/'native_probe-validation.json').read_bytes());inp=json.loads((o/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(939,0,49)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in inp['preLaunchSha256'].items())
ledger=p/'material-repair-progress.json';j=json.loads(ledger.read_bytes());rows=[]
for i,row in enumerate(j['states']):
    result={'phase':i}
    for mode in ['bare','helmet']:
        f=r/row['candidateSources'][mode]['file'];assert sha(f)==row['candidateSources'][mode]['sha256'];a=np.array(Image.open(f).convert('RGBA'));original=np.array(Image.open(p/f'master-head-review-v16/{mode}-{i:03d}.png').convert('RGBA'))
        assert np.array_equal(a[:,:,3],original[:,:,3]);ys,xs=np.where(a[:,:,3]>=128)
        result[mode]={'bounds':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'alphaExactToSamePhase':True,'bootsFrom200ExactToSamePhase':bool(np.array_equal(a[200:],original[200:]))}
    rows.append(result)
master=p/'../james-west-master-carry-v1/registered-original-master.png';a=np.array(Image.open(master).convert('RGBA'));ys,xs=np.where(a[:,:,3]>=128);master_bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
(o/'geometry-audit.json').write_text(json.dumps(dict(alphaThreshold=128,registeredStandingBareMasterBounds=master_bounds,registeredMasterSha256=sha(master),rows=rows,scope='Bounds and exact source alpha only. Does not prove limb proportions, perspective, foot contact or absence of height bob.'),indent=2)+'\n')
findings=['All49paired native captures/four sizes visually inspected in17packed boards. Fine body detail retained; lower-refined4..8and12finish differs from many protected original boots, confirming coordinated lower polish remains.','Same-phase alpha exact in all49both variants. Bare crown76fixed; posed soles223..226span3rows; master bounds106,76,150,224. Posed extent is not standing anatomy equality and small sole changes need moving foot-contact review.','Full939nativechecks cover98sources, exact timing/pivots/rulers, helper finite clamp and3time-based fixture loops through production frame path for both gears. Fixture key has no distance stride mapping; not normal distance-driven carry controller acceptance.','Browser preview observed playing at frame1original rate and38quarter rate, paused27master comparison saved. Sampled observations are not continuous49motion/no-flash/seam acceptance.','V172841checks/194failures arose from incorrectly expecting frame_at_elapsed transition helper to loop. Contract corrected inV173without runtime edits. InitialV173parse error fixed with explicitfloattype; final939pass replaces parse failure as current evidence.','No normal selection changed. Next lower hardware finish coordination, continuous motion/master proportions/foot contact, normal carrying lifecycle and all-family consistency/polish.']
(o/'review.json').write_text(json.dumps(dict(nativeChecks=939,nativeFailures=0,pairedSources=98,reviewedNativeCaptures=49,reviewedNativeBoards=[f'native-review-{i}.png' for i in range(17)],fullCycleMs=1680,timeBasedFixtureCyclesTestedPerGear=3,browserObservedPhases=[1,38,27],browserScreenshot='playback-master-review.png',playbackHtml='playback-review.html',findings=findings,continuousVisualMotionAcceptance=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
(p/'full-gait-review-v172/review.json').write_text(json.dumps(dict(disposition='invalid_loop_assertion_for_finite_transition_helper',checks=841,failures=194,nativeCapturesProduced=49,nativeCapturesVisuallyReviewed=0,correctedEvidence='../full-gait-review-v173/review.json',normalChanged=False,sourceAcceptance=False),indent=2)+'\n')
j['nextVisualRepair']='Coordinate lower hardware finish starting9; full moving gait/master anatomy/contact audit, normal carrying lifecycle and all-family consistency'
ledger.write_text(json.dumps(j,indent=2)+'\n')
section='''### James full49 timed source cycle verified with lower polish still open - October3,2026

V173assembles all49current provisional phases into paired full-cycle manifests,
original1680ms clock, exact APNG decode, loop=true. Native939checks/0failures/49paired
four-size captures; all17packed native boards visually inspected. Exact sources,
original interval timing, pivot/ruler metadata, deliberate transition-helper clamp
and3time-based fixture loops through production frame() path verified in both gears.
This fixture uses carry-full-review without distance stride mapping; it does not
prove normal distance-driven carry controller, rooms, lifecycle or Continue.
Scratch APPDATA owner profile unchanged; frozen inputs/runtime/registry stable.

Geometry audit verifies all49both-gear alpha exact to original same-phase source.
Bare crown76fixed, posed soles223..226span3rows versus registered standing master
[106,76,150,224]. Those bounds do not prove proportions/perspective, planted foot
contact or no height bob. Full visual review confirms lower-refined4..8/12finish
differs from many protected original boots. Fine body fabric/fittings retained,
but coordinated lower-metal finish and master anatomy/detail remain provisional.

Self-contained playback-review.html includes original standing bare master plus
both carrying gears, original timing/quarter speed/pause/seek. Browser observed
playing1and38, paused27master screenshot saved. These sampled observations and
49static captures are not continuous-motion/no-flash/seam acceptance. Original
master remains authority; no normal selection changes. Full James lifecycle and
all-family master consistency/polish remain incomplete.

Review correction: V172expected finite transition helper frame_at_elapsed to loop,
yielding841checks/194failures. Source preserved; V173tests its deliberate clamp
and looping frame() separately. InitialV173explicitfloat parse repair preserved in
initial-parse-validation.json, final939pass authoritative. No runtime code edit.
Lesson: test the intended playback path and state whether a fixture is driven by
time or movement distance; do not infer normal gait/lifecycle from either source
coverage or a time-only fixture. Next lower hardware coordination beginning9,
continuous moving/master/contact review, normal lifecycle and all-family polish.
Evidence:character/james-west-carry-walk-keys-v1/full-gait-review-v173/review.json.
'''
guides=record_guides(r,section,'### James carrying start0..3 rebuilt after source/master audit')
handoff='''# Project handoff

Updated: October3,2026. Full James master-matched library and polish active.

## Objective and acceptance
All families match original master art, colour, perspective, size, height and
proportions; verify motion/integration and cross-family consistency/polish.

## Accepted decisions and constraints
Reversible repairs authorized. Preserve owner saves/normal selection and masters.
Source coverage, registration and timed fixture tests do not prove art acceptance.

## Changed files and current state
V172failed loop assertion evidence,V173corrected full49fixture,geometry audit,
self-contained browser preview/master screenshot,ledger,five guides.49provisional
phases;lowerfinish differences confirmed. No normal installation,commit/PR/export.

## Verification
939checks/0failures;49paired four-size captures across17boards visually reviewed.
3timed fixture loops per gear;all49same-phase alpha exact,source timing preserved.
Owner profile and frozen references/runtime/registry stable. Browser samples only.

## Remaining work
Coordinated lower finish beginning9,full continuous motion/contact/master anatomy,
normal distance-driven carrying lifecycle and all-family consistency/polish.

'''
for folder in [p/'full-gait-review-v172',o]:(folder/'HANDOFF.md').write_text(handoff+section,encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in [p/'full-gait-review-v172',o] for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
a=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert len(a)==3*len(rasters)+1 and all(x==b'lfs' for x in a[2:-1:3])
print(json.dumps(dict(checks=939,failures=0,reviewedCaptures=49,cycleMs=1680,masterBounds=master_bounds,bareSoleRange=[min(x['bare']['bounds'][3] for x in rows),max(x['bare']['bounds'][3] for x in rows)],guides=guides,lfsRasters=len(rasters))))
