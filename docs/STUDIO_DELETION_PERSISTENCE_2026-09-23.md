# Studio deletion persistence handoff

Updated: September 23, 2026 · Project: BrineSpace

## Objective and acceptance

Prevent deleted legacy furniture returning in Pressure Control at 90°, and apply
that protection throughout the Room Layout Studio.

## Accepted decisions and constraints

Preserve owner layouts, marks and source artwork. Keep deletion, undo and explicit
tray restoration available. No commit, push or release packaging.

## Current state

- `rooms/full-wall-v1/full_wall_prop.gd`: Studio always builds the same source
  furniture before applying its draft. Saved wall-bank deletions previously changed
  that source, exposing displaced legacy props on the next load.
- `scripts/room_layout_editor.gd`: both save paths preserve explicit null deletion
  records even when the corresponding asset is absent from the source defaults.
  Previously a missing default compared equal to null and dropped the deletion.
- Added `tests/test_layout_deletion_persistence.gd` and its UID; registered in the
  layout-studio subsystem. Actual owner JSON and artwork were not edited.

## Verification

- Reproduced the failure before the fix: deleting Pressure Control's visible q1
  props brought back `life_fan` and `life_filter`; the following save brought back
  the wall bank. Evidence: `output/layout-deletion-probe.log`.
- Regression passes 188 combinations (47 rooms × four rotations), checking source
  membership remains stable with saved deletions. Actual Pressure Control editor
  coverage includes deletion, disk reload, rotation roundtrip, repeated Save All,
  and deletion records for absent source assets.
  Log: `output/test-layout-deletion-persistence.log`.
- Native Pressure Control q1 review passes the same save/reload sequence. Inspected
  `output/layout-deletion-before.png` and `output/layout-deletion-after.png`:
  deleted furniture stays absent; fixed room shell remains. Native log has no errors.
- Existing editor suite passes natively: all 47 rooms, deletion, undo/redo, tray
  restoration, disk/runtime application, duplication, rotation Save All and reset.
  Log: `output/test-room-layout-editor-deletion-native.log`.
  An initial headless invocation could not capture its viewport at line 107;
  stopped it and used the required native rendering lane.

## Next action

Implementation and validation complete locally. Owner can reopen
Studio and continue editing; already-lost deletion records cannot be reconstructed
safely, so an asset whose earlier deletion was lost may need deleting once more.
Owner art/pacing acceptance from the procedural-site work remains separate.

