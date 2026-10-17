from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-return-source-v316';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
v=json.loads((o/'native_probe-validation.json').read_bytes());n=json.loads((o/'native-evidence.json').read_bytes());f=json.loads((o/'native-inputs.json').read_bytes());assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta'];assert(n['checks'],n['failures'],n['captures'])==(65,0,6);assert all(sha(r/x)==h for x,h in f['preLaunchSha256'].items())
inputs=json.loads((o/'inputs.json').read_bytes());assert all(sha(r/x)==h for x,h in inputs['references'].items());assert sha(o/'prompt.txt')==inputs['promptSha256'];assert sha(r/inputs['originalTarget'])==inputs['originalTargetSha256']
m=json.loads((o/'bare-review-manifest.json').read_bytes());s=m['states'][1];dec=Image.open(o/'bare-unload-study.apng');assert dec.n_frames==6
for i,src in enumerate(s['frameFiles']):dec.seek(i);assert np.array_equal(np.asarray(dec.convert('RGBA')),np.asarray(Image.open(r/src[6:]).convert('RGBA')));assert dec.info['duration']==s['frameDurationsMs'][i]
support=[]
for src in [s['frameFiles'][3],s['frameFiles'][4],m['states'][0]['frameFiles'][4]]:
 a=np.asarray(Image.open(r/src[6:]).convert('RGBA'))[:,:,3];spans=[]
 for left,right in[(0,128),(128,256)]:
  ys,xs=np.where(a[210:224,left:right]>=128);spans.append([int(xs.min()+left),int(xs.max()+left+1)])
 support.append(dict(file=src[6:],region='y210..223 alpha128 split x128; pixel spans only.',spans=spans))
(o/'boot-span-diagnostic.json').write_text(json.dumps(support,indent=2)+'\n',encoding='utf-8')
findings=['316 preserves return depth approximately: crown106 versus old107, sole224 unchanged, narrower feet, empty hands and existing floor case visible. Arms/body width increases, quilt/hardware grade and backpack details change; provisional.', 'Candidate six sources: exact turnend0/new3091/new3132/new3143/new3164/old5, original520ms timing. All source/native four-size phase boards viewed;65checks0, owner unchanged, frozen hashes stable and6APNG pixels/clocks exact.', 'Return4-to5 crown106to76 still jumps30px; needs authored intermediate rise, case disposition/idle join and continuous observed pacing.309sole225 remains1px issue; exact moving contact and master material/anatomy not proven.', 'No helmet fitting, actual arrival selection or normal runtime adoption. Full-set integration/lifecycle and all-family consistency/polish remain.']
report=dict(disposition='provisional_narrower_empty_handed_return',sourceBoardAndRawReviewed=True,nativeCapturesReviewed=6,nativeChecks=65,nativeFailures=0,decodedApngExact=6,totalMs=520,normalChanged=False,selected=False,sourceAcceptance=False,fullGoalComplete=False,findings=findings,bootSpanDiagnostics=support)
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');ledger=p/'material-repair-progress.json';old=ledger.read_bytes();d=json.loads(old);d['northUnloadBendReview']=dict(version=316,file=(o/'review.json').relative_to(r).as_posix(),sourceVersions=[309,313,314,316],selected=False,sourceAcceptance=False,normalChanged=False);d['nextVisualRepair']='Author intermediate empty-handed rise from registered316 to original idle5 without float, preserve floor-case disposition. Observe full sequence pacing; then master material/head/gear/proportion/boot joins, helmet fit and carry/turn start. Actual arrival/controller/lifecycle/normal adoption and all-family consistency remain.';assert ledger.read_bytes()==old;ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
section='''### James empty-handed return support repair - October3,2026

V316 built-in edit of existing unload4 separates stance/material repair from rise.
Refs/prompts frozen; raw1254 saved, whole nearest256 once, no fit/translation/art
painting. Crown106 versus old107, sole224 unchanged, narrower feet, empty hands
and original floor case visible. Raw/full chronology/all6native four-size captures
viewed. Candidate0 exact turnend,1=309,2=313,3=314,4=316,5 original,520ms unchanged.
65checks0/6captures, scratch owner unchanged/frozen hashes stable; six APNG frames
pixels/clocks exact. Arms/body broaden and quilt/hardware/backpack details differ.
Return4to5 still jumps30px; next authored intermediate rise and continuous pacing
review. Floor case/idle disposition, anatomy/contact,3091pxsole, master grade/gear,
helmet, actual arrival/lifecycle/normal adoption and full-family polish remain.
Normal unchanged, source provisional, full goal active/incomplete.

Lesson: repair support in existing pose before changing action depth. A restored
sole level does not prove exact contact, stable anatomy or smooth return; review
horizontal spans, knee connections, equipment and floor prop across neighbors.
Handoff: character/james-west-carry-walk-keys-v1/north-unload-return-source-v316/HANDOFF.md.
'''
guides=record_guides(r,section,'### James lowest unloading pose and rejected floating rise')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James unloading return

## Objective and accepted decisions
Full James master-matched set, actual integration and all-family consistency.
Registered support; matte master material/identity; wrench on right belt.

## Current state/changed files
316 builtin source/receipt/frozen prompt/refs, whole256 export, six-state-phase
review manifest/APNG/source board/measurements/boot spans, probe/UID/log/evidence/
native captures and reviewed phase boards. Reusable313 builder extended316;
ledger and five maintained guides updated. Normal selectors remain unchanged.
Candidate0 turnend exact,1=309,2=313,3=314,4=316,5 original;520ms original clocks.

## Verification and limitations
Raw/source chronology and all6native four-size captures viewed.65checks0, scratch
owner unchanged/frozen hashes stable; sixAPNG pixels/clocks exact.316 sole224 and
crown106 vs old107, narrower stance/empty hands/floor case retained. Arms/body
broaden, texture/gear redraw;309sole225 and neighbor support drift remain.30px
last rise jump needs in-between. No continuous observed motion/contact/helmet/
actual arrival integration or master/full-set acceptance.

## Next action and remaining work
Author intermediate rise with planted boots and coherent floor case/idle join;
observe full pacing. Then master material/head/gear/proportions and shared helmet,
latest carry-to-turn start, actual arrival selector currently bypassing turn,
normal checkpoint/Continue/interruptions and whole-family polish. Goal active.
''',encoding='utf-8')
with(p/'HANDOFF.md').open('a',encoding='utf-8') as stream:stream.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for f in o.iterdir() if f.suffix in('.png','.apng')];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3));print(json.dumps(dict(checks=65,failures=0,capturesReviewed=6,decodedExact=6,guides=guides,lfsRasters=len(rasters),fullGoalComplete=False)))
