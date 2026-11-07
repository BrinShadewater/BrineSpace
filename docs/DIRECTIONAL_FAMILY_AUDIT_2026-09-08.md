# Reusable directional-family metadata audit

## Objective and changes

`tools/audit_directional_family.py` replaces one-off family checks with explicit coverage, inward/backing metadata, unique export paths, source/export/review hashes, native evidence existence and long-axis scale checks. It supports current `directions` and older `orientations` maps, plus the two established native-evidence fields. Partial families remain explicitly incomplete.

## Verification

Eight focused tests pass, including false coverage, incorrect facing, stale export, scale mismatch, missing evidence and legacy-field cases. Water-assay and galley each pass with four directions. Reports: `output/water-assay-family-metadata-audit.json` and `output/galley-family-metadata-audit.json`. Galley's first run exposed the older nested evidence path; that compatibility case now has a test.

```powershell
python -m unittest discover -s tests -p test_directional_family.py
python tools/audit_directional_family.py assets/water-assay-wall-v1/family.json --output output/water-assay-family-metadata-audit.json
```

## Limits and next action

This validates metadata and linked files, not pixels, actual fixture direction, occupied clearance or runtime placement. It does not change art, owner acceptance or review verdicts. Run it after changing a family index and preserve native visual review. Continue additional art production.

## Report protection follow-up

Reports now use an identifying schema marker and atomic replacement. Output must be JSON under project `output/`; family-linked dependencies and unrecognized existing JSON files are protected. Validation failure, including a missing family file, replaces an earlier tool-owned pass with a failure report and the CLI exits1. The report records the family hash when available.

Thirteen focused tests pass. New protected-format real reports are `output/water-assay-family-protected-audit.json` and `output/galley-family-protected-audit.json`; both cover four directions. Earlier reports lack the ownership marker and are deliberately not overwritten: choose a new report filename on migration. No art or runtime changes.
