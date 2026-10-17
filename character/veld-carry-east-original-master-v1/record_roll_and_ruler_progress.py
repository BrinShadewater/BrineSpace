from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'standing-step-video-v2-native';D=S/'global-standing-ruler-v1'
roll=json.loads((S/'boot-roll-diagnostic.json').read_text(encoding='utf-8'));ground=json.loads((S/'ground-outline-diagnostic-v2.json').read_text(encoding='utf-8'))
entry={'status':'Full support/roll diagnosis completed; rigid contact remains unaccepted','rigidAppearanceWeakFrames':{r['role']:r['weakOrBoundaryFrames'] for r in roll['roles']},'correctedGroundOutline':ground,'visualReview':'Both complete19pose roll overlay boards, both original and corrected ground-outline boards reviewed. Warm-mask correspondence weakens on heel/toe roll. V0near32 catches other boot and narrow single-row baseline overstates footprint excess; not valid source-contact evidence. Connected boot component plus two-row sole envelope corrects it, still limited by shape/occlusion/quantization.','bindings':{str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [S/'boot-roll-diagnostic.json',S/'ground-outline-diagnostic.json',S/'ground-outline-diagnostic-v2.json',S/'audit_boot_roll.py',S/'audit_ground_outline_v2.py']}}
(S/'ROLL_VERDICT.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf-8')
ruler={'status':'Complete alternate global148standing registration; final proportion/contour repair failed','registration':json.loads((D/'source-registration.json').read_text(encoding='utf-8')),'replay':json.loads((D/'replay-record.json').read_text(encoding='utf-8')),'visualReview':'Whole original/prior/alternate first,mid,wrap,end master comparison viewed. Standing height148/floor223 restored, but head27vs26 and upper43..48vs42 plus pale outline remain. Not adopted or advertised as final fidelity. All142poses retained at one common plate254wide317high/scale.3302083333/offset2,-30; no individual rescale/recenter/colour/anatomy edits.'}
(D/'VERDICT.json').write_text(json.dumps(ruler,indent=2)+'\n',encoding='utf-8')
ledger=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
for g in ledger['generations']:
 if g['id']=='448578329612795':g['fullRollReview']=S.name+'/ROLL_VERDICT.json';g['alternateGlobalRuler']=S.name+'/global-standing-ruler-v1/VERDICT.json';break
else:raise AssertionError('Original ledger missing')
(P/'EXECUTIONS.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
title='## Veld full boot-roll evidence and uniform standing ruler — October 3, 2026'
note=title+'''\n\nNative-input source448578329612795 now has independent broader heel/flat/toe
diagnostics: far14..32 and near32..50. Rigid warm-boot rotation/translation fits
preserve role identity more reliably than nearest boot, but10far/8near of38frames
fall belowNCC.8, minima.481/.511. Both complete annotated19pose boards viewed:
heel/toe roll changes appearance enough that weak matches cannot prove rigid
support or its absence. No source/art/root edits, no new native replay needed.

Independent alpha ground outline initially failed as a diagnostic: rectangular
near32 window included other boot and a single bottom row made the flat sole
reference too narrow, overstating11.6px excess. V0 retained INVALID for that claim.
V2 uses connected opaque boot component nearest inspected role and two-row sole
envelope, all38overlays viewed. At presumed2.8sourcepx/frame root, far projected
floor221 constant/max footprint excess2.8px; near221..222/max3.4px. Quantized alpha
extent, component merger/occlusion and changing shape still limit physical claims.
Stable short-window material translation alone cannot certify whole sole/roll.

Alternative global-standing-ruler-v1 corrects common encoded standing density:
ONE plate317px high (254wide),scale.3302083333/offset2,-30 applied identically to
ALL142whole raw frames. Same white alpha extraction1rawpx erosion, no hole fill,
no per-frame rescale/translation/RGB/body patches, original1/3 source preserved.
Both standing ends148/floor223 vs former150/224; head still27vsoriginal26,
upperbody43..48vs42, pale outline remains. Master/prior/new beginning/mid/wrap/end
board reviewed.284exact full142replay checks0/5917ms;308prior native inputs intact.
Alternate source retained as height registration evidence, NOT final head/body/
contour repair or ordinary selector adoption. Native/stride recalibration would
need a separate interval if later selected; prior106.4stride belongs to prior ruler.

Lessons: avoid interpreting weak rigid appearance fit as a contact result. Ground
windows must isolate the actual boot, and curved soles need more than a single
lowest-alpha row; corrected metrics do not make pixels literal physics. One whole
source density correction can restore shared height but cannot repair internal
proportions/material/contours. Next whole-source contour/head/body fidelity and
standing handoffs, full contact/roll validation; original North and complete
action/direction/furniture/controller/save/Continue, final cross-library polish
remain. Full goal active/incomplete, no live generation or normal selectors changed.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.
\n'''
h=P/'HANDOFF.md'
if title not in h.read_text(encoding='utf-8'):
 with h.open('a',encoding='utf-8') as f:f.write('\n'+note)
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(Path(__file__)),'exec'))
print('Broader roll diagnosis and common source-ruler evidence recorded; full goal active.')
