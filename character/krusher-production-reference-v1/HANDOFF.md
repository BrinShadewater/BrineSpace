# Project handoff

Updated: 2026-10-02 · Project: BrineSpace · Task: Krusher production reference sheets

## Objective and acceptance
Make character and animation references for Krusher Dom and demonstrate existing crew body reuse while matching source density, size and timings.

## Accepted decisions and constraints
System Administrator / AI & Robotics / matte muted grey-cyan. Bill body demonstrated; Bill, Veld, James and Marsh are proposed future families according to likeness/build. Veld is the owner's suggested default for female characters. Preserve independent direction sources and original art. Candidate remains unselected.

## Current state
Four PNG sheets cover four-direction bare/helmet appearance, native heads and neck anchors, equipment density/placement and west terminal action keys. README.md records production rules and limits; reference-manifest.json locates source images, hashes, tile placements and head metadata. build_references.py assembles existing pixels deterministically; validate_references.py verifies source preservation and exact sheet tiles.

## Verification
130 checks passed, zero errors: 36 source hashes, 47 tiles within bounds and exact against source composition. All four sheets visually inspected for labels, spacing, source size and direction order. Existing sprite/frame packages unchanged; no generation or Godot run required for sheet composition. No game selectors changed.

## Next action
Continue artistic motion review using the compact preview and native evidence. Consolidate source packages for the required animation consumer after motion quality is accepted. Expressions/turning sources, other base family trials and station integration are not established by these reference sheets.
