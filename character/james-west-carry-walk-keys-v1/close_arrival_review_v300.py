from pathlib import Path
import json,hashlib,base64,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-turn-chronology-v300';source=p/'arrival-turn-pose3-v299';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((source/'inputs.json').read_bytes());assert sha(source/'prompt.txt')==d['promptSha256'];assert sha(r/d['sourceFile'])==d['sourceSha256'];assert all(sha(r/f)==h for f,h in d['referenceSha256'].items())
(source/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='99b3f6c7-a3f3-45a0-a460-9b68861b8c26',method='builtin_imagegen_single_original_pose_target',rawSha256=sha(source/'raw.png'),prompt='prompt.txt',disposition='provisional_middle_orientation_and_material_revision'),indent=2)+'\n')
(source/'review.json').write_text(json.dumps(dict(rawVisuallyReviewed=True,sourceBoardReviewed=True,geometry=json.loads((source/'registration-diagnostic.json').read_bytes()),findings=['Original148high/crown77/sole224; new149/crown76/sole224. Same horizontal extents, no body-fit or translation.', 'Mostly rear-directed head and restrained material closer to neighboring296 than brighter290; original-master identity/grade/anatomy and equipment joins not fully accepted. Whole silhouette/detail can still change.'],selected=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
v=json.loads((o/'native_probe-validation.json').read_bytes());n=json.loads((o/'native-evidence.json').read_bytes());f=json.loads((o/'native-inputs.json').read_bytes());inp=json.loads((o/'inputs.json').read_bytes());b=json.loads((o/'browser-inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(57,0,6);assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta'];assert all(sha(r/x)==h for x,h in f['preLaunchSha256'].items());assert all(sha(r/x['file'])==x['sha256'] for x in inp['sources']);assert sha(o/'playback-review.html')==b['htmlSha256']
html=(o/'playback-review.html').read_text();arrays=json.loads(html.split('const sources=',1)[1].split(', clocks=',1)[0]);m=json.loads((o/'bare-review-manifest.json').read_bytes());embedded=0
for state in m['states']:
 for url,path in zip(arrays[state['id']],state['frameFiles']):assert base64.b64decode(url.split(',',1)[1])==(r/path[6:]).read_bytes();embedded+=1
assert embedded==13
browser=dict(tabId='2',url='http://127.0.0.1:8877/playback-review.html',serverSession=82639,quarterSpeedObserved=['Phase0 playing','Phase5 paused after finite replay','Phase3 playing after loop replay'],normalSpeedObserved=['Phase2 playing','Phase5 playing; following screenshot crossed loop seam to Phase0'],screenshots=['browser-slow-review.png','browser-normal-review.png'],continuousEveryFrameMotionAcceptance=False,exactEmbeddedSources=13,htmlSha256=b['htmlSha256'],markedDeliverable=True)
(o/'browser-review.json').write_text(json.dumps(browser,indent=2)+'\n')
report=dict(disposition='provisional_bare_turn_middle_repair',nativeChecks=57,nativeFailures=0,nativeBoardsReviewed=6,sourceAndEquipmentBoardsReviewed=True,decodedFramesExact=6,clockTotalMs=800,browser=browser,selected=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=['299 replaces brighter face-exposed290 middle, improving mostly rear-facing orientation and restrained material relative to296.', 'Old0/1/5 retained,297 early150high/sole225 still1px low. Early1/2 project similarly then turn3 introduces larger angle change. Case/head/hardware/material change across joins; no measured degree acceptance.', 'Latest49 carry and north-unload endpoints remain distinct; shared helmet and original-master full anatomy/grade not accepted. Actual arrival/controller/stance/save lifecycle not covered.'])
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();j=json.loads(old);j['arrivalTurnChronologyReview']=dict(version=300,file=(o/'review.json').relative_to(r).as_posix(),sources=[296,297,299],retainedOldPhases=[0,1,5],selected=False,sourceAcceptance=False,normalChanged=False);j['nextVisualRepair']='300 middle299 reduces290 brightness/head-yaw jump. Author distinct early intermediate instead of near-repeat1/2; establish exact latest49 carry to stationary turn start and turn end to north-unload joins. Preserve original master head/body/grade/hardware and stance;297 sole1pixel low. Shared helmet, actual arrival/controller/normal lifecycle and all-family polish remain.';assert ledger.read_bytes()==old;ledger.write_text(json.dumps(j,indent=2)+'\n')
section='''### James middle turn source and live chronology review - October3,2026

V299 builtin single original turn3 pose target refines restrained matte cloth/head
orientation without master-reference pose override.149high/crown76/sole224 versus
original148/77/224; same horizontal extents. Raw and whole-source original/299/290
board inspected.299 reduces brighter290 middle and keeps mostly rear-directed head,
more coherent with296 late angle. Whole generated anatomy/equipment/material still
provisional; no body-fit, pose translation, recoloring or per-part artwork patching.

V300 complete six bare chronology old0/1/5+297/299/296, original800ms clocks.
57nativechecks0/6four-size phase captures all viewed; scratch owner unchanged,
frozen runtime/manifest/source hashes stable. Six decoded APNGframes exact. Browser
page embeds13source images byte-exact. Live quarter replay0playing to5paused;
looped3playing; normal2playing then5playing, screenshot crossed loop seam to0.
Saved full-page slow/normal screenshots, both rows/four sizes visible after reducing
preview empty spacing. These samples prove advancing playback, NOT continuously
watched every-frame cadence or actual gameplay/physical support acceptance.

Remaining visible early1/2 angle repetition then larger jump into3.297sole1px low;
case/head/hardware/boot details still vary. Exact latest49carry/stationary-turn and
north-unload joins absent; old0/1/5 retained openly. Shared helmet, original-master
anatomy/grade, actual arrival/controller/save/Continue and full-library polish pending.
Normal bank unchanged. Full goal active/incomplete.

Lesson: preserve orientation/material together using the original pose target;
retain whole-source/native chronology and live playback samples as distinct evidence.
Stable heights and native checks cannot certify smooth yaw spacing or endpoint joins.
Do not label a looping sampled browser review as continuous game-motion acceptance.
Handoff: character/james-west-carry-walk-keys-v1/arrival-turn-chronology-v300/HANDOFF.md.
'''
guides=record_guides(r,section,'### James full arrival-turn chronology exposes yaw collapse')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James turn middle repair

## Objective and acceptance
Complete master-matched James set, normal gameplay/lifecycle, full-family polish.

## Accepted decisions and constraints
Original matte/yellow/proportions/perspective. Wrench on belt, case in hands.
No fitting, RGB regrading or per-part painting to hide source drift.

## Current state and changed files
New299 raw/frozen original3 target/exact prompt/global256source/receipt/review.
New300 six-source chronology/APNG/native manifest/probe+UID/six captures/HTML/browser
screenshots/review. Material ledger updated; status/pipeline/bible/both skill copies
updated.300 replaces middle290 with299; old0/1/5 and297/296 retained. Normal selectors
and game code unchanged. Browser tab2 marked deliverable; server session82639 live
at launch, revalidate before later use. Current URL localhost8877/playback-review.html.

## Verification and limits
Raw/source/equipment/full chronology and six native four-size captures viewed.
57nativechecks0, scratch owner unchanged, frozen hashes stable. APNG6decoded exact,
800ms. HTML13embedded exact. Live slow/normal playing phases and finite endpoint
observed, saved full-page images; sampled advancement is not continuously watched
every frame, actual traveling stance/contact or normal arrival/lifecycle acceptance.

## Next action and remaining work
Fix weak early yaw spacing and297sole1px drift; establish exact latest49carry to
stationary-turn start and turnend to north-unload. Check original-master head/body,
grade, case/belt/wrench/backpack/boot continuity, then shared helmet/actualarrival/
normal bank/checkpoint/interruptions/Continue. Full directions/actions consistency
and polish still required. Goal active, no blocker.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as out:out.write('\n'+section)
rasters=[q.relative_to(r).as_posix() for folder in (source,o) for q in folder.iterdir() if q.suffix in ('.png','.apng')];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(source=299,chronology=300,nativeChecks=57,failures=0,nativeCapturesReviewed=6,embeddedSourcesExact=13,decodedFramesExact=6,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
