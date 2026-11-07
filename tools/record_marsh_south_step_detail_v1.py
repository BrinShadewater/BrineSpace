"""Record selected whole-pose revision, rejected framing and actual visual scope."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'character/marsh-south-step-detail-v1';NORMAL=ROOT/'character/marsh-v2/supplemental/south-step-detail-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
for v in ['01','02']:
    req=read(SOURCE/f'candidate-{v}.request.json')
    assert sha(ROOT/req['result']['rawPath'])==req['result']['sha256']
    assert all(sha(ROOT/r['path'])==r['sha256'] for r in req['references'])
p=SOURCE/'fixed-canvas-comparison.json';r=read(p)
r['visualReviewed']=True;r['normalAdmission']=True
r['reviewedBoards']=[{'file':n,'sha256':sha(SOURCE/n),'actuallyInspected':True} for n in ['comparison-2x.png','neighbors-candidate02.png']]
r['selection']={'rejected':'01','selected':'02','reason':'01 shrinks original pose to86.18%height and raises sole20pixels at fixed canvas scale.02 preserves crown,sole-1pixel,height99.34%,opaqueIoU.95268; whole collar/harness construction closer to own idle/master and neighboring pose. Detail/grade/cadence/contact/full-family polish still provisional.','admissionReceipt':'character/marsh-v2/supplemental/south-step-detail-v1/admission.json'}
p.write_text(json.dumps(r,indent=2)+'\n')
p=NORMAL/'verification.json';r=read(p)
for b in r['boards']:assert sha(NORMAL/b['file'])==b['sha256'];b['actuallyInspected']=True
r['visualScope']='All seven native old/selected/own-idle source/station captures actually inspected in four complete boards. Whole source master comparison and seven-pose neighborhood reviewed. Sampled stateful player playback, not continuous watched cadence or natural actor floor-contact/fullSave/Continue acceptance.'
r['sourceComparisonSha256']=sha(SOURCE/'fixed-canvas-comparison.json')
p.write_text(json.dumps(r,indent=2)+'\n')
latest=ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-south-step-detail/inventory.json'
r=read(latest)
r['heldReviewEvidence']={'previousInventory':'character/marsh-selected-normal-audit-2026-10-03-post-cargo-alias/inventory.json','previousInventorySha256':sha(ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-cargo-alias/inventory.json'),'unchangedStates':227,'revisedState':'walk-step-south','verification':p.relative_to(ROOT).as_posix(),'verificationSha256':sha(p),'scope':'Prior whole-source coverage retained for227unchanged states; all seven current short-step poses inspected in own-master/neighborhood and native source/station comparisons. No full quality/motion/contact acceptance.','fullGoalComplete':False}
latest.write_text(json.dumps(r,indent=2)+'\n')
note='''
## Marsh South short-step whole detail revision — October 3, 2026

Compared actual selected phase3 with original South standing identity, current
own idle and all seven neighboring step poses. Collar/harness construction was
weaker than authority. Two built-in whole-pose edits with exact prompts/references/
result receipts, raw sources immediately copied into character/marsh-south-step-detail-v1.
First edit01 rejected: normalized opaque height131vs152 (86.18%),sole20pixels up,
crown1down,IoU.61694. Do not repair by fitting occupied pose bounds. Retry02 used
equally sized1024square nearest-expanded target/idle references and explicit crown/
sole/stride anchors. Actual raw1254square; one whole-canvas184/1254factor.02opaque
height151vs152 (99.34%),crown unchanged,sole1pixel up,IoU.95268. Collar/harness detail
closer to master/own idle; whole before/after/master and full neighboring board
actually inspected. Original master display uses fixed standing147/1232scale,
independent of candidate poses. No pose fit/pivot shift/alpha patch/head or limb
splice/recolour. Alpha thresholds are measurement only; raw alpha preserved in
whole-canvas resampling. Small head/material/detail/grade differences remain.

Normal final overlay character/marsh-v2/supplemental/south-step-detail-v1 selects
ONLY walk-step-south phase3 revision02. Six other drawings and all original
timing/facings/waterKinds/depth/pivot/H/stride metadata retained;227other states
exact. Source is used only at this state/slot; no shared-pose aliases missed.
228normal body states/1190slots/88ordered body manifests. Existing PNG whole paths
retained; no gameplay/actor/contact/room/resource/save changes, no commit/export.

Actual normal body/equipment player50checks/0failures,7exact source slots, stateful
and elapsed clocks,7same-clock restores and7complete native old/selected/own-idle
source/station captures. All four capture boards actually inspected.5311bounded
source/runtime/art inputs and2931owner non-log files unchanged under scratch APPDATA.
Engine terminalexit0,no ERROR/WARNING/SCRIPT ERROR. This is bounded source/player
progress, not continuously watched cadence or natural actor/floor/fullSave/Continue
acceptance. Raw generation detail alone did not justify the first candidate.
Latest authoritative inventory:
character/marsh-selected-normal-audit-2026-10-03-post-south-step-detail/inventory.json.
Prior74complete family held reviews retain evidence for227unchanged states; revised
seven-pose state has new master/neighborhood/native review. Full objective active.

Lesson: a tiny pose target plus larger original master can yield attractive detail
while shrinking/reframing the body. Equal-sized pose/idle reference canvases and
explicit foot/crown anchors helped this retry preserve geometry; one successful
result is not a guarantee. Inspect fixed whole-canvas registration before selection,
retain rejection/raw/receipt, and compare all neighbors at actual density. Do not
hide shrinkage with per-pose fitting. Next moving/native actor contact and full-set
head/detail/material/camera/grade joins against actual original directional masters.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for q in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with q.open('rb') as f:f.seek(max(0,q.stat().st_size-100000));tail=f.read().decode('utf-8',errors='ignore')
    if '## Marsh South short-step whole detail revision' not in tail:
        with q.open('a',encoding='utf-8') as f:f.write(note)
installed.write_bytes(canonical.read_bytes())
print('Two source receipts verified,01rejected/02selected;master/neighbors and all7native captures reviewed;pipeline/bible/status/skill recorded')
