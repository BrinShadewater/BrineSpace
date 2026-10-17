from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-bunk-body-fire-resume-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
records=json.loads((O/'records.json').read_text());assert len(records)==6
checks=int(re.search(r'VELD BUNK FIRE RESUME: (\d+) checks,0 failures',(O/'native.log').read_text()).group(1))
captures=len(list(O.glob('*-room.png')));steps=sum(len(x['reference'])+len(x['resumed']) for x in records)
previous=json.loads((R/'output/veld-bunk-body-settle-resume-v1/inputs-after.json').read_text())
assert all(previous[f.relative_to(R).as_posix()]==hashlib.sha256(f.read_bytes()).hexdigest() for f in (P/'frames').rglob('*.png'))
note=f"""## Veld bunk evacuation full Continue motion - October 1, 2026

Six actual disk saves/reads and fresh main-scene Continue restores now cover
fire interruption while lowering (progress .81), held and rising (remaining .9),
both bare/helmet. Fixture prescribes room fire and supported phase; ordinary
actor.update dispatches FireSafety and Veld finite rise. Existing paid/restored
Bill ward wakes through CryoRecovery/roster logic; normal run eligibility remains.
No free-build/failure bypass, forced resurrection or owner layout change.

{checks} native checks, zero failures/{report['seconds']}s; engine terminal zero,
clean log. {steps} uninterrupted/restored 20ms future actor steps, through actual
clear-floor refuge movement out of burning hab. Every step compares exact source
RGBA hash, physical foot, stage/state/timer, needs, equipment, visual clock and
contact/depth. Foot stays planted during finite rise; exact standing master
returned at its original padded pixel pivot before movement. Saved fire predicate,
evacuation goal, supported anchors and paused exact entrance restored. {captures}
actual native room captures plus {captures} exact source frames; six paired boards
reviewed beside same-ruler standing masters. Native flame effect partly obscures
body; separate adjacent source is exact, not an unobscured native motion movie.
Twenty authored PNGs match prior partial Continue milestone; no art/grade/scale
or production change in this interval. Candidate explicitly injected every scene;
normal paired body selection remains unchanged/unselected.

Owner {report['realProfileFileCount']} non-log files unchanged in scratch APPDATA;
{report['targetedInputCount']} targeted source/test/production/manifest inputs match
before/after. Broader engine dependencies not frozen. New paired UID test, isolated
runner, board builder and evidence fire-resume-evidence.json retained. This proves
fresh scene disk Continue and future actor motion for prescribed rotation-zero
alarm cases, not naturally ignited fires, whole-world hazard/suppression cadence,
new process/title Continue, every rotation or universal owner acceptance.

Lesson: an interruption checkpoint must preserve the incoming pose, finish its
supported action, and then reach a real safe destination. Checking a saved pose
or finite rise alone misses later route continuity. Compare exact source, anatomy
and furniture registration with uninterrupted motion, while separately asserting
the original standing master before foot movement. Keep flame-obscured native
views separate from exact-source material review. Early bunk/lounged falls,
whole-world hazards, normal paired body installation, remaining Veld families
and cross-family master polish remain open. Full goal active; no commit/export.
"""
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for i,path in enumerate(targets):
 old=path.read_bytes();payload=note.replace('\n','\r\n').encode()
 if note.splitlines()[0].encode() not in old:path.write_bytes(payload+b'\r\n'+old if i==0 else old+b'\r\n'+payload)
handoff=f"""# Project handoff

Updated:2026-10-01 - Project:BrineSpace - Task:Veld paired bunk motion

## Objective and acceptance
Full Veld animation set matching masters, followed by cross-family polish.
Goal active/incomplete. Staged body/helmet; owner visual acceptance open.
No normal paired body selection, commit or export.

## Accepted decisions and constraints
Exact standing masters, one148/408 source anatomical ruler/pooled grade.
256x272/p128,224/H148 preserves whole limbs at original pixel scale.
20PNG exports unchanged since arm-support repair. Five paired states/50refs.
Derived supported death reuses descent and relaxed arm; early falls/lounged
sources remain separate incomplete coverage. Preserve all owner room geometry.

## Current state
Builders/sources/prompts/manifests/reviews/evidence here. Rebuild bare then
helmet then build_settle.py. Production marked-bunk East arrival, finite fire
rise and strict dynamic settling recipes use shared original bed contact.
New test_veld_bunk_body_fire_resume.gd/UID, isolated runner and six paired boards.

## Verification
Latest {checks}native fire Continue checks0fail/{report['seconds']}s,6fresh disk restores,
{steps}future actor steps,{captures}room+source captures,six boards/master comparisons.
Actual fire predicate/goal restored; finite planted rise reaches exact standing
master before actual clear-floor route to non-burning refuge. Owner
{report['realProfileFileCount']}non-log files unchanged;{report['targetedInputCount']}targeted inputs frozen.
Prior8125partial Continue checks/4fresh disk restores/1200steps;14813partial
source/API checks/80cases/320same-clock actor-file restores. Held1306/water1953
regressions0fail. Earlier169paused Continue,7121future Continue,3395service,
9668approach,8037emergency/45sharedfire checks retain separate dated scopes.
130package checks and all20PNG unchanged; normal library unselected.
Flame-obscured native captures/exact adjacent sources reviewed separately.
Prescribed phase and actor-only updates do not prove natural whole-world hazard
cadence, title/fresh-process Continue or universal room/owner acceptance.

## Next action
Early standing/crouching bunk fall and lounge death artwork, then whole-world
hazard cadence and normal paired body installation with lifecycle evidence.
Finish remaining Veld families and full-set master/cross-family polish.
"""
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[O/n for n in ['native.log','records.json','validation.json','inputs-before.json','inputs-after.json']]+[R/'tests/test_veld_bunk_body_fire_resume.gd',R/'tests/test_veld_bunk_body_fire_resume.gd.uid',R/'tools/run_veld_bunk_body_fire_resume.py']+list(P.glob('native-fire-resume-*.png'))+[P/'fire-resume-review.html',P/'review_fire_resume.py',P/'record_fire_resume.py',R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png',R/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png']
(P/'fire-resume-evidence.json').write_text(json.dumps({'validation':report,'checks':checks,'freshDiskSceneRestores':6,'futureActorSteps':steps,'nativeRoomCaptures':captures,'exactSourceCaptures':captures,'sourcePNGsEqualPriorPartialContinueMilestone':True,'normalPairedBodySelection':False,'scope':'Prescribed rotation-zero alarms and actor-only future updates through clear-floor refuge; not natural world hazard cadence','visualReview':'Six paired native/source boards with original pixel-scale masters; flame effect obscures some native body','bindings':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
index=P/'index.html';link='<p><a href="fire-resume-review.html">Evacuation: full Continue motion check</a></p>'
old=index.read_text()
if link not in old:index.write_text(old+'\n'+link)
print(f'{checks}checks;{steps}future steps;{captures}room/source captures;five notes and concise handoff saved')
