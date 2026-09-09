# Water-assay directional candidate handoff

## Objective and constraints

Complete standalone wall art for each direction while retaining task inventory, matte science materials and inward access. This milestone concerns art coverage; actual mounting and occupied access remain separate.

## Current state

`assets/water-assay-wall-v1/family.json` indexes north, south, west and east. Each has its own source, exact built-in prompt, registration, transparent export and agent review. East was added this turn. No room or gameplay code changed.

| Wall | Inward | Visual world size |
|---|---|---|
| North | South |328×77.51|
| South | North |328×72.67|
| West | East |82.30×328|
| East | West |77.61×328|

Keep source aspect ratios. These visible sizes are not collision footprints; recreated views differ in preparation area and instrument visibility.

## Verification

Each directional native review was visually inspected during production. East full-length light/dark columns and individual fixtures pass agent review. All four source/export hashes and evidence links match in `output/water-assay-family-audit.json`. Family coverage is complete at the standalone candidate stage only.

## Next action

Owner review and placement against actual walls, checking door exclusions, working clearance and mounting depth. Continue additional art and workflow improvements; this family milestone does not finish the ongoing production objective.
