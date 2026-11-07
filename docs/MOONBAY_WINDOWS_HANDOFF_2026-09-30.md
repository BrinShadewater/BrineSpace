# Project handoff

Updated: 2026-09-30 · Project: BrineSpace · Task: Inner sub-bay observation windows

## Objective and acceptance
Owner requested windows on the inner sub-bay walls. Six framed observation-window assemblies installed and visually reviewed in all four rotations; owner hands-on acceptance remains open.

## Accepted decisions and constraints
Two wide windows on each lateral bay wall and two shorter windows above/below the crew airlock opening. Keep the ocean gate, low wall height, seamless corners, pressure interlocks and crew routes. Glazing is restrained blue-green with steel frames, pressure mullions, subtle reflections and recessed fasteners.

## Current state
rooms/large-rooms/moonbay.gd adds observation_windows and a procedural inset-glass drawing helper. Window registration rotates with the actual bay walls; frames use the existing top-surface offset. Sealed wall collision remains unchanged. Only Moonbay's artwork and assets/large-room-cards/moonbay.png changed for this correction. No new raster dependencies or gameplay changes.

## Verification
Native geometry/rotation probe PASS: all six frames are contained by actual wall segments and clear the wet-side doorway in all four orientations. Four 640px room views inspected; maintained Moonbay-only card bake succeeds. Scoped whitespace check passes. Scratch APPDATA throughout; 2,924 owner files fingerprinted with zero changes. Initial local type-inference error was corrected before final passes. Evidence: output/moonbay-observation-windows-20260930/ (native views, probe, logs and fingerprints).

## Next action
Reload source game or Studio for owner review. No export or publication performed. Earlier water and pressure handoffs remain current for their behaviors; their media predates these windows.
