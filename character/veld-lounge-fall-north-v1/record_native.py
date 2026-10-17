"""Native mortality/save milestone, preserving concurrent actor records."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-lounge-fall-north-native-v1';G=R/'output/veld-bunk-body-settle-v1'
native=json.loads((O/'validation.json').read_text());regress=json.loads((G/'validation.json').read_text());package=json.loads((P/'package-checks.json').read_text())
assert native['passed'] and regress['passed'] and package['checks']==62 and package['failures']==0
records=json.loads((O/'records.json').read_text());assert len(records)==8
note='''## Veld North lounge fall actual mortality and fresh Continue - October 1, 2026

Staged character/veld-lounge-fall-north-v1 now opts into real North seated death
through loungeFallDeathMode=seated-north-v1; CrewSpritePlayer tags those sources.
VeldDeathMotion captures only matching dry gear and registered North seat source:
selected held breathing, final lowering5 or initial rising0 with seat amount>=.8.
Exact displayed whole source/position/depth retained180ms. Authored interiors then
play finite1440ms. Saved local foot, seat, depth and entry amount survive die()
clearing live furniture state. Offset holds through360ms, fades linearly to zero
by720ms; max(natural depth, saved chair front) prevents re-occlusion during fall.
Strict saved selectors/gear/first/pose/range/finite vectors/foot-root/offset/depth
binding; foreign lounge fields rejected on other clips. No normal loader admission
yet. Earlier partial seating poses retain existing behavior pending authored coverage.

Changed scripts/crew_sprite_player.gd and scripts/veld_death_motion.gd; new paired
fall root opt-in in builder/manifests. All12PNG sources unchanged by integration;
one148/693ruler, matte pooled grade, original North seat/floor and native depth-pitch
helmets retained. Package now62checks0fail (two opt-in guards added), builder20.
Fixture loads only new fall; ordinary selected North sitting/breathing remains
normal loader output. No furniture/owner layout/economy/free-build changes.

Native23581checks0fail/312.08s,engine0/cleanlog. Eight actual RoomFlooding.kill
cases: two distinct held breathing sources, final lowering and initial rising,
both gears. Eight eligible actual RunSave disk writes/reads and fresh main-scene
restore_staged.150reference+150resumed20ms actor steps per case=2400future updates;
independent source clock/root/depth oracle plus exact uninterrupted/resumed pixels,
foot/timer/gear/needs/offset/depth/corpse state.64malformed source/root/gear guards;
unmarked candidate rejects opt-in. Exact incoming source and chair root/depth,
paused Continue, clear dead navigation and original finite floor terminal checked.
Paid existing Bill ward wake/roster provides real surviving crew/save eligibility;
that fixture does not certify ward repair/approach or natural hazard triggers.

Eight complete paired native/source/master boards reviewed;112future room/source
presentations,128room and128source captures including entrances/restores. Clear
chair-to-floor contact, body/helmet identity and matte grade retained. Replay uses
actual recorded source/root traces; not a continuous native world recording.
Prescribed current default lounge rotation0 only, actor-only future updates while
main paused; not new-process/title Continue, natural chooser/hazard/world cadence
or all room rotations.35targeted inputs before/after unchanged; broader dependencies
not frozen. Scratch APPDATA/all2931owner non-log files unchanged.

Scoped changed-selector regressions also pass:14813partial-bunk native71.71s,
1306held-bunk native78.54s,1953water headless37.21s; total189.22s,allengine0/cleanlogs,
29targeted inputs unchanged/all2931owner files unchanged. Earlier early-floor/full
world evidence retains its dated scope; no unrelated full asset test batch.

Lesson: saving the source selector alone loses chair position and sort contact
when death clears live stages. Capture registration with the displayed pose,
validate it against physical foot and incoming source family, then advance a
finite root/depth path on the saved visual clock. Exercise different breathing
interiors and lowering/rising joins; compare future frames after real eligible
disk/fresh-scene restore, not just snapshots at one time. Tests do not replace
master/native review or owner motion acceptance. Full Veld goal active/incomplete.
Next earlier partial-seat floor entrances and other cardinal lounge sources,
then real natural hazard cadence/normal admission and complete cross-family polish.
No commit/export requested.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for i,path in enumerate(targets):
 old=path.read_bytes();payload=note.replace('\n','\r\n').encode('utf-8')
 if note.splitlines()[0].encode() not in old:path.write_bytes(payload+b'\r\n'+old if i==0 else old+b'\r\n'+payload)
handoff='''# Project handoff

Updated:2026-10-01 - Project:BrineSpace - Task:North lounge death/fresh Continue

## Objective and acceptance
Full master-matching Veld set and cross-family polish active/incomplete.
North lounge fall integration staged; normal admission and owner review open.

## Accepted decisions and constraints
Real lounge North facing; exact selected seat/breathing entrance, existing floor
sources, fixed148/693ruler, matte grade/native rear depth-pitch helmet unchanged.
Capture actual source plus chair registration before die() clears live stage.
Preserve owner geometry, navigation foot, ordinary save eligibility and other actors.

## Current state
CrewSpritePlayer/VeldDeathMotion opt-in metadata, seated selector and saved root/
depth law:180ms exact entrance, seat/slump holds to360ms, root fades to720ms.
Strict saved source/gear/foot/seat/offset/depth checks. Builder/manifests updated;
12PNG unchanged. New native test+UID/runner, review_resume.py, resume-review.html,
eight native boards/replay traces/14exact source images; five lesson targets.
Normal North seating already selected; fall manifest injected only by fixture.

## Verification
20builder/62package checks0fail. Native23581checks0fail/312.08s,engine0/cleanlog:
8actual mortalities,8real eligible disk/fresh-scene restores,2400future20ms actor
updates,independent source/root/depth oracle,64malformed guards,paused continuity.
Different held breathing pixels verified; lower5/rise0 joins covered.128room+
128source captures;8full paired master/native boards reviewed,112future views.
35targeted inputs unchanged/all2931owner files unchanged/scratch APPDATA.
Regressions14813partial/1306held bunk/1953water pass,189.22s total;29targeted
inputs/all2931owner files unchanged. Broader dependencies not frozen.
Scope rotation0prescribed APIs,actor-only future while main paused; no natural
hazard/route,new-process/title Continue or continuous native world-movie claim.

## Next action
Earlier partial-seat entrances and other cardinal lounge falls; real world hazard
cadence and wider room contact, normal paired bunk/fall admission. Then full
cross-animation master/style/camera/scale/proportion/material polish.
No blocker, commit/export or final owner acceptance claim.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
for filename in ['index.html','native-review.html']:
 f=P/filename;s=f.read_text(encoding='utf-8')
 if 'resume-review.html' not in s:s+='<p><a href="resume-review.html?v=actual-continue-v1">Actual mortality and saved continuation review</a></p>'
 f.write_text(s,encoding='utf-8')
files=[R/'scripts/crew_sprite_player.gd',R/'scripts/veld_death_motion.gd',R/'tests/test_veld_lounge_fall_north_native.gd',R/'tests/test_veld_lounge_fall_north_native.gd.uid',R/'tools/run_veld_lounge_fall_north_native.py',P/'build.py',P/'validate.py',P/'bare-manifest.json',P/'helmet-manifest.json',P/'HANDOFF.md',P/'review_resume.py',P/'resume-review.html',P/'replay-traces.json',P/'package-checks.json',P/'record_native.py',O/'native.log',O/'validation.json',O/'records.json',O/'inputs-before.json',O/'inputs-after.json',G/'validation.json']+list(P.glob('native-fall-*.png'))+list((P/'frames').rglob('*.png'))+list((P/'replay-frames').glob('*.png'))
bindings={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(P/'native-evidence.json').write_text(json.dumps({'native':native,'regressions':regress,'nativeChecks':23581,'worldDeaths':8,'freshDiskRestores':8,'futureActorSteps':2400,'malformedGuards':64,'nativeSourceCaptures':256,'normalFallSelection':False,'scope':'Prescribed actual rotation0 lounge mortality, normal selected seat source, full disk/fresh main scene future actor continuation; not naturally triggered whole-world/title/process coverage','bindings':bindings},indent=2)+'\n',encoding='utf-8')
print('Native North lounge death/Continue recorded; five lessons and current handoff saved')
