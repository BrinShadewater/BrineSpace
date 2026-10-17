# Project handoff

Updated: 2026-09-30. Project: BrineSpace. Task: Veld north/east cargo turns.

## Objective and acceptance
Continue from installed east/south turn pair. North-east and east-north pivot-v1
are staged, not installed, for owner visual review.

## Accepted decisions and constraints
Accepted rear and east carry poses define identity, matte palette and equipment.
Rear-to-side rotation keeps scanner on character left and canisters on character
right. Case sits in front on the far side in rear view and gradually becomes
visible beyond the right silhouette. Exact accepted carry frame-zero endpoints
match the runtime destination handoff. Original800ms nonloop facings and dry
cargo metadata retained; canvas256, pivot128/224, standing height148. Reverse
turn uses the same frames reversed, without mirroring equipment.

## Current state
Built-in imagegen source-v1 and exact prompt-v1 saved. Six poses per variant,
including four authored intermediate rear/three-quarter/side views. build.py
registers boots and applies one pooled neutral material curve per variant;
face/hair contrast preserved. Both endpoint poses replaced by exact accepted
carry frame zero.24 frames, two manifests, four GIFs, contact/native/browser
preview and provenance checks saved. Review playback slowed independently
of runtime. No loader or ACTIVE_ASSETS changes for this staged candidate.

## Verification
102 packaging checks pass: original metadata, clipping, decoded GIF exteriors,
exact endpoint pixels and reverse equality.123 native checks pass including
both equipment variants and runtime turn selection/destination frame-zero
handoff. Source/contact and browser preview visually inspected. Native probe
used scratch APPDATA; real profile fingerprints unchanged. Owner visual
acceptance pending; technical checks do not establish motion acceptance.

## Next action
Owner review, then install on acceptance. Remaining north/west, south/west and
180-degree cargo turns unchanged. No commit, push or export.
