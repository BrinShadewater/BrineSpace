# Room review ledger audit

Updated September 22, 2026.

## Objective and constraints
Keep pipeline evidence attached to selected art rather than retired furnishing.
Do not reinterpret missing review metadata as missing art or new owner acceptance.
No art, layouts, library marks or playable exports changed in this pass.

## Findings and changes
Current engine inventory decodes all 47 selected cards with zero inventory errors.
Card-bound ledger reviews: 1 current (Biodome), 3 stale, 43 missing. The initial
undifferentiated count of 46 hash mismatches included missing records; it does not
mean 46 existing reviews describe older cards. Dated handoffs and CURRENT_STATUS
may contain newer evidence that the rollout ledger has not yet incorporated.

tools/audit_room_review_inventory.gd now reports current/stale/missing review
counts and each entry's recorded card path/hash separately from asset errors.
tools/build_room_composition_review.py labels unbound historical notes and shows
the counts without inferring visual approval. Fixed a real crash caused by
Observation's list-valued limitations; both prose and list notes now render.
Historical claims are preserved, not promoted to current acceptance.

## Verification
Native engine inventory exits 0. Current-data report builds all 47 HTML entries.
Checks confirm 1/3/43 counts, all cards valid, and Observation's list note rendered.
Evidence: output/room-ledger-audit-2026-09-22/inventory.log, inventory.json and
review.html. This validates inventory/report generation, not fresh native gameplay
or owner approval of 47 rooms. Existing test packages remain valid for their
recorded source revision; this pass changes authoring/reporting tools only.

## Next action
Reconcile review bindings as rooms receive genuine current visual review. Keep
missing bindings distinct from unreviewed art and preserve owner acceptance as
a separate requirement. Use current status and dated handoffs before acting on
any historical limitation shown in the generated board.
