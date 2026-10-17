# Project handoff

Updated: 2026-09-30. Project: BrineSpace. Task: Veld north pickup.

## Objective and acceptance
Owner accepted north unload master-v1; installed. North pickup derived-v1
was owner accepted and installed on2026-09-30.

## Accepted decisions and constraints
Exact reversal of the accepted unload frames, preserving rear posture,
gloves, matte materials, helmet fit and equipment ownership. Original pickup
520ms nonloop timing and dry cargo metadata retained. Canvas 256, pivot128/224,
standing height148. Review playback slowed independently of runtime timing.

## Current state
build.py derives twelve bare/helmet frames in order5/4/3/2/1/0. Source provenance
hashes, manifests, GIFs, contact sheet and preview saved. No new artwork.
Accepted idle exit becomes pickup entry. Outer case occlusion follows the
accepted source; the visible center remains the same.

## Verification
56 packaging checks passed: exact source pixels, original metadata, clipping,
decoded GIF exterior and accepted idle entry. Contact sheet visually inspected.
59 candidate native checks passed with scratch APPDATA. Installed north unload
selection independently passed59 checks. Real profile fingerprints unchanged
in both verification intervals. Installed selection additionally passed59 checks with scratch APPDATA; real profile unchanged. Owner accepted.

## Next action
East/south cargo turn pair pivot-v2 staged for review; other turns remain.
No commit, push or export.
