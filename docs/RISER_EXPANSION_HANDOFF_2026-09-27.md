# Project handoff

Updated: September 27, 2026 · Project: BrineSpace · Task: 28 bespoke expansion-room risers

## Objective and acceptance
Owner confirmed making unique riser walls for the 28 newer rooms that inherited
older room art. All 28 are generated and installed in source; owner visual acceptance
is pending. Review: `assets/room-risers-expansion-v1/index.html`.

## Accepted decisions and constraints
Match the painted structural collection. Keep three quiet infill panels for the
existing window/door overlays; identify rooms through shallow end fittings, lower
service bands and restrained materials. No new layouts, mechanics or paid Higgsfield
jobs. Preserve owner material overrides, all original masters and the other 47 rooms.

## Current state
`assets/room-risers-expansion-v1/` contains 28 unchanged generated PNGs, exact prompts,
reference hashes, previous bindings, measured registrations, provenance, source/native
review sheets and gallery. `assets/architecture-rollout-2026-09-26/walls.json` selects
these 28 wall/cap sources in both base and integrated modes. No renderer code changed.
`tools/review_riser_expansion.gd` and its UID supply the focused native review.
Pack scripts reproduce registration, gallery and isolated capture/card production.

## Verification
- Checkout index and HEAD both contain 36,418 paths; no committed paths absent from index.
- All 28 unique sources pass measured face/cap bounds, opaque-face coverage, exterior
  transparency, unclipped margin and aspect checks. PNGs use Git LFS. Fold Chamber has
  near-opaque alpha 253–254; the apparent tool-preview haze is transparent in the PNG.
  No image cleanup, recolouring or resampling changed source pixels.
- Godot 4.7.2: 112 native room orientations, 28 bare-wall captures, zero failures.
  All four native comparison sheets visually inspected: room materials, north doors,
  window reserves and joins fit; existing furnishings remain unchanged.
- Godot printed its isolated scratch user directory. Real-profile fingerprints changed
  in `last_session.json` and `room_layouts.json.recovery.json` during the review; separate
  live Godot processes were confirmed. Do not claim real-profile byte equality.
- All 28 cards baked with the maintained baker using a scratch copy of the owner's
  Studio layouts, decoded and installed at their existing registered paths. Three
  representative cards visually inspected; previous card bytes retained in the local
  evidence backup. Card run also changed the same two real-profile breadcrumb files
  concurrently; no profile restoration attempted.
- Gallery search, department filter and four-orientation disclosure passed browser
  checks; screenshot saved in `evidence/gallery-proof.png`. Local gallery served at
  http://127.0.0.1:8812/ and left open. No playable export, commit, push or release check.

## Next action
Owner reviews the bespoke collection. New room art and cards are source-integrated;
restart an already running game to reload cached textures. Make any requested visual
revisions as new candidates, retaining originals and exact prompts.
# Crew Fitness colour revision — September 27, 2026

Subsequent owner request: Cargo Dispatch, Crew Cinema and Music Room muted too.
Revised masters, exact prompts, provenance, bindings, cards and gallery installed;
each original retained under `revisions/<room>-v1`. Source audit passes. Music
Room's measured face ends seven pixels above its lower alpha fringe; source pixels
unchanged. Twelve native orientations passed, with Music Room's four repeated after
registration adjustment; all three q0 views visually reviewed. Three-card scoped
bake uses isolated APPDATA. Owner acceptance pending; no release export performed.

Owner rejected the bright orange. Built-in imagegen revised the large panels to
muted rust-brown, preserving the dark frame and fitness fittings. Master, exact
prompt, provenance, measured registration, live binding, card and gallery updated.
Original master/prompt/registration/provenance/card retained under
`assets/room-risers-expansion-v1/revisions/crew_fitness-v1`.
Source alpha/registration audit passes; four native orientations pass, q0 visually
reviewed. Scoped card bake passes with scratch APPDATA. Live owner session changed
`last_session.json` during native checks; no claim of profile byte equality.
Owner visual acceptance remains pending. Other room art unchanged.
