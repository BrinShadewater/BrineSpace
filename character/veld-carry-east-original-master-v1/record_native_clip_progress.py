from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'standing-step-video-v2-native';N=R/'output/veld-east-native-input-source-v1'
g=json.loads((S/'generation.json').read_text(encoding='utf-8'));assert g['status'].lower()=='success'
entry={'id':g['task_id'],'folder':S.name,'status':'Success; provisional complete dense motion study, final master/contact unaccepted','estimatedUSD':g['estimatedUSD'],'billingVerified':False,'raw':S.name+'/source.mp4','prompt':S.name+'/prompt.txt','verdict':'Native original3x input holds fixed headAxis123 throughout142frames vs earlier41.5px excursion. Head27vs26, upper43..48vs42, height143..150/floor221..224; start/endstanding150vs148. Repeated alternating steps exceed requested2; pale contour and torso/case/endpoint drift remain. Cloth64..70.5/60..68/60..68 vs66/64/63 materially closer than earlier midclip darkening. Complete source retained; no per-frame position/density/RGB rescue. All6raw/6alpha/master endpoint and6native chronology boards viewed. Paired original whole shell preserves all142bodies;710sourcechecks0. Native577checks0/284presentations/10.32s/engine0/301stable2931owner unchanged.568native exact replay checks0. No rigid near/far support, accepted stride/start-stop, normal controller/save adoption.','nativeValidation':json.loads((N/'validation.json').read_text(encoding='utf-8'))}
entry['bindings']={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [S/'source.mp4',S/'prompt.txt',S/'input-record.json',S/'master-audit.json',S/'full-source-record.json',S/'native-review.json',S/'index.html',N/'records.json']}
(S/'VERDICT.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf-8')
ledger=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
for i,x in enumerate(ledger['generations']):
 if x['id']==entry['id']:ledger['generations'][i]=entry;break
else:ledger['generations'].append(entry)
(P/'EXECUTIONS.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
title='## Veld native-input continuous motion study — October 3, 2026'
note=title+'''\n\nDirect Hailuo02 task448578329612795 terminalSuccess,142frames24FPS/5917ms
in standing-step-video-v2-native. EstimatedUSD0.28/billing unverified, no live job
or blind retry. Exact actual original native source3x nearest input has a byte-exact
inverse reference; identical first/last endpoints. ONE frozen scale1/3,offset0,-32,
returned768x960 verified before alpha mapping. Whole RGB untouched before resample;
white alpha extraction1rawpx erosion, no hole fill/per-frame recenter/density repair.
All6raw/all6alpha chronology boards and full master/endpoint head/body board viewed.

Important progress: headAxis123 remains fixed across ALL142 vs earlier high-resolution
input trial41.5px excursion. Head27 throughout vs original26. Actual continuous
alternating repeated steps exceed requested2. Body143..150/floor221..224; standing
endpoints150vs original148, upperbody43..48vs42. Cloth diagnostic64..70.5/60..68/60..68
vs original66/64/63; much closer than prior severe middle darkening, still not final
grade. Pale source contour, case/torso widths, initial standing-to-stride jump and
near/far support identity/contact remain. Do not confuse shared head position or
valid source clock with physical planted soles, correct start/stop or final artwork.

Complete142-pose source paired with original whole profile shell,142bodies protected
byte-exact;710sourcechecks0. Actual native source-clock577checks0/284three-scale
presentations,10.32s/engine0;301inputs unchanged/2931owner files unchanged under
scratch APPDATA.568exact native replay pixel/duration checks0; all6native chronology
boards and paired full47/93/148 raw36 views inspected. Static local paired complete
replay/master page clearly marks study only. No normal selectors or controller
adoption, accepted gait loop/stride/support/start-stop/Save/Continue claim.

Lesson: pixel-dense native master conditioning can constrain identity/path more
effectively than high-resolution source while introducing pale edges and changing
dimensions. Preserve a whole input-frozen ruler and inspect EVERY phase, both
endpoint silhouettes, materials and actual supports. Next independent bilateral
contact/physical root calibration and dense start/stop, source contour/proportion
repair without anatomy/RGB patches; original North gait and full action-direction,
furniture/controller/save/Continue and whole-library polish remain. Full goal active.
Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.
\n'''
h=P/'HANDOFF.md'
if title not in h.read_text(encoding='utf-8'):
 with h.open('a',encoding='utf-8') as f:f.write('\n'+note)
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(Path(__file__)),'exec'))
print('Complete native-input motion evidence recorded; full goal remains active.')
