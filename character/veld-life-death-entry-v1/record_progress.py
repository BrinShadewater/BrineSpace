from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-life-death-audit-v1';W=R/'output/veld-water-death-entry-v1'
assert json.loads((O/'validation.json').read_text(encoding='utf-8'))['passed']
assert json.loads((W/'validation.json').read_text(encoding='utf-8'))['passed']
records=json.loads((O/'records.json').read_text(encoding='utf-8'));assert len(records['records'])==18 and records['renderJumpCases']==0
title='Veld life-pose death entrance contact repair - October 1, 2026'
note=f'''## {title}

Actual selected life-pose death audit found18/18presentation offset jumps when
die() clears furniture stage/progress, despite byte-exact source retention.
Staged dry collapse also chose standing interior1 in all18cases. Completed
before-repair360check interval/18case captures retained under
output/veld-life-death-audit-v1/before-entry-contact-repair.

scripts/veld_death_motion.gd now captures optional typed entry_position_offset
and entry_sort_depth for dry sit/read/lie/sleep/bunk sources in existing saved
recipe. grid_canvas.gd consumes them only during exact live entrance <180ms;
ordinary live/water/legacy poses and authored interior anchors retain existing
behavior. Finite vectors/384length and finite512depth bound, paired fields,
dry/furniture-source admission enforced; old recipes lacking fields accepted.
No new artwork, source regrade/rescale, physics foot/furniture/nav change,
mortality/survival rule or normal dry-family selection. Patch is opt-in through
staged lowered-entry dry pack until that family is adopted.

Final756native checks0failures/60.51s engine0:18actual mortality cases in current
default lounge North sitting, observation South reading and specialised East
bunk, at lowering/held/rise,both gears. Exact incoming source, physical foot and
actual retained-render member position/sort depth now stable:0/18render jumps.
18typed actor disk writes/reads and fresh dead actor restores preserve exact
entrance at same retained world clock, without navigation graph. Legacy recipe
admission and144invalid-contact rejections;180ms hold/release boundaries verified.
Actor disk proof is not full RunSave/fresh-scene Continue or saved world-clock
restoration. Earlier repaired558check interval remains scoped no actor disk.
Both six-case held source/native boards reviewed, including restored entrances.
This certifies entrance preservation, not original furniture contact/visibility,
later collapse continuity or complete owner acceptance. Every current source
sprite remains unchanged; hashes after interval, dependency stability unmeasured.

Normal selected water regression1954checks0failures/37.85s,64actual oxygen deaths,
incoming source/clocks/actor-player memory restore retained. No water fresh disk
or new furnished-water claim. Both final intervals preserve all2931owner non-log
files under scratch APPDATA. Failed fixture42.37s occupied-cell check and144.52s
post-death room placement/script error preserved; errored test Godot process
119584 explicitly stopped. Corrected only fixture: pre-place all real rooms on
verified vacant cells before deaths, hide report UI for art captures. Normal
failure/end-run state remains untouched; no survivor/failure bypass.

Lesson: an exact source texture is not an exact displayed pose. Save entrance
position and furniture depth before mortality clears stage, and validate them
independently of reconstructed navigation. Inspect source/native complete motion;
standing-derived collapse makes held bunk42/45px sources jump to135/147px upright
interiors. Never normalize frame height or substitute kneeling slots to hide it.
Next author/adopt appropriate seated and lying life-collapse interiors/contact,
then full RunSave/fresh-scene Continue, broader rotations/clearance and normal
dry-family selection. Inherited source grade/detail/helmet and cross-family motion
polish remain; full goal active/incomplete.
Handoff/review: character/veld-life-death-entry-v1.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
 old=target.read_bytes()
 if title.encode() not in old:
  addition=note.encode('utf-8');target.write_bytes(addition+b'\n'+old if target.name=='CURRENT_STATUS.md' else old+b'\n\n'+addition)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 1, 2026. Project: BrineSpace. Task: life-pose death entrance.

## Objective and acceptance
Full master-matched Veld set and cross-animation polish active/incomplete.
Preserve complete displayed life-pose entrance on actual mortality; replace
inappropriate later standing-derived life collapse before normal selection.

## Accepted decisions and constraints
Exact selected life and staged dry-collapse pixels, fixed master rulers/grade.
Navigation foot/furniture unchanged. Optional typed dry/furniture entrance
offset/depth in existing recipe, only180ms live hold; legacy fields absent valid.
No normal dry selection or gameplay failure/survival-rule change.

## Current state
veld_death_motion.gd captures/validates entry contact; grid_canvas.gd consumes it.
New test_veld_life_death_audit.gd/.uid and isolated runner, measured18cases,
native/source contact boards/index/evidence. Before-repair completed diagnostic
saved under output/veld-life-death-audit-v1/before-entry-contact-repair.

## Verification
756checks0failures/60.51s engine0,18actual life mortality cases,0render position/
depth jumps during entrance. Selected default lounge/observation/bunk sources,
candidate dry collapse only; prescribed lowering/held/rise contact phases/gears.
18typed actor disk round trips/fresh dead actor restorations, exact entrance
without navigation graph;144invalid contact payloads rejected, legacy recipes
admitted. Same retained world clock, NOT full RunSave/fresh-scene Continue.
180ms boundary hold/release verified. Source/native six held boards reviewed;
entrance preservation does not reaccept furniture visibility or later motion.
1954normal water regression checks/64oxygen deaths0failures/37.85s. Both strict
scratch guards preserve2931owner non-log files. Input hashes after interval;
dependency interval stability unmeasured.
Two failed fixtures retained: occupied cell, then placement after end-run caused
script error/hang; errored test process119584 explicitly stopped. Pre-place real
rooms at verified vacant cells, hide report UI only. Normal failure state retained.

## Next action
Seated and lying life-collapse interiors are still wrong in all18cases: authored
standing interior, especially bunk42/45 ->135/147px rise. Author appropriate
motion and floor/bed contact, without frame-height normalisation or kneel-slot
substitution. Then full RunSave/fresh scene/rotation clearance and normal dry
selection; complete broader source/master/helmet/grade/detail/motion polish.
''',encoding='utf-8')
files=[f for f in P.iterdir() if f.is_file() and f.name!='evidence.json']+[f for folder in (O,W) for f in folder.iterdir() if f.is_file()]
files += [R/f for f in ['scripts/veld_death_motion.gd','scripts/veld_death_motion.gd.uid','scripts/grid_canvas.gd','scripts/veld_npc.gd','scripts/bill_npc.gd','scripts/crew_life.gd','tests/test_veld_life_death_audit.gd','tests/test_veld_life_death_audit.gd.uid','tools/run_veld_life_death_audit.py','tests/test_veld_water_death_entry.gd','tools/run_veld_water_death_entry.py']]
bindings={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
for family in ['veld-seated-north-selected-v1','veld-seated-south-selected-v1']:
 bindings.update(json.loads((R/f'character/{family}/source-bindings.json').read_text(encoding='utf-8'))['bindings'])
(P/'evidence.json').write_text(json.dumps({'bindings':bindings,'scope':'actual opt-in dry life entrance source/position/depth preservation and typed actor disk/fresh actor; later life motion and full RunSave/fresh scene/normal dry selection unproven','nativeChecks':756,'nativeFailures':0,'actorDiskRestores':18,'invalidContactRejections':144,'renderJumpCases':0,'inappropriateStandingInteriors':18,'waterRegressionChecks':1954,'visualReview':'six held life source sequences/native room sequences reviewed; contact/motion acceptance scoped separately','intervalStability':'hashes after run; dependency stability unmeasured'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'notes':5,'bindings':len(bindings),'goalComplete':False}))
