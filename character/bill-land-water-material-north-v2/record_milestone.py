from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
e=json.loads((P/'review.json').read_text(encoding='utf-8'));v=e['validation'];c=json.loads((P/'comparison.json').read_text(encoding='utf-8'))
assert v['passed'] and not v['frozenInputChanges'] and not v['realProfileChanges']
heading='Bill North blended waterline material pass — October 2, 2026'
body=f'''Fixture-only character/{P.name} retains NorthV3 source art, nine-pose
500ms timing, common scale/pivot, canonical helmet and actual current normal actor/
player. Rendering now blends the existing standing and swimming world waterlines
over the finite bridge's material progress. Previous material kernel used the
standing split for the whole bridge even as the authored body lowered and flattened.
Existing water tint/opacity, head treatment, source pixels and movement are retained.

{e['checks']}native checks/0failures in{v['seconds']}seconds;{v['frozenInputs']}prelaunch targeted inputs
stable and all{v['realProfileFileCount']}owner non-log files unchanged with scratchAPPDATA. Each
gear admits/completes one finite entry, returns exact current swimming phase, and
passes gear/facing/death/stage/clock/collision takeover checks. All{e['capturePairs']}source-room
pairs identify frozen decoded source profiles. Before/after comparison proves
{c['sourceRootClockWaterExactPairs']}pairs retain exact source pixels, root, state/facing, material/head values;
all90advancing pairs retain clock/water/medium/path/goal/cell.20fixed native-scale
before/after selected comparisons published. Source comparisons use common physical
canvas registration. No production selection, full save/Continue or North exit yet.

Visual review: {e['visualReview']}

Lesson: a finite dry-to-swim pose bridge needs a water-surface split that follows
its changing standing/swimming projection. A shared physical root and stable source
pivot do not make the standing waterline suitable throughout the pose bank. Check
both endpoint world formulas and interpolate the presentation while retaining
actual movement and source art. Compare matched source/root/clock/water snapshots
to isolate material geometry; separately review chronology/contact/master fidelity.

Next finish North moving/contact/master audit, independently authored exit and
checkpoint/TitleContinue; South bridges, normal admission/cargo lifecycle and full
cross-family consistency/polish remain. Full objective active/incomplete.
Review: character/{P.name}/index.html.
'''
entry='## '+heading+'\n\n'+body+'\n'
for relative,prepend in [('docs/CURRENT_STATUS.md',True),('docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',True),('docs/ASSET_PIPELINE_AND_WORKFLOW.md',False),('docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',False),('skills/brinespace-character-pipeline/references/crew-consistency.md',False)]:
 f=R/relative;s=f.read_text(encoding='utf-8')
 if heading not in s:f.write_text(entry+s if prepend else s+'\n'+entry,encoding='utf-8')
f=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md');s=f.read_text(encoding='utf-8')
if heading not in s:f.write_text(s+'\n'+entry,encoding='utf-8')
(P/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October 2, 2026 · Project: {R} · Task: Bill North waterline material

## Objective and acceptance
Complete full Bill set matching masters, perspective, proportions and matte grade,
then cross-family consistency and polish. This is a staged material milestone.

## Accepted decisions and constraints
Retain original source art, common physical scale, actual normal actor/player and
finite500ms bridge. Fixture only; scratch profile. North exit independently authored.

## Current state
New sibling North material V2 view blends dry/swim waterline. prepare.py stages
current main/grid/test/runner and frozen source inventory. build_review.py and
build_comparison.py publish chronological source/native boards and matched pairs.

## Verification
{e['checks']}native checks/0failures;{c['sourceRootClockWaterExactPairs']}exact paired source/root cases;
{v['frozenInputs']}stable targeted files;{v['realProfileFileCount']}owner files unchanged.
{e['visualReview']}

## Next action
North full moving/contact/master audit, independent exit, checkpoint/Continue;
South bridges, normal admission/cargo lifecycle and complete-set polish remain.
''',encoding='utf-8')
print(json.dumps(dict(guidanceFiles=6,handoff=True,goal='active/incomplete')))
