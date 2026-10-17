from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'full-gait-review-v285';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();n=json.loads((o/'native-evidence.json').read_bytes());v=json.loads((o/'native_probe-validation.json').read_bytes());f=json.loads((o/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(939,0,49)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/path)==h for path,h in f['preLaunchSha256'].items())
changed=[];reused=[]
for i in range(49):
 a=o/f'native/carry-full-review-west-{i:03d}.png';b=p/f'full-gait-review-v280/native/carry-full-review-west-{i:03d}.png'
 if sha(a)==sha(b):reused.append(dict(phase=i,fromEvidence=b.relative_to(r).as_posix(),sha256=sha(a)))
 else:changed.append(i)
assert changed==[28,29,30]
(o/'visual-evidence-reuse.json').write_text(json.dumps(dict(changedPhasesReviewed=changed,changedNativeBoardsReviewed=[9,10],reusedPreviouslyReviewedCaptures=reused,scope='Three changed poses freshly viewed;46 byte-identical captures reuse V280/V265/V242 visual chain.'),indent=2)+'\n')
findings=['Latest near/far thigh283 sources checked in full49 original clock; source49 thigh board and changed native boards9/10 inspected. Late44..46 fitting remains ambiguous; preserve until equipment chronology is established.', 'Live local browser playback verified playing, pause, seek0/12/30/44 and resumed. Three screenshot samples saved. This is observed functional source playback with sampled visual review; not continuous visual acceptance or traveling world contact.', 'Alpha-threshold diagnostic: original and bare carrying crown74 at alpha1,76 at128,77 at250. Helmet crown68 at1/128,69 at250 throughout49. Bare head top extent matches master, helmet top stable; this does not prove face/neck fit or anatomical proportion.', 'Master sole225/223/222 at alpha1/128/250; source stride ranges224..228/222..225/221..225. Transparent fringe and projected toes affect bounds; do not warp body to equal bounding boxes. Near/far physical foot support needs moving-root review.', 'Whole-grade seam-free cloth comparison, original helmet identity, body proportions, normal cargo lifecycle and all-family polish remain unaccepted.']
(o/'review.json').write_text(json.dumps(dict(nativeChecks=939,nativeFailures=0,nativeCaptures=49,embeddedSourcesVerified=98,changedPhasesReviewed=changed,identicalReviewedCapturesReused=46,browserPlaybackObserved=True,browserSamplePhases=[0,12,30,44],savedBrowserScreenshots=['browser-phase12.png','browser-phase30.png','browser-phase44.png'],selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=findings),indent=2)+'\n')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();j=json.loads(old);j['latestWholeStudyReview']=dict(version=285,file=(o/'review.json').relative_to(r).as_posix(),selected=False);j['nextVisualRepair']='Full latest49 and live sampled master playback reviewed. Bare crown matches original across alpha thresholds; helmet crown stable but fitting/anatomy unaccepted. Review moving-root near/far foot support, source body proportions/grade and late44..46 equipment identity before normal cargo lifecycle integration and all-family polish.';assert ledger.read_bytes()==old;ledger.write_text(json.dumps(j,indent=2)+'\n')
section='''### James latest full-cycle browser samples and alpha-sensitive master ruler - October3,2026

V285 freezes latest31 garment studies plus18 selected poses,98paired sources,
original1680ms cycle.939native checks0/49captures, scratch owner unchanged, frozen
hashes stable.98HTML sources exact. Changed28..30 native boards9/10 freshly viewed;
46identical captures reuse V280/V265/V242 chain. All49 thigh board inspected.
Local browser playback actually playing, paused, seek0/12/30/44 and resumed;
saved12/30/44 screenshots. Functional playback and sampled visual evidence only,
not continuous visual motion acceptance, normal traveling root or gameplay lifecycle.

Master/bare crown extent matches at alpha1/128/250:74/76/77 respectively throughout
all49; helmet68/68/69 stable. Master sole225/223/222 vs stride224..228/222..225/
221..225. Low-alpha fringe makes bounds larger than apparent anatomy. No source
warping/grade edit applied. Stable top extent does not certify face/neck fitting,
whole proportions, boot support or actual root contact. Late44..46 gear identity
still ambiguous; preserve. No normal bank changed; whole goal incomplete.

Lesson: compare registration using the SAME alpha threshold on master and source;
report fringe sensitivity separately from anatomy. A playing preview plus screenshots
proves observed playback and samples, not continuous contact. Next moving-root
near/far support, whole body/helmet/master grade and belt-equipment chronology,
then normal pickup/carry/turn/unload/Continue and cross-family polish.
Handoff: character/james-west-carry-walk-keys-v1/full-gait-review-v285/HANDOFF.md.
'''
guides=record_guides(r,section,'### James separate far-thigh cloth and near-leg identity guard')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James whole carrying comparison

## Objective and acceptance
Full James master-matched animations, integrated and cross-family polished.

## Accepted decisions and constraints
Matte fine quilt, muted yellow seams. Belt wrench; diagnostics tablet; repair torch.
Actual original master governs grade/anatomy. Do not warp to fringe bounding boxes.

## Current state
Full-gait-review-v285 exact latest mixed49 sources, manifests/APNG/HTML, native,
source/master boards, alpha-threshold rulers and browser screenshots. Latest ledger
records review; five guides updated. Browser tab1 localhost8875 left playing, marked
deliverable; server exec session12969 was confirmed live at launch. Normal bank unchanged.

## Verification
939checks0/49captures;98embedded sources exact.3changed native poses freshly viewed,
46identical prior review reuse.49thigh board reviewed. Browser pause/seek/play verified,
sampled0/12/30/44,12/30/44 screenshots saved. Scratch owner unchanged/hashes stable.
Bare crown matches original at all3thresholds; helmet crown stable. No continuous
visual/contact, original helmet fitting, anatomical or normal lifecycle acceptance.

## Next action
Moving-root near/far foot support and whole anatomy/helmet/grade; belt equipment
chronology44..46, seam-free master cloth samples. Versioned normal cargo joins and
lifecycle/interruptions/Continue, finish coverage and all-family consistency/polish.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as h:h.write('\n'+section)
rasters=[x.relative_to(r).as_posix() for x in o.rglob('*') if x.suffix.lower() in ['.png','.apng']];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(checks=939,failures=0,captures=49,changedReviewed=3,reused=46,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
