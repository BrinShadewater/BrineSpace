from pathlib import Path
import json, hashlib, shutil, uuid, time
P=Path(__file__).resolve().parent; R=P.parents[1]
S=P/'small-clearance-source-v1'; N=R/'output/veld-east-trailing-key-v1'
entry={'id':'a92ca06b-d33b-48db-81af-c3af120fbed6','folder':S.name,'raw':S.name+'/raw-small-clearance-v1.png','prompt':S.name+'/prompt.txt','status':'Completed; requested forward first lift failed; alternate trailing recovery key provisional','verdict':'Whole source H148/head26/upper42 matches original held; cloth68,67,66 vs66,64,63 slightly lighter. Actual boot lifts backward behind support foot rather than requested forward. Retain actual trailing recovery semantics; near/far anatomical identity, physical support, joining gait and final grade unaccepted. Original whole helmet protects body; paired native appearance reviewed at47/93/148,13checks0/2presentations/engine0.20inputs stable and2931owner files unchanged. No normal adoption.','nativeValidation':json.loads((N/'validation.json').read_text(encoding='utf-8'))}
entry['bindings']={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [S/'raw-small-clearance-v1.png',S/'prompt.txt',S/'source-audit.json',S/'key-record.json',N/'records.json',P/'forward-lift-guide-v1/GUIDE.json']}
(S/'VERDICT.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf-8')
ledger=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
if not any(g['id']==entry['id'] for g in ledger['generations']):ledger['generations'].append(entry)
(P/'EXECUTIONS.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
title='## Veld trailing recovery key and explicit foot guide — October 3, 2026'
note=title+'''\n\nOriginal-only single source a92ca06b-d33b-48db-81af-c3af120fbed6
in small-clearance-source-v1 holds original height148/head26/upperbody42.
One whole-source resample .0737667128, no anatomy/RGB patches. Cloth68,67,66
vs original66,64,63 remains slightly lighter. Requested tiny FAR forward lift
FAILED: actual boot lifts behind the advanced support foot. Alternative trailing
recovery source retained provisionally under its actual motion, not relabelled
as the missing forward first lift. Near/far identity and physical support pending.
Original whole profile helmet protects body; paired native13checks0/2presentations,
4.77s/engine0,20inputs unchanged and2931owner files unchanged under scratch APPDATA.
Both complete47/93/148 master comparison boards reviewed. One320ms diagnostic
key is not a stride, transition/contact acceptance or normal controller adoption.

Next conditioning changes to an explicit original-foot guide. Clean original native
master enlarged whole4x nearest, with a separate annotation copy identifying the
larger near foreground boot as planted and smaller far screen-right boot moving
UP/RIGHT. Both inspected. Annotations are instructions only, no new artwork or
contact proof. Appearance authority remains the original; never let labels or
arrows enter generated art. Judge actual output foot identity/direction rather
than trusting a prompt. Missing first lift, continuous gait/start-stop, North
contacts, full action/direction matrix, furniture/controller/save/Continue and
final library polish remain. Full goal active/incomplete.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.
\n'''
h=P/'HANDOFF.md'
if title not in h.read_text(encoding='utf-8'):
 with h.open('a',encoding='utf-8') as f:f.write('\n'+note)
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(Path(__file__)),'exec'))
print('Actual trailing key and guide recorded; frozen native key record untouched.')
