from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
native=json.loads((p/'actor-return-v9-evidence.json').read_bytes())
guard=json.loads((p/'actor-return-v9-validation.json').read_bytes())
inputs=json.loads((p/'actor-return-v9-inputs.json').read_bytes())
cases=[c for c in native['results'] if 'trace' in c]
assert native['checks']==991 and native['failures']==0 and len(cases)==6
assert sum(len(c['trace']) for c in cases)==48
assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
refs=json.loads((p/'reference-evidence.json').read_bytes())
assert all(hashlib.sha256((r/c['path']).read_bytes()).hexdigest()==c['sha256'] for c in refs['sources'])
prior=json.loads((p/'actor-return-v7-evidence.json').read_bytes())
prior={(c['mode'],c['target']):c for c in prior['results'] if 'trace' in c}
unchanged=0
for c in cases:
    if c['target']=='workshop_carry':continue
    old=prior[c['mode'],c['target']];assert len(old['trace'])==len(c['trace'])
    for a,b in zip(old['trace'],c['trace']):
        for key in ['source','world']:
            assert hashlib.sha256((r/a[key].removeprefix('res://')).read_bytes()).digest()==hashlib.sha256((r/b[key].removeprefix('res://')).read_bytes()).digest()
        unchanged+=1
assert unchanged==10
package=json.loads((p/'package-v9-evidence.json').read_bytes())
assert package['protectedOriginalRgbaChecks']==225280 and package['protectedCandidateBodyRgbaChecks']==299008
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    tmp.write_bytes(new);assert path.read_bytes()==old;os.replace(tmp,path)
review_path=p/'actor-return-v9-review.json';review=json.loads(review_path.read_bytes())
review.update(visualReviewPending=False,
    reviewed='38 changing carry native source/world pairs inspected in two boards, plus14 registered master/source presentations. Other10 pickup/unload source/world pairs byte-exact to reviewed V7 captures. Original upper-region restores exact head/goggles/helmet size. V8 last interiors less frontal/slimmer than V7, feet stay planted. Head orientation switch at third interior and upper/lower collar/shoulder joins still need continuous motion polish; complete master/material consistency remains unaccepted.',
    continuousNativeMotionAcceptance=False,fullMasterMatchAcceptance=False,completeReturnAcceptance=False)
atomic(review_path,(json.dumps(review,indent=2)+'\n').encode())
report={'selected':False,'fullGoalComplete':False,'checks':991,'failures':0,'actualPrescribedReturns':6,
    'nativeSourceWorldPoses':48,'newCarryPosesVisuallyReviewed':38,'unchangedPreviouslyReviewedPairsVerified':10,
    'registeredSourceMasterPresentationsReviewed':14,'originalUpperRegionRgbaChecks':225280,
    'candidateLowerBodyRgbaChecks':299008,'frozenTargetedInputsUnchanged':21,'originalReferenceHashesUnchanged':6,
    'ownerProfileUnchanged':True,'originalHeadSizeUpperRegionRetained':True,'completeVisualJoinAccepted':False,
    'sourceReplay':'actual-return-v9-source-replay.gif','sourceReplayIsContinuousNativeMovie':False,
    'remaining':['Continuous head-orientation/collar/shoulder join polish.','Full body material/proportion matching against masters.','Explicit floor-case/standing handoff.','Paired ordinary RunSave/Continue and production admission.','Remaining cardinal/layout contexts and full cross-family James consistency.']}
(p/'study-review-v9-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
section='''## James West bridge v8 correction and original-headed v9 — October 2, 2026

Built-in v8 raw edit/prompt retained: later interiors less frontal/slimmer and
generated helmet enlarged. New raw bare ruler414, row boundary448, shared148/414
scale. First two V7 bare/helmet lower-body candidates protected205824RGBAchecks.
Actual v8 six returns991checks0fail,38changed carry presentations reviewed; other10
source/world pairs byte-exact to prior review. Measured generated helmet alpha
tops73/72/71/71 versus original68carry/66unload still fail exact shared-shell size.

V9 keeps V8 coherent body below110 exactly and original endpoint upper rectangle
above110 (carry first two, unload last two).225280original-region plus299008
candidate-body RGBAchecks; not semantic head masks. Original endpoints/pivots/ruler
retained. Registered14presentations inspected: original face/goggles/helmet size
restored, later stance closer. Upper/lower collar/shoulder seam and third-interior
head orientation switch still need continuous motion polish. Full body material/
proportion and complete visual join acceptance remain pending; candidate unselected.

Actual v9 six prescribed pickup/carry/late-unload returns991checks0fail.38changed
carry native source/world pairs reviewed; other10pairs byte-exact to reviewedV7.
Engine0/no timeout/whole owner profile unchanged scratch. All21targeted prelaunch
hashes and six original hashes unchanged; not whole-world dependency freeze.
V8/V9 package runs also scratch/engine0. LFS filter verified for raw8/interior9.
19paired captured native source drawings replay at2120ms plan plus700ms viewer hold,
one common GIF palette. Replay is reconstructed source timing, not native world movie
or authored loop. Explicit floor-case/idle and ordinary return Continue still pending.

Lesson: sheet edits can change row spacing and source ruler; inspect actual cut line
before reusing extraction. Compare helmet scalp height at registered native scale,
and retain original upper artwork where that geometry fits coherent body changes.
Pixel-exact retained regions do not certify the new collar/shoulder join. Next full
continuous joins/material polish, crate floor handoff/Continue, remaining contexts
and full James master/cross-family consistency. Full goal active/incomplete.
Evidence: character/james-cargo-return-bridges-v1/study-review-v9-evidence.json,
bridge-v9-registered-review.png and actual-return-v9-source-replay.gif.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
    r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',
    Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:
        atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James cargo return original-headed bridge

## Objective and acceptance
Full James set matching master identity/material/perspective/height/proportions;
then cross-family consistency. Full objective active/incomplete, candidate unselected.

## Accepted decisions and constraints
Original endpoint authority and declared pivot/ruler. Coherent body rotation,
planted feet, no per-frame grade/height normalization. Live needs/safety, union
clearance for changing poses. Unsupported candidate return snapshots reject normal
saves; production/room geometry unchanged. Every native run scratch APPDATA.

## Current state
V8 raw/prompt/package correct late body stance but generated helmet size fails.
V9 exact original upper rectangle above110 on V8 exact coherent body below110.
Native package/paired UIDs/manifests/reviews and timed source replay retained.
Five guides updated. No production selection change, commit or export.

## Verification
V8 and V9 each991checks0fail/six prescribed actual returns. V9:38new carry source/
world presentations reviewed,10other pairs byte-exact to reviewedV7;14registered
master/source panels.225280original-region+299008candidate-body pixel checks.
Engine0/owner profile unchanged scratch.21targeted prelaunch/six reference hashes
unchanged.19source-slot2120ms replay is reconstruction, not continuous world movie.

## Next action
Continuous collar/shoulder seam and third-interior head orientation polish, full
body master/material check; authored crate floor/standing disposition; paired
ordinary RunSave/Continue and production admission. Remaining cardinal/layout
contexts, West tablet edges and full James/cross-family polish. Bill floor-case
study inspected only as reference; no James floor-case asset or renderer authored yet.
Do not restore full shared source files from historical snapshots.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('V9 recorded:991checks/38new+10unchangedpairs;original upper art exact;five guides/handoff updated. Full goal incomplete.')
