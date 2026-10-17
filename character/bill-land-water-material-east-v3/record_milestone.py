from pathlib import Path
import json

P = Path(__file__).resolve().parent
R = P.parent.parent
e = json.loads((P / 'review.json').read_text(encoding='utf-8'))
assert e['validation']['passed'] and e['checks'] == 3487
assert e['sourceCapturesExactToV2'] == e['nativeCapturesExactToV2'] == 190
assert e['worldAndWaterExactToV2'] and len(e['nativeGuardPresentations']) == 14
assert not e['validation']['realProfileChanges']
e['visualReview'] = (
    'All14 native synthetic active/takeover presentations inspected in native-guards.png. '
    'Active bridge shading clears to authoritative normal presentation for six guards per gear. '
    'All190 advancing source AND native RGBA images are exact to previously reviewed V2; '
    'that visual review transfers by pixel equality. Guard raw source thumbnails are not '
    'common-pivot registered. Death flag snapshot shows normal selected source at that instant, '
    'not completed death motion. Full support/contact/master-motion acceptance remains open.'
)
(P / 'review.json').write_text(json.dumps(e, indent=2) + '\n', encoding='utf-8')

note = '''## Bill East live transition material binding and takeover review — October 2, 2026

Unselected V3 grid retains current selected source; staged view reads material
weight/head offset at actual draw only when that source matches its actor texture.
It resets to normal treatment otherwise. Removed fixture step parameter copying.
No source repaint/rescale, shared texture metadata mutation or normal installation.

3487 native checks, zero failures, engine0/126.99s; scratch APPDATA and all2931
owner non-log files unchanged. Both gears: native active bridge plus synthetic
gear/facing/death/stage/clock reversal/local blocker takeovers,14 presentations.
All14 inspected: bridge material clears to normal current-source presentation.
Death flag snapshot is not completed death animation; synthetic stage is not
natural priority dispatch. Actual clock/player/geometry restored after each probe.

All190 advancing source AND native RGBA images, world feet/water/state/direction
exact to V2; prior complete board review transfers by exact pixel equality.
204 native/source presentations,408 original image files retained. Eight APNGs
verify380 advancing decoded intervals; guards are separate static snapshots.
Guard source thumbnails preserve original canvas proportions but are not common-
pivot registered. Waterline/head/wake/support/contact/master-motion acceptance,
unpaused natural gameplay, paired clock/source checkpoint and Title Continue,
normal admission and other cardinal bridges remain open. Full Bill set, cargo
lifecycle and cross-family master/material/proportion polish remain incomplete.

Lesson: bind per-instance presentation to the actual texture at draw time, and
recheck bridge cancellation even at an unchanged simulation clock. A temporary
obstacle and reversed clock need captured draw evidence, not source checks alone.
Do not interpret a direct flag takeover as natural action completion.
Review:character/bill-land-water-material-east-v3/index.html.
Handoff:character/bill-land-water-material-east-v3/HANDOFF.md. No commit/export.

'''
heading = note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md', 'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
    f = R / rel
    text = f.read_text(encoding='utf-8')
    if heading not in text:
        f.write_text(note + text, encoding='utf-8')
for f in [R / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
          R / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
          R / 'skills/brinespace-character-pipeline/references/crew-consistency.md',
          Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    text = f.read_text(encoding='utf-8')
    if heading not in text:
        f.write_text(text + '\n' + note, encoding='utf-8')
(P / 'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Bill live water material

## Objective and acceptance
Complete master-consistent Bill set, then cross-family consistency and polish.
This staged East bridge does not complete the full objective.

## Accepted decisions and constraints
Preserve original source pixels, anatomical scale/pivots, actor rules and saves.
Keep presentation per instance and bound to actual selected texture at draw.

## Current state
V3 grid.gd/view.gd and paired UIDs, generated fixture main/scene/input evidence,
prepare.py, native test/UID and scratch runner, build_review.py, captures/boards/
eight APNGs/review.json. Live render binding replaces V2 step copying. Status,
continuation, pipeline, bible and maintained/installed skill lessons updated.

## Verification
3487 native checks0fail/126.99s/engine0;2931 owner files unchanged.
190 advancing source AND native RGBA pairs exact to previously reviewed V2;
world feet/water/state/direction exact. Fourteen synthetic guard presentations
viewed, material cleared for gear/facing/death/stage/clock/blocker changes.
204 paired presentations/408 image files;8 APNGs/380 advancing decoded intervals.
Static guard raw thumbnails are not pivot registered; death is a flag snapshot.

## Next action
Paired source/clock snapshot and fresh disk restoration, then actual Title Continue
and guarded normal admission. Verify continuous water/contact/head/wake/support,
natural priorities and other directions. Cargo lifecycle and full-set master/
material/proportion/cross-family polish remain. Goal active. No commit/export.
''', encoding='utf-8')
print('Recorded live material review and scope; full Bill objective remains active.')
