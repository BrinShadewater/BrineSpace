"""Keep native contact evidence and limitations current without changing art."""
from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'continuous-video-v3-white';N=R/'output/veld-east-phase-probe-v1'
title='## Veld East independently rendered boot review — October 3, 2026'
note='''## Veld East independently rendered boot review — October 3, 2026

Full37-phase native ground chronology inspected from existing actual traveling
captures; no source, manifest, player or new Godot run changed. Added independent
native-pixel boot registration at93/148, uniform/paced, both gears. Raw source
coordinates INITIALIZE templates only; all subsequent matching uses rendered RGB.
Tiny4-6px material patches at93 jump between details (apparent6.86px span), INVALID
as physical sliding measurement. Retained original failed diagnostic and overlays.
Broader masked boot comparison excludes grid/background, both inspected planted
windows:93px spans1.210/0.960 uniform ->0.220/0.443 paced;148px spans2.329/2.093
->0.332/0.673. This supports timing improvement independently of computed source
landmark positions, still a whole-boot translation PROXY rather than rigid sole proof.

Full-ground37-phase board and bare paced93/148/uniform93 +helmet paced93 overlays
reviewed. Template clearly loses intended boot in first push-off raw26..29 at both
sizes (NCC~0.42-0.49); matching rotation/occlusion with a flat boot is invalid.
Later boot touchdown/push-off raw34..48 also rotates; translation cannot certify
heel/toe anchoring. Warm boot-material floor sample stays0-2px above148px grid floor
through all37 poses, not full alpha/sole contact proof. Full contact NOT accepted.

Lesson: native tiny-patch aliasing can look like real sliding. Use readable material
coverage and inspect overlays/confidence; retain failures. Do not treat rotational
point motion or template switches as physical drift. Both flat supports now have
independent rendered evidence; heel/toe rolls and near/far occlusion need a different
rigid-contact measurement. Never patch anatomy or suppress full phases to pass.

Next rotation-aware heel/toe landmarks through touchdown/push-off and overlapping
legs, temporal wrap, exact master held start/stop. Head/skin/hair/suit final fidelity,
North walking contact failure, remaining original action/direction/furniture,
normal controller/save/menu Continue and full library consistency/polish remain.
No ordinary selectors changed, no live paid job. Full goal active/incomplete.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.

'''
for name,review in [('rendered-contact-audit.json','Native148 paced/uniform and93 paced detail overlays reviewed; all37 ground chronology reviewed. Tiny93px templates jump between details, invalid for contact calibration. Extended rotation/occlusion also loses material. No full contact accepted.'),('rendered-boot-audit-v2.json','Broader boot overlays reviewed: bare paced93/148, uniform93, helmet paced93; same body outputs produce identical gear comparisons. Both planted windows show lower apparent translation with paced timing. First push-off26..29 loses flat-boot template visibly; cannot certify rotation/heel-toe contact. No full contact accepted.')]:
    data=json.loads((V/name).read_text(encoding='utf-8'));data['visualReview']=review;(V/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
data=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
data['independentRenderedContactAudit']={'reports':['continuous-video-v3-white/rendered-contact-audit.json','continuous-video-v3-white/rendered-boot-audit-v2.json'],'status':'Flat-window improvement independently supported; full rolling contact unresolved','verdict':'Tiny native93px patches visibly mis-track, preserved invalid diagnostic. Broader boot registered93px spans1.210/0.960 uniform ->0.220/0.443 paced;148px2.329/2.093 ->0.332/0.673. Flat-template first push-off26..29 fails under rotation/occlusion; no full contact, final stride or gait admission.'}
(P/'EXECUTIONS.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
with (P/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('''
## Latest independent rendered contact diagnosis
Added audit_rendered_contacts.py/rendered-contact-audit.json and
audit_rendered_boots_v2.py/rendered-boot-audit-v2.json, existing native captures only.
Full37-phase ground boards inspected. Tiny native93px material patches switch
details; apparent6.86px is INVALID physical drift. Broader masked native boot
registration independently supports paced flat windows:93px1.210/0.960 ->0.220/0.443,
148px2.329/2.093 ->0.332/0.673. Broad overlays inspected bare paced93/148, uniform93,
helmet paced93. First push-off26..29 visibly loses flat template at both scales;
rotation/occlusion is unresolved, not a passing full-foot contact result. Warm boot
material0-2px above148px floor through37 phases is diagnostic, not alpha/sole proof.
Next rotation-aware heel/toe/contact measurements and near/far overlap, complete
temporal wrap and exact master held start/stop. Full goal remains intact/incomplete.
''')
# Verify relevant read-only diagnostics still reference the frozen native interval.
frozen=json.loads((N/'inputs-after.json').read_text(encoding='utf-8'))
changes=[name for name,sha in frozen.items() if hashlib.sha256((R/name).read_bytes()).hexdigest()!=sha]
assert not changes,changes
carry={'frozenInputsUnchanged':True,'frozenInputCount':len(frozen),'scope':'Carry-forward after read-only rendered contact review, no new native run or expanded acceptance.','diagnosticBindings':{str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [V/'audit_rendered_contacts.py',V/'audit_rendered_boots_v2.py',V/'rendered-contact-audit.json',V/'rendered-boot-audit-v2.json',N/'records.json']}}
(V/'rendered-contact-carry-forward.json').write_text(json.dumps(carry,indent=2)+'\n',encoding='utf-8')
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(P/'record_rendered_contact_progress.py'),'exec'))
print(json.dumps({'nativeFrozenInputCount':len(frozen),'changedFrozenInputs':0,'fullContactAccepted':False}))
