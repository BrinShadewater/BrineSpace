# Project handoff

Updated September21,2026 · BrineSpace · Powered-display redraw reduction

## Objective and acceptance
Avoid clock-only redraws for the new displays while unpowered, preserving exact
pixels and correct return to live animation. Broad project goal remains unfinished.
No source art, layout, gameplay, release package or owner marks changed.

## Current state
Radio signal console and Holo layered projector/chart return operating from their
is_animated_prop branches. The existing retained canvas operating-state key redraws
state transitions; no shared renderer rule changed. Other machine classifications
remain as before. Changed rooms/full-wall-v1/radio_lab_view.gd and
holographic_core_view.gd. Added tests/test_powered_display_retention.gd with its
Godot-generated UID and room-art/native index entry.

## Verification
Native before test reports8expected-count failures: each off Radio console draws
12times/12frames; Holo projector+chart24times. After change all counts/parity pass.
Stronger final fixture reuses identical queue and prop objects across on/off/on,
so power state itself must invalidate cached slots. Two rooms/four quarters/three
states each,12advancing frames per state: off redraws0, active counts12/24, no
clock-only static redraws, all24retained/direct images byte-exact. Offline q0
retained images inspected. Native test runner classifies the new test correctly.
Evidence: output/powered-display-retention-2026-09-21 (before.log,after.log,
same-queue.log and current captures). Old snapshots at shared paths were replaced
by the stronger final fixture; before counts are preserved in the original log.

## Next action
This is a scoped command-redraw reduction, not measured total render/FPS improvement.
Current0b2b3ab132bb4781 exports predate this and Radio feedback; batch future fixes
before another export. Continue broader expedition, Bill/art acceptance and measured
performance work. No full-station parity run was needed or claimed for this
three-prop classification change; exact focused on/off/on parity is the evidence.
