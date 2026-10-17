from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'full-gait-review-v280';h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((o/'native-evidence.json').read_bytes());v=json.loads((o/'native_probe-validation.json').read_bytes());frozen=json.loads((o/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(939,0,49)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(h(r/f)==s for f,s in frozen['preLaunchSha256'].items())
changed=[];reuse=[]
for i in range(49):
 a=o/f'native/carry-full-review-west-{i:03d}.png';b=p/f'full-gait-review-v265/native/carry-full-review-west-{i:03d}.png'
 if h(a)==h(b):reuse.append(dict(phase=i,fromEvidence=b.relative_to(r).as_posix(),sha256=h(a)))
 else:changed.append(i)
assert changed==list(range(5,10))+list(range(16,31))
(o/'visual-evidence-reuse.json').write_text(json.dumps(dict(changedPhasesReviewed=changed,changedNativeBoardsReviewed=[1,2,3,5,6,7,8,9,10],reusedPreviouslyReviewedCaptures=reuse,scope='Changed native poses viewed in nine unscaled boards;29 identical captures reuse V265/V242 visual chain. Source49 thigh and master seam boards freshly viewed. No continuous visual motion acceptance.'),indent=2)+'\n')
clock=json.loads((o/'bare-manifest.json').read_bytes())['states'][0]['frameDurationsMs'];frames=[Image.open(o/f'native/carry-full-review-west-{i:03d}.png').convert('RGBA') for i in range(49)]
frames[0].save(o/'native-paired-cycle.apng',save_all=True,append_images=frames[1:],duration=clock,loop=0,disposal=0,blend=0)
with Image.open(o/'native-paired-cycle.apng') as im:
 assert im.n_frames==49
 for i,f in enumerate(frames):
  im.seek(i);assert im.info['duration']==clock[i] and im.convert('RGBA').tobytes()==f.tobytes()
findings=['Fine quilt has replaced the early/middle near-thigh blocks in latest studies; stitch size/seam visibility remain uneven through crossing28..31 and late44..46. Far-side garment needs separate protection-aware review.', 'V279 cloth comparison contains yellow seams in master and several candidate ROIs; old-panel medians alone cannot establish master grade. Do not darken candidates solely to match defective old panels. Next samples must isolate actual cloth away from equipment/seams and account for pose lighting.', 'Late44..46 outlined area remains ambiguous with belt equipment. Preserve until gear attachment/chronology is established; user wrench stays on belt.', 'Standing-master comparison still shows broader carrying silhouette; raised arms/held case differ, so width or total alpha bounds cannot certify anatomical proportions. Original master perspective, head size, contact and whole motion remain unaccepted.']
(o/'review.json').write_text(json.dumps(dict(nativeChecks=939,nativeFailures=0,nativeCaptures=49,embeddedSourcesVerified=98,changedPhasesReviewed=changed,identicalReviewedCapturesReused=29,reviewedSourceBoards=['all-thigh-review.png','seam-master-review.png'],nativeReplayDecodedExact=True,selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=findings),indent=2)+'\n')
a=p/'master-cloth-audit-v279';(a/'review.json').write_text(json.dumps(dict(boardVisuallyReviewed=True,validForGradeAcceptance=False,reason='Yellow seam content contaminates master and some candidate tiny ROIs; pose and illumination also differ. Evidence invalidates using old defective panel as sole grade target, but cannot prove current master colour match.',next='Use seam/equipment-free matched cloth material samples and complete motion review.',normalChanged=False),indent=2)+'\n')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();j=json.loads(old)
j['latestWholeStudyReview']=dict(version=280,file=(o/'review.json').relative_to(r).as_posix(),selected=False)
j['nextVisualRepair']='Full latest49 studies reviewed at source/native sizes: resolve seam/quilt transitions28..31, far-side garment and late44..46 equipment identity. Grade against original master cloth with yellow seams/equipment excluded; old defective panel brightness is not a fidelity target. Whole-motion contact/anatomy/helmet, normal cargo lifecycle and all-family polish remain.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(j,indent=2)+'\n')
section='''### James latest full carrying study and original-cloth reference correction - October3,2026

V278 late31..46 detail review preserves ambiguous outlined44..46 fitting pending
belt-equipment chronology; original west master has a front belt device, and user
wrench must remain on belt. Do not erase a fitting as a cloth defect without identity.
V279 original/candidate/old-panel cloth board reviewed. Yellow seam pixels occur
inside master and several candidate tiny samples: medians are diagnostic, not a
master-grade acceptance. Old invented dark panels cannot be the sole colour target;
future cloth samples exclude yellow seams/equipment and account for pose lighting.

V280 freezes current31 construction studies plus18 other selected poses,98paired
sources, original1680ms clock.939native checks0/49captures, owner profile unchanged,
frozen sources stable;98HTML embedded sources byte-exact. Changed20native poses
freshly viewed in nine boards;29identical captures reuse V265/V242 visual chain.
All49 thigh and master seam boards reviewed. Exact native-capture APNG prepared,
not observed continuous station travel. Fine quilting is improved, but stitch/seam
transitions28..31, far-side cloth and late fitting identity remain. Whole-body
proportion/grade/perspective/contact and helmet fidelity are still unaccepted.

Lesson: compare final material to original master, not defective intermediate art.
Protect equipment based on identity and chronology; screenshot/source clocks do
not prove moving ground contact. Latest mixed previews must use frozen manifests.
Next seam/equipment-free cloth sampling, crossing/far-side consistency, full-motion
review, normal pickup/carry/turn/unload and all-family polish. No normal bank changed.
Goal active/incomplete. Handoff:
character/james-west-carry-walk-keys-v1/full-gait-review-v280/HANDOFF.md.
'''
guides=record_guides(r,section,'### James crossing near-thigh construction and complete knee protection')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James full animation set

## Objective and acceptance
Complete all James action families matching original masters in identity, material,
perspective, size, proportions and moving contacts; integrate and cross-family polish.

## Accepted decisions and constraints
Matte finish, muted yellow seams. Wrench stays on belt; tablet for diagnostics,
forward torch for repair/construction. Preserve ambiguous belt fittings. New studies
remain unselected. Actual original cloth is grade reference; avoid yellow-seam samples.

## Current state
Full-gait-review-v280 freezes latest31 construction studies plus18 selected poses.
98sources, HTML/master/thigh boards, exact native-capture APNG and review evidence.
V278 late-thigh/V279 cloth audits reviewed; material ledger records full review.
Five current guides updated. Normal gameplay source selections unchanged.

## Verification
939native checks/0failures/49captures; scratch profile, real owner files unchanged;
frozen inputs stable,98embedded HTML sources exact.20changed captures freshly viewed,
29byte-identical reuse prior reviewed chain.49thigh/seam boards inspected.
Native replay decoded exact; no continuous motion/world contact acceptance.

## Next action
Resolve crossing28..31 stitch/seam transitions and far-side cloth; identify late44..46
belt equipment before edits. Sample master/candidate cloth away from seams and gear.
Then full moving master/helmet/anatomical/contact comparison, versioned normal cargo
lifecycle integration, interruptions/Continue and complete all-family consistency.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in [o,p/'late-thigh-audit-v278',a] for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(checks=939,failures=0,captures=49,changedReviewed=20,reused=29,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
