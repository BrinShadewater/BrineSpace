from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'standing-step-video-v2-native';N=R/'output/veld-east-native-stride-probe-v1'
review=json.loads((S/'native-stride-review.json').read_text(encoding='utf-8'))
review['visualReview']='Enlarged24leg phase board, separate near/far support window board, both complete native38pose148 boards, actual moving wrap53->16 both gears and full47/93/148 raw35 pair viewed. Promising short-window stability, near heel first frame changes shape/vertical, complete roll/occlusion/material/standing handoffs remain.'
(S/'native-stride-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
evidence={'status':'provisional complete38-pose stride trial, final contact/artwork unaccepted','nativeValidation':json.loads((N/'validation.json').read_text(encoding='utf-8')),'nativeReview':review,'bindings':{str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [S/'leg-phase-diagnostic.json',S/'support-window-diagnostic.json',S/'phase-timing-study.json',S/'native-stride-review.json',S/'stride-review-v1/index.html',N/'records.json']}}
(S/'STRIDE_VERDICT.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
ledger=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
for entry in ledger['generations']:
 if entry['id']=='448578329612795':entry['strideStudy']={'status':evidence['status'],'evidence':S.name+'/STRIDE_VERDICT.json','diagnosticStrideNativePixels':106.4,'nativeChecks':1015,'nativeFailures':0};break
else:raise AssertionError('Original generation ledger entry missing')
(P/'EXECUTIONS.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
title='## Veld original-native full-cycle stride trial — October 3, 2026'
note=title+'''\n\nRead-only whole lower-body recurrence favors38frames (error19.97vs37/39
39.25/48.72); enlarged24phase board reviewed. Larger near versus smaller far knee
pad continuity distinguishes alternating legs; similarity alone never proves that.
Separate front-support windows far16..20/near34..38 use warm boot materials,
not closest foot across overlap. Both rates67.2nativepx/sec imply provisional
106.4nativepx stride per38sourceframes. Far minNCC.945/dy0; near raw34 heel-landing
minNCC.698/dy-1: flat-support correspondence is weaker during heel roll, not final
rigid contact. Complete source142poses unchanged; selected full two-leg cycle16..53
retains ALL38sourceposes byte-exact, original uniform41/42ms durations1583ms,
original whole helmet.228source/reference replay checks0. No pacing or art repair.

Actual distance-driven crew_sprite_player trial uses full38poses/two cycles/both
gears/three scales, provisional stride106.4 and normal diagnostic world speed46.
1015checks0/156presentations/7.80s/engine0,308inputs stable/2931owner files unchanged
under scratch APPDATA.468exact native replay/selected-source checks0. Independent
RENDERED warm boot matching at93/148 across both support windows/both cycles/gears:
integer dxSpan0 in all16runs, dySpan0 except near148heel frame1px, NCC far.929..973
and near.728..761. These are material appearance proxies, not literal soles or
complete heel/toe support. All38native148poses both gears, traveling wrap53->16,
and representative complete47/93/148 pair reviewed.308inputs still intact.
312exact caption-crop/duration checks0 for nontechnical paired review replay.

Promising root/pose coordination, still PROVISIONAL. Pale contours, original
head/body/case fidelity and native pixel grade remain; dense standing start/stop,
full near/far occlusion/contact/roll and wrap validation still required. No normal
selectors/controller/save or final stride adoption. Lessons: fixed-view independent
rendered material matching is stronger than adding presumed root to source landmarks,
but stable translations can coexist with shape-changing heel contact. Keep those
claims separate and preserve the full bilateral cycle and entire original clip.
Next complete roll/sole contact plus source contour/proportion/start-stop repair;
original North and full action/direction/furniture/controller/save/Continue,
then whole-library polish. Full goal active/incomplete.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.
\n'''
h=P/'HANDOFF.md'
if title not in h.read_text(encoding='utf-8'):
 with h.open('a',encoding='utf-8') as f:f.write('\n'+note)
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(Path(__file__)),'exec'))
print('Full-cycle stride evidence recorded; final support/master/standing transitions remain open.')
