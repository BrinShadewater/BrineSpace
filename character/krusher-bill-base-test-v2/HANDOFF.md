# Project handoff

Updated: 2026-10-02 · BrineSpace · Krusher Dom cardinal body-base trial

## Objective and acceptance
Continue the Krusher/Bill reuse test toward a consistent character animation pack.
Full goal remains active: equipment/action registration and actual station evidence
are incomplete. This milestone supplies all cardinal idle/walk and helmet fits.

## Accepted decisions and constraints
Krusher Dom / System Administrator / AI & Robotics / muted matte grey-cyan.
Existing Bill body and suitable motions reused, with independent Krusher head
views from accepted concept. No mirrored profile. Keep original libraries intact.

## Current state
`build_cardinals.py`: deterministic head extraction, pose fitting and suit recolour.
948frames:474bare and474helmet across8states per variant (cardinal idle/walk).
184canvas, (92,172) foot pivot,148standing ruler. Original durations/loops retained.
One source density for four heads; previously reviewed South component reused.
Head sizes South23×28, East26×29, North24×23, West23×29. Original helmet shell and
alpha silhouette preserved; only visor face pixels/department markings change.
`bare-manifest.json`, `helmet-manifest.json`, per-frame masks, source hashes,
`verification.json`, exact APNGs and `review/index.html` retained.
`review/cardinal-comparison.png` and four sampled neck-review boards show source
scale and equipment. `bill-base-cardinals.png` is the original base comparison.
Separate `character/krusher-equipment-study-v1/` holds12accessory views and static
hip-fit comparison. These are not applied to this locomotion pack yet.

## Verification
`validate_cardinals.py`:5273checks,0errors. All948APNGframes decodeexact; source
hashes unchanged, pixels outside edit masks exact, lower bodies/feet exact, shell
alpha unchanged, no clipping. Agent viewed eight idle cardinal masters at full
and reduced size, East/North/West sampled neck boards and all cardinal walk browser
samples, both equipment variants. South bare appearance retains prior reviewed
trial; helmet South and West idle playback sampled. Motion sampling is not formal
all-cycle/native station/owner acceptance. No Godot run or owner-save interaction.

## Next action
Register closed terminal/data cartridges across moving bodies with hand occlusion;
author representative held-open-terminal/typing poses and joins using these whole
body bases. Bill's six-pose east interaction was inspected as a reusable console
reach candidate, but no action has been added yet. Continue master/helmet facial
polish and actual station-scale/depth evidence before normal NPC integration.
Static concept heads currently lack expression/blink/turn motion. Goal incomplete.
