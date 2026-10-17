from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];A=R/'character/veld-animation-coverage-audit-v1'
e=json.loads((A/'side-carry-master-evidence.json').read_text(encoding='utf-8'))
for relative,digest in e['bindings'].items():assert hashlib.sha256((R/relative).read_bytes()).hexdigest()==digest,relative
e['reviewedBoards']=e['boards'];e['visualReview']='Both original-master boards/all12presentations inspected. Current East/West carry head/face/bun breadth exceeds approved originals at same physical ruler, including owner-approved West v7. Proxy widths27master vs35–36carry support visual finding, not precise skull measurement. Gait foreshortening is preserved, not per-pose height normalized. Source repair warranted; original motion/gear joins and shared colour still govern.'
(A/'side-carry-master-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
crosspath=A/'cross-family-review-evidence.json';cross=json.loads(crosspath.read_text(encoding='utf-8'))
snapshot=A/'selected-library-before-status-promotion.json'
if not snapshot.exists():snapshot.write_bytes((A/'selected-library.json').read_bytes())
assert hashlib.sha256(snapshot.read_bytes()).hexdigest()==cross['inventorySHA256']
cross['inventorySnapshotPath']=snapshot.name
crosspath.write_text(json.dumps(cross,indent=2)+'\n',encoding='utf-8')
for version,folder in [('1',P),('2',P/'v2-study')]:
    reg=json.loads((folder/'study-registration.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((P/f'raw-v{version}.png').read_bytes()).hexdigest()==reg['sourceSHA256']
    reg['sourceComparisonViewed']=True
    reg['visualReview']='All6whole-body source comparisons inspected; v1still32–33pxhead breadth and rejected as final repair' if version=='1' else 'All6whole-body source comparisons inspected; v2head breadth27–28pxmatches master27pxproxy, connected shoulders/hips/case retained in static samples. Promising ungraded source candidate; no helmet/native/motion/admission acceptance.'
    (folder/'study-registration.json').write_text(json.dumps(reg,indent=2)+'\n',encoding='utf-8')
block='''## Veld West carry master proportions source repair — October 2, 2026

Direct approved side-foundation comparison/all12East/West source presentations
confirms broader carry head/face/bun at sharedH148:top20pxsilhouette27master,
29–30idle,35–36currentcarry (includes bun/collar, not skull measurement). Current
West v7 was owner-approved but still drifts under direct original-master review.
Do not use its historical v6 audit measurements as current source evidence.

Two built-in imagegen edits/exact prompts/reference hashes/raw/execution metadata
retained at character/veld-carry-west-master-proportions-v1. V1ungraded32–33pxhead
breadth rejected as final repair; V2exactWest high-density master crop reference
and targeted correction yields27–28px. All six V2whole-source comparisons viewed:
compact original proportions, connected body/case grip and phase order retained
in static samples. Singlefirst-pose148ruler/floor, no per-pose height normalization.
No grading, helmet manifests, native/motion test or selected source replacement yet.
Next fixed source-family material calibration, sharedWest helmet fit, original
840msmetadata/joins and advancing native review before paired adoption. East and
South carry/other directional source polish remain in the full objective.

Normal South partial fall status now selected; exact tested manifests retained in
verified-manifests and normal-admission.json proves status-only change.166selection
checks0fail, source/profile/timing unchanged; no runtime rerun for descriptive field.
Normal85500check interval retains its original hashes rather than being rewritten.
Pre-status inventory snapshot retains prior80source comparison binding; refresh
current inventory separately. Full natural gameplay and cross-library polish open.

Lesson: original high-density masters plus measured body-relative comparison are
needed even after an approved detail pass. Repeated vague smaller-head prompts
can under-correct; view registration and actual source proportions before grading.
Silhouette proxies support visual review without certifying anatomy or motion.
Full goal active/incomplete. No commit/export.

'''
for dest in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
    old=dest.read_text(encoding='utf-8')
    if block.splitlines()[0] not in old:dest.write_text(block+old,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld West carry proportions

## Objective and acceptance
Full master-consistent Veld set and cross-family polish. Repair current oversized
side carry heads while preserving accepted gait, connected body, matte materials,
case grip, shared helmet and840msmetadata. No full-set completion claim.

## Accepted decisions and constraints
Original approved West side foundation governs identity/body-relative proportions;
currentcarry v7 supplies gait only. No per-pose normalization or independent grades.
Use authored whole bodies; protect original selected sources until paired review.

## Current state
raw-v1/v2.png, prompts, reference hashes and execution metadata retained. V1 study
is partial correction; V2raw2100x749RGBA plus v2-study contains six deterministic
extractions and all-source comparison. Accepted original West crop exactly from
side-master-01 bounds931/51/1187/962, no resize/grade. Candidate remains unselected.

## Verification
Original/current East/West boards/all12presentations viewed. Mastertop20px27 vs
currentcarry35–36. V1study32–33; V2study27–28, six connected bodies and alternating
phases inspected. These are silhouette proxies including bun/collar. Fixed148first
pose ruler and common floor; no material/helmet/native/fullmotion acceptance yet.
Source provenance retained; no selected image/controller change for this repair.

## Next action
Match one pooled West-master material transform, inspect skin/hair without flattening
fine detail, fit actual sharedWest helmet and keep collar continuity. Package original
timing/stride/pivot in paired candidate; review allframes/loop seam/source-native gait
and case/foot handoffs before adoption. Extend master proportions repair to East and
South as warranted; side sit/read and natural full-game coverage remain open.
Normal South partial bundle is verified/statusselected with tested bytes retained.
Audit snapshots preserve earlier intervals. No commit/export; full goal active.
''',encoding='utf-8')
normal=R/'character/veld-sofa-partial-fall-south-selected-v1/HANDOFF.md'
old=normal.read_text(encoding='utf-8')
note='''\n## Verified metadata closeout\nPaired descriptive status promoted to selected after normal proof. Exact tested\nbytes in verified-manifests; normal-admission.json records before/after hashes\nand exact runtime/source equality. Builder retains selected status.166selection\nchecks0fail; no new runtime/art change. Prior pending-status next step superseded.\nCurrent original-master source repair lives in veld-carry-west-master-proportions-v1.\n'''
if '## Verified metadata closeout' not in old:normal.write_text(old+note,encoding='utf-8')
print('Source studies/master comparisons/metadata closeout recorded; five references updated')
