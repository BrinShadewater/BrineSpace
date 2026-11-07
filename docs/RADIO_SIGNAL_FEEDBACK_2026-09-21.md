# Project handoff

Updated September21,2026 · BrineSpace · Radio signal-panel feedback

## Objective and constraints
Repair static signal imagery using source-local powered displays, preserving
physical panel artwork and all layouts. No Higgsfield or source image generation.
The broad goal remains active; full-game and owner visual acceptance remain open.

## Current state
rooms/full-wall-v1/radio_lab_view.gd now masks the two existing screen apertures
with dark glass offline and draws restrained green waveforms when operating.
Source rectangles [144,322,237,163] and [874,322,237,163] map through life_point;
knobs, cables and bezel source pixels remain unchanged. Waveforms derive from
machine_clock; live classification includes the signal console and its source ID.
Changed regression: tests/test_removed_bank_restoration.gd (paired UID retained),
checking the console remains present/live across repeated rotation setup.
Refreshed assets/room-cards-v2/radio_lab.png in its normal offline card state.
No default/saved layout, source atlas or owner registry data changed.

## Verification
Four-quarter native effect fixture passes: each aperture has moving pixels;
all time-varying and off/on changes remain inside the two screen rectangles plus
2pixel raster tolerance. Off and held-clock images stable. This is stronger than
accepting arbitrary changes somewhere within the whole console. All four powered
views, native live crop and completed card inspected. Four-room repeated-setup
regression0failures. Actual station visual clock advances running, then clock and
complete room RGBA stay identical through pause (0.4seconds plus settles). Live
fixture completed52/75-percent views. Layout/default byte guards passed.
Evidence: output/radio-signal-feedback-2026-09-21/.

## Next action
Current Windows/Mac 0b2b3ab132bb4781 checkpoint predates this screen/card update;
batch future fixes before another export. Continue normal expedition and Bill
motion review, remaining source-detail issues and measured performance work.
The panel's decorative source indicator lamps were not redesigned; this verification
specifically covers its two signal displays, not every light in Radio Lab.
