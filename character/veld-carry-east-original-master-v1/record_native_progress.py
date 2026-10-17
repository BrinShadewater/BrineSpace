from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'continuous-video-v1'
executions=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
executions['video']['verdict']='Retained motion evidence, not final artwork: direct same-scale master comparison shows suit purple drift introduced by video despite neutral/olive-grey starting key. All raw/extracted frames inspected. Native diagnostic motion passed; full physical contact and original material acceptance unresolved.'
executions['videoGradeTrial']={'taskId':'448379855364450','folder':'continuous-video-v2','status':'Submitted','change':'Same byte-identical master input and motion prompt; added explicit original neutral/olive-grey cloth grade preservation only. One scoped trial; no automatic paid retry.'}
executions['nativeMotionProbe']={'failedInterval':'output/veld-east-original-motion-probe-v1','failedReason':'Boundary-clock sampling skipped source slots;2275 checks64 frame-coverage failures. Source/player unmodified.','correctedInterval':'output/veld-east-original-motion-probe-v2','checks':2299,'failures':0,'presentations':396,'inputs':75,'ownerFilesUnchanged':2931,'scope':'All32 source slots/both gears/three diagnostic strides/47,93,148px actual distance-driven player. No accepted stride, complete rigid contacts, start/stop or normal controller integration.'}
(P/'EXECUTIONS.json').write_text(json.dumps(executions,indent=2)+'\n',encoding='utf-8')
review=json.loads((V/'native-motion-review.json').read_text(encoding='utf-8'))
review['visualReview']={'inspected':'All six native stride/gear chronological boards and live browser shorter/middle/longer controls; walking source/held master at same scale.','finding':'Travel/gear fit coherent at47/93/148. Master comparison identifies video-introduced purple cloth drift; final material fidelity fails. Sparse captures cannot establish full temporal contact.','browserURL':'http://127.0.0.1:8791/character/veld-carry-east-original-master-v1/continuous-video-v1/?v=native-travel-study-v1','screenshot':'browser-travel-review.png'}
(V/'native-motion-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
frozen=json.loads((R/'output/veld-east-original-motion-probe-v2/inputs-after.json').read_text(encoding='utf-8'))
changes=[name for name,value in frozen.items() if hashlib.sha256((R/name).read_bytes()).hexdigest()!=value]
assert not changes,changes
(V/'native-input-carry-forward.json').write_text(json.dumps({'checkedInputs':len(frozen),'unchanged':True,'scope':'Frozen75 inputs from corrected native interval remain exact after review/documentation.'},indent=2)+'\n',encoding='utf-8')
note='''## Veld original East traveling gait diagnosis — October 3, 2026

character/veld-carry-east-original-master-v1/continuous-video-v1 has a paired32-frame
source study exercised by actual distance-driven crew_sprite_player at47/93/148,
three diagnostic strides96.53/100.13/103.73 source pixels, two cycles each gear.
Corrected midpoint fixture:2299checks0/396presentations/11.89s;75inputs and all2931
owner non-log files unchanged under scratch APPDATA. Boundary-sampled first fixture
missed frame slots:2275checks64failures retained separately; no art/player changes.
All six native gear/stride boards inspected. Sparse native travel replay and browser
master comparison delivered; no complete rigid contact or normal integration proof.

Early flat-support toe-outline proxy drift0.48-1.23px at93px across the tested distances
is encouraging but covers only two five-frame windows, not heel/toe roll or every
near/far support. No final stride selected.32-frame similarity alone is insufficient.
Direct five-figure same-scale comparison catches video-induced PURPLE cloth drift:
starting V2 key/original-held/true original empty are neutral/olive-grey, video is plum.
Stability within a clip does not establish colour fidelity to its reference.
V1 retained as motion evidence, not final artwork. Scoped grade-preservation trial
448379855364450 submitted to continuous-video-v2 using byte-identical original input,
same motion wording plus explicit neutral/olive-grey cloth/no-purple instructions.
EstimatedUSD0.19; billing unverified; exclusive ledger and no automatic paid retry.

Lessons: sample authored duration midpoints to exercise every pose; equal clock bins
can land on unequal-duration boundaries. Verify physical contact independently of
player phase. Compare the video directly with its unchanged source AND original
masters; a stable purple grade can pass all temporal/pixel checks and still be wrong.
Next review entire grade trial, both-foot material landmarks/loop, final stride,
authored start/stop and held handoffs; North contact repair, full original action/
direction matrix, ordinary controller/save integration and library polish remain.
Full objective active/incomplete. Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.

'''
template=(P/'record_milestone.py').read_text(encoding='utf-8');start=template.index('title=');end=template.index('paths=[')
script=template[:start]+'title='+repr(note.splitlines()[0])+'\nnote='+repr(note)+'\n'+template[end:]
(P/'record_native_milestone.py').write_text(script,encoding='utf-8')
exec(compile(script,str(P/'record_native_milestone.py'),'exec'),{'__file__':str(P/'record_native_milestone.py')})
with (P/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('''
## Native traveling diagnosis and grade issue

Corrected midpoint fixture/output v2:2299checks0,396presentations,75 frozen inputs,
2931 owner files unchanged. Initial boundary-sampled fixture/output v1 failed64
coverage checks and remains preserved. All three strides/both-gear native boards
reviewed; browser tab51 provides sparse engine travel plus original held comparison.
Early toe-outline windows are encouraging0.48-1.23px drift at93px, not full contacts.
Same-scale-master-grade-review.png identifies purple cloth introduced by video,
not the neutral/olive-grey starting key. V1 is motion evidence, not final art.
Grade-preservation trial448379855364450 submitted in continuous-video-v2 with same
input/motion and explicit no-purple/reference-colour wording. Reconcile/poll this
same task; no blind paid retry. Inspect all raw frames before any candidate admission.
Then complete physical contacts/loop, stride/start/stop/held handoffs and full scope.
''')
print('Native evidence, grade failure, scoped submission and five maintained references recorded;75 frozen inputs unchanged.')
