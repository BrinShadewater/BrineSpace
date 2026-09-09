# Project handoff

Updated: September 8, 2026 · BrineSpace · Mechanical tool directional records

## Objective and constraints
Continue wall assets with modest matte proportions and reliable placement records.
Metadata validation remains separate from visual, runtime and owner acceptance.

## Current state
Converted `assets/mechanical-tool-wall-v1/family.json` to the existing reusable
direction-map schema, adding review links and explicit backing edges. Preserved
the south tool-construction differences and missing west/east views. Added hashes
of rejected south sources/prompts and final native evidence to its review record.

## Verification
Both source dimensions and source/export hashes match their records. Visible
depths derive from source registration: north81.675, south82.770 at320-unit width.
`tools/audit_directional_family.py` passes both indexed directions and correctly
reports incomplete coverage. Report: `output/mechanical-tool-family-metadata-audit.json`.
No raster changed, so prior native visual evidence remains the relevant review.

## Next action
Create west/east reconstructions and review every working face. Retain the low
backing; measure room doors and operator space before installation. Reuse the
existing audit and production guide rather than adding a competing family format.
