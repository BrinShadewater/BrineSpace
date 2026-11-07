# Project handoff

Updated September21,2026 · BrineSpace · Holographic Core analysis display

## Objective and acceptance
Repair baked chart emission while preserving the physical stand and original pack.
Keep owner room layouts/marks safe. The broad project objective remains unfinished.

## Current state
New registrations/holo-chart-v1.json references the existing undercity/16.png atlas;
only the lower stand region (local y45..76) is sampled. No raster generation/edit.
The Holographic Core custom renderer supplies a dark physical panel, restrained grid
and visual-clock-driven trace. Offline removes the grid/trace, not the stand/panel.
Shared bought entry cyb-146b remains unchanged for other consumers.
Four complete room-holographic_core keys substitute the dedicated chart with exactly
the previous placement/scale. All other saved/default keys guarded unchanged.
Updated card. The previous projector/calibrator implementation is retained.

Changed code: rooms/full-wall-v1/holographic_core_view.gd; extended existing native
regression tests/test_removed_bank_restoration.gd, keeping its UID. New registration
rooms/full-wall-v1/registrations/holo-chart-v1.json. Defaults/save/card updated.
Evidence and backups: output/holo-chart-2026-09-21/.

## Verification
Four-room/four-quarter/repeated-setup regression passes with chart custom/live-path
assertions. Four-quarter render fixture checks animated changes separately in each
of projector, calibrator and chart, all confined to their bounds. Off/held-clock
stable; lower40percent of chart bounds (stand) is pixel-identical between off/on.
Native candidate/default review each four views/640 walking samples0failures;
full RGBA candidate/default parity exact in all four. Powered four-view images and
q0 offline reviewed. Live52/75-percent fixture completed; native crop reviewed.
Actual station pause: visual clock advances running, then clock and complete room
RGBA stay identical while paused across0.4seconds plus rendering settles. Completed
single-room card bake inspected. No paid-balance or full expedition claim.

## Next action
Batch the recent room layouts, Radio/Holo placement fixes and layered display repairs
into maintained Windows/Mac exports, with exact PCK audits and actual Windows release
checks. Native Apple Silicon play remains owner-hardware work. Overall room visual
acceptance, other source-detail issues and Bill motion acceptance remain open. The
old c09c packages do not include these changes. No Higgsfield or publication used.
