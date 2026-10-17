"""Retain South source/native evidence, current selection boundaries and reusable lessons."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];E=R/'character/bill-carry-start-south-v2'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
native=read(R/'output/bill-carry-south-start-station-v2/validation.json')
player=read(R/'output/bill-carry-south-start-player-v2/validation.json')
journeys=read(R/'output/bill-carry-south-start-station-v2/journeys.json')
assert native['passed'] and player['passed'] and not native['realProfileChanges'] and not player['realProfileChanges'] and journeys['failures']==0
frozen=read(R/'character/bill-carry-start-north-v2/version-input-hashes.json')
changed=[f for f,h in frozen.items() if hashlib.sha256((R/f).read_bytes()).hexdigest()!=h]
assert not changed,'Normal North milestone changed; inspect before carrying forward selection claim'
assessment={'date':'2026-10-02','normalSelectionChanged':False,'goalComplete':False,'packageChecks':143,'playerChecks':71,'nativeChecks':3716,'native':native,'directEntry':player,'cases':4,'roomSourcePairs':128,'candidatePairs':68,'uniqueCandidateSelectionsReviewed':24,'visualReview':'All six gait and six entry slots both gears in complete native/source boards; source contact/opposite-half compared with original held masters and current East3/West2/North2 sources, both gears. Browser recorded-source replay sampled at82and148. No continuous native-film or global smoothness/contact certification.','sourceScope':'New South gait3/start2 staged; selected normal controller/player types with fixture-only South source overrides. Normal bank remains South gait2/start1 with installed North gait2/start2 for new sessions. No saved-source admission for new South, no normal selection or owner acceptance claim.','routeScope':'Real workshop service and real collision geometry, prescribed long clear South lane replaces generated short route; original generated route retained. Candidate East/South turn, finite entry, exact contact0 phase.139 then next moving tick slot1. All active entries classified separately from gait. Not natural chooser/short-route coverage.','sourceContract':'Original256canvas,nominal148,p128224,840ms/.12stride and320ms bridge preserved. Actual South opaque master ruler144, not nominal148. Original upper RGBA above168, identical paired lower, common per-family calibration/ground, pooled neutral grade100/.82, no mirrors/per-pose scale/exposure. All24candidate soles222 and crowns match originals.','normalMilestoneFrozenInputs':len(frozen),'changedFrozenInputs':changed,'pending':['Compatible South source-version admission and actual arrival/return/Continue/priority','Full natural-route and short-path foot contact','Loop cadence and support/glide polish across all directions','Floor-case-to-idle, remaining equipment/actions and full-set master consistency']}
(E/'review-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n',encoding='utf-8')
e=read(E/'runtime-evidence.json');e.update(assessment);(E/'runtime-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
heading='## Bill South actual-master-ruler carrying candidate - October 2, 2026'
body='''
New paired bill-carry-south-gait-v3 and bill-carry-start-south-v2 are staged.
South already had useful foot movement; review did not justify exaggerating it to
match side-view spread. Existing authoring used nominal148ruler while original
opaque South held master is144high (crown79/sole222). New raw walking sources fit
that actual144ruler; runtime256/p128224/standingHeight148 unchanged. Original head,
helmet, torso, hands/cargo RGBA above168 exact, identical paired lower bodies.
All6gait/all6entry slots both gears opaque sole222; current gait2 diagnostic soles
224,222,222,223,222,223 retained, not an anatomical support/glide certificate.
One full-standing ruler/ground per accepted raw family, pooled neutral matte100/.82,
no per-pose exposure/scale or reflection.840ms/.12stride and finite320ms clock kept.

Five generated transparent source sheets/prompts retained. First half uses0/1/2;
two opposite attempts rejected entirely for wrong leading leg. Edited partial sheet
uses0and2; its sample1 still had wrong support. Targeted second-figure correction
uses sample1 only. Three accepted source families, complete standing calibrator
in each. New entry reuses exact original South first-step raw/prompt (standing578),
re-packaged at144/578; canonical held0 and gait0 exits4/5 exact byte copies.
Gait pooled gain[.981818,.981481,1]; entry[1.058824,1.06,1.061224]. Canonical upper
protected independently of generated torso/face, no whole-frame grading.

73gait+70entry package guards;71player checks0fail/5.63s, direct pickup/entry,
all6rows, exactcontact0/.139phase exit then next moving60Hz gait1, gear/backclock
cancel and pending East/South ordering.3716native0fail/73.63s, engine0/no errors;
actual selected controller/player types, baseline plus fixture-only candidate South
sources, real workshop service and prescribed long collision-clear South lane.
128room/source pairs (68candidate), all6entry/all6gait both gears;24unique candidate
sources exactRGBA matched to native captures and all24presentations reviewed.
Both cardinal master/contact/opposite-half comparison boards reviewed against
East3,West2,North2. Browser recorded-source replay sampled82/148; fixed review pivot,
not native continuous film. Separate authored840ms walking-loop view exposes the
end/start join independently of the finite replay's return to standing; sampled82.
All2931owner non-log files unchanged under scratch
APPDATA in both intervals; PNG LFS filters. Prior220North selection/runtime/art
input hashes unchanged after work. New input snapshot is post-run, not prelaunch.

New South remains UNSELECTED pending compatible saved-source bank admission and
arrival/return/Continue/priority. Normal selection stays South2/start1, North2/start2
for new sessions, with old restored-session bank retained. No owner acceptance,
source/body-style or full contact/smoothness completion claim. Next compatible
South bank admission, real natural/short-route contact and cross-family loop polish;
floor-case-to-idle, remaining equipment/actions and full Bill set remain open.
Handoff: character/bill-carry-start-south-v2/HANDOFF.md. No commit/export.
'''
def add(path,text,prepend=False):
 current=path.read_text(encoding='utf-8')
 title=text.splitlines()[0]
 if title in current:
  a=current.index(title);b=current.find('\n## ',a+len(title));current=current[:a]+text+'\n'+(current[b:] if b>=0 else '')
 elif prepend:current=text+'\n'+current
 else:current+='\n'+text
 path.write_text(current,encoding='utf-8')
add(R/'docs/CURRENT_STATUS.md',heading+'\n'+body,True)
add(R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',heading+'\n'+body)
lesson='''## Directional ruler and opposite-leg review - October 2, 2026

Compare movement before increasing amplitude: a frontal step can reasonably read
more compact than a side stride. Bill South's actual opaque master is144high while
the runtime nominal ruler remains148. Calibrate generated whole-standing references
to the actual directional master; retain runtime canvas/pivot/nominal profile and
protected original upper. Do not force all facings to equal bounding-box heights.
Registered source soles are a useful guard, not anatomical foot support or glide
acceptance. South new gait/entry allsole222 vs old gait222..224; native context matters.

Opposite-leg prompts can repeatedly return the same leading leg, even beside an
explicit contact reference. Review each figure, preserve wrong-support sources as
rejected, and accept only correct samples. A targeted second-figure correction
worked where whole-sheet opposite prompts failed; independently validate standing
calibration and rebuild protected upper, rather than trusting instructions to keep
the rest unchanged. Do not mirror asymmetric clothing/equipment to hide the error.
South3/start2:143package/71entry/3716native guards, all24unique native/source slots
and both cardinal master boards reviewed, recorded-source replay sampled82/148.
Prescribed collision-clear lane is not natural/short-path coverage; full loop and
source-version lifecycle admission remain separate. New sources staged; installed
normal North and old South untouched. Skills/pipeline/bible record evidence scope,
not an owner acceptance or full-set completion claim.

Expose an authored walking-loop view separately from finite held-to-walk replay.
A replay reset to standing can masquerade as a gait seam problem; review the actual
end/start at its source clock without that unrelated reset. Keep the full task join
view too. Source-loop mode at a fixed pivot does not prove moving-root foot contact
or continuous native motion. South preview offers first-step, full replay and840ms
six-pose loop modes; source replay sampled82/148, separate loop sampled82.
'''
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:add(path,lesson)
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill South carry ruler/step polish

## Objective and acceptance
Full Bill master-matching animation set and cross-family consistency/polish. This
milestone authors paired South walking3/first-step2; normal admission still open.

## Accepted decisions and constraints
Exact original upper above168; actual South opaque144ruler vs nominal148,256canvas,
p128224. All24source soles222; common per-family ruler/ground and pooled matte grade.
No mirrors/per-pose scale/exposure, owner saves/geometry or commit/export.

## Current state
New gait3:6paired rows,840ms/.12stride. Five raw sheets/prompts/provenance retained;
two entirely rejected, one partial accepted0/2, targeted pass accepted1. New entry2
repackages original authored source at144/578, six rows/320ms, master0 and exact
new gait0 exits4/5. Build/verify/provenance/native/source/cardinal review and page
retained. Selected type fixtures override South sources only; no persistence schema
for this new South bank. Normal remains South2/start1, installed North2/start2.

## Verification
143package,71entry headless/5.63s,3716native/73.63s, all0fail/engine0. Real workshop
service, prescribed clear long South lane,128room/source pairs/68candidate.24unique
candidate selections exactRGBA verified and all reviewed on paired native boards.
Cardinal master/contact/opposite-half boards and browser82/148 sampled. All2931
owner non-log files unchanged in scratch intervals; previous220North milestone
inputs unchanged. New input hashes post-run; no prelaunch freeze claim. Source
sole/connected-body tests do not certify anatomical contact or uninterrupted motion.

## Next action
Compatible South source-version admission retaining current saved banks, actual
arrival/return/Continue/priority. Natural/short-route foot contact and cross-family
loop cadence/support/glide; floor-case-to-idle, equipment/actions matrix and full-set
master polish. Full goal active/incomplete; no owner acceptance claim.
'''
(E/'HANDOFF.md').write_text(handoff,encoding='utf-8')
(P/'HANDOFF.md').write_text('South paired gait3, October 2, 2026. Staged; see ../bill-carry-start-south-v2/HANDOFF.md for actual-master144ruler, source rejections, paired/native/cardinal review, checks and remaining source-version/lifecycle/full-set work.\n',encoding='utf-8')
inputs=set(frozen)
for folder in [P,E,R/'character/bill-carry-south-gait-v2',R/'character/bill-carry-start-south-v1']:
 for file in folder.rglob('*'):
  if file.is_file() and file.suffix in ['.png','.json','.py','.txt','.html'] and file.name!='input-hashes.json':inputs.add(file.relative_to(R).as_posix())
for name in ['tests/test_bill_carry_south_start_station_v2.gd','tests/test_bill_carry_south_start_station_v2.gd.uid','tests/test_bill_carry_south_start_player_v2.gd','tests/test_bill_carry_south_start_player_v2.gd.uid','tools/run_bill_carry_south_start_station_v2_validation.py','tools/run_bill_carry_south_start_player_v2_validation.py']:
 inputs.add(name)
hashes={name:hashlib.sha256((R/name).read_bytes()).hexdigest() for name in sorted(inputs)}
(E/'input-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
print(f'South candidate recorded:143package/71player/3716native,24reviewed unique sources,{len(hashes)}post-run hashes; selected normal banks unchanged')
