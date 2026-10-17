from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;G=R/'character/bill-carry-west-gait-v2'
lesson='''
## Bill West carry material and first-step repair — October 1, 2026

Staged `bill-carry-west-gait-v2` replaces flat/light moving knee hardware with
two authored support halves referenced to the original West held master and
its enlarged leg detail. Small beveled rectangular plates, rivets, straps,
grain and compact boots are visible in source and actual-room comparisons.
Six140ms poses retain840ms/.12 stride. `bill-carry-start-west-v2` adds three
small standing weight transfers between exact held0 and byte-identical new
gait0 contact rows4/5; finite320ms, resume phase.139 then gait1.

One same-threshold physical master ruler138px calibrates each full-standing
source family; runtime nominal148 is retained, not misused as anatomical
source height. Protect original upper above153, above the knee plates, and
register at the upper-thigh axis. Old164 cuts through moving armor. Feet are
registered to opaque master sole222 by rigid whole-figure translation; all
master upper pixels move together with a small walking bob. No limb stretch,
per-pose scale/exposure or mirrored direction. Pooled neutral grade and one
shared100/.82 highlight curve. Color statistics alone cannot certify plate
construction or matte detail.

Initial unregistered gait fit retained under sources/unregistered-fit-v1;
first bridge source rejected before packaging because all three poses were
already near a full stride. Replacement prompt specifies small standing
weight shifts and omits full-stride target reference. Exact prompts/raw PNGs,
execution IDs, hashes, calibration and rejection reasons are retained.

72 gait package/2532 native checks;61 bridge package/71 headless playback
guards/2746 native checks, all pass. Native intervals47.65s/59.12s and guard
5.32s. Scratch APPDATA throughout; all2931 owner non-log files unchanged.
Four gait room/source boards40 captures with18 staged exactRGBA selections;
two bridge boards24 unique exactRGBA source selections reviewed, both gears.
Browser reviewed at82 and148. Prescribed graph-clear West lane through actual
main/workshop; these are staged checks, not natural-route, stance-lock,
interruptions, snapshot/Continue or normal-loader admission. No production
selection, owner save, inventory/floor-prop semantics, commit or release change.

Next: compare the latest East/South/West/North carry families together, then
resolve natural short/long travel, arrival/return and lifecycle adoption. The
full Bill set remains incomplete; historical package counts are scoped evidence.
'''
for f in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 path=R/f
 with path.open('a',encoding='utf-8') as out:out.write('\n'+lesson)
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
with installed.open('a',encoding='utf-8') as out:out.write('\n'+lesson)
status=R/'docs/CURRENT_STATUS.md';text=status.read_text(encoding='utf-8');status.write_text(lesson.strip()+'\n\n'+text,encoding='utf-8')
handoff='''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: Bill West carry repair

## Objective and acceptance
Continue full Bill master-matching set. This milestone repairs West moving
leg material and matching first-step entry for bare and helmet; full set open.

## Accepted decisions and constraints
Original directional held masters, paired equipment, matte detail; no mirror,
pose rescaling or exposure shifts. Existing reversible work authorized. Preserve
other character work and owner saves. Keep normal selection until lifecycle
coverage and visual fidelity are established.

## Current state
New gait-v2/start-west-v2 sources, manifests, registration, builders, verifiers,
preview actor/player, native/headless fixtures and runners with paired UIDs.
Prompts/provenance/rejected fits retained. Review HTML, GIFs and boards saved;
pipeline/bible/maintained and installed consistency guidance updated.

## Verification
72 gait package +2532 native;61 bridge package +71 headless +2746 native,
zero failures. 40 gait native/source samples and24 unique bridge/gait selections
visually reviewed with exact source agreement. Scratch APPDATA,2931 owner files
unchanged each interval. Original upper above153 preserved under whole-figure
floor shifts; one138px measured source ruler per family,148 nominal unchanged.
Both equipment previews reviewed82/148. Raster filter LFS verified.

## Next action
Update cardinal audit to latest West bank; compare details/build and contact
cadence across directions. Natural short/long travel, partial arrivals/returns,
hazard/gear/medium interruptions and snapshot/fresh Continue remain, followed
by normal runtime admission and the remaining Bill actions. No completion claim.
'''
for root in [P,G]:
 (root/'HANDOFF.md').write_text(handoff,encoding='utf-8')
 (root/'review-assessment.json').write_text(json.dumps({'reviewed':True,'sourceBoards':True,'nativeBoards':True,'browserSizes':[82,148],'material':'Detailed dim rectangular knee plates, straps and boots closer to directional held master','normalSelectionChanged':False,'remaining':['Full cardinal material/contact cadence','Natural travel and lifecycle admission','Full Bill action set']},indent=2)+'\n')
print('Recorded scoped milestone and preserved existing status content')
