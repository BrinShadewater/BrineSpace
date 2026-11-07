# Project handoff

Updated: October 6, 2026 · BrineSpace · Private loader failure and title lifecycle coverage

## Objective and acceptance
Preserve selected animation pixels, loading diagnostics and save/Continue behavior
while reducing repeated PNG loading. This is candidate validation, not release certification.

## Accepted decisions and constraints
Compressed crew storage remains private. Normal gameplay, art, save rules and owner
layouts unchanged. Every probe verifies resolved scratch user data before writes.
Keep original failed evidence; no package or upload produced.

## Current state
Private `single-buffer/batch.gd` and `prepare-single-buffer.py` now open encoded
files without spurious missing-file engine errors, avoid hashing empty buffers,
validate PNG headers before decoding, and return SafeImage's drawable placeholder
and error status instead of asserting. Valid-image storage and sharing are unchanged.

Evidence under `output/compressed-crew-2026-10-06/bounds-cache/single-buffer/`:
`error-paths/` retains before, intermediate and independent final runs;
`title-lifecycle/` retains reference/candidate native runs. Generator:
`output/compressed-crew-2026-10-06/prepare-single-buffer-lifetime.py`.

## Verification
Before: two failures, seven engine errors, two assertions. Final independent check:
15 checks, zero failures/errors/assertions. Missing and damaged files independently
register the same SafeImage failures and return identical placeholders; valid PNG
pixels match. Mutating returned images leaves subsequent loads independent.
This does not cover every corrupt PNG structure or release executable behavior.

Native title → New Game → transmission Continue → play/Studio → save/title →
Continue → save/title: 154 checks each reference/candidate, zero failures/engine
errors/exit leak warnings. Actual recovery supplies James/Marsh; restoration checks
needs, decision RNG, foot, active state, goal and stage. Sampled old players,
CPU sources, router/bank/presenter release; title texture memory matches at both
settled states (182.795 then 186.266 MiB). All 2,936 owner files unchanged.

Observed interface/grid startup stage: reference 13.894 s fresh / 4.705 s Continue;
candidate 12.411 / 4.625 s. These are single runs with separately generated sites,
not matched deterministic performance certification. Dialogue is advanced by the
fixture; progress responsiveness and end-to-end cold loading remain unmeasured.
Do not infer ten-transition warning closure from these clean two-cycle runs.
Python generators/runners compile successfully.

## Next action
Measure loading-screen progress and bounded worker alias decoding; separately
profile rendering/upload stalls, which the loader gain does not fix. Retain the
anonymous ten-cycle warning, longer endurance, 12-room memory, original bug closure
and packaged Windows/Mac gates as open. No normal backend admission yet.
