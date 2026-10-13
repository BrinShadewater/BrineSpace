"""Bind four-key source evidence and maintain lessons without claiming full cadence."""
from pathlib import Path
import json,hashlib,ast,subprocess
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';K=P/'keypose-review-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=json.loads((K/'review.json').read_text(encoding='utf-8'));assert all(sha(Path(p))==h for p,h in review['inputs'].items());assert all(sha(Path(p))==h for p,h in review['selectedInputs'].items());assert [r['heightDelta'] for r in review['records']]==[1,1,0,1] and all(r['soleDelta']==0 for r in review['records'])
for slot in [0,12,24,36]:
 D=P/(f'stride-{slot:03}-v2' if slot==24 else f'stride-{slot:03}-v1');report=json.loads((D/'review.json').read_text(encoding='utf-8'));report.update(status='provisional_source_keypose',visualReviewed=True,visualFindings='Whole raw and full selected/edit-target/new/master/continuity boards inspected. Material and warm angular face closer to master. Geometry/proportion and neighbor/seam continuity remain provisional; preferred packing/registration and family review in keypose-review-v1.');(D/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
review.update(visualReviewed=True,visualFindings='Entire original/new/master whole/head board and four-density comparison inspected. Matte quilt/detail and warm face closer across four phases. Source phase-dependent heights preserved to0/1px; face/collar and boot shape still vary, phase36 left bound4px wider and horizontal support not certified. Static keys do not establish smooth neighbors/seam/full48 motion.',boardHashes={name:sha(K/name) for name in ['whole-master-comparison.png','density-comparison.png','foot-comparison.png']},openIssues=['44preferred source phases absent; no full loop/manifest/native runtime acceptance.','Face/collar/material variability and neighbor/seam continuity remain.','Boot anatomy/phase36 side extent and2Dsupport remain provisional; Ysole equality does not certify planted feet.'])
(K/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
tools=['prepare_bill_walk_stride000_v1.py','prepare_bill_walk_crossing_trials_v1.py','review_bill_walk_source_trial.py','build_bill_walk_keypose_review_v1.py','review_bill_walk_keypose_feet_v1.py','record_bill_walk_keypose_milestone_v1.py']
for name in tools:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
pngs=list(P.rglob('*.png'));result=subprocess.run(['git','check-attr','filter','--']+[p.relative_to(R).as_posix() for p in pngs],cwd=R,capture_output=True,text=True,check=True);assert len(result.stdout.splitlines())==len(pngs) and all(x.endswith(': filter: lfs') for x in result.stdout.splitlines())
validation=dict(passed=True,preferredSourcePoses=4,totalRequiredSourceSlots=48,remainingSlots=44,generationUnits=5,selectedProtectedInputs=49,selectedChanges=[],heightDeltas=[1,1,0,1],soleYDeltas=[0,0,0,0],normalAdmission=False,nativeTested=False,pythonSyntaxFiles=6,pngLfsCount=len(pngs),boardHashes=review['boardHashes']);(K/'validation.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
note=f'''

## Bill East four representative master walking poses — October3,2026

New built-in whole-pose0/12/36 and24v2 head/neck settling repair extend source
study to4of48preferred walking poses; five generation units including superseded
original24. Four new raws and all full target/new/master boards inspected.
keypose-review-v1 compares all four originals/candidates/master, source/head and
H148/82/54/27density; all boards inspected. Full loop not reduced to four holds,
no partial manifest or normal admission.44source slots remain unpreferred.

Phase24v2 reduces prior height+4 to exact selected142pixels. Its whole canvas
is losslessly registeredy-1, survivingRGBA and alpha counts exact/no discarded
alpha. Other three whole uniform256packed sources unchanged. Preferred occupied
heights145/147/142/147 versus selected144/146/142/146, deltas1/1/0/1; Ysole deltas
zeroall4. Bounds delta0(-1,-1,+1,0),12(0,-1,+1,0),24(-1,0,+2,0),36(-4,-1,+1,0).
Matte quilt/worn hardware/warm angular faces closer, face/collar/boot shape still
variable. Phase36 extra4pxleft extent remains anatomy/motion review concern.

Fixed foot crop reviewed. Lowest-row Xcentroid deltas.75/1/-1/7.818px are raster
diagnostics, not physical support positions. Phase36 bottom4rows span120..151
selected versus122..151new, despite large lowest-row centroid difference. Changed
sole shape/rasterization can alter this statistic; neither centroid difference
nor matching Ysole alone proves/slips2Dplanted anatomy. Preserve full foot review.
Declared standingH148 does not require constant occupied gait height: keep
authored phase-dependent body articulation rather than fitting everypose to148.

Four receipt/reference/prompt chains and49selected manifest/frame hashes stable;
sixPython syntax/{len(pngs)}PNG LFS checked including preparation/old source evidence.
No native run/browser/full48cadence or normal loader change this pass. Prior910
nativechecks cover idle/reach only. Next inspect accepted East gait source/motion
provenance before blind44near-phase redraws; refine shared face/boot continuity,
expand complete48original phases/timing and native joins. West/cardinal/gear/
water/life/hazard/full-library master polish remains. Full goalactive/incomplete;
previous turn progress, all four current generation jobs terminal/raws saved.
Handoff:character/bill-east-walk-master-pilot-v1/HANDOFF.md.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for root in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths += [root/'references/crew-consistency.md',root/'references/source-density.md']
for p in paths:
 with p.open('a',encoding='utf-8') as f:f.write(note)
print(json.dumps(validation))
