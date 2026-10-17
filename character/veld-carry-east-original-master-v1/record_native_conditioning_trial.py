from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'guided-heel-peel-source-v1';V=P/'standing-step-video-v2-native'
entry={'id':'80491d7e-c5e0-436c-99d7-e719b33230c2','folder':S.name,'raw':S.name+'/raw-heel-peel-v1.png','prompt':S.name+'/prompt.txt','status':'Completed; rejected requested toe-down heel-peel source','verdict':'Separate original near/far/toe/heel annotations do not establish requested motion. Whole148/head27/upper44 vs original148/26/42; cloth68,66,65 vs66,64,63. Actual far foot shifts forward, heel remains insufficiently distinct; requested fixed toe/heel peel not proven. Complete source/master head/leg comparison viewed; no helmet/native packaging or normal adoption.'}
entry['bindings']={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [S/'raw-heel-peel-v1.png',S/'prompt.txt',S/'source-audit.json',P/'heel-peel-guide-v1/GUIDE.json']}
(S/'VERDICT.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf-8')
g=json.loads((V/'generation.json').read_text(encoding='utf-8'))
video={'id':g['task_id'],'folder':V.name,'status':g['status'],'estimatedUSD':g['estimatedUSD'],'billingVerified':False,'conditioning':'Exact current original native sprite3x nearest on white768x960 plate, same image both endpoints. Distinct input from previous high-resolution raw source. Whole inverse3x reference byte-exact original; fixed scale1/3 and offset0,-32. Full continuous two-step/start-stop target, no per-frame re-registration/density/colour rescue.','prompt':V.name+'/prompt.txt','inputRecord':V.name+'/input-record.json'}
ledger=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
for item in [entry,video]:
 if not any(x['id']==item['id'] for x in ledger['generations']):ledger['generations'].append(item)
(P/'EXECUTIONS.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
title='## Veld heel-peel rejection and native-source continuous trial — October 3, 2026'
note=title+'''\n\nGuided heel-peel builtin80491d7e-c5e0-436c-99d7-e719b33230c2 retained
complete in guided-heel-peel-source-v1 with exact prompt and original/annotation
reference provenance. Whole148/head27/upper44 vs original148/26/42, cloth68,66,65
vs66,64,63. Source/master head/leg board inspected. Requested toe-fixed heel-peel
not established: far boot advances, heel articulation insufficiently distinct.
REJECTED requested transition; no helmet/native or normal adoption. No procedural
anatomy/body RGB edits. New original guide does not itself certify contact.

Changed dense-motion conditioning submitted as direct Hailuo02 task448578329612795
in standing-step-video-v2-native, last poll Processing. EstimatedUSD0.28, actual
billing unverified; exclusive generation ledger, no blind paid retry. Input is
ACTUAL ORIGINAL NATIVE master3x nearest, not earlier high-resolution raw or a
regenerated key: source SHA6e120106..., white768x960 plate,96px vertical margin.
Whole inverse3x crops only empty margin and is byte-exact original RGBA. Both
endpoints identical inputSHAbabc0cb0...; input comparison viewed. Source-fixed
scale1/3, native256x320,offset0,-32; extraction guards exact returned video dimensions
before mapping. Requested full two small alternating in-place steps, authored
heel/toe progression and standing start/end. Full clip must establish actual path,
near/far support, master proportions/materials before any admission. No ordinary
selectors changed. Goal active/incomplete; all full action/direction/contact,
furniture/controller/save/Continue and final library polish requirements retained.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.
\n'''
h=P/'HANDOFF.md'
if title not in h.read_text(encoding='utf-8'):
 with h.open('a',encoding='utf-8') as f:f.write('\n'+note)
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(Path(__file__)),'exec'))
print('Rejected heel key and live changed-conditioning full motion trial recorded.')
