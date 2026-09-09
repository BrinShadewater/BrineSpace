# Project handoff

Updated: September 8, 2026 - BrineSpace - gallery context evidence

## Objective and acceptance
Improve the art workflow so standalone material passes do not obscure placement failures or limited proposals.

## Accepted decisions and constraints
Keep review scopes and owner acceptance separate. Preserve earlier rejected layouts as evidence.

## Current state
Changed tools/build_material_review_gallery.py and tests/test_material_review_gallery.py. Additional dictionary review gates appear as individual sections with verdicts, findings, optional scope and evidence/report links. Missing or outside-project links fail generation; changed hashed evidence receives a stale warning. Workflow and CURRENT_STATUS updated.

## Verification
Five unit tests pass, including rejected host plus limited proposal, HTML escaping, evidence links and stale warning. Gallery rebuilt72 records, zero stale export hashes. Browser layout/filter not visually rechecked; no new claim about browser rendering.

## Next action
Continue art assets and validate seed relocation crew/service access before runtime installation.
