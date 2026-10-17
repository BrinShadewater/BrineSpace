from pathlib import Path
import json,os,uuid,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
n=json.loads((P/'validate-evidence.json').read_text());v=json.loads((P/'validate-validation.json').read_text())
c=json.loads((P/'continue-evidence.json').read_text());cv=json.loads((P/'continue-validation.json').read_text());k=json.loads((P/'candidate-checks.json').read_text())
for native,guard in [(n,v),(c,cv)]:assert native['failures']==0 and guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
assert len(n['cases'])==24 and len(c['cases'])==3 and all(case['completed'] for case in c['cases'])
def atomic(path,data):
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(data);os.replace(temp,path)
review={'status':'controller_interruption_visual_defect_confirmed_candidate_staged','runtimeInstalled':False,'fullSetComplete':False,'interruption':{'checks':n['checks'],'cases':24,'captures':len(n['records']),'profileGuard':v,'scope':n['scope']},'continue':{'checks':c['checks'],'cases':3,'captures':len(c['records']),'profileGuard':cv,'scope':c['scope']},'visualFinding':'All72 interruption captures/four boards reviewed: actual paid work/contact and sparks behavior pass, but direct state idle creates an abrupt arm/tool disappearance and restored state snaps back to work pose. This is not visual acceptance. All21 fresh Continue views reviewed on one board; saved source and progress are exact. North after-restore camera differs by242viewport pixels; one fixed post-restore crop used for six captures, no sprite transform or height normalization.','candidate':k,'candidateVisualReview':'Four eight-sample-per-phase source boards reviewed; original whole poses, fixed148 ruler/pivot, retained entry and resumed source exact, idle seam exact, no color/material/shape changes. Candidate is source choreography, not actual controller proof.','remaining':['Generalize to arbitrary actual source indices; integrate stow/return while preserving paid work, safety precedence, contact and progress','Capture every new native source transition, including repeated loss/restoration during exit/return','Fresh disk Continue inside new interruption motion and all facing-phase combinations','Repair effect/contact and full James consistency, owner/export acceptance']}
atomic(P/'selection-review.json',(json.dumps(review,indent=2)+'\n').encode())
for path in [R/'character/james-construction-controller-v2/selection-review.json',R/'character/james-torch-material-residue-v2/selection.json']:
    old=json.loads(path.read_text());old['constructionInterruptReview']={'path':'character/james-construction-interrupt-v1/selection-review.json','simulationVerified':True,'visualDefectUnfixed':True,'candidateInstalled':False,'freshContinueCases':3}
    old['remaining']=review['remaining'];atomic(path,(json.dumps(old,indent=2)+'\n').encode())
block='''## James construction interruption defect and fresh Continue — October 1, 2026

character/james-construction-interrupt-v1:24 actual power/door holds across draw,
weld and stow, four bare directions/four real paid jobs.1581native checks pass,
72captures/four boards reviewed. Work/contact/reservation preserved, sparks stop,
access resumes original work, paid rooms finish. Visual defect remains: shared
construction changes state directly to idle, dropping the arm/tool immediately;
restored access jumps directly back to the current work pose. Passing simulation
checks do not establish smooth motion. Preserve these baseline artifacts.

Three actual fresh-scene disk Continues pass1104checks: North partial draw, East
held weld, South partial stow. Exact actor/playback/source RGBA/visual clock/pause,
paid order and metal restored; paused no advance; normal60Hz update finishes each
job without another charge or replay.21views reviewed on one board. Both native
jobs engine0/no timeout/scratch APPDATA/strict owner profile unchanged. Not all
facing-phase pairs or interrupted-transition checkpoints. Fresh North camera is
242viewport pixels lower; crop once per restored scene, not per source pose.

Uninstalled source candidate uses existing selected whole poses: reverse partial
draw; finish remaining stow; retain current held source50ms then authored stow;
return by exact reversed exit. Twelve observed entry poses/four directions,
24finite states/316refs/113existingPNGfiles/zero new artwork;60source checks,
four sampled boards reviewed. Retained start/resumed RGBA and neutral seams exact,
fixed148 ruler/pivot/material/alpha unchanged. Duplicate weld slots can be pixel-
equivalent; equality does not identify a unique source index. No current runtime
fix or complete source-motion acceptance claim; candidate remains staged.

Next generalize arbitrary source phases, integrate actual exit/hold/return with
paid work preserved and safety precedence, review every native transition, repeat
interruptions and fresh Continue inside the new motion. Then repair contacts and
full cross-family/gear/furniture/rotation polish/owner/export acceptance. Full
James goal remains active/incomplete. Handoff: this folder/HANDOFF.md.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i,path in enumerate(paths):
    old=path.read_bytes();new=block.encode();assert new not in old;atomic(path,new+old if i==0 else old+b'\n\n'+new)
handoff='''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James construction interruptions

## Objective and acceptance
Complete full James animation/master consistency and cross-family polish. Active
and incomplete. Native interruption motion has a confirmed defect; candidate
source choreography is staged/uninstalled, not owner accepted.

## Accepted decisions and constraints
Paid work survives power/door holds; sparks stop immediately and construction
targets the doorway. Bare eligibility. Exact selected matte whole poses,148
standing ruler/p92,172, planted contact and belt wrench. Safety must precede
work animation. Preserve concurrent actor changes and owner data.

## Current state
validate.gd/.uid:24 actual power/door holds,72views/four reviewed boards.
continue.gd/.uid:three actual fresh-scene disk saves,21views/one reviewed board.
build_candidate.py:24uninstalled finite source aliases/316refs/113original PNGs,
exact reversal/neutral joins, four sampled boards/GIFs, bindings/source hashes.
selection-review.json/evidence, parent James selections and five guides updated.
No runtime/artwork installation or currently running process from this turn.

## Verification
1581interruption and1104Continue checks0fail. Both engine0/no timeout/strict owner
unchanged/scratch APPDATA. Continue restores exact actor/playback/clock/source
and paid order, pause, finishes once/no re-charge. North fresh camera shifted242
viewport pixels; fixed post-restore scene crop, no per-pose transform. All72+21
native views reviewed. Simulation pass exposes visual failure: idle arm drops
instantly and restored work snaps back. Candidate60source checks only; no native
controller proof. Four candidate boards sample8poses per phase; not all316refs.

## Next action
Generalize exit/return source sequences to arbitrary selected indices, integrate
actual James controller without bypassing safety; hold paid progress during tool
transitions; fixed contact. Capture all source changes; repeated interruption
mid-exit/mid-return; fresh Continue inside new motion. Existing candidate is a
12observed-entry proof, not a hardcoded solution for those twelve only. Then
repair contacts and wider family/gear/furniture/rotation owner/export polish.
'''
atomic(P/'HANDOFF.md',handoff.encode())
print(json.dumps({'interruptionChecks':n['checks'],'continueChecks':c['checks'],'candidateChecks':k['checks'],'runtimeInstalled':False,'visualDefectUnfixed':True,'guidesUpdated':5}))
