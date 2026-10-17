from pathlib import Path
import hashlib,json,os,time,urllib.request
P=Path(__file__).resolve().parent;R=P.parents[1];O=P/'whole-pose-join-v4/material-review/case-review-v1';B=O/'browser-review'
evidence=json.loads((O/'review-evidence.json').read_text())
evidence['visualReview']='Seven whole/case comparison columns and six explicit case masks visually inspected. Case tone closer to repaired held master, but phase2/4 surface pattern still differs. Six paused browser source poses inspected plus three playing screenshots after clock fix. No uninterrupted video/native/cadence or final case texture acceptance.'
evidence['browserReview']={'pausedPoseFiles':[{'pose':i,'path':f'browser-review/pose-{i}.jpg','sha256':hashlib.sha256((B/f'pose-{i}.jpg').read_bytes()).hexdigest()} for i in range(1,7)],'initialPlaybackFailure':'Source rAF clock initialized with performance.now could receive earlier first frame timestamp, producing negative index and undefined frame src. Initial samples retained with elapsed0; no progress claim based on these.','clockFix':'Clamp frame delta to nonnegative before applying modulo840. Reload and observable next-pose wait verified advancement.','fixedSamples':json.loads((B/'fixed-playback-samples.json').read_text()),'continuousVideoReviewed':False,'nativeReview':False}
assert len({v['state']['phase'] for v in evidence['browserReview']['fixedSamples']['playing']})>1
assert len({v['state']['elapsed'] for v in evidence['browserReview']['fixedSamples']['playing']})>1
evidence['initialCaseGuardFailure']='Initial protected-glove assertion failed; mask now explicitly excludes y136:160/x125:157; all37checks pass after fix.'
verification=[]
for name in ['index.html','cycle.png','case-master-comparison.png']:
 with urllib.request.urlopen('http://127.0.0.1:8791/character/veld-carry-east-master-proportions-v1/whole-pose-join-v4/material-review/case-review-v1/'+name) as response:
  verification.append({'file':name,'status':response.status,'exactBytes':response.read()==(O/name).read_bytes()})
assert all(v['status']==200 and v['exactBytes'] for v in verification)
evidence['previewVerification']=verification;evidence['status']='reviewed_case_source_browser_snapshots_full_motion_pending'
(O/'review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
block='''## Veld East case-surface grade and actual browser review — October 2, 2026

review_case_material.py adds explicit native case lid/right-panel polygons,
protected clasp and glove/cuff envelope, one pooled luminance curve against
repairedNEheld005. No geometry changes or per-frame histogram normalization.
First glove guard catches a mask overlap; explicit y136:160/x125:157 exclusion
fixes it.37checks0fail: alpha/outside-mask/clasp exact, glove excluded,6exact
140ms APNGframes/840ms. Source case-surface knots38.67/57.33/61.67/67/76.67/96.33
map to master38.35/52.73/56.67/58.33/61.67/69.88. All7whole/case comparisons and
6mask plates inspected. Tone closer; phase2/4case surface texture still differs.

Actual IABtab25 local case-review-v1 page visibly opened, six paused source poses
inspected/savedJPEGs. Browser controls exposed a real first-rAF-clock error: initial
timestamp can precede performance.now seed, negative pose index stops callback.
Nonnegative delta clamp fixes preview only. Reload/observable next-pose wait,
3playing JPEGs +DOM elapsed317.0/383.7/433.7 and phase2→3 verify actual playback
advances. Initial frozen samples retained as failure evidence. These snapshots
do NOT certify uninterrupted visual cadence/native/world movement. Browser tab
marked deliverable; local index/APNG/board HTTP200/exactbytes. Source frame clocks
unchanged; no Godot/owner profile access or normal-selection mutation this interval.

Lesson: APNG decode and a Play button do not prove live motion. Verify advancing
rendered source/observable clock after controls change, wait on actual next-pose
text before screenshots, and distinguish sampled browser proof from native full
cadence acceptance. Palette masks must explicitly exclude clasp/glove; a broad
case bounding box is insufficient. Shared tone cannot erase authored case-pattern
drift: keep remaining texture work visible rather than declaring final consistency.
Next finish case surface detail consistency, then paired original shared East
helmet/package/native 30Hz two-cycle review and actual cargo transitions. East
actions/South/North/worldownership/interruptions/Continue and full-library polish open.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(5):
  old=path.read_bytes();source=old.decode('utf-8-sig')
  if block.splitlines()[0] in source:break
  tmp=path.with_name(path.name+'.veld-case.tmp');tmp.write_text(block+source,encoding='utf-8')
  if path.read_bytes()!=old:tmp.unlink();continue
  try:os.replace(tmp,path);break
  except PermissionError:tmp.unlink(missing_ok=True);time.sleep(.5)
 else:raise RuntimeError(f'Could not update {path}')
with (P/'SOURCE_REVIEW.md').open('a',encoding='utf-8') as f:f.write('\n'+block)
for path in [P/'HANDOFF.md',R/'character/veld-cargo-turns-master-family-v1/HANDOFF.md']:
 source=path.read_text(encoding='utf-8');start=source.index('## Next action')
 source=source[:start]+'''## Case-surface/browser continuation
Explicit lid/right-panel masks, one pooled repairedNEheld case tone curve, exact
alpha/outside-mask/glove/clasp protection. First glove guard fails, mask exclusion
fixed;37checks0fail/6exact140ms APNGframes.7whole+case columns/6masks visually seen;
phase2/4surface pattern still differs despite closer tone. Actual IABtab25 visibly
opened;6paused JPEGs inspected. First rAFnegative-index clock bug stops Play;
nonnegative delta clamp fixed and3playing JPEGs/DOM clock317/383.7/433.7 withphase2→3
verify actual advancement. Initialfailedsamples retained. Not uninterruptedvideo,
native/world/cadence/helmet acceptance. Browser tab marked deliverable.3previewfiles
HTTP200/exactbytes; no Godot or normal admission. Five maintained references updated.

## Next action
Finish case surface-detail consistency, then original shared East helmet/paired
package/native 30Hz two-cycle proof. Keep whole anatomy/source ruler and pose clocks.
East actions/South/North cargo matching, actual controller/room/ownership/
interruptions/Continue, guarded adoption and full-library consistency polish open.
'''
 path.write_text(source,encoding='utf-8')
print(json.dumps({'caseChecks':37,'failures':0,'pausedBrowserPoses':6,'advancingBrowserSnapshots':3,'httpExactFiles':3,'maintainedReferences':5,'handoffs':2,'scope':'source tone/browser samples; full objective incomplete'}))
