from pathlib import Path
import json

P = Path(__file__).resolve().parent
R = P.parents[1]
for name in ['native-staged', 'native-behaviour', 'native-installed', 'native-installed-behaviour']:
    report = json.loads((P / (name + '-validation.json')).read_text())
    assert report['exitCode'] == 0 and report['realProfileUnchanged'] and not report['timedOut'], name
assert json.loads((P / 'packaging-validation.json').read_text())['passed']
assert json.loads((P / 'selection.json').read_text())['runtimeInstalled']

def atomic(file, transform):
    before = file.read_bytes()
    after = transform(before)
    temp = file.with_name(file.name + '.james.tmp')
    temp.write_bytes(after)
    if file.read_bytes() != before:
        temp.unlink()
        raise RuntimeError('Concurrent edit: ' + str(file))
    temp.replace(file)

note = '''### James distress and recovery installed — September 30, 2026

Supersedes the earlier staging snapshot and pending side-source corrections.
Eight states/48refs per mode installed through literal normal grid loaders and
ACTIVE_ASSETS.json. Selected sources: E water v2/recovery master-only v4; W both
master-only v4; S v1; N v2. West now matches the partially occluded projected belt
tool edge. Existing shared helmet sources remain fitted at fixed physical size.
Earlier edits preserved incorrect camera/tool projection; remake from selected
masters when repeated edits keep inheriting the same defect. Do not force an
occluded belt tool into conspicuous near-side visibility.

Fixed anatomical rulers: E water25/65, dry25/135; W water25/60, dry25/76;
S water25/78, dry25/72; N22/66 both. Per-action source drawing densities differ;
one fixed cranial ruler per row preserves anatomy, never normalize pose heights.
Canvas256x360,p128224,standing148 gives transparent registration padding while
preserving exact swim endpoints and exact final idle pixels. Dry boot-contact and
prone cranial anchors are recorded separately. Retained960ms distress/3s recovery
clocks and metadata remain intact. Only distress life clearance was unioned.

528 package,1045 staged player,1044 installed player checks PASS. Both candidate
and installed controlled state fixtures passed467 checks each: actual low-air
selection,6 distress slots, safe-room recovery,6 timer slots, pause, interruption
and exact standing completion.96 installed captures and both boards reviewed.
Scratch APPDATA, real owner profile unchanged. Fixture explicitly changes room
water level; it does not prove refuge travel, dewatering, pathfinding, traffic or
all layouts. Installed status is owner_review_pending, not owner taste acceptance.
Current coverage173bare/171helmet states,3196/3172 slots;8 retained death states
remain. Full-set cross-family anatomy/material/motion/journey polish remains open.
See docs/JAMES_AIR_HANDOFF_2026-09-30.md.
'''
headline = '''## James distress and air recovery installed — September 30, 2026

Eight states in both modes installed after master-only side-source remakes.
528 package,1044 installed player and467 actual installed low-air/recovery checks
PASS; scratch owner profile unchanged. Native state boards reviewed, exact idle
completion retained. Controlled room-water fixture, not a refuge journey proof.
Eight retained ground/water death states remain; full-set consistency/polish open.
See [handoff](JAMES_AIR_HANDOFF_2026-09-30.md).

'''
atomic(R / 'docs/CURRENT_STATUS.md', lambda b: b if headline.encode() in b else headline.encode() + b)
for file in [R / 'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md', R / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md', R / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', R / 'skills/brinespace-character-pipeline/references/crew-consistency.md', Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    atomic(file, lambda b: b if note.encode() in b else b + b'\n\n' + note.encode())
supersession = b'> Superseded by [installed handoff](JAMES_AIR_HANDOFF_2026-09-30.md). This staging record preserves its original evidence scope.\n\n'
atomic(R / 'docs/JAMES_AIR_STAGING_HANDOFF_2026-09-30.md', lambda b: b if supersession in b else supersession + b)
(R / 'docs/JAMES_AIR_HANDOFF_2026-09-30.md').write_text('''# Project handoff

Updated: 2026-09-30 · Project: Brine Space · Task: James distress/recovery installation

## Objective and acceptance
Complete James's animation set and cross-family consistency/polish. This milestone
installs8 distress/recovery states; owner visual acceptance and full-set completion
remain unclaimed.

## Accepted decisions and constraints
Matte neutral current masters, fixed anatomy/camera, original belt-tool ownership.
Retain960ms distress and3s recovery. Exact current swim and idle seams; no pose-height
normalization. Reversible installation authorized by continued animation work.

## Current state
character/james-air-family-v1 plus four james-air-facing source folders installed.
Normal grid literal loaders, ACTIVE_ASSETS.json and distress-only life clearance
updated. Source E waterv2/dryv4, Wv4, Sv1, Nv2. Original candidates preserved.
256x360,p128224,standing148;48refs per mode. Current selected inventory173bare/
171helmet states,3196/3172 slots;8 retained death states remain. Pipeline/bible/
continuation and canonical+installed consistency skill record the source lessons.

## Verification
528 package,1045 staged and1044 installed player checks PASS.467 candidate and467
installed behavior checks PASS through actual RoomFlooding.step_crew, life chooser,
normal grid rendering and live clearance.6 distress+6 recovery slots per case;
pause, interruption and exact final standing handoff.96 installed captures and
both native behavior boards visually reviewed. All wrapper profiles unchanged.
Controlled room-water toggle proves state/timer/render behavior, not actual
refuge travel, dewatering, pathfinder/traffic or every room layout.

## Next action
Death family masters/contracts prepared in character/james-death-family-v1 and
four james-death-facing folders. Author8 ground/water death states, review physical
fall/floating registration and shared helmet pitch, preserve finite terminal holds,
validate normal runtime death selection and paused/terminal playback. Then full
cross-family consistency and journey polish. No commit/export/full-set completion.
''', encoding='utf-8')
print('Recorded installed AIR milestone;8 retained death states and full-set polish open')
