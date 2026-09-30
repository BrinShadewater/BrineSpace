# Project handoff

Updated: September 29, 2026 · Project: BrineSpace · Task: card artwork batch 3

## Objective and acceptance
Deliver frame, department emblems, rarity marks and back in the maintained matte
painted style, retaining card geometry and text at 960/1280/1600/2560 widths.

## Accepted decisions and constraints
Logical card 200x284. Physical cards at those widths: 100x142, 133.333x189.333,
166.667x236.667, 266.667x378.667, from the 1920x1080 design viewport. Nine-slice
corners 16px; existing content margins 8/8/8/7. Plain linear filtering retained.
Neutral inner stock stays separate from department trim. Colors derive from the
existing RoomDatabase.room_color result and muted conversion. Emblems 16px,
rarity marks 12px beside unchanged text. Hallways do not get an Engineering mark.
Derelict is a condition/registry category. Removed draw/discard controls stay hidden;
back is delivered and wired only to the existing retained pile renderer.

## Current state
15 PNGs, two immutable built-in imagegen sources, exact prompts/symbol geometry,
manifest, bake, raster validator, contact sheet, native before/after captures and
metric comparison in assets/sea-life-v1/cards. Runtime: scripts/card_art.gd,
draft_card.gd and a two-line card-style replacement in main.gd. Raw loader validates
dimensions, caches and warns once; old flat frame/back rendering remains fallback.
Tests have paired UIDs. tools/check_card_art.py isolates all Godot profiles.
Shared release manifest/build metadata/import roles refreshed; no executable export.

## Verification
75 raster checks and deterministic rebake pass. 28 runtime checks cover all art,
neutral stock, content margins, mark sizes and fallback. Eight native screenshots
at all four widths pass exact card/text geometry comparison and visual review.
Baseline: output/card-art-20260929-200834; accepted after: -201553; runtime: -202037.
Card drag reports PASS in output/lighting-20260929-201652 (older wrapper incorrectly
classified its literal PASS report; raw exit0/log are the evidence). Hand backdrop
PASS: output/card-art-20260929-201811. Owner fingerprints unchanged on these runs.
Existing card-binding parity script fails on 28 newer room IDs outside its database
identity parser; this batch changes none of those bindings/catalog entries.
An initial capture encountered an in-progress drone_dust compilation error, corrected
by the concurrent session before the accepted baseline; no unrelated source edited.

## Next action
Owner review of card artwork. Next batch is screen-effect maps; do not start it
until requested. Commit only this pack/helper/tests/runner/draft-card changes and
the card-style hunk in main.gd; other dirty changes belong to concurrent sessions.
