from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
native=json.loads((R/'output/bill-carry-east-start-station-v4/validation.json').read_text());join=json.loads((R/'character/bill-carry-start-east-v4/join-diagnostic.json').read_text())
assert native['passed'] and join['passed']
lesson='''
## Bill cardinal carry comparison and East floor correction — October 1, 2026

`character/bill-carry-cardinal-audit-v2` inventories latest eight paired profiles:
East gait3/start4, South gait2/start1, West gait2/start2, North gait1/start1.
Current hashes, physical opaque bounds, same-pixel source/detail boards and
animated fixed-pivot master comparisons retained; initial pre-East measurements
and boards preserved. All profiles keep nominal148/pivot128,224,840ms walk and
320ms entry; East8poses versus other directions6. All final bridge contacts
match their referenced gait0. This is staged source coverage, not full Bill or
normal-runtime/lifecycle completion.

Audit found East bridge soles223,223,222,220,224,224 against directional master
223. New gait3 shifts whole original gait figures up1px; start4 preserves exact
held0, rigidly translates interior rows1/2/3 by0/1/3px, and byte-copies corrected
gait0 into4/5. All now opaque sole223. Entire RGBA and alpha count preserved;
no resampling, recoloring, invented anatomy or per-pose ruler. Original artwork
and runtime clocks unchanged; original upper pixels move with the whole body.

138 source/metadata/pixel-preservation/input/paired-endpoint checks pass. Native
actual main/workshop prescribed South-to-East turn, bridge and two East cycles
passes2337checks0failures/55.98s, both gears; all6entry/all8gait rows exercised.
78 native/source samples generated;48 staged views visually reviewed. Recorded
source selections and both exact turn/bridge/gait joins independently checked;
gait resumes.104 then next60Hz sample slot1. Scratch APPDATA; all2931 owner
non-log files unchanged. Source comparison browser reviewed bare148 and helmet82.

Lesson: nominal height and an exact final texture join do not establish floor
registration throughout the entrance. Measure each authored interior against
its own directional master. Whole-figure shifts preserve connected anatomy;
do not stretch isolated legs or equalize differing directional-master silhouettes.
Front/back opaque sole variation of1–2px can include projected swing/heel pixels;
do not blindly flatten those rows by a maximum-pixel rule. Anatomical support
and contact cadence still require motion evidence. North remains visually a
short shuffle beside side-view strides, and needs physical travel/stance review.

No normal selection, Title Continue, inventory/floor-prop semantics, commit or
release change. East candidate retains existing turn-only start player; direct
pickup entry and all-direction lifecycle admission remain open. Earlier return
and stow packages still bind their older source banks and must be reconciled
before adoption. Next: integrate the latest cardinal source choices into one
staged controller and test natural short/long routes and arrival, then lifecycle
interruptions/snapshot/Continue. Full Bill objective remains active/incomplete.
'''
for rel in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/rel).open('a',encoding='utf-8') as f:f.write('\n'+lesson)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+lesson)
status=R/'docs/CURRENT_STATUS.md';old=status.read_text(encoding='utf-8');status.write_text(lesson.strip()+'\n\n'+old,encoding='utf-8')
assessment={'reviewedBoards':['bare-all-gaits.png','bare-leg-detail.png','helmet-all-gaits.png','../../output/bill-carry-east-start-station-v4/staged-bare-review.png','../../output/bill-carry-east-start-station-v4/staged-helmet-review.png'],'browser':[{'gear':'bare','size':148,'motion':'gait'},{'gear':'helmet','size':82,'motion':'bridge'}],'sourceChecks':138,'native':native,'recordedSourceEvidence':join,'normalSelectionChanged':False,'remaining':['North physical stride/contact review','Latest cardinal controller and natural routes','Older return/stow source bindings','Full animation set and polish']}
(P/'review-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
handoff='''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: Bill cardinal carry audit

## Objective and acceptance
Full master-matching Bill animation set, then consistency/polish. This scoped
milestone compares current cardinal carry sources and repairs East floor drift.

## Accepted decisions and constraints
Original directional masters and proportions, paired matte detail, existing
reversible authorization. No pose stretch/regrade or equalized direction boxes.
Preserve other character work, owner geometry and saves; full goal stays open.

## Current state
Audit-v2 eight-profile coverage/hashes/bounds, animated HTML and source/detail
boards. New East gait3/start4 rigidly registered PNGs/metadata/preview player,
native fixture/runner with UIDs, builders/verifier/join diagnostic. Old sources
and audit pre-repair evidence retained. Pipeline/bible/skill guidance updated.

## Verification
138 package checks. Native2337checks0failures/55.98s; both equipment versions,
all6bridge/all8gait slots, two walking cycles and actual service progression.
78room/source samples,48 staged views reviewed. Independent recorded source
agreement, exact joins and.104-to-slot1 proof. Scratch APPDATA,2931 owner files
unchanged. Browser source comparison bare148/helmet82. No normal adoption.

## Next action
Unify latest cardinal source choices in one staged controller. Test direct
pickup, planted turns, natural short/long carry and partial arrival. Reconcile
old return/stow banks before admission; North visible shuffle still needs
physical travel/stance review. Lifecycle interruptions and fresh Continue open.
Full action set incomplete; do not mark goal achieved from this scoped evidence.
'''
for root in [P,R/'character/bill-carry-east-gait-v3',R/'character/bill-carry-start-east-v4']:(root/'HANDOFF.md').write_text(handoff,encoding='utf-8')
print('Recorded current cardinal evidence, East correction and remaining full-scope work; exact source records',join['exactRecordedSourceSelections'])
