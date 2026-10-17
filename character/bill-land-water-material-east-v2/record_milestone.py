from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-land-water-material-east-v2'
v=json.loads((O/'validation.json').read_text());data=json.loads((O/'records.json').read_text());assert v['passed'] and data['failures']==0
e=json.loads((P/'review.json').read_text());assert e['sourceArtRGBAExactToPrior'] and e['all190WorldPositionsWaterStatesExactToPrior']
e['visualReview']='All190source/native presentations in four boards and16old/new native pairs inspected. Abrupt upright/wet tint change reduced; original face/suit detail more readable during rise. Waterline/wake/support/contact, continuous gameplay/master/full-set acceptance remain incomplete.'
e['reviewPackagingRepair']='First build completed captures/APNG/JSON but failed reading UTF8 HTML with Windows default cp1252; explicit UTF8 fixed, packaging rerun passed without repeating native test.'
e['sameClockGuardScope']='Inherited source cancellation probes, not native material cancellation capture. Fixture copies per-instance grid material parameters to view during step; normal renderer binding and interruption presentation still pending.'
e['eventHashMeaning']='EventSHA hashes hex-encoded RGBA strings; sourceRegistration keys are actual decoded RGBA SHA256.'
(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
note=f'''## Bill East transition water material blended — October 2, 2026

New unselected grid.gd extends staged East source bridge; per-instance500ms
smoothstep weight blends standing-waterline and readable swimming treatment,
reversed on exit. New view.gd draws single top/bottom source regions with blended
tints (no double full-body ghost), interpolates original wake contact/width and
fades head/bubbles by wet weight. Head highlight uses registered interior crown
offsets instead of prone offset for upright bodies; dynamic endpoint head positions
remain approximate normal references. Original source texture pixels/scale/pivot,
actor navigation/medium/oxygen/safety, collision envelope and target gait unchanged.
Only fixture step copies material fields into staged view; normal binding pending.

{data['checks']}nativechecks0fail/{v['seconds']}s/engine0,2931owner non-log files
unchanged/scratch APPDATA. Four entry/exit admissions and exact target completions;
eight inherited synthetic same-clock gear/facing/death/stage source guards pass.
Added1200per-tick material range/finite-bridge checks. These do not prove natural
priority/material cancellation/gear gesture/death completion or Continue.

190advancing60Hz source/native presentations/380original paired captures retained;
all190RGBA sources, physical roots/world positions/water/states/directions EXACT
to prior runtime interval. All inspected in four full boards plus16old/new native
comparison pairs.8lossless APNGs verify380decoded capture intervals/original
750msentry and833msexit windows. Sudden upright/wet darkening materially reduced;
face/suit detail more readable through rise. Continuous water/head/wake/contact/
support/master-motion acceptance still incomplete; no unpaused continuous route,
natural hydrology, normal integration/cardinal expansion or checkpoint admission.

First review packaging failed UTF8HTML read through Windows cp1252 default after
native/images/APNG/JSON succeeded. Explicit UTF8 fixed; packaging rerun passed,
no repeated Godot run. New script/test UIDs distinct and paired; initial generator
inherited old fixture UID strings, corrected before any normal import/admission.
No production artwork/loader/controller/renderer or owner data changes.

Lesson: bridge rendering must blend standing surface treatment and swim treatment
on its finite source clock rather than switching via a provisional all-wet pose
flag. Register head highlight to actual pose and keep presentation per instance;
never alter shared texture metadata or repaint artwork to fix runtime tint.
Next actual per-render parameter binding and material cancellation/contact,
paired saved-clock Continue/normal admission, other cardinal bridges and full
Bill master/cross-family polish/cargo lifecycle. Goal active/incomplete.
Review: character/bill-land-water-material-east-v2/index.html. No commit/export.

'''
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 f=R/rel;f.write_text(note+f.read_text(encoding='utf-8'),encoding='utf-8')
for rel in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=R/rel;f.write_text(f.read_text(encoding='utf-8')+'\n'+note,encoding='utf-8')
f=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md');f.write_text(f.read_text(encoding='utf-8')+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Bill East transition water treatment

## Objective and acceptance
Full master-consistent Bill animation set followed by cross-family polish.
This native material preview remains unselected and does not complete the goal.

## Accepted decisions and constraints
Preserve source art/proportions/size/matte grade, actual actor movement/safety,
and owner saves. Per-instance render parameters; no shared texture mutation.

## Current state
grid.gd/view.gd+paired distinctUIDs, reproducible generated fixture main/scene,
prepare.py, native test+UID/scratch runner, captures/8APNG/4boards/before-after
comparison/review.json. Continuous standing-waterline/swim material weight on
500ms bridge; registered interior head offsets. Fixture copies fields during
step; live per-render binding not implemented. Pipeline/bible/status/skills updated.

## Verification
3383native checks0fail/120.53s/engine0;2931owner non-log files unchanged.
190source RGBA/world roots/positions/water/states/directions exact to prior.
All190paired presentations and16native old/new comparisons viewed.8APNGs/
380decoded intervals exact. Sudden tint change reduced, readable suit/face.
Eight synthetic same-clock source guards inherited; not material cancellation
capture or natural priorities. UTF8HTML packaging read fixed; no native rerun.

## Next action
Bind parameters per render and capture priority/gear/death/clock reversal material
takeovers. Waterline/head-wake support/contact and true continuous motion still
need acceptance. Paired source/clock checkpoint/Continue, normal guarded admission,
all cardinals, cargo lifecycle and full library master/polish remain. No commit/export.
''',encoding='utf-8')
print('Native material milestone and runtime-tint/pose-head lessons recorded; full Bill goal incomplete.')
