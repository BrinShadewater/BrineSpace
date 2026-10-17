from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'prelift-source-v2';N=R/'output/veld-east-initial-step-v2'
entry={'id':'4cedbbc8-4090-4fc5-bad3-9ce05271f0ae','folder':S.name,'raw':S.name+'/raw-prelift-v2.png','prompt':S.name+'/prompt.txt','references':['../veld-east-held-original-master-v1/raw-held-v1.png'],'status':'Completed; provisional near-standing initial clearance key','verdict':'Original-only minimal whole-pose source148/head26/upperbody42 matches original held148/26/42. Near opaque floor band122..130 vs held120..131, centroid126vs125.5; far distal floor219 vs original220. Output reads tiny whole-foot clearance, not confirmed requested toe-contact heel peel. Cloth71,69,68 vs66,64,63 lighter. Master/source and native both gear47/93/148 visually reviewed. Retain provisional source; no complete transition/physical-contact/final-grade acceptance.','nativeValidation':json.loads((N/'validation.json').read_text(encoding='utf-8')),'bindings':{str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [S/'raw-prelift-v2.png',S/'prompt.txt',S/'source-audit.json',S/'key-record.json',N/'records.json',N/'bare-000-native.png',N/'helmet-000-native.png']}}
(S/'VERDICT.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf-8')
ledger=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
if not any(g['id']==entry['id'] for g in ledger['generations']):ledger['generations'].append(entry)
(P/'EXECUTIONS.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
title='## Veld East near-standing initial-step source — October 3, 2026'
note=title+'''\n\nOriginal-only source4cedbbc8-4090-4fc5-bad3-9ce05271f0ae saved exact prompt/raw/
audit in prelift-source-v2 after sparse-chain moving-root diagnosis. Full source
and master/enlarged head/legs viewed. ONE global148ruler, head26/upperbody42 match
original held26/42, no clipping. Near opaque floor band122..130 vs held120..131,
centroid126vs125.5; far distal219 vs master220. Legs remain close and source is
visibly earlier than retained lifted-foot key. Actual pose is tiny whole-foot
clearance, not confirmed requested toe-contact heel peel; record actual semantics.
Cloth median71,69,68 vs66,64,63 remains lighter, final material/identity acceptance
pending. Preserve raw source; no procedural RGB/anatomy/source-region repairs.

Original profile helmet108,66, protected body byte-exact;3sourcechecks0. Native
13checks0/2three-scale paired presentations reviewed,20inputs stable/2931owner files
unchanged/engine0/4.93s/scratch APPDATA. One finite320ms appearance review only;
does not verify this new key in the moving chain or fix earlier4px planted-boot
jump. Earlier three-key diagnostic/manifests/native/source inputs remain frozen.

Lesson: original-only minimal-pose conditioning better retains standing master
head/torso proportions than an advanced lift guide, but material grade and exact
toe-contact semantics still require separate review. Near-standing resemblance
does not establish gait continuity. Next four-key chain with dense faithful
intermediates, full upper-body/material matching, actual root/contact/start-stop
proof; East full cycle/near-far identity, North gait, full original action-direction,
furniture/ordinary controller/save/Continue and cross-library polish remain.
Full goal active/incomplete. No live generation; normal selectors untouched.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.
\n'''
h=P/'HANDOFF.md'
if title not in h.read_text(encoding='utf-8'):
 with h.open('a',encoding='utf-8') as f:f.write('\n'+note)
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(Path(__file__)),'exec'))
print('Initial clearance source and native appearance recorded; full transition and library goal remain incomplete.')
