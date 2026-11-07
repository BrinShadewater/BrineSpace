# Material review gallery handoff

Updated September 8, 2026. Review workflow for ongoing art production.

## Objective and constraints

Make standardized asset candidates easier to compare while keeping native scale, technical checks and owner acceptance distinct. This covers `assets/*/material-scale-review.json` and compatible per-asset `*-review.json` records, not legacy manifests or the complete room inventory.

## Current state

Run `python tools/build_material_review_gallery.py` to rebuild `output/material-review-gallery.html` and its audit JSON. The local page has fitted thumbnails, department search, facing/scale details and links to native boards, PNGs and records. Stale export hashes are labelled separately from review findings. No asset acceptance or runtime state is changed.

The latest rebuild contains22 standardized records, including both Storage dispatch
assets. Discovery checks the expected record fields and rejects duplicate export
paths instead of double-counting. Review panels include written findings as well
as verdicts; missing verdicts stay unreviewed. Legacy records remain excluded.

## Verification

The latest build has22 matching export hashes and110 resolving local image/record/
evidence links. Three focused tests pass for multi-asset record discovery, legacy
exclusion, duplicate-export refusal and preserving unreviewed findings. Invocation:
`python -m unittest discover -s tests -p test_material_review_gallery.py`.
The earlier browser local-file URL policy blocked graphical preview; rendered
layout and interactive filtering remain unverified. Existing native boards remain
the visual evidence for the assets themselves.

## Next action

Open the HTML locally for review, and rebuild it as standardized records are added. Continue new wall/prop production. Include legacy/multi-asset records only through an explicit compatible adapter; do not present this subset as total coverage.
