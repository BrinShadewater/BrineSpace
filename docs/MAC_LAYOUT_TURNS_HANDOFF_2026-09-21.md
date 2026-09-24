# Matching Mac candidate handoff

Updated: 2026-09-21 - BrineSpace

## Objective and acceptance
Prepare current room/animation work for Apple Silicon testing after Windows startup
validation. Native Mac behavior is a separate acceptance lane.

## Accepted decisions and constraints
Preserve owner layouts and older builds. No public upload, Higgsfield or changes
to game rules. Local ad-hoc signing only; no notarization claimed.

## Current state
Maintained tools/export_macos.py completed its full export path successfully.
Candidate: builds/BrineSpace-mac-layout-turns-2026-09-21/BrineSpace.zip.
Source fingerprint matches verified Windows: brinespace-e7c1ea935b573fd2.
README, NOTICE, build metadata, expected manifest, validation and SHA256SUMS accompany it.

## Verification
Official selected template/editor preflight passed. Bundle has arm64 and x86_64,
executable permissions 100755, one PCK, no QA override. Exact PCK: 15,146 checked,
zero missing/changed/remapped/unexpected. Export exits zero without errors.
Evidence: output/mac-layout-turns-validation-2026-09-21/ and candidate export.log.
These are Windows-hosted static checks, not Mac gameplay or signature acceptance.

## Next action
Owner can test on Apple Silicon using the included checklist. Meanwhile continue
Bill's ordinary gait/anatomy repair and room visual polish; the full goal remains
unfinished. New source changes will require their own build validation.
