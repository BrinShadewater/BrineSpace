# Asset record initializer handoff

Updated September 8, 2026. Reusable provenance step for ongoing art production.

## Objective and constraints

Replace repeated one-off metadata setup with a command that records verified file facts and preserves the distinction between technical checks and visual review. Existing reviewed assets must never be overwritten.

## Current state

`tools/init_material_scale_review.py` reads the maintained review template and accepts registration, export, exact prompt, asset id and one intended width or height. It records source/export/prompt/registration hashes, actual dimensions and optional role-labelled reference hashes. Opposite visual dimension derives from the registered equipment region. Department and review findings remain for the artist; owner and visual verdicts remain unset.

## Verification

Five focused tests cover scale derivation without acceptance, stale source hashes, opaque exports, invalid regions and invalid scales. All pass. A real east-galley record matches its existing export hash and intended scale. A second CLI invocation refuses overwrite with exit2 and leaves bytes unchanged. Evidence: `output/galley-east-metadata-initializer-check.json`. No new art or runtime changes in this pipeline step; existing visual evidence remains applicable to existing exports.

## Next action

Use the initializer for the next asset after export, then fill actual material, scale, alpha and placement review findings. Continue wall/prop production. Do not use this metadata command to promote unreviewed artwork.
