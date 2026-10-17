from pathlib import Path
import hashlib,json
root=Path.cwd();base=root/'character/marsh-retained-gesture-material-v1';out=base/'cardinal02-unselected'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=base/'east04-unselected/verification.json';r=json.loads(p.read_text());r['actuallyInspected']=True;r['visualAssessment']='Source cross-family board and six-pose native board inspected. Slimmer lower legs and boots improve own-idle agreement. Neutral common-height width32.94055 vs own32; regional neutral leg/boot spans25/30 vs own23/28. Connected compact gloves, bare near-left temple and material palette retained. Final arms-to-idle jump and remaining profile/head differences need motion polish; no normal admission.';p.write_text(json.dumps(r,indent=2)+'\n')
p=out/'verification.json';r=json.loads(p.read_text())
for b in r['nativeEvidence']['boards']:b['actuallyInspected']=True
r['visualAssessment']={'method':'East04 cross-family source and full native six-pose board actually inspected; all four directions slots1..5 inspected as full-page browser screenshots. Slot0 verified by restart/exact-source endpoint checks. Sampled screenshots, not continuously watched motion.','normalAdmission':False,'fullGoalComplete':False,'next':'Polish final gesture-to-idle transition before catalogue admission; complete remaining family/controller joins.'}
r['browserEvidence']={'url':'http://127.0.0.1:8759/index.html','viewerSha256':sha(out/'index.html'),'allDirectionalImagesLoaded':True,'pauseHeldBetweenObservations':True,'restart':'0ms/slot0/paused','stepTimesMs':[151,301,451,601,751],'playingClock':{'beforeMs':751,'afterMs':1018,'ticksBefore':13410,'ticksAfter':13426},'warnErrorLogs':[],'screenshots':[{'path':(out/f'viewer-slot{i:02}.jpg').relative_to(root).as_posix(),'sha256':sha(out/f'viewer-slot{i:02}.jpg'),'actuallyInspected':True} for i in range(1,6)],'scope':'Exact copied whole-source six150ms holds with300ms repeat idle gap; browser clock/controls and sampled source/station visual review only. No live actor/contact/fullSave/Continue proof.'}
prior=base/'cardinal01-unselected/verification.json';r['unchangedDirectionsNativeEvidence']={'path':prior.relative_to(root).as_posix(),'sha256':sha(prior),'directions':['west','north','south']}
p.write_text(json.dumps(r,indent=2)+'\n')
receipts=[]
for q in sorted((base/'sources').glob('*.request.json')):
 t=json.loads(q.read_text())
 for ref in t['references']:assert sha(root/ref['path'])==ref['sha256']
 assert sha(root/t['result']['path'])==t['result']['sha256']
 receipts.append({'request':q.relative_to(root).as_posix(),'sha256':sha(q),'result':t['result']})
assert len(receipts)==12
(out/'generation-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
note='''
## Marsh retained gesture East04 and timed cardinal02 review — October3,2026

East04 whole-source edit narrows the lower legs/boots without altering upper-body
scale. At own147 occupied height, neutral width32.94055 improves East03's33.923
against own32. Alpha>80 row spans head/torso/pelvis/legs/boots are28/30/26/25/30,
versus own27/30/26/23/28; East03 was28/30/26/28/32. Measure neutral regions;
a raised glove legitimately enlarges torso-row span and is not torso width drift.
Regions are directional row bands, not a universal anatomy segmentation.

All five generated body heights656 use ONE147/656 factor, whole connected
extraction and fixed4px fringe. No per-pose fit/anatomy patch/head splice/recolour.
Exact source request/prompt/result SHA retained; selected East04 generation is
exec-51ace1bb-5e5c-457a-90c1-b1c787e131f3. Cardinal builder now keys generation
IDs by(direction,version), preserving accurate receipts for older builds.

cardinal02-unselected combines East04/West03/North02/South03:8aliases/48slots,
original six150ms finite holds and exact own-idle endpoints.12raw generation
receipts verified. East04 source cross-family and complete native boards actually
inspected. East-only native192checks/52samples/6player restores/6captures passed
with0errors/warnings/failures/exit0.1049bounded inputs and2931owner non-log files
unchanged under scratchAPPDATA. Unchanged West/North/South reuse cardinal01
receipts; this is not a second complete four-direction native run.

Timed index.html compares exact copied sources with own idle at source1x and
station65.28height. Pause holds; restart returns0ms/slot0; next-frame selects
151/301/451/601/751ms. Playing clock advanced751→1018ms, ticks13410→13426;
all four image banks loaded, no browser warning/error logs. Full-page screenshot
slots1..5 actually inspected, with source SHA receipts. Sampled screenshots and
clock observations do NOT establish continuously watched motion. The300ms repeat
idle gap is viewer-only, beyond authored900ms finite holds.

Whole figures now read closer to master style/proportions than coarse old bank.
East neutral legs/boots still exceed own by~2pixels in measured regions, and the
final bent arms→exact idle transition needs motion polish. Source/player success
is not catalogue admission, real helmet implementation, live actor/contact,
fullRunSave/titleContinue or full-set acceptance. Next polish return poses and
cross-family joins before admission; the full Marsh goal remains active.
'''
canonical=root/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert canonical.read_bytes()==installed.read_bytes()
for p in [root/'character/ANIMATION_PIPELINE.md',root/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',root/'docs/CURRENT_STATUS.md',canonical]:
 with p.open('rb') as f:
  f.seek(max(0,p.stat().st_size-100000));tail=f.read().decode('utf-8',errors='ignore')
 if '## Marsh retained gesture East04 and timed cardinal02 review' not in tail:
  with p.open('a',encoding='utf-8') as f:f.write(note)
installed.write_bytes(canonical.read_bytes())
print('East source/native and5timed screenshot reviews recorded;12generation receipts verified;pipeline/bible/status/skill updated')
