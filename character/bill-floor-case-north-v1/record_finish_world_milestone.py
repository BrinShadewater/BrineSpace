from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'finish-world-review-evidence.json').read_text());assert e['validation']['passed'] and len(e['boards'])==12
note='''## Bill staged live ordinary service-loss set-down — October 2, 2026

New unselected finish_actor/finish_player+UIDs run finite North finish_plan through
actual selected-main workshop cargo progression. Existing advance_work_return hook
runs after normal needs and fire/flood safety. Suspension/prescribed power loss
clears service goal/stage/path and reward opportunity; remaining exact authored
contact/rise plays on existing normal source consumer. Fixed root, finite .64s
authored end and source-bound floor ownership independent of service power.
Actor/player/room renderer fixture-injected; production selection/art unchanged.

1182native checks0fail/12cases, engine0/61.43s: both gears, actual suspension or
power map loss at .10/.32/.55s unload. Each live source follows exact remaining
clock; root planted through exit, normal curiosity need increases/no service reward,
released floor case persists.12boards/all80native source-room presentations viewed;
160original captures copied unchanged. Head/helmet/detail/matte source reuse retains
identity. Terminal stance change persists; sampled captures do not certify continuous
motion/contact/foot glide or final owner acceptance. All2931owner non-log files
unchanged under scratch APPDATA. Post-run hashes, not broad prelaunch freeze.

Candidate snapshot includes explicit finish_exit actor/player metadata; restore
refuses active exit pending detached full admission. Ordinary save/Continue during
this exit is unsupported. Priority predicates/public gear and death clearing are
implemented but actual fire/flood/gear/death/removal during exit are not yet tested.
Arrival/turn prefixes and other directional carrying exits remain separate gaps.

Lesson: finish ordinary interrupted contact through the established post-needs,
post-safety hook; a source-only replay cannot establish live needs/reward/root
behavior. Keep floor ownership distinct from source presentation. Do not represent
untested priority/restore behavior as admitted merely because ordinary exits pass.
Next actual priority interruptions, bound detached checkpoint/Continue, shared-room
lifetime and native continuous idle join; then normal admission and full Bill set/
cross-family master/grade/proportion polish. Goal active/incomplete. Review:
character/bill-floor-case-north-v1/finish-world-review.html; FINISH_WORLD_HANDOFF.md.
No commit/export.

'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 old=path.read_text(encoding='utf-8');assert note.splitlines()[0] not in old;path.write_text(note+old,encoding='utf-8')
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 with path.open('a',encoding='utf-8') as f:f.write('\n\n'+note)
e['boardsViewed']=12;e['presentationsViewed']=80;e['postRunInputs']={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'finish_actor.gd',P/'finish_player.gd',P/'finish_plan.gd',R/'tests/test_bill_floor_case_finish_world_v1.gd',R/'scripts/bill_carry_npc.gd',R/'scripts/bill_carry_player.gd']}
(P/'finish-world-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
(P/'FINISH_WORLD_HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill live ordinary set-down exit

## Objective and acceptance
Full Bill animation set matching masters/style/perspective/stature/proportions/matte
grade, then cross-family consistency/polish. Goal active and incomplete.

## Accepted decisions and constraints
Ordinary service loss may finish remaining authored contact/rise. Safety remains
ahead of this hook. Preserve original sources, production selection and gameplay.

## Current state
New finish_actor/finish_player+UIDs, actual-world fixture/runner,12native review boards,
160unchanged source/room captures. Staged candidate runs through normal needs/safety
update and source consumer; clears service without reward, preserves root and case.

## Verification
1182native checks/12cases pass: suspension/prescribed power loss at .10/.32/.55s,
both gears. Engine0/61.43s;2931owner non-log files unchanged under scratch APPDATA.
All80native presentations/12boards reviewed. Source reuse preserves head/helmet/matte;
terminal stance still changes. Static samples do not certify continuous motion.

## Next action
Actual fire/flood/gear/death/removal during exit, then detached actor/player/clock/source
checkpoint binding and ordinary disk/fresh-main Continue. Candidate active-exit restore
currently refuses unsupported state; not normally selected. Shared-room lifetime,
continuous idle join, remaining directional/equipment families and full-library polish
remain. No commit/export or owner motion acceptance.
''',encoding='utf-8')
print('Live ordinary exit milestone recorded; pipeline/bible/both skill copies updated.')
