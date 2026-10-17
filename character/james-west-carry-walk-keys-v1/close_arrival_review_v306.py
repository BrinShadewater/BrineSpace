from pathlib import Path
from PIL import Image
import numpy as np
import json,hashlib,base64,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-turn-chronology-v306';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
receipts=[('arrival-turn-pose2-v301','67fd9624-77a4-4457-ae0a-baa528ed39d9','rejected_before_native_backpack_redesign_and_insufficient_yaw'),('arrival-turn-pose2-v302','74043fe6-f4e4-43bf-af02-c0c052ce9953','provisional_earlier_turn_from_middle_source'),('arrival-turn-pose1-v304','01a919b3-e4ea-469e-a3b0-804c61b38420','superseded_missing_original_master_moustache'),('arrival-turn-pose1-v305','3237f51e-ccdc-4650-959f-17ac34452821','provisional_early_pose_with_restored_master_facial_identity')]
promptset=['# James arrival turn source prompts','Built-in image generation; versioned complete sources. All candidates remain provisional.']
for folder,execution,verdict in receipts:
 q=p/folder;d=json.loads((q/'inputs.json').read_bytes());assert sha(q/'prompt.txt')==d['promptSha256'];assert sha(r/d['sourceFile'])==d['sourceSha256'];assert all(sha(r/f)==h for f,h in d['referenceSha256'].items())
 actualrefs=[(q/'edit-target.png').relative_to(r).as_posix()]+([(q/'original-master-face-reference.png').relative_to(r).as_posix()] if folder.endswith('v305') else [])
 (q/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,method='builtin_imagegen',rawSha256=sha(q/'raw.png'),prompt='prompt.txt',referencedImagePaths=actualrefs,disposition=verdict),indent=2)+'\n')
 (q/'review.json').write_text(json.dumps(dict(disposition=verdict,rawVisuallyReviewed=True,sourceBoardReviewed=True,geometry=json.loads((q/'registration-diagnostic.json').read_bytes()),selected=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
 promptset.extend(['\n## '+folder,verdict+'\n', (q/'prompt.txt').read_text()])
(o/'prompt-set.md').write_text('\n'.join(promptset),encoding='utf-8')
# A face edit is not assumed to preserve body pixels just because the prompt asks it.
a=np.asarray(Image.open(p/'arrival-turn-pose1-v304/fixed-canvas-source.png').convert('RGBA'))[110:];b=np.asarray(Image.open(p/'arrival-turn-pose1-v305/fixed-canvas-source.png').convert('RGBA'))[110:];am=a[:,:,3]>=128;bm=b[:,:,3]>=128;union=am|bm;body=dict(diagnosticRegion='entire canvas below y110; not anatomical segmentation',alpha128BodyIoU=float((am&bm).sum()/union.sum()),exactRgbaFractionOnUnion=float(np.all(a==b,axis=2)[union].mean()),sourceBodyExact=False)
(p/'arrival-turn-pose1-v305/body-preservation-diagnostic.json').write_text(json.dumps(body,indent=2)+'\n')
for version in (303,306):
 q=p/f'arrival-turn-chronology-v{version}';v=json.loads((q/'native_probe-validation.json').read_bytes());n=json.loads((q/'native-evidence.json').read_bytes());f=json.loads((q/'native-inputs.json').read_bytes());inp=json.loads((q/'inputs.json').read_bytes())
 assert (n['checks'],n['failures'],n['captures'])==(57,0,6);assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta'];assert all(sha(r/x)==h for x,h in f['preLaunchSha256'].items());assert all(sha(r/x['file'])==x['sha256'] for x in inp['sources'])
 html=(q/'playback-review.html').read_text(encoding='utf-8');arrays=json.loads(html.split('const sources=',1)[1].split(', clocks=',1)[0]);m=json.loads((q/'bare-review-manifest.json').read_bytes());count=0
 for state in m['states']:
  for url,path in zip(arrays[state['id']],state['frameFiles']):assert base64.b64decode(url.split(',',1)[1])==(r/path[6:]).read_bytes();count+=1
 assert count==13 and sha(q/'playback-review.html')==json.loads((q/'browser-inputs.json').read_bytes())['htmlSha256']
 (q/'review.json').write_text(json.dumps(dict(disposition='provisional_full_bare_turn_source_study',nativeChecks=57,nativeFailures=0,nativeBoardsReviewed=6,wholeChronologyReviewed=True,equipmentHeadFeetBoardReviewed=True,decodedFramesExact=6,clockTotalMs=800,htmlSourcesExact=13,browserPlaybackObserved=False,selected=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=['302 precedes299 with more side face and slightly less rear exposure; torso/hip/boot projections still close, no measured degree or smooth yaw acceptance.', '305 restores older grey moustache/sideburn/hair identity using original master face crop while retaining304 early body pose. Whole generated body is not byte-exact; diagnostic saved.', '306 has four revised poses305/302/299/296 and retained old0/5.305151high/crown75/sole225,302150/crown76/sole225 versus middle/late149/crown76/sole224. Extent and material/head differences across joins remain.', 'Original master anatomy/grade, exact latest49carry and north-unload endpoints, shared helmet, physical stance and actual arrival/controller/save lifecycle not yet accepted.']),indent=2)+'\n')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();j=json.loads(old);j['arrivalTurnChronologyReview']=dict(version=306,file=(o/'review.json').relative_to(r).as_posix(),sources=[296,299,302,305],retainedOldPhases=[0,5],selected=False,sourceAcceptance=False,normalChanged=False);j['arrivalTurnReview']['rejectedSourceTrials']=sorted(set(j['arrivalTurnReview']['rejectedSourceTrials']+[301,304]));j['nextVisualRepair']='306 four revised turn poses;305 face matched to original crop. Check head/material and actual body-yaw spacing across305/302/299/296; early soles1px low/crown3051px high. Exact latest49carry stationary start and north-unload endpoints, shared helmet, moving stance/contact and actual arrival/lifecycle/normal bank required; full-family consistency/polish remains.';assert ledger.read_bytes()==old;ledger.write_text(json.dumps(j,indent=2)+'\n')
section='''### James early turn angles and original-master face identity - October3,2026

Four builtin complete-source receipts301/302/304/305 frozen and terminal.301
original profile target requested later yaw but redesigned backpack without enough
rotation: rejected before native.302 derives preceding pose from299 middle, retains
central backpack emblem/device/belt wrench and more side face; body projections
still close to299, requested15degrees not measured acceptance.304 earlier angle
plausible but loses original grey downward moustache; superseded by305 correction.

305 full-source facial identity edit uses304 as pose target plus exact original
master face crop530,115,710,280 only. Older moustache/sideburn/grey textured hair
restored with pose/equipment mostly retained; raw/source/master/native reviewed.
151high/crown75/sole225 vs304150/76/225. Whole body below110 NOT pixel-exact;
body-preservation-diagnostic records silhouette/RGBA evidence, not anatomy proof.
No fitting, source translation, recoloring or per-part painting to hide deviations.

303 and306 full six-source bare chronology native57checks0/6captures each, all12
four-size captures inspected. Scratch owner unchanged, frozen inputs stable; both
six decoded APNGframes exact at original800ms and13HTMLembedded sources byte-exact.
No new live browser playback observed for303/306; prior300 samples are not new-source
motion acceptance.306 four new poses305/302/299/296 with old0/5 retained. Early
soles1px low,305crown1px high, body-yaw spacing/head/material/equipment differences,
original-master proportions/grade and exact latest49carry/north-unload joins remain.
Shared helmet, actual arrival/physical stance/controller/save lifecycle not covered.
Normal selectors unchanged; full goal active/incomplete.

Lesson: rotating a mostly rear-view source can invent an unrecognizable profile;
compare distinctive facial identity whenever it becomes visible. A separate original
face crop can restore likeness without the full-body master dominating pose, but
still inspect whole-body preservation, crown/sole drift and every neighboring seam.
Do not turn requested rotation degrees or improved face into full-bank acceptance.
Handoff: character/james-west-carry-walk-keys-v1/arrival-turn-chronology-v306/HANDOFF.md.
'''
guides=record_guides(r,section,'### James middle turn source and live chronology review')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James early arrival turn

## Objective and acceptance
Full master-matched James animation set, normal lifecycle and all-family polish.

## Accepted decisions and constraints
Original older grey moustache/goggles identity, matte charcoal/yellow, same master
proportions and camera. Wrench on belt, case in both hands; whole source registration.

## Current state and changed files
301 rejected backpack redesign,302 provisional earlier pose from299.304 earlier
pose missing moustache;305 original-face-crop identity repair, complete source.
303/306 full six-pose bare review banks, native probes/UIDs/manifests/captures,
APNGs/HTML/frozen inputs/reviews.306 uses old0/5 and305/302/299/296. Ledger and five
guides updated; prompt-set and four terminal receipts saved. Normal bank unchanged.

## Verification and limits
All new raw/source/chronology/head-gear-feet boards and12native captures inspected.
303/306 each57/0/6captures; scratch owner unchanged/frozen hashes stable; APNG6exact
at800ms and HTML13embedded exact. New live browser not observed;300 prior samples
do not certify new motion.305 body below110 not exact; see diagnostic.305151high,
302150, middle/late149; earlysoles225vs224, crown30575vs76 remain.

## Next action and remaining work
Review actual body-yaw spacing, consistent face/hair/head size, grade and case/belt/
wrench/backpack/boot geometry throughout. Solve early1px floor drift and exact
latest49carry stationary turn start/north-unload end source joins. Then shared
helmet/actualarrival/moving stance/contact/normal bank/checkpoint/interruptions/
Continue. Full directions/actions and all-library consistency/polish still required.
Full goal active; no blocker.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as out:out.write('\n'+section)
folders=[p/x[0] for x in receipts]+[p/'arrival-turn-chronology-v303',o];rasters=[q.relative_to(r).as_posix() for folder in folders for q in folder.iterdir() if q.suffix in ('.png','.apng')];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(receipts=4,nativeRuns=2,nativeChecks=114,failures=0,capturesReviewed=12,bodyDiagnostic=body,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
