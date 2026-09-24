# Solar/Tidal furnishing review

Updated September 21, 2026. Broad polish objective remains active.

## Objective and constraints
Remove overlapping equipment and compose readable service groups in unprotected
rooms. Solar Array and Thermal Power Control refer to the same room identity here,
not two separate catalog entries. Preserve owner rooms and library marks.

## Current state
Installed: `output/generation-room-review-2026-09-21/candidate-r1.json`.
Saved/default snapshots and guarded promotion script sit beside it. Eight keys changed
in defaults and player layouts; every other key preserved. Both room-card PNGs in
assets/room-cards-v2 refreshed, visually reviewed and LFS filters verified. Source
art and registry unchanged. Existing thermal/tidal primary machinery stays;
bought overlays and loose valve/gauge accessories are hidden. Solar retains a
transformer, operator terminal and tool cabinet; Tidal retains grouped controls and
a medium barrel. Positions are quarter-specific around the actual door ports.

## Verification
Current saved native review: eight views, 1280 walking samples, no route failures,
but numerous visual overlaps. Native images show equipment hidden under other props.
R1: eight views, 1280 walking samples, zero failures and zero reported visual overlaps.
All eight candidate views visually inspected; retained medium props have consistent
bounds across quarters. Both rooms pass four-quarter operating/offline/held-clock
pixel checks, preserving existing machinery feedback. These do not certify every
decorative lamp or actual station pause. Isolated funded native station at two zoom
levels passed framing; focused gameplay-scale crops reviewed. Not balance evidence.
Installed saved/default reviews each pass eight views/1280 walking samples; all16
decoded RGBA comparisons against the candidate are identical. Both cards reviewed.
Main machines are readable again. Owner aesthetic acceptance remains separate.

## Next action
Continue remaining room and animation review; obtain owner composition feedback.
Batch these changes into a future release refresh. Current validated
867eac6b1b17b4fc packages remain unchanged and predate this integration.
