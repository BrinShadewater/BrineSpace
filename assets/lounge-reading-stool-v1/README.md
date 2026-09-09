# Lounge reading stool candidate

September 8, 2026. A small backless rust-fabric stool with a matte walnut frame,
matching the reading-and-games wall. `stool.png` is a1254×1254 true-alpha canvas,
visible26×25.95 world units. Built-in imagegen source and exact prompt are saved.

Native Godot material/scale and light/dark alpha review pass. Evidence:
`output/lounge-reading-stool-v1/stool-scale.png` and `output/lounge-reading-stool.log`.
The between-leg gap is transparent; the seat remains opaque. Texture simplifies
at26 units intentionally; do not enlarge the furniture to expose source detail.

Standalone, not installed or owner accepted. Placement still needs seat approach,
cabinet and door clearance checks. No seated-crew interaction was implemented.

## Shared-scale arrangement

`group.json` pairs the26-unit stool with the320-unit reading wall. Native/2x
review in `output/lounge-reading-stool-v1/group-scale.png` passes for visual
proportion, palette and complete capture; export hashes match. Run Godot with
`--script res://tools/review_prop_group.gd -- --group=res://assets/lounge-reading-stool-v1/group.json --review=res://output/lounge-reading-stool-v1/group-scale.png`.

The stool is below the open-book zone with20.22 units of visible separation.
The cabinet has a solid front and no knee recess: this is not proof of a usable
seated reading workstation. Actual posture, reach, approach and doors remain
unverified. Do not infer interaction support from the attractive grouping.
