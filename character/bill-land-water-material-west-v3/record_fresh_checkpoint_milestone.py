from pathlib import Path
import json

P = Path(__file__).resolve().parent
R = P.parent.parent
D = P / 'fresh-checkpoint-review'
e = json.loads((D / 'review.json').read_text(encoding='utf-8'))
assert e['validation']['passed'] and e['failures'] == 0
assert not e['targetedInputChanges'] and e['frozenInputCount'] == 527
assert len(e['freshRestores']) == 4
assert len(e['nativeSourcePairs']) == 8
assert all(x['roomExact'] and x['sourceExact'] for x in e['nativeSourcePairs'])
assert not e['validation']['realProfileChanges']
e['visualReview'] = ('All sixteen immediate/future before-after native presentations reviewed. '
    'Eight native/source pairs byte-exact. Entry push-off and exit half-kneel retained '
    'with both equipment states; normal swimming/walking resumes identically. '
    'Normal gait boundary suit-detail/face/material differences remain visible. '
    'These static comparisons do not establish continuous motion, contact or full master consistency.')
(D / 'review.json').write_text(json.dumps(e, indent=2) + '\n', encoding='utf-8')

note = f'''## Bill West entry/independent exit fresh save restoration — October 2, 2026

Four normal checksum RunSave write/read/restore_staged passes into fresh same-process
scenes/worlds/normal Bill actors, entry and independently authored exit, both gears.
Fixture-only resource-free bridge sidecars admitted after world/actor restoration.
Entry tick81 exercises current push-off index003 (retained V3 material pose in
current V4 bank); exit tick432 exercises new half-kneel index004. Loaded current
main/grid paths and all28 entry/exit bank frame pixels explicitly checked.
No normal optional save field, production source admission or Title Continue wiring.

{e['checks']}native checks,0fail/{e['validation']['seconds']}s; scratch APPDATA,
all{e['validation']['realProfileFileCount']}owner non-log files unchanged.
527 targeted code/source inputs unchanged from prelaunch freeze, including current
normal gait sources. Forty future60Hz updates per case (160total) exactly match
uninterrupted foot/facing/state/medium/needs/oxygen/tank/source/material/head/bridge
trajectories and finish into normal gait. Thirty-two malformed sidecars covering
version/clock/gear/phase/bank-source/extent/incoming-source/previous-facing rejected,
each without changing admitted bridge/playback. Paused updates equal on both branches.

All16 immediate/future native presentations reviewed; eight full native/source
before-after pairs byte-exact. This proves the tested restoration parity, not
native pixels at every future tick or continuous full-speed/master/contact acceptance.
Normal walking boundary detail/face/material differences remain visible. New V4
lift/prone artwork is bank-verified and traversed, but save tick81 is push-off,
not the new lift. Preserve that distinction when reusing evidence.

Lesson: independently authored exit needs its own saved active pose, continuation
and invalid-sidecar guards. Reject incompatible source/timing/registration before
mutating the admitted animation. Freeze the actual normal boundary/takeover banks
alongside the candidate, and name the saved source pose rather than inferring it
from an animation-family label. Restoration equality does not certify master fidelity.

Review: character/bill-land-water-material-west-v3/fresh-checkpoint-review/index.html.
Next: current West new-process actual Title Continue, continuous source/native
master and endpoint matching, then remaining North/South bridges and guarded normal
admission. Cargo lifecycle and full-family perspective/scale/anatomy/detail/matte
grade/loop polish remain. Full Bill goal active/incomplete; no commit/export.

'''
heading = note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md', 'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
    f = R / rel
    current = f.read_text(encoding='utf-8')
    if heading not in current:
        f.write_text(note + current, encoding='utf-8')
for f in [R / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
          R / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
          R / 'skills/brinespace-character-pipeline/references/crew-consistency.md',
          Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    current = f.read_text(encoding='utf-8')
    if heading not in current:
        f.write_text(current + '\n' + note, encoding='utf-8')
(D / 'HANDOFF.md').write_text(f'''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Bill West fresh water restoration

## Objective and acceptance
Complete Bill's full set matching original masters, style, perspective, size,
height, proportions and colour grade, then cross-family polish. Goal incomplete.

## Accepted decisions and constraints
Current normal actor/world/save rules retained. Fixture-only bridge sidecar;
WestV4 entry and independently authored exitV1, no reverse/mirror substitute.
Godot validation isolated from owner saves, equal paused updates and exact images.

## Current state
Current-main fresh fixture/UID, West checkpoint codec/UID, native test/UID,
scratch runner and527-input freeze; publisher and recorder. Four base-loop saves,
four sidecars,32 source/native captures, comparison board and review.json.
Status/continuation/pipeline/bible/maintained and installed skill references updated.

## Verification
{e['checks']}checks0fail/{e['validation']['seconds']}s. All2931 owner files unchanged.
Four fresh same-process restores;160 future update trajectories exact;
32 malformed sidecars rejected without changing admitted playback;527inputs stable.
Eight native/source pairs exact, all sixteen native presentations visually reviewed.
Entry saved push-off003 and exit new half-kneel004. Full motion/master/contact pending.

## Next action
New-process actual Title Continue for current West banks, continuous motion and
normal endpoint/master matching, remaining North/South water bridges. Guarded normal
admission, cargo lifecycle and entire cross-family consistency/polish remain.
No normal save extension, commit or export.
''', encoding='utf-8')
print(json.dumps({'recordedChecks': e['checks'], 'exactPairs': 8,
                  'stableInputs': e['frozenInputCount'], 'guidanceFiles': 6}))
