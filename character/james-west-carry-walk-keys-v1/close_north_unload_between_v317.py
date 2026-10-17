from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-rise-between-v317';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();v=json.loads((o/'native_probe-validation.json').read_bytes());n=json.loads((o/'native-evidence.json').read_bytes());f=json.loads((o/'native-inputs.json').read_bytes());assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta'];assert(n['checks'],n['failures'],n['captures'])==(69,0,7);assert all(sha(r/x)==h for x,h in f['preLaunchSha256'].items())
inputs=json.loads((o/'inputs.json').read_bytes());assert all(sha(r/x)==h for x,h in inputs['references'].items());assert sha(o/'prompt.txt')==inputs['promptSha256'];assert sha(r/inputs['originalTarget'])==inputs['originalTargetSha256'];m=json.loads((o/'bare-review-manifest.json').read_bytes());s=m['states'][1];old=json.loads((p/'north-unload-return-source-v316/bare-review-manifest.json').read_bytes())['states'][1];assert s['frameFiles'][:5]==old['frameFiles'][:5] and s['frameFiles'][6]==old['frameFiles'][5];assert s['frameDurationsMs']==[80,100,100,90,40,40,70] and sum(s['frameDurationsMs'])==520;dec=Image.open(o/'bare-unload-study.apng');assert dec.n_frames==7
for i,src in enumerate(s['frameFiles']):dec.seek(i);assert np.array_equal(np.asarray(dec.convert('RGBA')),np.asarray(Image.open(r/src[6:]).convert('RGBA')));assert dec.info['duration']==s['frameDurationsMs'][i]
report=dict(disposition='provisional_seven_pose_unload_rise',sourceBoardAndRawReviewed=True,nativeCapturesReviewed=7,nativeChecks=69,nativeFailures=0,decodedApngExact=7,totalMs=520,normalChanged=False,selected=False,sourceAcceptance=False,fullGoalComplete=False,findings=['317 derived from exact original standing unload5, modest knee flexion: crown85/sole224 versus endpoint76/224. Asked approximate15px descent, got9px. Return crown106->85->76 replaces30px jump with21+9; not evenly spaced.', 'New pose changes body/hardware/head detail and widens boot stance toward original endpoint; anatomy, support and matte master joins remain provisional. Existing floor case remains visible between lower legs; idle transition disposition still requires actual integration review.', 'Seven candidate sources preserve prior six images, inserting317 before final. Existing return hold80ms split40+40, total520ms unchanged.69native checks0/7captures all viewed at148/82/54/27, scratch owner unchanged/frozen hashes stable,7decodedAPNG pixels/clocks exact.', 'Static native phases and source chronology are not continuously watched pacing or actual arriving controller motion. No helmet or normal bank admission. Full master material/identity/height/proportion/support, carry-to-turn/arrival lifecycle and all-family polish remain.'])
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');ledger=p/'material-repair-progress.json';before=ledger.read_bytes();d=json.loads(before);d['northUnloadBendReview']=dict(version=317,file=(o/'review.json').relative_to(r).as_posix(),sourceVersions=[309,313,314,316,317],candidateFrames=7,totalMs=520,selected=False,sourceAcceptance=False,normalChanged=False);d['nextVisualRepair']='Observe full seven-pose317 unloading at original520ms and slower diagnostic speed; judge21+9px final rise, stance/case/grade/head/detail transitions. Adjust sources/pacing from observed evidence. Then shared helmet and carry-to-turn, actual arrival/controller/lifecycle/normal adoption and all-family master polish.';assert ledger.read_bytes()==before;ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
section='''### James additional unloading rise pose - October3,2026

V317 built-in edit of exact original unload5 standing endpoint adds modest knee
flexion; frozen target/prompt hashes, raw1254 saved, whole nearest256 once, no
fitting/translation/painting. Crown85/sole224 vs endpoint76/224; requested15px
descent yields9px. Return106to85to76 splits30px jump into21+9, still uneven.
Candidate preserves previous six sources and inserts317 before endpoint; prior
80ms return hold splits40+40ms,7poses520ms. Raw/full chronology/all7native captures
at148/82/54/27 viewed.69checks0, scratch owner unchanged/frozen hashes stable,
all7APNG pixels/clocks exact. Head/body/gear detail and stance change; floor case
still visible, idle disposition needs actual review. No continuously watched
pacing, contact/anatomy/master material acceptance, helmet or normal adoption.
Full set/integration/lifecycle/all-family consistency remain incomplete.

Lesson: adding a drawing can split a large rise without extending action time,
but unequal pose spacing plus shorter holds needs advancing playback review.
Keep original/candidate clock mappings separate when frame counts differ; phase
indices are not matching timestamps. Next continuous520ms/slow review, then refine
support/grade/head/gear and shared helmet. Handoff:
character/james-west-carry-walk-keys-v1/north-unload-rise-between-v317/HANDOFF.md.
'''
guides=record_guides(r,section,'### James empty-handed return support repair')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James unloading rise

## Objective and decisions
Full master-matched James set, actual integration and whole-family polish.
Fixed support, matte grade/identity/proportions, wrench remains on belt.

## Current state and changed files
317 original-standing-source edit/raw/receipt/frozen target/prompt, whole256
in-between, seven-pose manifest/APNG/source chronology/measurements, native probe/
UID/log/evidence and all seven captures/review boards. Assembler now accepts
explicit capture count while six remains default. Ledger/five guides updated.
Previous six sources retained; new317 before endpoint, return80ms split40+40,
total520ms. Normal selectors unchanged, provisional/unselected.

## Verification/limitations
Raw/source board/all7native four-size captures viewed.69checks0, owner unchanged,
frozen hashes stable;7APNG frames/clocks byte exact. New crown85/sole224, final
rise106->85->76,21+9px uneven. Body/head/gear/boot stance differs. Floor case
visible between lower legs; idle handoff disposition needs review. No continuous
watched pacing, physical contact, helmet fit or actual arrival/controller proof.

## Next work
Observe seven-pose full520ms and slower diagnostic motion before further source
retakes; judge timing, stance/support/grade/head/gear/case. Then shared helmet,
carry-to-turn/actual arrival selector bypass, normal lifecycle/checkpoint/Continue/
interruptions and all-family consistency/polish. Full goal active, no blocker.
''',encoding='utf-8')
with(p/'HANDOFF.md').open('a',encoding='utf-8') as stream:stream.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for f in o.iterdir() if f.suffix in('.png','.apng')];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3));print(json.dumps(dict(checks=69,failures=0,capturesReviewed=7,decodedExact=7,totalMs=520,guides=guides,lfsRasters=len(rasters),fullGoalComplete=False)))
