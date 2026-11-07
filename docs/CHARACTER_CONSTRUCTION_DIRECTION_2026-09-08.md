# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: character construction animation direction

## Objective and acceptance

Owner requested a blowtorch animation and a reusable visual sequence showing rooms slowly being constructed. Owner proposed that opening construction be performed by the character from existing rooms. These move ahead of general console/seating animation in the animation priority discussion.

## Accepted decisions and constraints

- Produce a recognizable character blowtorch action and gradual room assembly.
- Treat character-led opening construction as the proposed gameplay direction; exact controls, pacing and the later handoff to drones are not settled.
- Preserve paid room costs and resource failures. Existing animation and room geometry remain authoritative inputs.

## Proposed animation contract

Character: approach a work point in the existing room, ready the torch, perform a repeatable welding pass, stop the torch, and recover to idle. Keep the feet and torch contact point registered. Use a small localized flame and restrained sparks; avoid a room-wide glow. Begin with an east-facing Bill pilot; eventual construction from any side needs separately reviewed north/south/east/west coverage and coverage for each selectable architect. Do not substitute Veld's sample-inspection repair clip for welding.

Room: foundation/support grid -> structural frame -> floor and hull panels -> interior fit-out -> completed room. Use shared structural stages with the actual destination room's final floor, doors and furnishings. This is a proposed stage breakdown, not an approved set of percentages or build durations. Keep the existing connection sealed until completion; the builder works on its interior side in the first proposed prototype. This avoids requiring a diving suit before the first expansion.

Tie assembly to completed construction work, not a looping cosmetic timer. Paused or interrupted work holds its visible stage. Resume from saved progress. Torch motion and effects run only during active work. A reusable room sequence can also serve later drone builders.

## Current state

This document and the linked CURRENT_STATUS entry record the direction. No new animation source, runtime construction change or gameplay acceptance is claimed.

Current code uses BRINE's emergency construction drone for opening builds, with a ten-second work phase; dedicated builders use six seconds. Orders pay costs and reserve their cell before the operational room is added. See scripts/drone_fleet.gd and docs/DRONE_FLEET.md. Character-led construction therefore needs a builder assignment/approach integration, not merely a sprite replacement.

## Verification

Read the current crew playback contract, activity controller, construction assignment/status code and art pipeline constraints. Documentation-only change; no engine or asset tests run. Native motion, tool contact, room-stage geometry, interruptions and Save/Continue remain unverified for this proposed feature.

## Next action

The owner subsequently accepted the playable first pass. See [implementation and verification](CHARACTER_CONSTRUCTION_IMPLEMENTATION_2026-09-08.md) for the current state; the direction and unimplemented baseline above preserve the earlier discussion.
