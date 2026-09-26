# Project handoff

Updated: 2026-09-21 · Project: BrineSpace · Task: Current cast review board

## Objective and acceptance
Review selected animation sources accurately while continuing Bill repair.
No natural-gait or full-cast visual acceptance is claimed.

## Accepted decisions and constraints
No production sprite, runtime animation or owner-layout edits in this pass.
No Higgsfield. Preserve per-pack registration and unsupported-state distinctions.

## Current state
Fixed tests/test_sprite_polish.gd, which loaded retired Bill v2, Veld v1,
Branforth v1 and Marsh packs. It now reads Player.REVISION_ROOTS catalogs for the
four crew, retaining existing companion bindings. Drawing uses texture pivot,
standingHeight and aspect ratio; loops wrap and one-shot clips clamp. Missing
states say Not authored instead of silently drawing idle. --states and --output
allow focused review without generating the full matrix. Final log wording now
separates coverage/join checks from visual acceptance.

## Verification
Native --states=walk,carry generated 24 boards in
output/selected-cast-review-2026-09-21/. Coverage/join failures zero. Carry board
inspected; the first inspection exposed the old idle fallback, which was then
replaced by explicit labels and recaptured successfully. Last change only clarifies
log wording. This preview is time-sampled clip review, not distance-driven gameplay
or completion of Bill's gait repair. Current and prior native walking fixtures
remain separate evidence.

## Next action
Use these current sources for further cast comparisons. Investigate actual motion
or anatomy failures before changing clips; the runtime walk/carry handoff itself
was not established as defective in this pass.
