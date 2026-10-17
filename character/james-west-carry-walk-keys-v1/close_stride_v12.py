from pathlib import Path
from PIL import Image
import hashlib,json,os,subprocess,uuid
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'paired-v12'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f,d):f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
d=json.loads((out/'review.json').read_bytes())
frozen=json.loads((out/'native-inputs.json').read_bytes())
assert all(sha(r/f)==v for f,v in d['inputSha256'].items())
assert all(sha(r/f)==v for f,v in frozen['preLaunchSha256'].items())
n=json.loads((out/'native/review.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes())
assert n['checks']==919 and n['failures']==0 and n['distanceSamples']==294 and n['stationaryChecks']==12
assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['profileDelta']
reuse={}
for i in (0,12,24,36,48):
 f=out/'native'/f'paired-{i:03}.png';old=p/'paired-v11/native'/f.name
 assert Image.open(f).convert('RGBA').tobytes()==Image.open(old).convert('RGBA').tobytes()
 reuse[f.relative_to(out).as_posix()]=old.relative_to(p).as_posix()
rasters=[f.relative_to(r).as_posix() for f in out.rglob('*') if f.suffix in ('.png','.apng')]
a=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(a)==len(rasters)*3+1 and all(x==b'lfs' for x in a[2:-1:3])
d.update(joinVisualReviewPending=False,nativeChecks=919,nativeFailures=0,
         distanceSamples=294,stationaryChecks=12,sourceMidpointSamples=98,
         continuousDistanceRenderSamples=len(n['naturalRenderClockSamples']),
         inputInventoryStable=True,realProfileUnchanged=True,unchangedReviewedNativeViews=reuse,
         continuousMotionWatched=False,normalChanged=False,sourceAcceptance=False,
         visualMotionAcceptance=False,joinReadyForNormalAdoption=False,
         joinFindings=['Standing reference is byte-identical to the authored turn West bare endpoint; remains provisional.',
                       'New walk0/48 retain original walking legs and a narrower torso/hip stance than the standing turn endpoint. Fixed foot ruler does not remove visible stance/contact changes.',
                       'Case panel/latch/grip differ between standing, walk and the larger/darker normal carry/unload case. These are unresolved art joins, not certified by distance tests.',
                       'Helmet remains original head/collar position and original49 timing. Distance stride copied from the actual donor walk, not the old six-frame cargo gait.'],
         lfsRastersVerified=len(rasters))
save(out/'review.json',d)
f=p/'dense-walk-v6-plan.json';plan=json.loads(f.read_bytes())
plan.update(currentPairedReview='paired-v12/review.json',distanceDrivenCandidate=True,
            strideDistanceCells=0.1796875,visualMotionAcceptance=False,fullGoalComplete=False)
save(f,plan)
section='''### James West carrying original distance stride and joins — October 2, 2026

Paired-v12 adds original selected walk-west stride0.1796875cells/cycle to the
unchanged49 carrying bare/helmet sources. V11 omitted stride metadata and therefore
played by elapsed time even without movement; retained as historical evidence.
The old six-frame cargo stride is not the matching original49-leg calibration.
Native919checks/0failures:98 exact source midpoint samples,294 distance-phase
samples across three speeds and both gears,12 stationary start/midstride holds,
six distance wraps;305 continuous distance-render samples over three loops.
Prelaunch source/helper/player inventories stable; scratch APPDATA and entire real
profile unchanged. Five native paired views pixel-identical to reviewedv11 views.
Two fixed-pivot whole/contact join boards reviewed: standing equals authored turn
West endpoint, but new walk retains narrower original walking torso/hip stance;
case panel/latch/grip differs from standing and larger/darker normal carry/unload.
These joins remain unaccepted. No normal controller, binding or bank changes.
Lesson: source timing is insufficient for locomotion; copy the exact matching
donor distance stride and exercise stationary holds, multiple speeds and wraps.
A stride pass does not establish case rigidity, continuous visual cadence, master
joins or actual room acceptance. Next contact/material/bridge source polish, real
room dispatch/interruption/fresh Continue/versioned adoption, full James cardinal
and cross-family review. Goal incomplete.
Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=path.read_bytes();entry=section.encode()
 if entry.split(b'\n',1)[0] in old:continue
 if path.name=='CURRENT_STATUS.md':
  at=old.index(b'### James West carrying full49 helmet pairing');new=old[:at]+entry+b'\n'+old[at:]
 else:new=old+b'\n'+entry
 temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
 assert path.read_bytes()==old
 os.replace(temp,path)
handoff='''# Project handoff

Updated: October 2, 2026 · James carrying motion

## Objective and acceptance
Full master-matched James animation set, then all cardinal/cross-family polish.
Incomplete. No normal adoption or owner approval inferred from technical checks.

## Accepted decisions and constraints
Actual49 selected chronological walk donors,1680ms variable clock,pivot128224/H148.
Original head/lower legs retained. Exact original helmet differences, no fitting.
Original49 walk stride0.1796875cells now governs unchanged candidate carry gait.
Standing local3 reference remains provisional. Preserve completed41 interiors.

## Current state
Full49 v10 bare draft,49 v11 helmet pairs; v12 manifests add distance stride.
V11 elapsed-only manifest superseded for candidate movement, historical evidence
retained. No normal sources/controllers/checkpoints changed. No live generation.
Standing/turn endpoint is identical, but walk stance and case/grip/latch differ;
normal carry/unload case is larger/darker. Contact/material/join art still open.

## Verification
V12 native919/0:98 midpoint source checks,294 distance samples at three speeds and
both gears,12 stationary holds,six wraps,305 continuous distance render samples.
Frozen prelaunch inputs stable,whole owner profile unchanged,scratch APPDATA.
Five native views match reviewedv11 pixels; two new whole/contact join boards
reviewed. New rasters LFS verified. All five guides updated. See paired-v12/review.
Continuous visual cadence,actual room dispatch,interruptions/Continue unverified.

## Next action
Case rigidity/grip/material and standing/turn/walk/unload bridge polish. Retain
actual original leg phase and stride; do not fit frames or copy a standing stance
over every gait pose. Then actual room/distance playback,interruptions/Continue,
versioned normal adoption,remaining full James cardinal and cross-family polish.
'''
(p/'HANDOFF.md').write_text(handoff,encoding='utf-8')
print(json.dumps({'checks':919,'failures':0,'distanceSamples':294,'stationaryHolds':12,
                  'guides':5,'joinBoardsReviewed':2,'normalChanged':False,'lfsRasters':len(rasters)}))
