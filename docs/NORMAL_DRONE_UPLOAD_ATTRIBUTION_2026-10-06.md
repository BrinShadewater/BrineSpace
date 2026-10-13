# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: normal drone upload stalls

## Objective and acceptance

Continue the full PC/Mac performance plan. Attribute remaining 4× stalls in the installed normal renderer and find a remedy that improves both pacing and memory while preserving animation pixels and timing.

## Accepted decisions and constraints

No normal cache change admitted. A longer eviction grace is rejected as a release remedy. Private lossless encoded assets are proof candidates only; original source art, normal animation catalogs, owner layouts and gameplay remain unchanged.

## Current state

Artifacts: `output/drone-normal-cache-2026-10-06/`. Instrumented copies of current normal DroneAnimation report eviction path, frame, age and incoming path. Both controls use the installed Moonbay optimization and actual normal Main/Grid/crew/drone source; candidate changes only eviction protection from 2 to 32 process frames. Existing flood diagnostic adapter and deterministic fixture flags are shared by both branches. Scratch benchmark records cache diagnostics at phase boundaries. No normal renderer edits this milestone.

## Verification

Both native six-phase mixed40 runs finish cleanly. All recorded full crew/drone/door/light/power/zoom states match; no missing art or engine errors. Owner profile fingerprints: 2,936 files before/after, zero changes. Processes terminal. Source/editor diagnostic, not packaged or Mac acceptance.

Control evicts 33 entries, 25 touched within 32 frames; candidate evicts 19. Total uploads decrease 50→42. Observed trace upload payload decreases 1,930.2→1,700.5 MiB, upload time 186.4→168.4 ms. Latest-event trace includes some pre-measurement uploads; these are observed totals, not an entire-session audit. South mining body/effects are uploaded again about 90 process frames later in both branches. Four mining sheets are each 144,506,880 decoded bytes, exceeding the 256 MiB cache budget in pairs. Control may already exceed its soft budget when recently touched entries prevent eviction.

4× idle p95 53.345→50.561 ms; pan 50.849→51.760 ms. Both have nine sampled frames over 50 ms. Final engine texture memory 4,389.85→4,758.37 MiB (+368.52 MiB); cache 689.61→966.00 MiB. Rejected: mixed pacing and greater memory, no gate closure. Upload-associated frames average approximately 46–50 ms versus 36–37 ms without an immediately preceding upload; CPU boundary attribution is diagnostic, not a GPU causation proof.

Six directly implicated sheets inventoried and source-hashed: South/West mining body and effects, South collection body and cargo. Mining bodies have 11,351/13,987 exact RGBA colours; both effects have 152; collection body/cargo 10,634/1,266. Private RG8 indices plus RGBA palette for bodies/cargo, R8 for effects, preserve all written-file pixels including transparent RGB. Complete reconstruction passes for all six files. Aggregate decoded payload 770,703,360→313,250,816 bytes (about 59.4% lower). This is encoded storage arithmetic and CPU byte verification, not measured GPU memory/upload improvement or native visual acceptance.

## Next action

Native exact frame/filter/material/composition checks for these six large sheets, then private integration with existing indexed drone/dock ownership and matched upload/memory/frame comparison. Existing provider lifecycle/fallback/full-room admission work remains. Continue larger sustained CPU/rendering work; normal frame/memory/loading gates, endurance, refreshed release audit, nine packaged bug reports and actual Windows/Mac certification remain open.
