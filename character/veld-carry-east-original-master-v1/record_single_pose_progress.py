"""Record original-guided independent pose and bounded native appearance evidence."""
from pathlib import Path
import json,shutil,uuid,time,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'single-transition-source-v1';N=R/'output/veld-east-single-transition-v1'
title='## Veld East independent whole transition key — October 3, 2026'
note='''## Veld East independent whole transition key — October 3, 2026

Builtin75bc5398-31b6-427d-a1b5-3c7c2067de8c creates ONE complete source directly
from unchanged original held raw, no atlas/gait/video appearance guide. Saved exact
prompt/raw RGBA/source audit under single-transition-source-v1. One global source
ruler: body148/head27 vs original held148/26 and original empty148/27; floor223,
no clipping. Upper body44px vs held42; sampled neutral cloth69/68/67 vs66/64/63,
no RGB correction. Whole master/source and enlarged head/legs reviewed. Retained
PROVISIONAL source key, not final grade/identity or complete transition admission.

Actual output lifts the FAR/smaller-pad boot, near/larger-pad boot down; prompt
requested near lift. Record actual foot identity, do not call it the requested one.
Planted sole band108..130 vs original113..133 under common head-axis registration;
physical root movement/contact calibration required. Do not silently align each
video frame or pretend zero-travel contact is proven. New whole-pose registration
is separate from the fixed-plate video, whose scale/offset stay untouched.

Original whole profile helmet fitted107,66, protected body outside fitting EXACT.
3source protection/clipping checks0. Paired one-key native appearance13checks0,
2presentations at47/93/148,20inputs and2931owner files unchanged,4.59s under scratch
APPDATA. Both complete native master comparisons visually reviewed. Finite320ms
single-key review manifests, no duplicated invented intermediates/full start-stop,
stride/contact/controller/save acceptance. No normal selectors changed.

Lesson: prove one complete independently authored pose from the original before
expanding a drifting atlas. A complete sprite remains subject to head/body/material
and native review; source-frame count is not motion coverage. Track actual foot
identity and planted contact/root travel separately from image head-axis alignment.
No head/anatomy/RGB patches to conceal failed sources. Earlier atlas rejects retained.

Next author remaining original-derived prelift/heel-touchdown/recovery whole poses,
exact held/gait joins and dense timing; complete actual root/contact/start-stop
playback. Gait near/far overlap/heel-toe/temporal wrap, final master consistency,
North contact failure/full original action-direction/furniture/controller/save/menu
Continue and cross-library polish remain. Full goal active/incomplete; no live job.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.

'''
entry={'id':'75bc5398-31b6-427d-a1b5-3c7c2067de8c','folder':S.name,'raw':'single-transition-source-v1/raw-transition-v1.png','prompt':'single-transition-source-v1/prompt.txt','references':['../veld-east-held-original-master-v1/raw-held-v1.png'],'status':'Completed; provisional whole-source key','verdict':'Original-only single whole pose retains148height/head27 vs original26-27/floor223/no clipping; neutral materials much closer. Upperbody44vs42/cloth69,68,67vs66,64,63, final fidelity pending. Output lifts FAR boot despite near-lift prompt. Paired original shell protects body; native13checks0/2three-scale presentations/20inputs stable/2931ownerfiles unchanged. No complete start/stop, physical contact, root/stride or normal admission.'}
data=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
if not any(g['id']==entry['id'] for g in data['generations']):data['generations'].append(entry)
(P/'EXECUTIONS.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
(S/'VERDICT.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf-8')
review={'nativeValidation':json.loads((N/'validation.json').read_text(encoding='utf-8')),'visualReview':'Complete bare and original-shell helmet native47/93/148 master comparisons inspected. Whole pose body/skin/hair/neutral quilting coherent and retained provisionally, final fidelity still pending. Head27 within original26-27 source range, original-equipment body protected. Planted foot/root travel and full transition not exercised.','actualFoot':'Far boot lifted, near boot down; preserve actual identity despite prompt.','initialPreviewSetupFailure':'Shell quoting failed before fixture creation or Godot launch; corrected using saved prepare_native_review.py, sole actual native interval passed with scratch APPDATA.','fullTransitionAccepted':False,'bindings':{str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [S/'raw-transition-v1.png',S/'prompt.txt',S/'source-audit.json',S/'key-record.json',N/'records.json',N/'bare-000-native.png',N/'helmet-000-native.png']}}
(S/'native-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
with (P/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('''
## Latest independent whole-pose source milestone
single-transition-source-v1 builtin75bc5398-31b6-427d-a1b5-3c7c2067de8c uses only
original raw-held-v1, one complete pose; head27/body148/floor223/no clipping versus
original held26/148 and original empty27/148. Neutral cloth median69,68,67 vs66,64,63;
upperbody44vs42, no RGB/head/limb correction. Provisional source key retained after
master/enlarged head-leg review, not final appearance or complete transition.
Output FAR boot lifts (prompt near); near larger-pad boot stays down. Ground band
108..130 vs original113..133 means actual root/contact calibration still needed.
Paired original whole shell107,66/protected body exact;3sourcechecks0. Native
13checks0/2presentations at47/93/148/20inputs unchanged/2931ownerfiles unchanged,
4.59s; both native comparisons reviewed. Scratch APPDATA interval under
output/veld-east-single-transition-v1, matching test+uid/runner in tests/tools.
One finite320ms key manifests only, no synthetic intermediates/full start-stop.
Next remaining original-derived prelift/heel-touchdown/recovery whole poses,
exact master held/gait joins and actual moving root/contact transition verification.
All gait/near-far/full action-direction/furniture/controller/save/library polish
scope remains active. No normal selectors changed and no live generation remains.
''')
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(P/'record_single_pose_progress.py'),'exec'))
print('One original-derived whole transition key and native appearance evidence recorded; full goal active.')
