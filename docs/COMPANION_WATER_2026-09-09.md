# Companion swimming and flooding

Updated: September 9, 2026 · BrineSpace · Margot swimming, River flotation, Josh shutdown

## Objective and acceptance

The owner requested Margot swimming, River floating, and Josh stopping work in waist-high water. Deliver authored water motion plus flood-driven runtime behavior, with native room, route and checkpoint evidence.

## Accepted decisions and implementation choices

- Margot starts swimming at 20% compartment flooding; River floats at 25%. Both have four-direction travel and stationary paddling/bobbing, stay at the surface, and resume dry behavior after drainage.
- Josh's waist-high cutoff is 50% flooding, matching the existing repair water cutoff. At or above it he stops movement and actions, extinguishes his repair torch, and holds his authored powered-down pose. He resumes below the cutoff. Flooded destinations are disabled in his route graph; movement also checks the swept route against water depth.
- Afloat companions suspend dry personality actions. Petting is unavailable while Margot swims. Existing companion oxygen/mortality rules are unchanged.
- Water mode and animation time are checkpointed separately from dry actions; pause freezes both motion and pose. Old saves default to dry mode and are reconciled against room flooding on the next simulation update.

## Current state

`character/companion-water-v1/` contains two authored source sheets with exact prompts and hashes, 16 new clips / 48 frame references, clearance profiles and [animated review](../character/companion-water-v1/review.html). Existing dry packs are untouched. `tools/build_companion_water.py` deterministically extracts magenta, registers Margot by bonnet center, downsamples and packages binary-alpha 92px frames with 64-color palettes.

`scripts/companion_water.gd` owns the water response and clock. `companion_npc.gd`, `companions.gd` and `flood_visuals.gd` connect selection, routing, checkpointing, pet availability, water tint and wakes. River stays upright: navigation uses the full width of his lower floating chassis rather than treating his elevated head as a prone swimmer's floor footprint. Margot uses her full swimming envelope. Paired UIDs supplied for the new helper and test.

## Verification

- Builder: all exported frame bounds, binary alpha, palette sizes and timing counts pass; PNGs remain LFS-covered.
- `output/companion-water/native-final.log`: PASS. Real rescues, flooded-room routes for Margot/River, production texture selection, paused/mid-water saves, Josh cutoff/recovery and flood-aware graph blocking/reopening.
- `output/companion-water/dry-regression.log`: PASS, prior directional actions and pause/checkpoint behavior.
- `output/companion-water/repair-regression.log`: PASS, existing paid hull repair and Josh assist gating.
- Sources inspected for identity, directions and distinct paddling. Native Margot/River swimming and Josh shutdown captures reviewed in flooded rooms. Sampled four animation phases in all four facings; GIFs remain available for owner motion review. Continuous browser playback was not reviewed through automation.
- Initial River route test exposed an overconservative human-style swimming envelope; the chassis footprint correction passes the same rescue-room route check. Initial camera captures were misfocused and were replaced by correctly focused captures.

## Next action

Requested source-game integration is complete. Owner can review the animation gallery and flooded-room captures. No executable rebuilt, and no unrelated room work changed.
