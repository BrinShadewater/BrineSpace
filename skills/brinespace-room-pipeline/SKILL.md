---
name: brinespace-room-pipeline
description: Use when generating, repairing, reviewing, or integrating BrineSpace room graphics, room-card art, doorway layouts, or functioning-room visual effects.
---

# BrineSpace room pipeline

Produce usable room assets, not just attractive images. Keep geometry authoritative
and distinguish **generated → cleaned → geometry-validated → integrated → verified**.
Track rejected candidates separately; counts at one stage never imply another.

## Establish the contract

Locate the BrineSpace checkout from the active workspace; never assume a drive
path. Read its AGENTS.md and docs/DEVELOPMENT_NOTES.md. Get room IDs, footprints,
door masks and walkways from scripts/room_database.gd; inspect the renderer's
coordinate transforms before specifying pixel positions. Existing art can have
incorrect doors. Inspect actual PNGs, not filenames or thumbnails alone.

Read [references/production.md](references/production.md) before production or
integration. It contains cleanup commands, evidence requirements and a manifest
example. Read [references/lessons.md](references/lessons.md) when revising the
pipeline or choosing generation/animation methods.

## Generate against geometry

Use the approved hybrid: readable machinery silhouettes, quiet dark slate floors,
worn steel detail, restrained system colors and overhead cutaway projection.
Preserve the requested scope; do not substitute recolors or count duplicates as
new rooms. Name every requested identity in a pack ledger before batching.

Separate references by role: style master, canonical layout, subject. A reactor
image is not a valid door template for a corner room. Prefer shared hull/door
templates with editable interior regions. If templates do not exist, author and
verify them before claiming geometry is locked. A prompt alone is not a lock.

Use the available imagegen skill/tool for generation. Make each room an individual
asset; assemble contact sheets afterward for comparison. Preserve raw outputs and
exact prompts. An illustration with an imitation checkerboard is opaque until
pixel inspection proves otherwise. Production target is 1280 square; record the
actual native dimensions and any normalization, rather than claiming the tool
honored the requested size.

## Repair and inspect

Use the project's tools/room_art_pipeline.py for authorized local cleanup. It
removes only edge-connected light neutral background and fits without stretching;
it does not validate doors, remove every fringe, or guarantee pixel-grid fidelity.
Compare raw and cleaned images. Repair a failed region without changing accepted
regions where practical; save revisions to new paths. Never crop away wrong doors
and call the footprint correct.

Inspect at full resolution, actual gameplay zoom, and in a same-scale pack sheet.
Check each doorway, sealed side, route, machinery footprint, light hierarchy and
transparent exterior. Dimensional tests cannot prove these visual properties.

## Integrate the accepted result

Static interiors, stateful doors and machinery effects have separate roles.
Define effect anchors in room-local coordinates and transform them with the room.
Keep operation state separate from discovery knowledge: offline machinery stops;
unknown recipes remain hidden. Pause freezes continuing motion.

Update both station and card consumers, including alternate-art selection, without
rewriting unrelated gameplay. Preserve originals and player saves. Validate raster
staging through Git LFS and keep Godot script/UID pairs together.

Finish with native Godot evidence and relevant regression tests. Report what is
generated, rejected, integrated and verified, plus remaining work. A full-set
request is not finished when only a pilot is good. Do not install external apps,
purchase generation, publish, or push merely because this skill is active.
