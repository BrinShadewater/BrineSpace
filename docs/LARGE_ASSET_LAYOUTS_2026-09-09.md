# Large-asset layout correction

Updated: September 9, 2026 · BrineSpace

## Objective and accepted direction
Owner wants uncluttered rooms with 3–4 large assets. This supersedes the earlier denser preferred-layout pass. A continuous fitted bank counts as one asset even when rendered as several pieces; doors and the shared hull are architecture. Existing rooms with fewer pieces stay simpler, without filler. BRINE retains its chamber and two corner banks, leaving its fourth slot for the opening recovery pod.

## Changes
Removed 139 prop instances across 97 orientations. Authored defaults cover all 188 Studio orientations; all 176 furnished orientations have at most four major assets. Kept assets retain their previous size and placement. No art regeneration, runtime hard cap, new gameplay rules or forced furniture additions.

Updated `rooms/full-wall-v1/default-layouts.json` and the owner's existing `room_layouts.json` removals, so personal overrides cannot resurrect the discarded props. Original personal bytes are backed up at `output/large-assets/owner-before.json`; prior defaults are `defaults-before.json`. Remaining owner coordinates/settings are preserved. Supersedes the previous handoff's unchanged-personal-file statement.

Refreshed 44 native cards in `assets/large-assets-v1/cards` and updated the primary/grid/variant paths in `scripts/room_card_art.gd` and `scripts/grid_canvas.gd`. Corridor artwork is retained.

## Verification
Native inventory matches all 176 kept-prop lists exactly; grouped asset count never exceeds four. All 188 editor/runtime comparisons match, and all eight rotation sheets were reviewed. Production crew route regression passed across 176 orientations before the final eight additional removals; those removals cannot introduce blockers. Card consistency passes for all 47 identities with decoded PNGs. Logs, snapshots and per-orientation kept/removed lists are in `output/large-assets/`.

## Next action
Review locally in the game or reopen Layout Editor. No executable rebuilt. Source, assets, and personal layouts are updated; previous layouts remain recoverable from the backups.
