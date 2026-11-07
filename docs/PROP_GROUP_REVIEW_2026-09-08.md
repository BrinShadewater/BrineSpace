# Prop group review guardrails

## Objective and changes

Prevent a successful diagnostic export from concealing cropped assets or replacing a source export. `tools/review_prop_group.gd` now validates entry structure, finite coordinates, positive dimensions, source-canvas bounds and both panel bounds. It rejects empty groups, stale export hashes and output paths that resolve to a group export.

The current board accommodates a group within490×150 world units. Larger arrangements need a larger board; shrinking the declared asset scale to bypass the guard invalidates scale review.

## Verification

`python tests/check_prop_group_review.py --godot C:/Users/Alex/Desktop/Projects/Godot_v4.6.1-stable_win64.exe`

Eight graphical Godot cases passed: valid group, out-of-canvas crop, off-panel position, negative position, nonnumeric width, stale hash, empty group and source-overwrite attempt. Rejections returned exit1 without producing a new capture. The protected export hash remained unchanged.

`output/prop-group-checks/valid.png` was visually inspected: both native and2x views retain the complete console and stool. Logs and isolated JSON fixtures are beside it.

## Remaining scope

This is static art review. It does not test occupied furniture, room doors, crew paths or collision. Continue asset production and use these checks for future group-board changes.
