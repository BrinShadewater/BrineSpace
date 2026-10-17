import hashlib
import json
import subprocess
from pathlib import Path
from milestone_notes import insert_status

root=Path.cwd();bank=root/'character/james-west-carry-walk-keys-v1';out=bank/'north-unload-reused-rise-v363'
provenance=json.loads((out/'provenance.json').read_text())
for name,digest in provenance['sourceSha256'].items():
    assert hashlib.sha256((root/name.lstrip('/')).read_bytes()).hexdigest()==digest
validation=json.loads((root/'output/james-unload-playtest-v363/validation.json').read_text())
native=json.loads((out/'native-review.json').read_text())
assert validation['exitCode']==0 and validation['ownerUnchanged'] and validation['qaOverrideRemoved']
assert native['checks']==1912 and native['failures']==0 and len(native['cases'])==8
assert len(native['captures'])==1878 and (out/'native_playtest.gd.uid').exists()
for path in out.glob('*.png'):
    result=subprocess.run(['git','check-attr','filter','--',str(path.relative_to(root))],capture_output=True,text=True,check=True)
    assert result.stdout.rstrip().endswith(': lfs')
report={'version':363,'selected':False,'normalChanged':False,'packageChanged':False,
    'method':'Reuse selected original slot2 after original slot4, before standing. Both gears use exact selected artwork; seven poses,520ms. Return hold80ms split40+40.',
    'alpha128CrownRisePixels':[107,94,76],'previousLastRisePixels':31,'newRiseStepsPixels':[13,18],
    'newArtwork':0,'rgbAltered':False,'decodedApngFramesVerified':14,
    'nativeChecks':1912,'nativeFailures':0,'nativeCases':8,'nativeCaptures':1878,
    'visualReview':'Both seven-pose source chronology boards, one paired browser comparison and all eight native pose/idle boards viewed. Continuous comparison supplied; not continuously observed by agent.',
    'nativeSourceTrace':'Array.find(texture) reports reused slot5 as index2. Chronological observed runs0,1,2,3,4,2,6 establish return after partial rise in all eight cases; no new simulation needed to resolve diagnostic alias.',
    'ownerUnchanged':True,'qaOverrideRemoved':True,
    'limits':'Existing wide crouch, master material/arm pose and North floor-case support unchanged. This is a staged timing study, not a shipping build or full original-master acceptance.',
    'next':'Admit seven-pose sequence with paired manifest/builder/verifier changes after join review; verify normal consumer and preserve existing pickup/carry and520ms duration. Then freeze a new James release snapshot if adopted.'}
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n')
section='''### James reused North unload rise — October 4, 2026

V363 reuses existing selected mid-rise drawing before standing, for both bare and
helmet. Seven poses520ms;80ms return hold split40+40. No new artwork, recoloring,
body warp or generation. Alpha128 crown rise107→94→76 splits31px into13+18.
Both chronology boards and paired browser view reviewed. Exact V351 packaged
fixture-only texture resequencing:1912checks0, eight real workshop layout/gear
cases,1878captures; all eight native boards viewed. Diagnostic Array.find reports
the reused slot5 as first identical index2; chronological0,1,2,3,4,2,6 proves the
return pose in all cases.14 APNG source frames/clocks exact. Scratch owner unchanged,
QA override removed. Staged/unselected; normal manifests, source pixels and ZIP
unchanged. Wide stance/material/arm and North case limitations remain. Next paired
manifest/builder/verifier admission and normal-consumer check if this join is used.
Review: character/james-west-carry-walk-keys-v1/north-unload-reused-rise-v363/.
'''
insert_status(root/'docs/CURRENT_STATUS.md',section,'### James North unload endpoint review — October 4, 2026')
ledger=bank/'material-repair-progress.json';data=json.loads(ledger.read_text())
data['northUnloadReusedRiseStudy']=report;data['nextVisualRepair']=report['next']
ledger.write_text(json.dumps(data,indent=2)+'\n')
(out/'HANDOFF.md').write_text('''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James reused North rise

## Objective and acceptance
Continue James polish and wrap the next game release. Seven-pose North timing study
splits the ending jump using existing selected artwork, with matching helmet.

## Accepted decisions and constraints
Original matte master, belt wrench, forward torch and inward tablet remain.
Keep original pixels and physical registration. No new generation needed here.

## Current state
V363 paired playback catalogue, provenance/hashes, source APNGs, chronology/browser
comparison, native fixture/UID, eight native boards, review.json and three helpers.
Current status and material ledger updated. Normal selection and V358 ZIP unchanged.

## Verification
Both source chronologies, browser430ms comparison and eight native boards viewed.
14 exact decoded APNG poses/clocks.1912checks0, eight layout/gear workshop lifecycle
cases,1878native captures. Actual pose runs0,1,2,3,4,2,6 confirm reused return texture;
index alias is the observer's Array.find, not a missing pose. Scratch owner unchanged,
QA override removed, exact tested EXE/PCK retained. Continuous movie supplied but
not continuously watched by agent. Existing stance/material/North case not repaired.

## Next action
Review seven-pose join, then paired manifests/build_pickup.py/verify.py admission
and normal-consumer verification; keep pickup/carry pixels and520ms unchanged.
If adopted, freeze/export a new James snapshot; V358 does not contain this timing.
Publishing and later shared UI/character inclusion remain undecided; human's Keep
going resumed local animation work and did not select an itch.io upload.
''',encoding='utf8')
print(json.dumps({'nativeChecks':1912,'failures':0,'cases':8,'decodedSourceFrames':14,'normalChanged':False,'newGenerationJobs':0}))
