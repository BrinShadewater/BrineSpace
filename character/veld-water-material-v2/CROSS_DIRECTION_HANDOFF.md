# Project handoff — Veld water cross-direction audit

Updated: September30,2026. Full Veld animation goal remains active.

## Objective and acceptance
Complete master-consistent animation coverage and cross-animation polish.
This pass corrects north material ownership and establishes a four-direction
comparison at one physical standingHeight148 scale. Owner acceptance separate.

## Accepted decisions and constraints
Selected dry masters anchor palette/native scale; original high-density art
anchors construction. No per-pose bounding-box normalization, runtime bindings,
commits or exports. Preserve raw sources and previous fitted files.

## Current state
North build.py blue/green patch ratio1.08→1.3 in source and master masks.
Pink ownership overlays confirm former mask captured cyan scanner screens;
1,984/2,577/2,656 raw pixels excluded across tread/swim/launch atlases.
Some excluded pixels are cyan patch highlights too: this threshold correction
is not a semantic segmentation guarantee. All48 paired frames rebuilt from raw.
Prior builder/frames/contacts/fit report retained in revisions/patch-ownership-v1.
New audit_material_ownership.py and patch-ownership-audit-v2.png/json preserve
source evidence. material-v2/build_direction_audit.py builds24 selected idle /
staged tread/swim slot0 panels at shared physical scale. Different dry/water
pivots remain visible; neither bounding boxes nor pose heights were equalized.
The east/west inherited faces/hair are visibly warmer/darker, body construction
still differs from selected masters. Next repair needs coherent source families.
Northern/southern apparent upright length also needs head/shoulder/hip rulers;
flexed knees alone are not grounds for changing source scale.

## Verification
48 fit,134 packaging/exact-join and48 exact-alpha/geometry checks PASS.
18,057 changed pixel references, including source-wide curve recalibration.
Combined native candidate v5 rerun:1104checks,0failures across32states/192refs;
scratch APPDATA; real profile changed[]. This validates latest north correction.
Reviewed source ownership overlays and full24-panel comparison, no panel clipping.
Slot0 comparison is not full-motion identity or world-clearance acceptance.

## Next action
Rebuild independent east/west tread/swim body sources against directional original
and selected masters, preserve handed equipment, warm skin/brown hair and matte
neutral suit. Verify physical head/shoulder/hip rulers before deriving start/stop
joins and fitting exact canonical helmets. Then full-motion/station-scale review,
water promotion/clearance and remaining full set. No genuine blocker.
