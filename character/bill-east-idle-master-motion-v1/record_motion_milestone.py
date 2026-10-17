from pathlib import Path
from PIL import Image
import json,hashlib,shutil,numpy as np
R=Path.cwd();P=R/'character/bill-east-idle-master-motion-v1';N=P/'native';S=R/'character/bill-east-idle-master-consistency-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();proof=json.loads((N/'verification.json').read_text());report=json.loads((P/'motion-review.json').read_text())
for file,h in proof['captures'].items():assert sha(N/file)==h
for page in proof['pages']:assert sha(N/page['file'])==page['sha256'];page['reviewed']=True
assert sha(P/'motion-review.json')==proof['motionReviewSha256'];shutil.copy2(P/'motion-review.json',N/'motion-review-native-input.json')
for file,h in report['frozenInputs'].items():assert sha(R/file)==h,file
adj=[]
for i,j in [(0,1),(35,36),(71,0)]:
 x,y=[np.array(Image.open(P/f'frames/idle-east/{n:03}.png').convert('RGBA')).astype(float) for n in [i,j]];adj.append({'pair':[i,j],'alphaMaskChanges':int(((x[:,:,3]>127)!=(y[:,:,3]>127)).sum()),'premultipliedMeanAbsoluteRGBChange':float(np.abs(x[:,:,:3]*x[:,:,3:]/255-y[:,:,:3]*y[:,:,3:]/255).mean())})
proof.update(visualReview='All five native pages/nine actual player captures inspected at H148/82/54/27. Warmer readable face and detailed matte suit stay coherent across observed breathing phases. Fixed source face/feet and no gross size pop. Source density evidence only, not natural actor/world floor/continuous watched cadence or full identity acceptance.',adjacentDiagnostics=adj,currentPhaseBoardSha256=sha(P/'phase-review.png'),currentPreviewSha256=sha(P/'index.html'));report['visualReview']='Complete selected/repaired phase board and all nine engine source-density captures actually inspected. Master face/material definition improved, full breathing replay eliminates independent redraw surface noise. No continuous watched cadence/worldcontact/actionjoin/fullset acceptance.';report['nativeRun']=True;report['nativeVerification']='native/verification.json';(P/'motion-review.json').write_text(json.dumps(report,indent=2)+'\n');proof['currentMotionReviewSha256']=sha(P/'motion-review.json');(N/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
lesson='''\n\n## Bill East complete master breathing replay — October 3, 2026

New character/bill-east-idle-master-motion-v1 replaces independent phase redraw
noise with the existing accepted chest-only animation recipe from one original-
master-guided whole-pose source0. Before reuse, recipe reconstructs ALL72selected
East RGBA frames exactly. Full72slots/37distinct phase groups/3000msdurations retained;
1.25pxchest expansion/.65pxrise, headrows0:53andfeet121:183exact at every phase.
This is motion authoring from generated artwork, not local identity painting,
recolouring, anatomical fitting, static holds or a reduced phase count. Seven
independent prior art studies retained as source/material diagnostics; thirty
additional independent redraws are not needed to replay the proven full motion.

First build failed exact phase0RGBA: premultiplied roundtrip cleared invisible RGB
in transparent chest pixels. Failed builder/72frames archived; zero-displacement
phase now uses source unchanged. Full144decoded normal/slow APNG frames exact.
Source donor0exact and all37originalduplicate groups preserved.

Actual normal Grid/Billplayer, fixture-only full idle override:448checks/0failures,
engine0/13.17s,all72source/cursor/snapshot checks, two wraps,nine density captures.
3688bounded inputs and all2931owner non-log files unchanged under scratch APPDATA.
Nine actual captures/five pages and selected/new phase board inspected. Improved
warm face/matte quilt remains coherent at H148/82/54/27. Source-player proof does
not certify main/world floorcontact, natural behavior, continuously watched
cadence,actionjoins/fullSave/TitleContinue or normal admission. Candidate unselected.
New tools keep paired .gd.uid;3Python AST/162PNG LFS checked including failed evidence.

Lesson: before reauthoring dozens of near-identical phases, inspect the accepted
motion recipe. Replay the entire proven chest envelope from improved generated
source, pin identity/support contacts, verify original replay pixel-exactly and
bind motion derivation separately from new art generation. Preserve all frames
and exact durations. Identity motion must preserve hidden RGBA as well as visible
appearance. Next idle/interact/sourcecontact joins and actual-world cadence; then
other cardinal/gear/water/life families and whole-library master polish.
Full Bill objective remains active/incomplete.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for root in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:
 for name in ['crew-consistency.md','source-density.md']:paths.append(root/'references'/name)
for path in paths:
 with path.open('a',encoding='utf-8') as f:f.write(lesson)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-03 · Project: Brine Space · Task: Bill East complete master breathing

## Objective and acceptance
Full Bill animation library faithful to original masters/style/perspective/physical size/proportions/matte grade, then full cross-family polish and normal runtime verification. Goal active/incomplete.

## Accepted decisions and constraints
Original master authority. New whole-pose source authored with built-in tool; existing accepted chest-only motion replay permitted by maintained crew/source-density guidance. No local identity painting, grade, anatomical fitting or part splice. Source H148/p92,172/184canvas. Normal assets/loader untouched; no commit/export. Godot always scratch APPDATA/owner fingerprints.

## Current state
Full72slot/37distinct phases/3000ms East breathing candidate from improved generated source0. Recipe replay proved exact all72selected RGBA before use. Fixed head/feet, original timing/duplicate groups, manifest, normal/slow APNGs, phase board,index.html,motion-review.json,native9captures/5pages/verification. First build hiddenRGB roundtrip failure archived in failed-build-v1; identity phase copies complete source unchanged. Prior7independent phase studies kept; no30more redraw requirement since full37phase motion is reproduced.

## Verification
72head/feet exact,source0exact,37groups intact,144APNG decoded frames exact. Native448checks0,engine0/13.17s,3688inputs/2931owner non-log files unchanged. All72actualplayer sources/clocks/snapshot restores/two wraps,nine density captures. Full phase board/all5native pages inspected; warmer face/matte detail stable at H148/82/54/27.3Python AST/162PNG LFS including failure evidence. No continuous watched cadence/main-worldcontact/natural actor/actionjoin/fullsave/titleContinue/normal admission acceptance.

## Next action
Review full breathing continuously and actual actor floor/contact; join to master-consistent interaction/cargo/gaits without1pxsourcecontact or head/material seams. New idle0 differs from older interaction study0, so that join is unresolved. Other East states/helmets, West48phase head/material source bank, North/South/water/life actions and whole-set polish remain open. Goal active,no blocker.
''',encoding='utf-8')
with (S/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\nFull breathing motion now packaged separately in character/bill-east-idle-master-motion-v1/HANDOFF.md,72slots/37phases/3000ms via pixel-proven accepted recipe. Seven redraws retained; no30more redraws required for coverage. Idle/action/worldcontact joins and cadence remain pending.\n')
print(json.dumps({'nativeChecks':448,'nativeFailures':0,'pagesReviewed':5,'adjacentDiagnostics':adj,'recordsUpdated':8}))
