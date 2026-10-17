from pathlib import Path
import json,hashlib,uuid,os
P=Path(__file__).resolve().parent;R=P.parents[1]
n=json.loads((P/'validate-evidence.json').read_text());w=json.loads((P/'validate-validation.json').read_text());v=json.loads((P/'packaging-validation.json').read_text())
assert n['failures']==0 and len(n['records'])==36 and not v['failures'] and w['exitCode']==0 and not w['timedOut']
status='installed_native_source_verified_owner_review_pending'
for mode in ['bare','helmet']:
    file=P/(mode+'-manifest.json');m=json.loads(file.read_text());m['status']=status;file.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
(P/'selection.json').write_text(json.dumps({'status':status,'runtimeInstalled':True,'fullSetComplete':False,'tool':'built-in imagegen','source':'source-v2.png','sourceOriginal':'C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-3ef6b782-31b7-43c7-8488-696b337ca776.png','prompt':'prompt-v2.txt','sourceSha256':hashlib.sha256((P/'source-v2.png').read_bytes()).hexdigest(),'sourceReferences':36,'statesPerMode':3,'fixedBodyScale':.5285714285714286,'fixedHelmetScale':.4430379746835443,'packageChecks':v['checks'],'nativeChecks':n['checks'],'nativeCaptures':36,'nativeFailures':0,'profileGuard':{'realProfileUnchanged':w['realProfileUnchanged'],'profileDelta':w['profileDelta']},'visualReview':'Original/new full source, fixed-ruler master/old/new head comparison, all36 paired source poses and all36 native prescribed-stage captures reviewed. More compact master-relative face; upward pitch and belt tool ownership retained.','nativeScope':json.loads((P/'scope-correction.json').read_text())['correctedScope'],'remaining':['Owner full-motion review','South reclining identity/pillow head-pitch repair; candidates rejected, exact-neutral Hailuo attempt447818168017344 submitted','Continuous/native actual task/gear/furniture/travel joins across complete James library']},indent=2)+'\n',encoding='utf-8')
note='''

## James West reclining identity and South source review — October 1, 2026

West james-rest-west-identity-v2/source-v2.png,prompt-v2.txt (built-in imagegen)
selected after ordinary rest materials; paired3states/36refs. Compact leaning
face replaces fuller source face; fixed.5285714286 body/.4430379747 common-shell
rulers, exact standing masters/neutral/reverse joins, unchanged3600ms sleep.
147package/225native checks0fail; all36 normal loaded source slots through
prescribed NPC life stages captured and reviewed at game scale, plus whole
paired source/master/head boards. Engine0/no timeout; strict real profile guard
true/no delta. No natural berth/Continue/locker claim. Copied fixture explanatory
West-bunk label corrected to East in scope-correction.json; original passed
evidence retained, source checks unaffected. Four metadata/ruler templates frozen.

South identity-v2 lying candidate compact heads reviewed but remains unselected:
two sheet edits retain front-facing sleeping heads instead of final upward tilt.
Isolated whole-neutral sleepv4/v5 fixes pitch but changes body projection. One
fixed neutral sole-gap ruler yields100..101px height/85..88width versus92/106
neutral; reject, never per-frame fit. Initial across-chest tool diagnosis was too
strong; closer review puts it at waist/thigh, scale concern distinct from pose.
Candidates/prompts/hashes/ruler evidence retained. Exact registered candidate
neutral4x green input now drives one direct Hailuo breathing attempt in
james-rest-south-sleep-source-v6,task447818168017344,estimatedUS$0.19,not verified
billing. Submission is not source acceptance; poll authoritative task before
replacement and inspect all raw motion. Full James goal active.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=path.read_bytes()
    if b'## James West reclining identity and South source review' in data:continue
    enc=note.encode('utf-8');new=enc.lstrip(b'\n')+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+enc;temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);os.replace(temp,path)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: West rest identity/South review

## Objective and acceptance
Full James library/master/style/perspective/scale/material consistency then
cross-family polish. Full goal active; West installed/source-native verified,
owner acceptance separate. South pending.

## Accepted decisions and constraints
Whole-source compact heads and supported pitch, fixed rulers, belt wrench,
shared accepted shell, exact masters/joins,3600ms sleep. Never normalize each pose.

## Current state
West paired3states36refs selected after material override in grid_canvas and
ACTIVE_ASSETS. source-v2.png/prompt-v2.txt built-in imagegen; four frozen original
metadata templates. Native fixture/.uid,36captures and source/native boards.
South identity-v2 candidate unselected; v2/v3 bad sleeping pitch,v4/v5 isolated
breathing changes projection. Evidence/prompts preserved; accurate tool scope
corrects earlier across-chest description. Exact neutral Hailuo v6 task
447818168017344 submitted; check provider ledger/status, never blind resubmit.

## Verification
West147package/225native0fail,36prescribed-stage NPC renderer captures reviewed
and source boards. Engine0/no timeout; scratch APPDATA,owner profile unchanged.
No natural furniture/Continue/gear journey; ordinary berthNorth,special bunkEast.
Copied explanatory scope label fixed separately, original evidence retained.
South one-ruler projected geometry differs from neutral, no installation.

## Next action
Poll/review full Hailuo v6 source, stable identity/head/pillow/camera/grade/boots/
belt; preserve raw source and complete motion. Pair/package/native only if it
fixes the demonstrated defect. Continue remaining source/native/context joins.
''',encoding='utf-8')
print(json.dumps({'status':status,'packageChecks':v['checks'],'nativeChecks':n['checks'],'realProfileUnchanged':w['realProfileUnchanged']}))
