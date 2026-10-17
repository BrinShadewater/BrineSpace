from pathlib import Path
from PIL import Image
import json,hashlib,os,uuid,time,subprocess,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'finite-handoff-v44';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in d['preLaunchSha256'].items())
native=json.loads((out/'native-evidence.json').read_bytes());validation=json.loads((out/'native_probe-validation.json').read_bytes());assert native['checks']==186 and native['failures']==0 and native['captures']==6 and native['handoffSourceSamples']==98 and native['handoffMs']==210 and native['journeyMs']==1890
assert validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
for mode in ['bare','helmet']:
    pack=json.loads((out/(mode+'-manifest.json')).read_bytes());assert all(s['frameCount']==3 and s['frameDurationsMs']==[70,70,70] for s in pack['states'])
for key in ['carry-prepare-west','carry-unprepare-west']:
    for i in range(3):
        f=out/'native'/(key+'-%03d.png'%i);old=p/'finite-bridge-v41/native'/(key+'-%03d.png'%(i if key=='carry-prepare-west' else i+1));assert np.array_equal(np.array(Image.open(f)),np.array(Image.open(old)))
assert d['preparationMs']==210 and d['journeyMs']==1890 and d['walkSourceFrames']==49
case=p/'case-contact-v43';review=json.loads((case/'review.json').read_bytes());review.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='rejected_insufficient_native_case_join_improvement',findings=['Raw and paired enlarged case/whole source boards actually reviewed. Native-size case/grip change is insufficient to solve final projection join, despite more squared hardware in enlarged raw. Do not accept upscaled-only improvements.', '64496 outside case/grip pixels exact and original head/legs/outside wrist exact. No native rerun or adoption warranted for visually rejected source.'],fullGoalComplete=False);(case/'review.json').write_text(json.dumps(review,indent=2)+'\n')
(case/'generation-index.json').write_text(json.dumps(dict(state='terminal_copied',rawSha256=sha(case/'raw.png'),promptFile=(case/'prompt.txt').relative_to(r).as_posix(),inputInventory=(case/'inputs.json').relative_to(r).as_posix(),disposition=review['disposition'],normalChanged=False),indent=2)+'\n')
(p/'case-projection-v42/review.json').write_text(json.dumps(dict(reviewedSourceCrops=9,scope='Three preparation/master case contacts and six distributed walking case contacts, not all49 frames.',findings=['Later projected case fittings appear rounder/brighter than standing design. Assess at native scale; apparent width change also includes orientation.'],normalChanged=False),indent=2)+'\n')
evidence=dict(nativeChecks=186,nativeFailures=0,handoffSourceSamples=98,reviewedNativeCaptures=6,reviewedNativeBoards=2,capturesPixelExactToReviewedV41=True,preparationFrames=3,preparationMs=210,walkSourceFrames=49,walkMs=1680,journeyFrames=52,journeyMs=1890,firstWalk0StartMs=210,firstWalk1StartMs=250,normalChanged=False,sourceAcceptance=False,continuousVisualMotionReviewed=False,fullGoalComplete=False,realProfileUnchanged=True,scope='Isolated candidate: finite preparation hands off to actual distance-driven CrewSpritePlayer walk with98exact source boundaries, no duplicated first walking hold. Normal cargo controller/room/Continue integration remains open.',knownRemaining=['Final chest/case projection/material join','Visible authored sole-row variation','Actual cargo lifecycle/rooms/interruption/Continue','Full cardinal and cross-family polish'],archivedFailedRuns=['failed-parse-v1','failed-parse-v2'])
(out/'review-acceptance.json').write_text(json.dumps(evidence,indent=2)+'\n')
section='''### James carrying preparation handoff clock corrected — October 2, 2026

V42 nine same-coordinate case/grip crops reviewed: three preparation/master and
six distributed walking contacts, not the full49. Later fittings read rounder and
brighter. V43 builtin local case detail source copied/prompt/input hashes retained;
64496 outside case/grip pixels exact. Raw and paired case/whole boards reviewed.
Rejected: enlarged squared fittings do not improve native case join sufficiently.
Do not admit upscaled-only detail gains or expand this repair across the walking bank.

V44 resolves a staged timing mismatch: V41 four-source250ms preparation already
contained walk0 for40ms; starting a fresh1680ms walk afterward would duplicate that
hold and total1930ms, unlike the1890ms combined preview. Use three preparation
sources at70ms each, then enter original distance-driven walk0 at210ms and walk1
at250ms. All49 original walking sources/clocks retained;52frame1890ms preview exact.
Native186/0 includes98 actual distance source-boundary samples across both gears.
Six native four-size paired captures reviewed, pixel-exact to reviewed V41 sources.
No geometry/source changes; final chest/case join and sole contact variation remain.

Two fixture parse failures archived (injection missed space indentation, then mixed
tabs/spaces); corrected program frozen before final launch. All runs terminal and
whole owner profile unchanged with scratch APPDATA. Normalize fixture indentation
before injecting new blocks and verify target insertion. Native checks certify this
explicit staged handoff, not normal cargo controller wiring/rooms/Continue.
Normal source/registry/cargo binding unchanged. Full set unfinished.
Next actual cargo lifecycle staging with210ms handoff, full motion/room and contact
review, interruption/Continue, source polish and versioned adoption; full-set polish.
Evidence:character/james-west-carry-walk-keys-v1/finite-handoff-v44/review-acceptance.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index(b'### James coherent carrying intermediate staged');new=old[:at]+entry+b'\n'+old[at:]
    else:new=old+b'\n'+entry
    tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    try:
        for attempt in range(5):
            assert f.read_bytes()==old
            try:os.replace(tmp,f);break
            except PermissionError:
                if attempt==4:raise
                time.sleep(1)
    finally:
        if tmp.exists():tmp.unlink()
(out/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · James preparation/walking handoff

## Objective and accepted decisions
Full James master-matched set and cross-family polish. Incomplete. Original matte
masters, physical proportions, correct equipment, original49walking chronology.

## Current state and changed files
V42 case contact comparisons and V43 local detail trial retained; V43 rejected.
V44 three-source210ms preparation/reverse and original49walk/1680ms bridge staged.
First walk0 starts210ms, walk1 starts250ms; no duplicate40ms walking entry hold.
Preview52frames1890ms exact. Helpers/manifests/fixture/reviews/five guides updated.
Normal loader/registry/cargo binding unchanged; no commit/PR/export.

## Verification
Native186/0,98 exact distance-driven walking source-boundary samples across2gears.
Six paired four-size captures reviewed, pixel-exact to V41 sources. Input/native
program hashes stable before final launch. Two parse failures archived and repaired.
All processes terminal, generation copied, whole owner profile unchanged with
scratch APPDATA. No normal cargo controller, room/Continue or full-motion acceptance.

## Remaining work and next action
Stage actual cargo lifecycle using210ms handoff; inspect whole journey in rooms,
case/chest projection/material and authored sole contacts. Verify interruption and
Continue before versioned adoption. Complete remaining full-set consistency polish.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in [p/'case-projection-v42',case,out] for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(nativeChecks=186,failures=0,handoffSourceSamples=98,reviewedCaptures=6,guidesUpdated=5,lfsRasters=len(rasters),normalChanged=False,fullGoalComplete=False)))
