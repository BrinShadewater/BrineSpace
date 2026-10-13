# Bill hair consistency

## Accepted direction
Owner accepts west motion with slightly darker brown hair matching each direction. Preserve suit and poses; deterministic palette processing authorized.

## Current state
`character/bill-hair-match-v1/` contains 266 idle/walk frames, manifest, before/after animation, checks and reproducible builder. Combines current matte Bill pack with new west v2. Targets 88% of east crown median, fixed RGB gains per direction shared across idle/walk. Conservative brown crown mask follows head top; face and beard untouched. Review candidate; not installed.

## Verification
Every alpha byte and every pixel outside crown mask identical to source. Before/after contact view inspected. Preview plays one 1500ms gait cycle across directions. Colour mask is conservative, not semantic segmentation of every hair strand. No Godot run or owner-save changes. No credits spent; last confirmed balance 48.

## Next action
Review darker hair pass, then install accepted corrected Bill pack with west motion. Side idle proportions and Branforth side work remain open.
