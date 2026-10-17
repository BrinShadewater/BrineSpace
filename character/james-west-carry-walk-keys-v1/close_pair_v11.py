from pathlib import Path
import hashlib, json, os, subprocess, uuid

p=Path(__file__).resolve().parent; r=p.parents[1]; out=p/'paired-v11'
def digest(f): return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f,d): f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
d=json.loads((out/'review.json').read_bytes())
assert all(digest(r/f)==sha for f,sha in d['inputSha256'].items())
v=json.loads((out/'native_probe-validation.json').read_bytes())
n=json.loads((out/'native/review.json').read_bytes())
assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['profileDelta']
assert n['checks']==301 and n['failures']==0 and n['sourceSamples']==98
assert len(n['naturalRenderClockSamples'])>=200
ns={'__file__':str(p/'audit_case_components_v5.py')}
exec((p/'audit_case_components_v5.py').read_text().split('results=[]')[0],ns)
assert all(len(ns['components'](out/f'{i:03}.png'))==1 for i in range(49))
rasters=[f.relative_to(r).as_posix() for f in out.rglob('*') if f.suffix.lower() in ('.png','.apng')]
a=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,
                 input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(a)==len(rasters)*3+1 and all(x==b'lfs' for x in a[2:-1:3])
d.update(nativeRun=True,nativeChecks=301,nativeFailures=0,nativeSourceSamples=98,
         continuousRenderClockSamples=len(n['naturalRenderClockSamples']),
         staticHeadBoardsReviewed=7,staticNativePairedCapturesReviewed=5,
         realProfileUnchanged=True,singleAlpha128ComponentsAll49=True,
         continuousMotionWatched=False,visualMotionAcceptance=False,
         normalSelectionChanged=False,lfsRastersVerified=len(rasters),
         findings=['All49 enlarged paired head views and five native full/station captures reviewed: original helmet/collar position retained without per-pose fitting.',
                   'Case width, latch placement, hand contact and belt exposure vary across sources; full continuous visual cadence remains unaccepted.',
                   'Candidate elapsed-clock looping is explicit. Distance stride, normal actor dispatch, room joins, interruption and Continue are outside this standalone check.'],
         postRunEvidenceSha256={f.relative_to(r).as_posix():digest(f) for f in
            [out/'native_probe.gd',out/'native_probe.gd.uid',out/'native/review.json',out/'native_probe-validation.json']})
save(out/'review.json',d)
planfile=p/'dense-walk-v6-plan.json';plan=json.loads(planfile.read_bytes())
plan.update(currentPairedReview='paired-v11/review.json',helmetPaired=True,visualMotionAcceptance=False,fullGoalComplete=False)
save(planfile,plan)
section='''### James West carrying full49 helmet pairing — October 2, 2026

Paired-v11 reuses the actual selected shared-helmet walk's49 chronological head
differences at original coordinates, translated36/52 with the body. Both original
walk contracts share49 variable20/30/40ms poses,total1680ms. No head fitting,
warping, repainting or invented gear motion. Equipment delta bounds111,67..146,108
include the collar; all carrying pixels outside each original helmet difference
mask are exact. All49 paired alpha128 silhouettes connected. Seven enlarged head
boards and five observed native paired views reviewed at148/82/54/27px rulers.
Standalone native301checks/0failures verifies98 exact source midpoint samples,
metadata and five post-draw paired captures;304 render-clock samples over three
continuous loops. Scratch APPDATA, whole owner profile unchanged. These render
loops were executed, not continuously visually watched. Case/grip/latch/material
variation remains provisional. No normal selection/controller/checkpoint changes.
Lesson: reuse exact per-phase helmet differences when body/gear clocks match;
include collar pixels deliberately and verify all unaffected carrying pixels.
Explicit elapsed-clock looping is not a distance-stride or real room scheduler
test. Native source/metadata checks and static captures do not certify cadence.
Next: continuous visual case/contact polish, standing/turn joins, real room and
distance-stride playback, interruptions/fresh Continue/versioned adoption, then
remaining full James cardinal/cross-family polish. Full goal remains incomplete.
Handoff:character/james-west-carry-walk-keys-v1/HANDOFF.md.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
       r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
       r/'skills/brinespace-character-pipeline/references/crew-consistency.md',
       Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    old=path.read_bytes(); entry=section.encode()
    if entry.split(b'\n',1)[0] in old: continue
    if path.name=='CURRENT_STATUS.md':
        anchor=b'### James West carrying full forty-nine-pose source draft'
        at=old.index(anchor);new=old[:at]+entry+b'\n'+old[at:]
    else: new=old+b'\n'+entry
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temp.write_bytes(new)
    assert path.read_bytes()==old
    os.replace(temp,path)
handoff='''# Project handoff

Updated: October 2, 2026 · James carrying motion

## Objective and acceptance
Full master-matched James set, then full cardinal/cross-family polish. Incomplete.

## Accepted decisions and constraints
Actual49 chronological donors, original variable clock1680ms, pivot128224/H148.
Original head/lower legs retained in bare sources. Selected helmet differences
reused at original per-phase coordinates; collar included, no per-pose fitting.
Standing local3 reference remains provisional, not owner-locked. No normal adoption.

## Current state
Full49 bare source draft v10 remains current, four material replacements retained.
Paired-v11 adds49 exact original helmet-difference pairs and source manifests.
Case width/depth/latch/grip/material/belt exposure still needs temporal polish.
No pending generation handles. No normal source/controller/checkpoint changes.

## Verification
All49 outside-equipment pixels exact, all49 paired silhouettes connected, seven
paired head boards and five native paired station captures reviewed. Native301/0,
98 exact source midpoint samples,304 continuous wall-clock render samples over
three loops. Entire real profile unchanged via scratch APPDATA. Continuous visual
motion not watched; real distance stride/room scheduler/joins/Continue unverified.
All five guides updated; new rasters LFS verified. See paired-v11/review.json.

## Next action
Review continuous case/contact motion, polish varying case/latches/grips and gear
exposure; master standing/turn joins, distance-stride and real rooms, interruptions/
fresh Continue/versioned normal adoption. Full remaining cardinal/family polish.
Do not regenerate the completed41 interior poses merely to rebuild packaging.
'''
(p/'HANDOFF.md').write_text(handoff,encoding='utf-8')
print(json.dumps({'nativeChecks':301,'failures':0,'paired':49,'headBoardsReviewed':7,
                  'nativeViewsReviewed':5,'guidesUpdated':5,'lfsRasters':len(rasters),
                  'continuousVisualAcceptance':False,'normalChanged':False}))
