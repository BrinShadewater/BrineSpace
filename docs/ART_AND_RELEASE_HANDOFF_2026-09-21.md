# Art and release handoff

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance

Continue the bought-art migration: natural room decoration, coherent character and
environment style, Bill's walk repair, stable release preparation and maintained
bible/workflows/skills. Technical checks alone do not establish art acceptance.

## Accepted decisions and constraints

Large/medium props form logical work areas; no random accessory scatter or blanket
upscale. Preserve owner layouts and library marks. No Higgsfield without an explicit
request. Apple Silicon is the owner's Mac testing target. No publication requested.

## Current state

- Windows migration build `brinespace-66abbef9bc1a8278` passed actual-release startup,
  simulation and F8 checks. Runtime legacy bindings and export guards were repaired.
- Mac candidate `brinespace-97c09d09887b0d5b` is in
  `builds/BrineSpace-mac-2026-09-20`, with README, notices and checksums. Local ad-hoc
  signing only; no notarization or native Mac acceptance.
- Crew Hab remains unchanged after the owner's provisional positive feedback.
  Maintenance/Bio revision 02 remains installed. Revision 04 is staged under
  `output/room-composition-pilot-2026-09-20/revision-04`; its current candidate omits
  the undersized drawer. Do not restore the earlier scale workaround.
- Bill's six west-walk PNGs now have the bounded enclosed-alpha repair (74 pixels total); broader motion is unchanged. Existing reconstruction exactly reproduces
  the 12 bare side-view frames and their joint defects. Generated alternatives failed
  phase/identity control; preserved as rejected, not integrated.
- Bible and maintained/installed pipeline skills record the findings. Export helper,
  manifest selection and explicit test-runner selection checks were improved.

## Verification and limits

Mac exact-PCK audit: 15,085 checked, zero missing/changed/unexpected. Bundle has
arm64/x86_64 and executable ZIP permissions. Windows cannot establish Mac gameplay.
Revision 04: eight views, 1,280 walking samples, zero failures. Only the recorded
views have visual review; owner acceptance is still open. Current starred/rename
fix queues are empty. Selected prop inventory is not proof of defect-free artwork.
Mac helper preflight and focused tests pass; the helper's full export command has
not been exercised. Existing candidate predates the helper. No Godot process was
running at this handoff; no export or native capture needs polling.

## Next action

Continue local Bill pixel-layer repair; the owner has authorized it and supplied
all ten reference rooms. Whole-limb studies remain unaccepted; production motion is unchanged apart from the separately recorded enclosed-alpha repair. Improve staged Maintenance/Bio compositions using these references.
The native live-geometry probe now confirms `library/tileset-lab-36` blocks the
Research q2 north-door center approach too. Other rotations are clear. A production Bill graph fixture confirms no route to the connected corridor in q2.
The separately staged research-door-candidate.json moves that one prop to (-170,112)
and restores routes in all four rotations. Four-view/640-sample composition checks
pass and q2 was visually reviewed. Owner saves remain unchanged; candidate awaits
visual acceptance.
Do not rearrange the owner reference to satisfy the review tool. Mac native testing
remains outstanding independently of local work.

Detailed evidence: BILL_WALK_REVIEW_2026-09-20.md,
ROOM_COMPOSITION_PILOT_2026-09-20.md, RELEASE_MIGRATION_2026-09-20.md and
MAC_RELEASE_PLAN.md. The overall goal is incomplete.


### Owner resumed and resolved input dependencies

The owner has now explicitly authorized script-assisted pixel-layer repair and
named ten hand-edited rooms (listed in CURRENT_STATUS.md). Preserve those rooms;
use the fresh output/owner-room-references-2026-09-21 snapshot for reference.
The former method/reference questions are no longer blockers. The goal also
explicitly includes observed animation defects, bug fixes, polish and performance.
Local joint-patch study started; not accepted or installed. Mac native test remains
pending independently of the ongoing local work.

### Latest character milestone

Upper-motion revision 2 is now integrated (20 changed side-view bare/helmet PNGs),
in addition to the six-frame pinhole repair. The source builder restores preserved
upper poses [0,1,2,5,2,1]; all lower-body pixels remain selected-production pixels.
11,773 complete-pack checks and 240 post-integration native equipped samples pass.
Keep remaining leg contours/overall motion quality open; no owner approval claimed.
Packaged Windows/Mac candidates are older and do not include these sprite changes.

### Performance checkpoint

40-cycle modest-station budget passes (800 frames, 0.90 ms mean/12.9 ms worst).
Soak reporting now counts every slow frame and reports actual completed cycles.
A separate normal-run report correctly stops at seven cycles/140 frames; no errors.
These are headless simulation measurements, not rendered FPS. Evidence is under
output/performance-2026-09-21. No gameplay rules or runtime performance paths changed.

## Maintenance repair-bay pilot installed — September 21, 2026

Revision 05 replaces the isolated diagnostic desk with two adjoining medium tool
benches, forming a manual repair bay opposite the robot assembly station. CNC and
parts storage remain across the upper work area. Native four-view/640-sample review
passes; q0/q2 visually inspected. Installed only four Maintenance keys in defaults
and owner saves, after verifying the owner keys still matched previous defaults;
all other keys preserved. Backups and evidence: output/room-composition-pilot-2026-09-20/revision-05.
The single Maintenance card was rebaked and visually inspected. Bio remains at
installed revision 02, with revision 04 staged; ten owner reference rooms unchanged.
This is an installed pilot for owner review, not owner visual acceptance.


## Bio Lab pilot and console registration repaired — September 21, 2026

Installed the previously staged revision 04 Bio layout: aligned preparation and
analysis benches, separate culture equipment, and rotation-specific console placement.
Four native views/640 walking samples pass after correcting lab-20's source region:
[144,389,144,91] included a neighbouring table edge and clipped the chair;
[180,389,108,115] contains the complete workstation. Region, absolute pieces,
display width and footprint were rebuilt together using the maintained helper;
source PNG unchanged, stable ID retained. Registry validation passes 10,507 props.
Only four Bio layout keys changed in defaults and owner saves after matching the
prior defaults; all other keys preserved. The single Bio card was rebaked.
Evidence/backups: output/room-composition-pilot-2026-09-20/bio-final.
Installed for owner review; no owner visual acceptance claimed.


## Next room pass and Galley serving candidate — September 21, 2026

Reviewed Galley, Cold Store, Clone Lab and Isolation Vault from a fresh owner-layout
snapshot: 16 native views/2,560 walking samples pass. Q0 images visually inspected;
Cold Store and Clone Lab already have readable groupings and remain unchanged.
Galley lacked a substantial serving area. A separate candidate adds adjoining hot
food and salad counters (mms-58/mms-60 at 0.75 scale) along the lower-left side;
existing kitchen, seating and vending stay in place. Door-dependent y positions
avoid the relocated vending unit in q2/q3. Four views/640 samples pass; q0/q2
visually inspected. Candidate not installed; owner references remain unchanged.
Evidence: output/room-next-pass-2026-09-21 (galley-candidate.json and galley/).


## Galley serving addition installed in saved layouts — September 21, 2026

Production Bill graph probe reaches both meal-service points in each of four
Galley rotations (eight routes, exact station-node matches) with the candidate.
The saved Galley layouts differ from shipped defaults, so installation adds only
the two serving counters' placement/scale fields to the four saved layouts after
verifying they still match the preview snapshot. No other saved placement changes;
shipped defaults remain unchanged. The Galley card was rebaked from saved layouts,
consistent with the current card workflow. Before-state backup and evidence:
output/room-next-pass-2026-09-21 (service-routes.json, owner-before-galley-install.json,
galley-card.log). This is a local composition addition, not a shipped-default update
or owner visual acceptance. Exported builds will not acquire these user layouts.

