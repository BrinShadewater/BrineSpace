from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-low-source-v314';q=p/'north-unload-rise-source-v315';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
v=json.loads((o/'native_probe-validation.json').read_bytes());n=json.loads((o/'native-evidence.json').read_bytes());f=json.loads((o/'native-inputs.json').read_bytes());assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta'];assert(n['checks'],n['failures'],n['captures'])==(65,0,6);assert all(sha(r/x)==h for x,h in f['preLaunchSha256'].items())
for folder in (o,q):
 inputs=json.loads((folder/'inputs.json').read_bytes());assert all(sha(r/x)==h for x,h in inputs['references'].items());assert sha(folder/'prompt.txt')==inputs['promptSha256'];assert sha(r/inputs['originalTarget'])==inputs['originalTargetSha256'];assert sha(r/inputs['supportOriginal'])==inputs['supportOriginalSha256']
m=json.loads((o/'bare-review-manifest.json').read_bytes());s=m['states'][1];dec=Image.open(o/'bare-unload-study.apng');assert dec.n_frames==6
for i,src in enumerate(s['frameFiles']):dec.seek(i);assert np.array_equal(np.asarray(dec.convert('RGBA')),np.asarray(Image.open(r/src[6:]).convert('RGBA')));assert dec.info['duration']==s['frameDurationsMs'][i]
support=[]
for src in [s['frameFiles'][2],s['frameFiles'][3],m['states'][0]['frameFiles'][3]]:
 a=np.asarray(Image.open(r/src[6:]).convert('RGBA'))[:,:,3];spans=[]
 for left,right in [(0,128),(128,256)]:
  ys,xs=np.where(a[210:224,left:right]>=128);spans.append([int(xs.min()+left),int(xs.max()+left+1)])
 support.append(dict(file=src[6:],region='Canvas y210..223 split atx128, alpha128; pixel spans, not anatomical contact proof.',spans=spans))
(o/'boot-span-diagnostic.json').write_text(json.dumps(support,indent=2)+'\n',encoding='utf-8')
(q/'review.json').write_text(json.dumps(dict(disposition='rejected_before_native',rawAndNeighborBoardReviewed=True,crown93=True,soleBottom218=True,bootSoleRisePx=6,findings=['Requested mid-rise crown achieved approximately, but soles lift6px, stance remains broad and case disposition changes. Reject rather than translate/fit body to disguise unsupported feet.'],normalChanged=False,selected=False),indent=2)+'\n',encoding='utf-8')
report=dict(disposition='provisional_narrower_low_unload_pose',sourceBoardReviewed=True,nativeCapturesReviewed=6,nativeChecks=65,nativeFailures=0,decodedApngExact=6,totalMs=520,normalChanged=False,selected=False,sourceAcceptance=False,fullGoalComplete=False,findings=['314 original lowest-pose geometry retained: crown113/sole224 match old3, boots narrower and original case between legs retained. Both gear meter/wrench/backpack emblem present; no new helmet source authored.', 'Sequence turnend0/new3091/new3132/new3143/old4..5; all6native phases at148/82/54/27 viewed. Fore-aft knee/support and actual hand-to-case contact unproven; slight2to3 boot spread remains. Material/head/gear detail and return4to5 height jump remain.', '65checks0 and all6APNG clocks/pixels exact520ms, scratch owner unchanged/frozen hashes stable. No continuous observed motion or actual arrival/normal integration.', '315 midway rise crown93 versus old107 but soles218 instead224; rejected before native. Full-canvas support reference is not pixel preservation.'],bootSpanDiagnostics=support)
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');ledger=p/'material-repair-progress.json';old=ledger.read_bytes();d=json.loads(old);d['northUnloadBendReview']=dict(version=314,file=(o/'review.json').relative_to(r).as_posix(),sourceVersions=[309,313,314],selected=False,sourceAcceptance=False,normalChanged=False);d['northUnloadRiseTrial']=dict(version=315,file=(q/'review.json').relative_to(r).as_posix(),disposition='rejected_before_native',normalChanged=False);d['nextVisualRepair']='Repair empty-handed rise without floating/wide boots, keep floor case disposition coherent.314 low source narrower but2to3 boot drift, material/head/gear joins,3091pxsole need refinement; full shared helmet, carry/turn start, arrival/controller/lifecycle/adoption and all-family polish remain.';assert ledger.read_bytes()==old;ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
section='''### James lowest unloading pose and rejected floating rise - October3,2026

V314 built-in repair of actual original low pose3 with same-canvas313 boot support
and original master quilt crop. Exact refs/prompts frozen before generation, raw
1254 saved, whole nearest256 once, no fitting/translation/art painting. Crown113
and sole224 match original low pose; stance narrower, original case remains visible
between knees, meter/wrench/emblem retained. Raw/full chronology/all6native captures
at148/82/54/27 viewed. Candidate0 exact turnend,1=309,2=313,3=314,4..5 original;
65checks0/6captures, scratch owner unchanged and frozen hashes stable. Six APNG
frames/pixels/clocks exact520ms. Slight2to3 boot spread, cloth/head/gear differences,
case contact/disposition and return height jump remain provisional. No continuous
observed motion, helmet fit, actual arrival or normal adoption; full goal incomplete.

V315 empty-handed midway rise asked crown about15px up from old107. New93 but
soles218 versus224 lift6px; stance still broad. Raw/neighbor board viewed, rejected
before native. Boots-only reference crop corrected before generation to exclude
the case; inputs freeze final crop. Kept raw and rejection, no body normalization.

Lesson: figure rise is joint articulation with fixed support, not a smaller body
or whole-figure shift. Measure crown and soles separately; support image cannot
promise exact pixels. Preserve visibility of the floor case through lowering,
release and standing rather than silently omitting it from a foot reference.
Handoff: character/james-west-carry-walk-keys-v1/north-unload-low-source-v314/HANDOFF.md.
'''
guides=record_guides(r,section,'### James existing-bend geometry and narrower unloading stance')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James unloading low/rise

## Objective/decisions
Complete master-matched James set, actual integration and all-family polish.
Natural registered support, dark matte master material, wrench stays on belt.

## Changed files/state
314 builtin low-pose edit, frozen prompt/refs/raw receipt, whole256 source, six-pose
manifest/APNG/source board/measurements/boot span diagnostic, native probe/UID/log/
evidence/captures.315 saved attempted midway rise/raw/board/measurements rejected.
Reusable313 builder extended314; previous evidence retained. Ledger/five guides
updated. Candidate0 turnend exact,1=309,2=313,3=314,4..5 original. Normal unchanged.

## Verification/limits
314 raw/full source chronology and all6native four-size captures viewed.65checks0,
scratch owner unchanged, frozen hashes stable, APNG6pixels/clocks exact520ms.
Low crown113/sole224 matches old, stance narrower but slight2to3 boot spread,
material/head/gear changes remain.315 new93crown/218sole lifts6px: rejected before
native. No continuous motion, actual hand-to-case contact, helmet fit or arrival
integration acceptance. Foot pixel spans are diagnostics, not anatomical proof.

## Next work
Repair empty-handed rise preserving support/floor case, then full material/head/
gear joins and helmet. Latest carry/turn start, actual arrival selector currently
bypassing generic turn, normal checkpoint/Continue/interruptions and full-family
consistency/polish remain. No external blocker; full goal active.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as stream:stream.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in(o,q) for f in folder.iterdir() if f.suffix in('.png','.apng')];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3));print(json.dumps(dict(checks=65,failures=0,capturesReviewed=6,decodedExact=6,guides=guides,lfsRasters=len(rasters),rejectedRise315=True,fullGoalComplete=False)))
