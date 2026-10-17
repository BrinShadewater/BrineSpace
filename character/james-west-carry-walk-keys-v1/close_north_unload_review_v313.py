from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-bend-source-v313';q=p/'north-unload-support-source-v312';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
v=json.loads((o/'native_probe-validation.json').read_bytes());n=json.loads((o/'native-evidence.json').read_bytes());frozen=json.loads((o/'native-inputs.json').read_bytes());assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta'];assert (n['checks'],n['failures'],n['captures'])==(65,0,6);assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
inputs=json.loads((q/'inputs.json').read_bytes());assert sha(r/inputs['editTarget'])==inputs['editTargetSha256'] and sha(r/inputs['referenceFile'])==inputs['referenceSha256'] and sha(q/'prompt.txt')==inputs['promptSha256']
m=json.loads((o/'bare-review-manifest.json').read_bytes());state=m['states'][1];dec=Image.open(o/'bare-unload-study.apng');assert dec.n_frames==6
for i,src in enumerate(state['frameFiles']):dec.seek(i);assert np.array_equal(np.asarray(dec.convert('RGBA')),np.asarray(Image.open(r/src[6:]).convert('RGBA')));assert dec.info['duration']==state['frameDurationsMs'][i]
report=dict(disposition='provisional_narrow_stance_unload_pose2',sourceBoardAndRawReviewed=True,nativeCapturesReviewed=6,nativeChecks=65,nativeFailures=0,decodedApngExact=6,totalMs=520,normalChanged=False,selected=False,sourceAcceptance=False,fullGoalComplete=False,findings=['313 starts from actual old unload2 geometry plus same-canvas preceding boots and original master quilt crop. Whole raw1254-to256 nearest only. Crown92 vs old94, sole224 vs preceding309225 and exact turnend224; narrower boots under hips.', 'New pose retains wrench/meter/backpack emblem and front case handles. Quilt/hardware are sharper/brighter than preceding sources and backpack/head details redraw: full master/material continuity still provisional.', 'Candidate0 exact old turnend,1 new309,2 new313,3..5 original. Later2-to3 stance widening and bottom-to-return head/body/grade changes remain. Full sequence source board and all6native four-size captures viewed.', '65native checks0, scratch owner unchanged, frozen runtime/source/manifest hashes stable; six APNG frames exact520ms. Phase snapshots/timing are not continuous observed motion, exact physical support, helmet fit or actual arrival integration.', '312 explicit boots-reference repair retained floated soles221 and changed crown87to84; rejected before native. No procedural body painting/fit/translation.'])
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();d=json.loads(old);d['northUnloadBendReview']=dict(version=313,file=(o/'review.json').relative_to(r).as_posix(),sourcePose2='313',sourcePose1='309',selected=False,sourceAcceptance=False,normalChanged=False);d['northUnloadBendSourceTrials']['versions'].append(312);d['northUnloadBendSourceTrials']['files'].append((q/'review.json').relative_to(r).as_posix());d['nextVisualRepair']='313 narrow-boot shallow bend provisionally replaces source2; refine later2-to3 crouch/return stance and master fabric/gear/head grade consistency,3091px sole discrepancy. Complete helmet, carry/turn start, actual arrival/controller/lifecycle normal admission and all-family polish.';assert ledger.read_bytes()==old;ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
section='''### James existing-bend geometry and narrower unloading stance - October3,2026

V312 explicit same-canvas309 boot-only reference edit of311 did not restore feet:
sole221 persists, crown84; raw stray mark removed, upper body changed. Rejected
before native. V313 instead uses actual original unload2 pose as geometry target,
same registered boot support and original master quilt crop as appearance only.
Builtin raw1254 saved, frozen prompts/reference hashes; whole nearest256 once,
no body fit/translation/procedural art painting. Raw and full source chronology
actually viewed.313 crown92 vs original94, sole224 vs309225/turnend224, narrower
boots under hips. Wrench/meter/emblem retained; finer quilt/hardware and changed
backpack/head detail still create grade/identity joins needing master polish.

Candidate six poses exact turnend0/new3091/new3132/original3..5,520ms unchanged.
Native65checks0/6four-size captures all viewed, scratch owner unchanged and frozen
hashes stable. All6APNG frames exact/clocks verified. No continuous observed
unloading, exact moving support, helmet fit or actual controller arrival proof.
Later2to3 widens stance; bottom/return head/body/material changes remain. Normal
unchanged, provisional/unselected, full goal active/incomplete.

Lesson: after repeated inferred-bend drift, actual existing action geometry is
a stronger edit target than requesting another new crouch from a standing pose.
A boot-support reference helps constraint communication but cannot guarantee
pixel registration; verify sole level, spacing, articulation and all neighbor
joins. Retain failed source trials, do not promote technical metadata as art proof.
Handoff: character/james-west-carry-walk-keys-v1/north-unload-bend-source-v313/HANDOFF.md.
'''
guides=record_guides(r,section,'### James north bend trials and planted-support constraint')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James north unloading

## Objective and decisions
Full James master-matched animation set, actual integration, all-family polish.
Dark matte master identity and proportions, wrench on belt, natural bend/support.

## Current state/changed files
312 saved builtin support repair rejected.313 builtin existing-pose repair target,
frozen prompts/refs, raw receipt, whole256 export, chronology/measurements, six-pose
bare manifest, probe/UID/log/evidence/captures/APNG. Main ledger and five maintained
guides updated. Candidate0 turnend exact,1=309,2=313,3..5 original,520ms. Normal
selectors unchanged; this remains provisional.

## Verification and limits
Raw/full source board and all6native four-size captures viewed.65checks0, scratch
owner unchanged/frozen hashes stable. Six APNG frames byte/timing exact.313 narrowed
boots, crown92/sole224; preceding309sole225 still1px difference.312sole221 not
fixed by reference; rejected.313 fabric/gear sharper/brighter than preceding,
backpack/head redraw and2to3 widening persist. No full continuous observed motion,
physical contact, shared helmet or actual arrival controller acceptance.

## Next action/remaining
Refine later crouch/return stance and master material/head/gear consistency. Fit
shared helmet, complete latest carry-to-turn start, verify actual arrival selector
currently bypassing generic turn. Then ordinary lifecycle/checkpoint/Continue/
interruptions/normal admission and all-family directions/consistency/polish.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as stream:stream.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in (q,o) for f in folder.iterdir() if f.suffix in ('.png','.apng')];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3));print(json.dumps(dict(checks=65,failures=0,capturesReviewed=6,decodedExact=6,totalMs=520,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
