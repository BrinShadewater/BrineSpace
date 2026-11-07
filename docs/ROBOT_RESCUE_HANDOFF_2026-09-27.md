# Robot rescue artwork handoff

Updated: September 27, 2026 · Brine Space · Josh and River rescue animations

Session closed at owner request. Workspace HEAD at closeout: `0919899b8`; the
rescue work and concurrent project edits are uncommitted, so HEAD alone does not
identify the reviewed artifact. Selected browser revision: `occupied-3`.

## Objective and acceptance
Redo their rescue assets to match the accepted robot artwork. Owner approved the
current Josh and River rescue artwork and animations, revision `occupied-3`, on
September 27, 2026: "I think we can approve the robot rescue work." Preview: http://127.0.0.1:8775/character/robot-rescue-v1/ .

## Accepted decisions and constraints
Keep identities, scale, eight-second powered recovery, payment and unlock rules.
River's sage salvage bin now has a front unloading ramp; Josh retains double
crate doors. Margot's pod art is unchanged. No owner layouts are rewritten.

## Current state
`character/robot-rescue-v1/` preserves generated source/prompt, build, 26 selected
frames and browser review. Owner stiffness feedback led to eight authored opening
poses per crate with 100–180 ms moving holds and a 300 ms open settle. Initial
four-pose art and the rejected mixed-sheet proportion study remain as provenance.
Robot occupants reuse current poses without recolouring
or resizing. `scripts/companion_rescue_art.gd` samples opening/reboot and composites
rollout toward the spawn navigation point. `companions.gd` shares that point with
spawn; `grid_canvas.gd` selects the new sequence. The found-room clearance is applied
after saved layouts in `nursery_south_facing.gd`, preventing machinery from covering
River's ramp. Ordinary rooms reset the recovery metadata. Test and UID are paired;
the companion test group and review registry include the new work.
Two additional empty-open textures serve rollout/recovered states (28 selected
exports total). Raw sources, rejected studies and superseded exports are retained.

## Verification
Build validates 26 selected frames, binary alpha, transparent margins and 2.267 pixels/world
unit. Existing companion lifecycle/save/reward suite passed. Native recovery fixture
covers both containers, pause, power interruption, checkpoint restore, eight-second
handoff, matching exit position and empty recovered state. Tests isolate APPDATA;
profile fingerprints and native captures are under `output/margot-polish-native/`
and `output/robot-rescue-native/`. Initial fixture errors (unpaid repaired sites) were
fixed; the first visual pass exposed a saved-layout reapply obscuring River.
The smoothing revision passed `robot-rescue-smooth` native checks with the entire
real profile unchanged. Browser revision `hinges-2` was visually checked after
cache-busting the module, manifest and frame images; both openings have eight
distinct frame hashes and exactly 1,200 ms total duration.

## Next action
Owner's occupied-crate correction is implemented: opening frames composite the
existing resting robot through registered aperture masks, maintaining door/ramp
occlusion. Closed frames hide the robot; final opening equals first reboot exactly.
Separate explicit empty textures prevent a duplicate occupant during rollout or
after recovery. Preview revision is `occupied-3`; builder verifies reveal pixels
and the exact opening/reboot join.
The occupied revision's native animation assertions passed (zero failures) using
the scratch APPDATA runner. Its real-profile fingerprint check did not pass:
save/checkpoint/comms and session/report files changed during the run. Attribution
is not established; fingerprints are preserved in `robot-rescue-occupied-profile-check.json`.
No attempt was made to restore or overwrite the owner's active files.

Visual acceptance is complete for the current opening, reboot and rollout. This source change is not in the
existing Windows export; package only when requested. No commit or upload.

## Closeout maintenance
Updated the visual bible, DEVELOPMENT_NOTES, CURRENT_STATUS and
ASSET_PIPELINE_AND_WORKFLOW. Added `references/companion-rescue.md` and entry-point
links to both character and room skills, in the checkout and installed copies.
Pre-existing divergence in other skill references was preserved. Validation is
structural/link/mirror evidence, not a fresh behavioral skill trial. No additional
asset generation or gameplay testing was needed for this documentation closeout.
The current status file contains a non-UTF-8 byte from other work; its existing
bytes were preserved when inserting the ASCII closeout notice.
