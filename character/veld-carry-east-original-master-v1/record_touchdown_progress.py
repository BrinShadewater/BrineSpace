"""Persist projected-contact lesson and bounded native appearance evidence."""
from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'touchdown-source-v2';N=R/'output/veld-east-touchdown-key-v2'
entry={'id':'19601e31-7374-4d66-9319-672beace3802','folder':S.name,'raw':S.name+'/raw-touchdown-v2.png','prompt':S.name+'/prompt.txt','references':['../veld-east-held-original-master-v1/raw-held-v1.png'],'status':'Completed; provisional projected heel-contact key','verdict':'Full original-only pose148/head27/near floor223/distal far boot220, original projected far floor220. Far heel low/toe raised, visibly distinct from airborne v1. Native bare/helmet47/93/148 reviewed; upperbody47vs42 and neutral cloth71,70,69vs66,64,63 remain final fidelity deviations. No calibrated physical contact/moving root/full transition/controller acceptance.','nativeValidation':json.loads((N/'validation.json').read_text(encoding='utf-8')),'initialRunnerSetup':'First invocation omitted required engine argument and exited before Godot launch. Corrected invocation was sole actual native interval, passed under scratch APPDATA.','bindings':{str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [S/'raw-touchdown-v2.png',S/'prompt.txt',S/'source-audit.json',S/'key-record.json',P/'projected-contact-source-review.json',N/'records.json',N/'bare-000-native.png',N/'helmet-000-native.png']}}
(S/'VERDICT.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf-8')
ledger=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
if not any(g['id']==entry['id'] for g in ledger['generations']):ledger['generations'].append(entry)
(P/'EXECUTIONS.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
title='## Veld East projected heel-contact key — October 3, 2026'
note=title+'''\n\nOriginal-only whole source19601e31-7374-4d66-9319-672beace3802 saved with exact
prompt/raw/audit under touchdown-source-v2. Body148/head27/no clipping; whole
original shell107,66 protects body byte-exact,3sourcechecks0. Native13checks0,
2paired presentations at47/93/148 reviewed,20inputs stable/2931owner files unchanged,
engine0/4.84s/scratch APPDATA. First runner invocation lacked engine argument and
exited before game launch; corrected sole native interval passed.

Master-perspective correction: original near boot projects to223 and far boot220.
Therefore identical horizontal screen floors are NOT the canonical contact rule.
Same-scale boot board and alpha extent confirm V1far217 versus original220;
new V2far220, near223, heel low/toe raised. Retain as PROVISIONAL projected heel-
contact key, not proof of physical support or actual moving root. Distal opaque
extent is not a calibrated heel landmark. No anatomical/grade patches applied.
Whole source head27 fits original26-27, but upperbody47vs42 and cloth71,70,69vs
66,64,63 remain final fidelity deviations. Native appearance pass cannot erase them.

Lesson: use master camera/depth to judge ground projection, not one screen-height
line for both feet. Separate near/far boot identity, projected contact, physical
root travel and appearance acceptance. Removing lifted-pose guide improved phase
distinctness; prompt still requests same-floor geometry, which future authoring
must replace with perspective-consistent far-floor constraint. Earlier two source
rejects remain; no frozen source/native records or normal selections changed.
Next chain representative original held/lift/contact poses, refine full master
proportions/materials, author missing prelift/recovery and prove moving contacts/
complete start-stop. North gait, full original action-direction/furniture/ordinary
controller/save/Continue and final cross-library polish remain. Goal active/incomplete.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.
\n'''
h=P/'HANDOFF.md'
if title not in h.read_text(encoding='utf-8'):
 with h.open('a',encoding='utf-8') as f:f.write('\n'+note)
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(Path(__file__)),'exec'))
print('Provisional projected heel-contact source/native review and perspective lesson recorded.')
