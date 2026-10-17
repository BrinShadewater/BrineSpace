from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'first-lift-row-source-v2'
entry={'id':'9d5765c3-b6eb-4bdd-b5ee-72419fcda89c','folder':S.name,'raw':S.name+'/raw-first-lift-v2.png','prompt':S.name+'/prompt.txt','references':['first-lift-row-source-v1/raw-first-lift-v1.png','../veld-east-held-original-master-v1/raw-held-v1.png'],'status':'Completed; rejected requested repair','verdict':'Whole-source row edit stabilizes all6head27vs V1head27-28, all148/floor223/no clipping. Does not narrow torso/case:46-47vs master42. Cloth68-70/67-69/67-68 brighter than V1andmaster. Nearsolecentroid125..128span3 vs V1span2.5; independent broad near-boot material matching dxSpan3 vs2, minNCC.856vs.794. Full before/after/master board and enlarged source reviewed. Wobble worsened despite requested rigid support. Complete rejected row preserved; no helmet/native packaging/adoption.','bindings':{str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [S/'raw-first-lift-v2.png',S/'prompt.txt',S/'source-registration.json',S/'transition-audit.json',S/'repair-comparison.json']}}
(S/'VERDICT.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf-8')
ledger=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
if not any(g['id']==entry['id'] for g in ledger['generations']):ledger['generations'].append(entry)
(P/'EXECUTIONS.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
old=json.loads((R/'output/veld-east-first-lift-row-v1/inputs-after.json').read_text(encoding='utf-8'));assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in old.items())
title='## Veld first-lift row repair rejection — October 3, 2026'
note=title+'''\n\nBuiltin whole-row edit9d5765c3-b6eb-4bdd-b5ee-72419fcda89c targets six-pose V1
with actual original raw-held-v1 as sole appearance reference. Complete source,
exact prompt, one global148ruler/sharedY/gutter extraction and before/after/master
board saved in first-lift-row-source-v2; all six poses reviewed. Head now27 inall6
vs previous27-28, allheight148/floor223/no clipping. Requested torso/case repair
FAILS:46..47vs original42 (before45..47). Cloth68..70/67..69/67..68 vs original
66/64/63 brightens. Nearsolecentroid125..128span3 vs prior2.5. Independent broad
near-boot material registration dxSpan3 vs prior2, minNCC.856vs.794. Stronger match
does not remove wobble or certify rigid physical support. Row repair REJECTED;
no native/helmet packaging or normal adoption. Prior36native inputs unchanged.

Lesson: requested fixes and stable shared floors cannot certify a repaired source.
Compare actual before/after master silhouette/material AND support movement.
Whole-atlas edits can stabilize one metric while worsening another; do not keep
repeating the same row repair. Earlier original-only single near-standing source
matches originalhead26/upperbody42 more closely, so next adjacent tiny first-lift
pose is independently authored from original only, without drifting row guide.
Whole-source generation remains required; no procedural limb/body/head/RGB patches.
Full East gait/start-stop/near-far/contact, North gait, original action-direction,
furniture/controller/save/Continue and final library polish remain. Goal active.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.
\n'''
h=P/'HANDOFF.md'
if title not in h.read_text(encoding='utf-8'):
 with h.open('a',encoding='utf-8') as f:f.write('\n'+note)
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(Path(__file__)),'exec'))
print('Source row repair rejected by master/support comparison; prior36native inputs preserved.')
