"""Record actual-world contact findings and limits, preserving failed evidence."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-east-walk-family-contact-v1'
RUN=ROOT/'output/marsh-animation-audit/east-walk-world-v3-2026-10-03'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=OUT/'world-review/verification.json';v=json.loads(p.read_text())
assert v['checks']==1653 and v['failures']==0 and v['pairedCaptures']==43
for b in v['boards']:
 assert sha(ROOT/b['path'])==b['sha256'];b['reviewed']=True
v['reviewScope']='First full1600x900native corrected capture and all eight unscaled928wide source/native comparison pages actually inspected; all43pairs seen. Full original native/source copies retained. Held chronological submission evidence, not continuous watched cadence.'
v['decision']='Registered staged family stays unselected pending head/material/cadence polish and broader joins; same-root sole depth passed for two prescribed actual routes.'
p.write_text(json.dumps(v,indent=2)+'\n')
frozen=json.loads((RUN/'inputs-after.json').read_text())
assert all(sha(ROOT/p)==h for p,h in frozen.items())
note='''

## Marsh East walking actual-world contact study — October 3, 2026

Actual normal Marsh controller/main/grid/equipment player studied with explicit
six-phase staged art override only in fixture player. Prescribed96/112world-unit
East routes in default furnished cold_store;20ms updates/advancing visual clock,
normal paid/failure flags, peers paused. All six walking holds and four start/stop
holds observed, idle closure, pause, three moving actor-only topology restores.
Each same-clock/root source compared to normal and both submitted through actual
station renderer. No StudyMain/private controller/geometry or runtime changes.

Unregistered V2:1653checks/70failures,43paired captures/270movement samples.
69same-root sole-depth failures only0/2:generated soles1sourcepixel higher. One
exact endpoint assertion also failed at112route by.0224609375world unit: normal
bill_npc movement removes path using foot.is_equal_approx(target), not exact==.
Corrected probe asserts existing approximate arrival contract and records residual;
no controller edit or strict contact tolerance change. V2 contact coordinates
mixed canvas roots with room-source scale; V3 uses actorworld+384*.038floorlift
and65.28/H source scale. Paired source1pixel mismatch remains established; do not
claim V2 absolute contact coordinates as a correct world-space diagnostic.
V2 protected interval changed only concurrent scripts/james_cargo_player.gd;
5367other inputs/2931owner non-log files exact. No claim all5368unchanged. Initial
V1 probe indentation parse failure retained,5368inputs/2931owner unchanged there.

New staged character/marsh-east-walk-family-contact-v1 losslessly translates
entire0/2RGBA drawingsY+1, outgoing bottom alpha0, surviving rows pixel-exact and
visible count unchanged; four other frames byte copies, state/pivot/height/timing
metadata retained. No anatomy paint/splice/scale/grade fitting or alpha repair.
Uniform registration also moves crown; post-registration0crown+1/2crown+3 against
original current walking poses. Head proportions/shading/bob remain review items,
not silently fitted. Normal228states/1190slots/89body manifests unchanged.

Registered V3 actual normal controller/main/grid:1653checks/0failures,270samples,
43paired native/source captures,3moving actor restores.5377bounded inputs and
2931owner non-log files unchanged under scratch APPDATA,engine0,no errors/warnings.
Same-root source sole depth exact for observed holds;112route residual.0224609375
retained under existing approximate arrival rule. Both native sessions terminal.
All86submitted source captures match expected selected/counterfactual RGBA. First
full1600x900corrected native and all eight complete928wide comparison boards
actually inspected, full originals retained. Fixed observed station crop
(400,190,680,350), not fitted to pose bounds. Native identity/collar/material better
defined; head/grade differences remain. Entire registered family PROVISIONAL/
UNSELECTED. No continuous watched cadence, full2Dplanted-foot acceptance, natural
goal selection, paid building, all rooms/rotations,disk fullSave/TitleContinue or
whole-set acceptance inferred. Reports output/marsh-animation-audit/east-walk-world-
v1/v2/v3-2026-10-03; staged world-review/verification.json binds source/native scope.

Lesson: compare candidate and current source at the same actual moving root before
admission; a successful native player proof misses physical contact. Use a single
coordinate system including actual floorlift; do not mix canvas root with room
sprite scale. A failed fixture assertion must match the current controller contract
before declaring a regression. Preserve original failures, record endpoint residuals
and concurrent protected-file changes explicitly, keep contact tolerance strict.
Next registered full-family head/material/bob/cadence polish against master/ownidle/
start/stop; then broader natural/save and other animation joins. Full goal active.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
 with p.open('a',encoding='utf-8',newline='\n') as f:f.write(note)
installed.write_bytes(canonical.read_bytes())
print('43native pairs/8pages actually reviewed;5377test inputs still exact;pipeline/bible/currentstatus/skill updated;staged bank remains unselected')
