# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: loaded effect storage immutability

## Objective and acceptance

Retain lossless native effect storage without changing loaded image pixels, API
results, filtering, fallback or session lifetime. Private until revised matched
station/loading measurements pass. Full PC/Mac release readiness remains open.

## Accepted decisions and constraints

Keep loaded selected art immutable. Source hash validates each fresh derived load;
fallback uses that load's encoded original PNG, not a later filesystem version.
Only tagged validated derived images enter the special descriptor; an edited
original LA-format PNG remains ordinary art. No original art edits, extra shader/
Group/look-ahead, quality reduction or new permanent image lookup.

## Current state

Private revision in
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/native-effect-adapter-immutable/`.
Validated image metadata carries source path and original encoded PNG; descriptor
holds that immutable PackedByteArray. Public get_image decodes an independent
original image; lazy get_rid fallback uploads the same loaded pixels. Encoded bytes
observed separately from decoded/GPU accounting. Three originals total471,962bytes
(0.450MiB), held only while loaded descriptor survives. No added decoded RGBA copy
until an actual original fallback is needed.

Tools: `prepare-immutable-effect-adapter.py`,
`check-effect-loaded-source-immutability.py`, `run-immutable-effects-pilot.py` under
`output/renderdoc-tools-2026-10-08/`. Normal DroneAnimation/art unchanged. Current
normal Bill topology optimization is shared by both updated benchmark lanes.

## Verification

Tiny native scratch-source reproduction against prior adapter:3checks/2failures
prove public image and lazy original fallback reread changed pixels while mask
keeps its loaded pixels. Only scratch1x1PNG changed; owner art untouched.
Corrected expanded5checks pass: loaded pixels after source edit, caller mutation
isolation, lazy original identity, fresh source-hash mismatch original fallback,
and edited ordinary LA8 source not misclassified as derived mask.

Native original/fallback/accounting/explicit lifetime21checks pass, jobs0.
Native576whole-image draw pairs exact, actual mask/fallback execution and byte
accounting checked. Native current SessionArtCache two-tree-exit ownership34checks
pass: first owner preserves storage; final exit releases weak descriptor/mask/
original references and drains pending decode. Full title/game/Continue endurance
still narrower than these callbacks and remains pending. Logs clean; every terminal
run owner2,938 unchanged and runtime override restored. No screenshots/art batches.

## Next action

Updated native mixed pair complete in `immutable-effects-pilot/`:2160frames,
12full states/cameras exact, owner2938 unchanged, job terminal/override restored.
Peak2928.086→2744.336MiB (-183.750), end1939.219same. Mean29.712→29.765ms (+0.18%),
p9544.774→44.782/p9954.586→54.580 essentially flat; max87.002→71.105,>50ms18→17,
no>100ms either lane.118native draws/0fallback, three catalog sources. Observed
encoded payload peaks313315bytes during measured phases, zero at settled end.
Scene load1151.849→1127.043ms/ready9812.634→9870.205ms; single diagnostic timings,
not certified cold/warm release loading. New memory benefit verified for this
revision; no FPS claim. `comparison.json` retains scope/metrics.

Three alternating updated mixed pairs now complete in `immutable-effects-mixed-repeats/`,
current normal Bill shared both lanes.6,480frames/36full states/cameras exact,
source identities/owner2938 unchanged, job terminal/override restored. Every pair
peak2928.086→2744.336MiB, end1939.219same. Pooled mean29.768→29.354ms (-1.39%);
pair means improve3.275%/.281%/.553%. p9544.627→44.222,p9952.954→53.440 (slightly
worse), max97.518→85.896,>50ms59→54, no>100ms either lane. Observed encoded maximum
313315bytes. Ready reference9.614–9.814s/trial9.604–9.838s; no material loading
regression in these diagnostic starts, not certified cold/warm candidate loading.
No general FPS/stutter gate claim. Memory/upload remedy now ready for guarded
normal-source integration and regression/export dependency checks. Platform-specific
native acceptance remains Windows-only; preserve original storage on unverified
platforms until native pixel checks pass. Preserve full
performance/endurance/bugs/UI/packages/
GTX1650/M1/Mac certification gates; no release publication.
