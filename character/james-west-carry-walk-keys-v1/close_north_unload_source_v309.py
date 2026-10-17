from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-start-source-v309';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
v=json.loads((o/'native_probe-validation.json').read_bytes());n=json.loads((o/'native-evidence.json').read_bytes());frozen=json.loads((o/'native-inputs.json').read_bytes())
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert (n['checks'],n['failures'],n['captures'])==(28,0,1)
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
base=json.loads((p/'north-unload-join-review-v308/bare-review-manifest.json').read_bytes())['states'][1]
files=[r/x[6:] for x in base['frameFiles']];files[1]=o/'fixed-canvas-source.png';clocks=base['frameDurationsMs'];images=[Image.open(x).convert('RGBA') for x in files]
images[0].save(o/'bare-unload-study.apng',save_all=True,append_images=images[1:],duration=clocks,loop=0,disposal=0,blend=0)
decoded=Image.open(o/'bare-unload-study.apng');assert decoded.n_frames==6
for i,im in enumerate(images):
 decoded.seek(i);assert np.array_equal(np.asarray(decoded.convert('RGBA')),np.asarray(im));assert decoded.info['duration']==clocks[i]
report=dict(disposition='provisional_early_bend_source_study',sourceAndNativeBoardsReviewed=True,nativeChecks=28,nativeFailures=0,nativeCapturesReviewed=1,apngDecodedExact=6,totalMs=sum(clocks),selected=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=['New early bend lowers alpha128 crown from76 to80;145px extent versus148px standing. Physical bend is not normalized back to standing height.', 'Narrower stance than old unload1; source retains belt wrench and meter plus backpack emblem. Entire body rerendered: arms wider and soles one pixel lower, equipment details change. Exact foot planting and master fidelity not proven.', 'Four-size native static comparison reviewed; original and candidate unload1 plus exact preceding turnend and runtime North comparison.28checks0, owner unchanged. No full animated native unloading, helmet source fit or actual arrival controller proved.', 'StudyAPNG keeps exact source pixels and original six clocks520ms. New1-to-old2 still needs support/stance/material continuity review; decoding proof is not observed continuous motion.'],sources=[dict(file=f.relative_to(r).as_posix(),sha256=sha(f),durationMs=t) for f,t in zip(files,clocks)])
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();d=json.loads(old);d['northUnloadStartSourceStudy']=dict(version=309,file=(o/'review.json').relative_to(r).as_posix(),selected=False,sourceAcceptance=False,normalChanged=False);d['nextVisualRepair']='Review/refine309 early-bend feet/body/equipment and1-to2/full north unload stance/material continuity; fit shared helmet from actual sources. Latest turn306/carry49 master fidelity and actual arrival/controller/save/normal adoption plus full-family consistency remain.';assert ledger.read_bytes()==old;ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
section='''### James north unloading early bend source study - October3,2026

V309 built-in imagegen from exact paired-join308 bare turnend; original West
master quilt crop appearance only. Target/ref/prompt hashes frozen before call;
raw1254 square saved, whole nearest resampled once256, no body fit/translation/
colour painting. Raw, source0/new1/old1/old2 board and native four-size comparison
actually viewed. New crown80 versus76 lowers torso into bend;145px silhouette
versus148 standing is not forced back to standing height. Narrower stance than
old1, belt wrench/meter and backpack emblem retained. Body fully rerendered:
arms wider, soles one pixel lower and gear detail changes; exact foot planting,
master material/proportions and full source acceptance remain unproven.

Native four static sources at148/82/54/27:28checks0/1capture reviewed, scratch
owner unchanged and frozen source/manifest/runtime hashes stable. Six-source
unload studyAPNG uses exact turnend0/new3091/old2..5 at unchanged520ms, all6
decoded exact. No observed continuous unload, paired helmet fit, actual arrival
selector or normal adoption. Provisional/unselected; full goal active/incomplete.

Lesson: crouch height must lower naturally from a registered standing pose. An
early bend can remove the old unrelated wide standing pose, but generation's
redrawn boots/arms/gear still require neighbor and support review. Small crown
changes and valid source/timing metadata cannot certify natural planted feet.
Handoff: character/james-west-carry-walk-keys-v1/north-unload-start-source-v309/HANDOFF.md.
'''
guides=record_guides(r,section,'### James exact north turn-to-unload source join')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James unloading early bend

## Objective
Complete full master-matched James set, integration and all-family polish.

## Accepted decisions
Matte master grade/proportions/camera, wrench on belt. Registered crouch can lower
height. Versioned source study; existing normal selectors remain untouched.

## Changed files and current state
309 frozen edit/reference/prompt inputs, raw generation receipt, whole-canvas
256 source, source-neighbor measurements/board, four-state static native manifest,
probe with paired UID, captures/log/evidence, six-source APNG and review. Main
ledger plus pipeline/bible/status/repo and installed consistency guides updated.

## Verification and limits
Raw/reference/source board/native comparison actually viewed.28native checks0,
one four-size capture; scratch owner unchanged and frozen hashes stable. Six
decoded APNG frames byte exact at520ms. Narrower initial bend than old1 but arms
and equipment redraw, soles one pixel lower; source acceptance unproven. Full
continuous unloading/helmet/physical contact/actual arrival and normal admission
remain unchecked. No procedural artwork edits or forced standing-height fitting.

## Next work
Refine early bend feet/body/gear and next bend/full unloading consistency. Fit
helmet from actual sources. Complete carry-to-turn start and full shared-helmet
turn; ordinary arrival currently skips generic carry-facing turn. Integrate after
source review, verify checkpoint/Continue/interruptions and whole-set consistency.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as stream:stream.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for f in o.iterdir() if f.suffix in ('.png','.apng')];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(checks=28,failures=0,capturesReviewed=1,decodedExact=6,totalMs=520,guides=guides,lfsRasters=len(rasters),normalChanged=False,goalComplete=False)))
