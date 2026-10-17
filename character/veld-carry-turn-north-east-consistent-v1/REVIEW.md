# Project handoff

Updated:2026-09-30. Project:BrineSpace. Task:Veld north/east stationary cargo turn.

## Objective and acceptance
Owner requested feet together after pivot-v1 review. Feet-together-v2 was
owner accepted and installed on2026-09-30, in both directions and bare/helmet variants.

## Accepted decisions and constraints
Stand with boots adjacent and planted throughout, including first/last poses.
No split walking stride, lifted heels or staggered foot placement. Connected
hips/body and steady two-hand case grip; rear-to-side angles and equipment
ownership retained. Original800ms nonloop timing, dry cargo metadata, canvas256,
pivot128/224 and standing height148 retained.

## Current state
Built-in source-v2/prompt-v2 correct stance only. Earlier source-v1/prompt-v1,
build-pivot-v1.py, validate-pivot-v1.py, native-pivot-v1.png and REVIEW-pivot-v1.md
preserve previous evidence. build.py now retains all six authored stationary
poses. IMPORTANT: no longer replaces endpoints with accepted locomotion frame
zero, because the east walking stride conflicts with the owner's stance request.
Turn endpoints therefore are not pixel-identical to installed carry gait. Live
locomotion packs and runtime logic remain unchanged.24 frames, manifests/GIFs,
contact/native/browser revision saved. Reverse direction exactly reverses poses.
One pooled neutral cloth curve per variant; face/hair details preserved.

## Verification
118 packaging checks pass: original metadata, clipping,24 decoded GIF exteriors,
reverse equality and planted boot-span guard. Reviewed source contact shows both
boots together in all views; guard is geometry evidence, not a visual substitute.
123 native checks pass: candidate pixels, dimensions/pivots/equipment, timing,
runtime turn selection and exit to existing locomotion frame zero. Native probe
used scratch APPDATA; real profile unchanged. Endpoint-to-locomotion visual
continuity is separate from functional handoff and needs review at installation.
Owner accepted. Actual installed selection additionally passed123 native checks
with scratch APPDATA. Real profile deltas: logs, bug report zip and last_session;
attribution unknown, listed in native-installed-v1-checks.json.

## Next action
Installed. installed-handoff-contact.png reviewed: upright pivot changes into
existing stepping gait; authored head/helmet detail and suit silhouettes differ
from locomotion, so this is not pixel-identical continuity. Other installed directional carry and east/south turn
poses unchanged. North/west turn candidate is next; south/west and180-degree turns unchanged.
No commit, push or export.
