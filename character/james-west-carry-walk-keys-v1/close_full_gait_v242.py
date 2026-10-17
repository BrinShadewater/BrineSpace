from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'full-gait-review-v242';old=p/'full-gait-review-v233';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(939,0,49)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
changed=[0,1,2,3,30];unchanged=[i for i in range(49) if i not in changed]
reuse=[]
for i in unchanged:
 name=f'carry-full-review-west-{i:03d}.png';a=out/'native'/name;b=old/'native'/name
 assert sha(a)==sha(b),f'Unchanged visual evidence differs at phase{i}'
 reuse.append(dict(phase=i,file=name,sha256=sha(a),priorReview='full-gait-review-v233/review.json'))
(out/'visual-evidence-reuse.json').write_text(json.dumps(dict(unchangedNativeCaptures=reuse,changedNativePhases=changed,scope='Exact PNG hashes permit reuse of44 previously visually reviewed captures; changed phases re-viewed in current native boards0/1/10.'),indent=2)+'\n',encoding='utf-8')
findings=['Current seam/master board and all49 lower crop grid reviewed. Opening toe highlights and phase30 knee now more restrained; frames1/3 and21/34/40/44..46 retain finish variation for moving review.', 'Native boards0/1/10 visually reviewed at four sizes, covering all five changed phases and neighbours. Other44 native captures are byte-identical to the visually reviewed V233 captures, with explicit hash evidence reuse.', 'Standing master remains visibly slimmer through trunk/legs than some carrying poses. Height/pivot/alpha evidence does not establish master anatomical proportions or world sole contact.', '939checks verify98 paired sources, original1680ms timing and three time-based fixture loops per gear. Continuous flash/seam acceptance and distance-driven normal gameplay lifecycle remain unverified.']
(out/'review.json').write_text(json.dumps(dict(nativeChecks=939,nativeFailures=0,pairedSources=98,reviewedChangedNativePhases=changed,reviewedNativeBoards=['native-review-0.png','native-review-1.png','native-review-10.png'],reusedExactNativeCaptures=44,fullCycleMs=1680,timeBasedFixtureCyclesTestedPerGear=3,reviewedMasterBoards=['seam-master-review.png','all-lower-review.png'],findings=findings,continuousVisualMotionAcceptance=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes());progress['nextVisualRepair']='Current full49 original/quarter-speed motion and anatomical master comparison; resolve trunk/leg proportion concerns, calibrate planted sole contact and versioned normal cargo lifecycle; all-family consistency/polish'
ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
section='''### James current full carrying cycle with opening and knee finish - October3,2026

V242 freezes49 current candidate phases/both gears includingV234..237 opening
andV240 restored knee finish.939 native checks/0 failures/49 captures,98sources,
1680ms original clock and three time-based fixture loops per gear; scratch owner
profile unchanged and frozen hashes stable. Native boards0/1/10 re-viewed for all
five changed phases and neighbours.44 other native captures byte-identical to
previously reviewedV233; explicit visual-evidence-reuse.json records their hashes.
Current seam/master and all49 lower grid visually reviewed; softer opening/knee
highlights. Finish variation1/3/21/34/40/44..46 needs moving-grade assessment.

Original standing master remains slimmer through trunk/legs than some carrying
poses. Physical master proportions are not accepted from height/pivot/alpha checks.
Lesson: reuse visual evidence only for exact unchanged captures and separately
review changed poses plus their joins; record that reuse instead of claiming a
new review of unseen boards. HTML/APNG are review aids, not uninterrupted motion
acceptance. Next actual original/quarter-speed motion and anatomical master
comparison, contact calibration and versioned normal cargo lifecycle, then full
animation-family consistency/polish. Normal selection unchanged; goal incomplete.
Evidence: character/james-west-carry-walk-keys-v1/full-gait-review-v242/review.json.
'''
guides=record_guides(r,section,'### James restored knee finish candidate retained')
(out/'HANDOFF.md').write_text('# Project handoff\n\n'+section+'\nChanged: V242 frozen manifests/APNG/native probe+UID/captures, playback HTML, master/lower comparison boards, evidence reuse and ledger next action.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for f in out.rglob('*') if f.suffix.lower() in ['.png','.apng']]
a=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(a[i+2]==b'lfs' for i in range(0,len(a)-1,3))
print(json.dumps(dict(checks=939,failures=0,captures=49,changedVisuallyReviewed=5,reusedExactCaptures=44,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
