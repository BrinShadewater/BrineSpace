from pathlib import Path
import json,hashlib,shutil
from PIL import Image
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;P=R/'character/krusher-animation-package-v11'
native=json.loads((H/'review/report.json').read_text());run=json.loads((H/'review/run-verification.json').read_text());joins=json.loads((H/'join-review.json').read_text())
assert native['failures']==0 and run['engineExit']==0 and not run['ownerFilesChanged']
assert not any(w in (H/'review/engine.log').read_text(errors='replace') for w in ['ERROR:','WARNING:','leaked'])
media=[]
for gear in ['bare','helmet']:
 im=Image.open(H/(gear+'-native.webp'));duration=0
 for i in range(im.n_frames):im.seek(i);im.load();duration+=im.info.get('duration',0)
 assert im.n_frames==426 and duration==14200,(gear,im.n_frames,duration)
 media.append({'gear':gear,'frames':im.n_frames,'durationMs':duration,'sha256':hashlib.sha256((H/(gear+'-native.webp')).read_bytes()).hexdigest()})
sources={str(p.relative_to(P)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'package.json',*sorted((P/'packs').glob('*.json'))]}
(H/'candidate-contract.json').write_text(json.dumps(sources,indent=2))
summary={'candidate':'krusher-animation-package-v11','changedArt':False,'sourceHandoffPlansReviewed':198,'turnsIncluded':72,'reviewSheets':17,'nativeChecks':native['checks'],'failures':0,'nativeFrames':len(native['records']),'nativePoseChanges':32,'nativeEquipmentVariants':['bare','helmet'],'ownerFilesFingerprinted':run['ownerFilesFingerprinted'],'ownerFilesChanged':run['ownerFilesChanged'],'media':media,'visualResult':'No additional head/neck defect found in the 198 pivot-aligned handoff witnesses or 32 native bunk pose-change captures.','limits':'Source handoff sheets use the 65.28px world standing ruler, not furniture context. Native evidence covers actual default-bunk lifecycles only. Replays reconstruct 30Hz simulation cadence; original capture ran slower than real time. Normal roster integration and owner visual acceptance remain separate.'}
(H/'summary.json').write_text(json.dumps(summary,indent=2))
dst=P/'verification/station-motion';dst.mkdir(parents=True,exist_ok=True)
for p in [H/'summary.json',H/'candidate-contract.json',H/'review/report.json',H/'review/run-verification.json',H/'review/engine.log']:shutil.copy2(p,dst/p.name)
(H/'HANDOFF.md').write_text('''# Project handoff

Updated: October 15, 2026 · Project: Brine Space · Task: Krusher Dom station-scale continuation

## Objective and acceptance
Continue the head/neck animation review through game-scale handoffs and actual station lifecycle updates. Preserve V11 unless a visible defect is found.

## Accepted decisions and constraints
V11 remains the current 586-state / 8,058-hold asset candidate. Keep original density, timings, pivots, geometry and private preview audience. No normal roster integration or gameplay edits. This pass adds verification and review media, with no art revisions or Site redeployment.

## Current state
character/krusher-station-motion-v1 contains the bounded native fixture, runner, candidate contract, chronological source joins, room captures and native animated WebP replays. index.html places both equipment replays side by side. V11 verification/station-motion contains the recorded reports. Source unchanged; previous private gallery remains current.

## Verification
All 198 contextual source handoff plans reviewed on 17 pivot-aligned sheets at the 65.28px world standing ruler, including all 72 turns. No further head/neck defect found. These sheets show source pose joins, not natural controller/furniture coverage.

Actual main scene/default bunk: normal fatigue chooser, path and arrival establish the contact; actual actor updates then advance entry, sleep, exit and idle for both equipment variants. 852 native draw captures at 30Hz simulated steps, 32 source/action changes, every authored bunk source reached; 4,317 checks, zero failures/errors/warnings/leaks. Exact viewport containment and centered camera checked. All 2,947 fingerprinted owner non-log files unchanged under scratch APPDATA. Source .gd/.uid pair retained.

Agent visually inspected the complete native pose-change witnesses plus room context; no detached collar or inconsistent head density observed. Two lossless WebP replays each decode 426 frames / 14.2 seconds. They reconstruct simulated cadence; PNG capture ran slower than real time. Final replay-to-entry jump is an artificial review loop. Initial test-fixture hash API and HTML output encoding errors were corrected before final reports; neither changed art or game code.

## Next action
Owner can review index.html or the native replays alongside the existing private animation gallery. No known remaining head/neck issue in the reviewed scope. Normal roster integration remains a separate decision; other furniture, interruptions and fresh Continue are not established by this bounded fixture.
''',encoding='utf-8')
status=R/'docs/CURRENT_STATUS.md';old=status.read_text(encoding='utf-8-sig')
entry='''## Krusher Dom station-scale handoffs checked — October 15, 2026

V11 art retained after review of all 198 contextual handoff plans / 72 turns at
the world actor ruler. Actual default-bunk entry, sleep, exit and idle advanced
with production actor updates in both equipment variants: 852 native frames,
32 pose/action changes, all authored bunk sources reached, 4,317 checks / zero
failures. No further head/neck defect observed. All 2,947 fingerprinted owner
files unchanged. Native replays reconstruct 30Hz simulation cadence; capture ran
slower than real time. Normal roster integration remains separate.
[Review](../character/krusher-station-motion-v1/index.html) and
[handoff](../character/krusher-station-motion-v1/HANDOFF.md).

'''
if not old.startswith('## Krusher Dom station-scale handoffs checked'):status.write_text(entry+old,encoding='utf-8')
print({k:v for k,v in summary.items() if k not in ['media','limits','visualResult']})
