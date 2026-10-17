# Project handoff

Updated: 2026-10-02 · Project: BrineSpace · Task: Krusher first character sheet

## Objective and acceptance
Create Krusher's first character sheet from the supplied face reference, matching
existing crew style, density and stature. Owner visual selection is pending.

## Accepted decisions and constraints
Owner direction: existing Bill, Veld, James and Marsh models become reusable body
base options chosen by likeness/build (Veld suggested for female characters).
See `docs/CREW_BASE_MODEL_DIRECTION.md`. Bill is a proposed Krusher starting base;
no derived pack or reusable-base implementation has been made.
Owner accepted the muted cyan direction and set the full name to **Krusher Dom**
and exact title to **System Administrator** (singular). AI & Robotics department.
`identity.json` records these decisions. Older title proposals are superseded.
Owner requested a computer-focused character named Krusher and a character sheet
first. Owner subsequently placed Systems Administrator under AI & Robotics with
matte cyan markings; this supersedes the initial Engineering yellow proposal.
Preserve swept brown
hair, fair complexion, blue-grey eyes and short beard. Shared graphite pressure
suit, terminal on anatomical left hip, tester/data cartridges on right.

## Current state
Current sheet: `concept-04-krusher-dom.png`, updated header only via built-in
image_gen; exact prompt/provenance in `full-name-prompt.txt` and
`full-name-provenance.json`. Agent reviewed name/title spelling and retained
muted cyan character design inline. PNG decode passed. Earlier sheets retained.
Latest: `concept-03-muted-cyan.png` supersedes the brighter cyan candidate following
owner feedback. Markings use dusty desaturated grey-cyan with matte shading.
Exact prompt/source recorded in `muted-cyan-prompt.txt` and
`muted-cyan-provenance.json`. Agent reviewed the inline image: shoulder colour is
substantially quieter, all views intact, original identity and suit consistent.
PNG decode passed; owner visual selection still pending. Previous revisions kept.

`concept-02-cyan.png` is the current design revision: matte cyan shoulders and
cartridge markings across all views, made with built-in image_gen. Exact edit
prompt and provenance are in `cyan-revision-prompt.txt` and `cyan-provenance.json`.
Agent visually reviewed the inline generated sheet: likeness, layout and suit
remain consistent; cyan paint is matte without bloom. PNG decode passed. Inline
image delivery replaces the local-file preview for mobile review. Initial sheet
and scale board below retain their historical yellow treatment.

`concept-01.png`: 1672×941 RGB sheet, hero plus south/east/north/west turnarounds.
`prompt.txt`: exact built-in image generation prompt.
`provenance.json`: original generation source and reference hashes.
`build_review.py`, `scale-review.png`: repeatable static comparison at a 148px
standing ruler, plus historical room-context composite at approximately 74px.
Source art stays intact; the concept background is intentionally opaque.
No gameplay, character selectors, animation packs or owner saves changed.

## Verification
Agent viewed the complete sheet and reduced comparison. Face/hair/beard and matte
suit family read consistently; all four bodies are complete. Equipment placement
appears directionally consistent. Krusher's detailing is somewhat sharper than
Bill's selected sprite; final export material/density calibration remains needed.
The room image is an explicitly labelled historical static composite, not native
Krusher gameplay evidence. PNG decode passed. No Godot tests required for concept.
No animation, transparency, registration, transition or owner acceptance claim.

## Next action
First Bill-body trial is now in `character/krusher-bill-base-test-v1/`; see its
handoff for132south idle/walk frames and669passing checks. Owner review pending.
Review design/title with the owner, then use the selected identity to establish
registered transparent neutral cardinal masters at the current 148px crew density.
Prove idle, walk and terminal interaction before expanding the shared crew action
matrix, helmet fitting and life states. Inspect current consumers when packaging;
older 74px/92px exports are historical profiles, not the current density target.
