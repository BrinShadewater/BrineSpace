from pathlib import Path
import json,hashlib,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'standing-step-video-v1'
generation=json.loads((S/'generation.json').read_text(encoding='utf-8'));assert generation['status']=='Success'
audit=json.loads((S/'master-audit.json').read_text(encoding='utf-8'))
entry={'id':generation['task_id'],'provider':'MiniMax direct','folder':S.name,'status':'Success; rejected final in-place/master motion','model':generation['params']['model'],'estimatedUSD':generation['estimatedUSD'],'billingVerified':False,'raw':S.name+'/source.mp4','prompt':S.name+'/prompt.txt','references':['../veld-east-held-original-master-v1/raw-held-v1.png'],'verdict':'Identical original first/last conditioned source produces142frames. End silhouette IoU.9937/.9943 but axis123.5..165, floor219..223/body141..148/head25..27; source darkening, body/case-angle drift, excess steps, late return left. Cannot adopt as in-place start/stop. No per-frame re-centering/RGB/body fixes or clipped half-cycle salvage. Full raw142 and extracted142 review boards inspected;284exact finite replay checks0.','masterAudit':audit,'bindings':{str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [S/'source.mp4',S/'master-input.png',S/'prompt.txt',S/'input-record.json',S/'source-registration.json',S/'master-audit.json',S/'replay-review.json',R/'character/veld-east-held-original-master-v1/REFERENCE_STATUS.json']}}
(S/'VERDICT.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf-8')
ledger=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
if not any(g['id']==entry['id'] for g in ledger['generations']):ledger['generations'].append(entry)
(P/'EXECUTIONS.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
title='## Veld original-source authority and dense endpoint trial — October 3, 2026'
note=title+'''\n\nCaught stale whole-held-pose-reference before paid submission: same148ruler head30
vs selected original held26. Rejected input-v0 review retained; new REFERENCE_STATUS
in original held folder names actual raw-held-v1 as appearance authority, stale
supporting source retained for historical frozen bindings. Rebuilt complete raw
figure on white768x1024plate, whole source resample only; fixed reference148/head26,
upperbody43vs42, cloth65,64,63vs66,64,63. Same exact inputSHAea9553dc... both ends.
No frozen old source/package/native bindings or ordinary selections changed.

Scoped MiniMax-Hailuo-02 first/last task448569058312574 terminalSuccess;6s768P,
published estimatedUSD0.28 rechecked official pricing Oct3, billing unverified.
Exact prompt/input/source/ledger preserved, no blind paid retry or live job.
142frames at24FPS/5917ms. All6raw and6fixed-alpha chronology boards plus whole
master/endpoints/enlarged head/body reviewed. ONE plate ruler .2080078125/offset63,47
for entire clip, no per-frame position/density or body RGB edits.284exact finite
source replay pixel/duration checks0; source review only, no native test/adoption.

Endpoints close (silhouetteIoU.9937/.9943, RGBMAE4.40/4.79) do NOT preserve path.
Middle head axis123.5..165 =41.5nativepx excursion despite in-place prompt;
body141..148/head25..27/floor219..223, excess steps, body/case angle and materials
drift, late return left to original. REJECTED final in-place/master motion. Do not
hide with frame re-centering, head/body edits, shortened loops or endpoint swaps.
Initial fixed viewport clothROI became empty when figure moved; reportv0 retained
INVALID for materials. Diagnostic-only ROI now follows head axis/top at constant
master offsets, no pixels altered. Cloth samples67,65,65 atstart,46,45,45 at110,
67,65,65 at end vs input65,64,63; correspondence/occlusion affect material proxy,
visual middle comparison independently shows source drift. Not full palette proof.

Lessons: validate source ROLE/provenance and native proportions before generation;
plausible filenames can bind rejected older artwork. First/last conditioning can
recover endpoints while intermediate motion still fails registration/identity.
Measure whole path and all-frame materials. A fixed screen ROI cannot follow a
moving material, and empty samples are invalid evidence. Existing neutral V3 gait
and original-source keys remain provisional; next controlled small transition
source and original-faithful dense joins/contact validation, not another blind
six-second walking retake. East full gait/start-stop, North contact repair/full
original action-direction/furniture/controller/save/Continue/library polish remain.
Goal active/incomplete. Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.
\n'''
h=P/'HANDOFF.md'
if title not in h.read_text(encoding='utf-8'):
 with h.open('a',encoding='utf-8') as f:f.write('\n'+note)
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(Path(__file__)),'exec'))
print('Source authority correction and dense motion rejection recorded; full objective active.')
