from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'lower-window-v175';folder=p/'lower-material-phase9-v174'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(73,0,5)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
d=json.loads((folder/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
assert sha(folder/'prompt.txt')==d['promptSha256']
review=json.loads((folder/'package-review.json').read_bytes())
assert all(review[k] for k in ['alphaExact','outerOnePixelRingExact','allRowsAbove181Exact','pairedBodyBelow110Exact'])
findings=['Phase9 toe/ankle highlights modestly softer and warmer, readable hardware retained. Upper-tail luma176.20to170.33; median64.68to67.71. This is not uniform darkening or a measured25percent highlight reduction.', 'Two source repair boards, phase8..12 source board and all five paired four-size native captures visually reviewed. Phases10/11 retain brighter original boot highlights; coordinated lower finish remains open.', 'Original alpha and one-pixel outer rim remain exact, rows above181 unchanged, paired body below110 exact. Interior hardware landmarks receive visual assessment; fixed alpha does not prove unchanged internal geometry.', 'Original clocks30/20/20/20/20ms (110ms) verified. Finite five-frame fixture is not continuous full49motion or normal movement/controller acceptance.']
review.update(disposition='retain_provisional_lower_finish',reviewedSourceBoards=['lower-detail-review.png','paired-lower-review.png'],findings=findings,nativeIncluded=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False)
(folder/'package-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
(folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='a5b64a01-2a7d-4c5d-9c8b-137dfb592f13',rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes());row=progress['states'][9]
sources={m:dict(file=(folder/f'{m}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{m}-head-protected.png')) for m in ['bare','helmet']}
if row['candidateSources']!=sources:row.setdefault('supersededCandidateSources',[]).append(row['candidateSources'])
row.update(candidateSources=sources,sourceAcceptance=False,reviewStatus='provisional_lower_finish_master_motion_pending')
progress['lowerMaterialRefinementPhases']=sorted(set(progress['lowerMaterialRefinementPhases']+[9]))
progress['nextVisualRepair']='Coordinate lower finish phases10/11 then remaining gait; continuous master anatomy/foot-contact review; normal carry lifecycle and all-family consistency'
assert progress['candidatePhases']==49 and not progress['remainingSourcePhases']
ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=73,nativeFailures=0,reviewedNativeCaptures=5,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],reviewedSourceWindowBoard='local-source-review.png',sourceIndices=[8,9,10,11,12],durationsMs=[30,20,20,20,20],findings=findings,continuousVisualMotionAcceptance=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='''### James carrying lower finish phase9 neighbour review - October3,2026

V174 phase9 lower crop retained provisionally after two source repair boards and
V175 phase8..12 source board plus all five paired native captures/four sizes were
visually reviewed. Original alpha, outer one-pixel rim, rows above181 and paired
body below110 remain exact;1026admitted/64510outside pixels. Highlights soften
modestly:95thpercentile176.20to170.33, median64.68to67.71. Not uniform darkening
or a measured25percent reduction. Phases10/11 still have brighter original boots.
Original master remains authority; phase5 is a provisional material reference,
not a pose/anatomy reference. Review helper now labels the actual phase5 reference.

V17573checks/0failures/five captures, exact original30/20/20/20/20ms(110ms),
engine terminal, scratch APPDATA owner profile unchanged, frozen hashes stable.
Ledger phase9 points toV174 while preservingV105.49/49candidate coverage is
unchanged; none of this is final source acceptance. V173 full-cycle evidence
applies to its frozen earlier sources, not a new full-motion validation ofV174.
Normal selection unchanged. Continue lower finish10/11 and remaining gait,
continuous master anatomy/contact/motion review, normal carrying lifecycle and
full James cross-family consistency. No full-goal completion.

Lesson: identify the actual reference shown in review boards; a provisional
finish reference never supersedes the master. Verify original clocks from the
manifest rather than remembered index ranges. Reduced upper-tail highlights
can coexist with lighter midtones; both require visual review against neighbours.
Evidence: character/james-west-carry-walk-keys-v1/lower-window-v175/review.json.
'''
guides=record_guides(r,section,'### James full49 timed source cycle verified with lower polish still open')
handoff='''# Project handoff

Updated: October3,2026. Objective: complete James master-matched animation set,
then full consistency/polish across families. Goal remains active.

Accepted constraints: master authority, original pose/registration, matte warm
charcoal/yellow and worn metal, no owner profile changes. Reversible work authorized.

Changed: V174 phase9 lower source pair/raw/frozen prompts and references; V175
five-frame manifest/APNG/native probe with paired UID/captures/evidence; ledger;
lower helpers (phase9 mapping and accurate provisional-reference board label);
CURRENT_STATUS, asset pipeline, visual bible and repository/installed crew skill.

Checks:73native/0failures,5captures all visually reviewed at four sizes; engine0,
no timeout, scratch owner profile unchanged, frozen input/runtime hashes exact.
Two V174 source boards plus V175 source-window board visually reviewed. Original
alpha/rim/upper rows preserved. Highlight change modest, midtones slightly lighter.

Remaining: brighter10/11boots and wider coordinated lower finish; full moving
49frame master proportion/contact/flash/seam review; versioned normal carry
lifecycle integration; all animation family consistency. V173 evidence is frozen
to earlier phase9. No continuous motion acceptance or normal selection change.
'''
for f in [folder/'HANDOFF.md',out/'HANDOFF.md']:f.write_text(handoff,encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for root in [folder,out] for f in root.rglob('*') if f.suffix.lower() in ['.png','.apng']]
a=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0')
assert all(a[i+2]==b'lfs' for i in range(0,len(a)-1,3))
print(json.dumps(dict(retainedPhase=9,checks=73,failures=0,reviewedCaptures=5,guides=guides,lfsRasters=len(rasters),normalChanged=False,goalComplete=False)))
