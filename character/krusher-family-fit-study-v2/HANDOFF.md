# Project handoff

Updated: 2026-10-02 | Project: BrineSpace | Task: cross-family collar fitting

## Objective and acceptance
Refine the initial alternate-body head study into source-preserving static neck joins. Continue the owner's proposed reusable Bill/Veld/James/Marsh family workflow without adopting candidates in the game.

## Accepted decisions and constraints
Krusher's native cardinal head images reused without rescaling. Bill remains the demonstrated cyan candidate; alternate suits keep original colours and tools. No new anatomy or normal-selection changes.

## Current state
build_study.py produces 16 static PNGs, comparison sheet, per-alternate collar/allowed masks and verification.json. Each alternate family/direction has a reviewed collar boundary and head-bottom anchor. Source collar pixels layer over the head. All source pixels below row 54 stay exact. v1 remains preserved.

## Verification
36 composition/protection checks pass. validate_study.py independently checks 48 input/output hashes and 24 protected-body/collar comparisons. Full corrected sheet visually reviewed. Earlier RGB masks damaged warm trim and retained scattered old hair shadows; rejected in favour of explicit source-reviewed boundaries. Rear heads moved higher to match actual collar position. No source RGB invented, no Godot run required for this static comparison.

## Next action
These are static fitting candidates. Representative moving neck joins, family-specific recolour masks and helmets remain necessary before claiming reusable animation templates. Optional priority question remains unanswered; current Bill-based Krusher remains unchanged. Continue with the chosen family's representative motion rather than copying static boundaries across all frames.
