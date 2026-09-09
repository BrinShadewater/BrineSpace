# Project handoff

Updated: September 9, 2026 · Project: Brine Space · Task: room-specific riser art

## Objective and acceptance
Create room-specific riser walls with baked functional fittings, window treatments and reserved entry space; integrate and review at native scale.

## Accepted decisions and constraints
Six rooms: medical, hydroponics, maintenance, galley, command and observation. Existing 60-unit rise and 72-unit doors retained. A 92-unit central reserve separates fitting/window zones. Window depictions are static. No furniture or gameplay changes.

## Current state
assets/room-risers-v2 contains six original sources, prompts, registrations, six refreshed cards and a 24-view gallery. riser_catalog.gd adds room-specific overrides; north_wall.gd avoids duplicate default Studio fittings but retains explicitly placed mounts. Six card paths updated in room_card_art.gd and grid_canvas.gd. Original departmental sources and personal saves preserved.

## Verification
Godot 4.6.1: six face registrations, source bounds/aspect and reserve/zone checks; 24 native rotations visually reviewed. Shared-edge adjacency, Studio mount retention and all 47 card bindings pass. Evidence: output/room-risers-v2. Existing environment image-loader warnings recorded; no packaged or full animated-door acceptance claim. No executable rebuilt.

## Next action
Owner visual review of installed strips. Further window interchangeability or additional room-specific walls can extend this art pack; baked windows currently remain part of their wall textures.
