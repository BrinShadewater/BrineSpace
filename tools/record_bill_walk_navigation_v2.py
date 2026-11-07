"""Retain as-tested actor movement evidence and the exact remaining join defect."""
from pathlib import Path
from PIL import Image
import json,hashlib,ast,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-walk-navigation-v1';W=R/'character/bill-east-walk-master-full-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=json.loads((D/'review.json').read_text(encoding='utf-8'));v=json.loads((D/'validation.json').read_text(encoding='utf-8'));assert v['engineExit']==0 and v['failures']==0 and not v['ownerChanges']
assert all(len(t['visitedSlots'])==48 and t['arrived'] and abs(t['distance']-320)<.001 for t in review['traversals'])
decoded=[]
for variant in ['candidate','selected']:
 records=[r for r in review['records'] if r['variant']==variant]
 for speed in [1,4]:
  with Image.open(D/f'{variant}-{speed}.png') as im:
   assert im.n_frames==len(records)
   duration=0
   for i,rec in enumerate(records):
    im.seek(i);world=Path(R/'output/bill-east-walk-navigation-v2'/rec['worldFile']);assert sha(world)==rec['worldSha256']
    expected=Image.open(world).convert('RGBA').crop(tuple(review['crop']));assert im.convert('RGBA').tobytes()==expected.tobytes()
    assert im.info['duration']==rec['durationMs']*speed;duration+=im.info['duration']
   decoded.append({'path':f'{variant}-{speed}.png','frames':im.n_frames,'durationMs':duration})
names=['prepare_bill_east_walk_navigation_v1.py','prepare_bill_east_walk_navigation_v2.py','run_bill_east_walk_navigation_v1.py','run_bill_east_walk_navigation_v2.py','publish_bill_walk_navigation_v2.py','record_bill_walk_navigation_v2.py']
for name in names:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
pngs=list(D.rglob('*.png'));result=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(p.relative_to(R).as_posix() for p in pngs)+'\0').encode(),cwd=R,capture_output=True,check=True);f=result.stdout.split(b'\0');assert len(f)==len(pngs)*3+1 and all(f[i]==b'lfs' for i in range(2,len(f)-1,3))
review.update(status='actor_distance_navigation_pass_concurrent_panel_changes',visualReviewed=True,fullVisualAcceptance=False,normalAdmission=False,pageHashes={p:sha(D/p) for p in review['pages']},decodedAPNG=decoded,visualFindings='All four full route comparison boards and normal/quarter browser snapshots inspected. Candidate remains matte, with warmer face and finer quilt detail through real movement. First step begins in extended stride and arrival returns directly to idle; a brief pose jump remains in both candidate and selected baseline. Native distance/phase checks and source review do not establish continuously watched cadence or fully smooth joins.',openIssues=['Inherited extended-stride first step and abrupt return to idle need authored join treatment.','Three unrelated UI panel files changed during native run; all tested Bill/renderer/current-bank inputs stable, but full input-freeze assertion failed.','No autonomous goal selection, equipment/water, normal admission or fullsave/TitleContinue.'])
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
validation={'mechanicalChecksPassed':True,'checks':4064,'failures':0,'completeInputFreezePassed':False,'concurrentPanelChanges':v['inputChanges'],'ownerChanges':[],'ownerNonLogCount':2931,'inputCount':4796,'routeLength':320,'actorUpdateStepsPerVariant':348,'visitedGaitSlotsPerVariant':48,'captureCount':190,'decodedAPNG':decoded,'pythonSyntaxFiles':len(names),'pngLfsCount':len(pngs),'normalAdmission':False,'fullVisualAcceptance':False}
(D/'scoped-verification.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
note=f'''

## Bill East real actor walking/arrival comparison — October3,2026

`character/bill-east-walk-navigation-v1/` retains native navigationV2 evidence:
actual Bill.update/move/arrive on a clear320unit East segment selected from the
default furnished ColdStore graph, with segment/floor checks. Candidate and
selected traverse the exact route in348simulation steps of.02s,6.96s each,
displaying all48gait slots. Retained renderer phase increments equal actual
distance/384/stride*.2seconds-cycle factor2.0; no phase prescription or actor
teleport between samples. Before/after idle and190actual world/source pairs
retained; four full route comparison pages inspected. Normal/quarter APNGs are
exact native505x155room crops with actual simulation capture intervals; four
decoded movies total380frames byte/timing exact. Current face/matte quilt detail
survives movement; direct extended-stride first step and arrival-to-idle pose jump
remain in candidate and baseline. These joins are the next concrete defect, not
evidence of changed body scale. No continuous-cadence/fullvisual acceptance.

Engine exit0,4064checks0failures,87.2s,2931owner non-log hashes unchanged under
scratchAPPDATA. All tested Bill/renderer/source-bank inputs stable. Complete
4796input freeze did NOT pass: concurrent airlock_panel.gd,crew_work_panel.gd,
moonbay_panel.gd edits captured in before/after hashes. Scope this as as-tested
actor movement proof, not a clean full-project run. No repeat of unrelated UI
work and no rewriting the failed freeze to passed. Earlier navigationV1 retained:
four fixture failures because absent construction goal cancelled route; current
neutral route uses goalempty. Room inspector lookup was already corrected in
shared source from inspector_label.parent to inspector_details.parent beforeV2;
this task's attempted patch did not apply and no UI change is claimed here.

Main/tick disabled, route/source binding explicit; only actor.update is advanced.
Actual movement/navigation/arrival and distance-driven renderer exercised, not
autonomous goal choice/full station progression. Resources/failure flags unchanged.
SixPython syntax/{len(pngs)}PNG LFS passed. Current normal Bill sources unchanged,
no export/commit. Full objective incomplete. Next author/review short whole-figure
first-step and stop joins without composited anatomy/ghosting, then normal family
admission and remaining West/cardinal/gear/water/life/cargo checks. Handoff:
`character/bill-east-walk-navigation-v1/HANDOFF.md`.
'''.replace('stride*.2seconds-cycle factor2.0','stride*2.0seconds-cycle')
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for root in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths += [root/'references/crew-consistency.md',root/'references/source-density.md']
for path in paths:
 with path.open('a',encoding='utf-8') as out:out.write(note)
handoff='''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: Bill walking joins

## Objective and acceptance
Finish Bill master-consistent animations soon, including smooth natural movement
and action joins. Full family/source/in-game acceptance remains incomplete.

## Accepted decisions and constraints
Preserve whole authored art, matte identity/detail and original motion. No anatomy
splicing or crossfade ghosts. Reversible work authorized; preserve concurrent UI
and crew changes. No normal source admission, commit or export this pass.

## Current state
Actual actor-update movement comparison in this folder: two95capture normal/quarter
native APNGs, four full comparison boards, original report/validation and both
input fingerprints. Full48source candidate remains ../bill-east-walk-master-full-v1.
New navigation fixtures/runners/publisher/record tools in tools, GDs paired UIDs.

## Verification
320unit legal route,348steps/6.96s per variant,all48gait slots,190capture pairs.
4064checks0failures,engine0/noerrors/warnings,2931owner files unchanged,scratchAPPDATA.
4796input freeze failed only for three concurrent UI panel files; Bill source/
renderer banks unchanged. All four boards and browser snapshots inspected;
380APNGdecoded frames exact. Start/arrival pose jump remains in both revisions.
SixPython syntax and PNG LFS passed. No autonomous goals or full station save test.

## Next action
Treat first-step/arrival joins as the concrete remaining East walking defect.
Author short coherent whole-source joins, preserving natural distance gait and
all48walking poses. Re-review joins in motion/game, then admission and other
families. Do not restart a full art pass or repeat unrelated UI tests.
'''
(D/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (W/'HANDOFF.md').open('a',encoding='utf-8') as out:out.write('\n\nOctober3 continuation: actual actor movement/all48gait phases now verified as-tested in ../bill-east-walk-navigation-v1/HANDOFF.md. Start/arrival pose jumps remain; three concurrent UI panel changes prevent clean complete input freeze.\n')
print(json.dumps({'checks':4064,'failures':0,'decodedFrames':380,'pngLfsCount':len(pngs),'recordsUpdated':8,'fullAcceptance':False}))
