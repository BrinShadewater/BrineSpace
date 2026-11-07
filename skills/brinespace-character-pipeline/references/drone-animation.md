# Drone animation production and closeout

## Runtime installation and release lessons — September 26

The motion pilot, directional packs and v10 docks are now installed; older candidate-state and next-session text below describes the earlier study. Read docs/DRONE_RUNTIME_INSTALL_HANDOFF_2026-09-26.md and docs/ROOM_ART_SESSION_CLOSEOUT_2026-09-26.md in the checkout.

Inspect both catalog props and built-in room renderers: changing one need not update the other. Match dock and exterior world scale to prevent launch size pops. Keep contact foam separate from vehicle fade, retain textures while draw commands reference them, and use pause-aware visual clocks. Bind art to existing simulation timings; an art study's duration does not authorize throughput changes. Registered clip count is not exercised gameplay-state coverage.

For packages, freeze source bytes under concurrent editing, retain explicit full asset paths, audit the exact PCK and exercise the actual release executable. Windows rendering evidence and identical Mac content do not prove native Mac gameplay. Record selected source, installed renderer, owner acceptance and platform-specific validation separately.

Current project authority: docs/CURRENT_STATUS.md, the visual bible, and
DRONE_ART_SESSION_CLOSEOUT_2026-09-26.md. Use the selected approved-v10 bundle
named there. Archived iterations and old pending-review labels are not task lists.

## Established decisions
Owner accepted the three new drone identities and v10 launch/recovery art study.
Construction/Salvage swim; Mining drives on seabed. Gray/steel with muted cyan;
yellow paint removed, functional amber warning/yellow status emission allowed.
Drone LEDs: blue operational, red stopped, yellow charging/out of power. Preserve
accepted offsets. Pad beacon positions follow the current bible, not generic
center-side placement. Rotate the amber light highlight rather than moving the
housing. Construction terminal telemetry stays within the existing bezel.

## Animation lessons
Keep water, contact foam, doors, cables, lift and vehicle separable. Entire vehicle
submerges together; surface foam must not inherit vehicle fade. Exposed water moves
continuously and quietly, including empty intervals. Avoid visibly stepped strip
warps. Cables share fixed winch coordinates; remain attached at rest and retract
instead of appearing/disappearing. Preserve braid pitch when extending cable.
Doors must cover the aperture at surface level. Departed drones remain hidden
beneath the base. Review contact, descent, away, retrieval and closed-hatch states.

## Density and production gates
Compare at native library pixel scale against locked source hashes, on light and
dark backgrounds. High-resolution motion previews do not prove game-size density.
Maintain per-pad component scale; never resize each part to an identical thumbnail.
Tiny native cable braid may simplify; do not compensate by enlarging the vehicle.
Source quality and material style require visual inspection, not only histograms.
Keep grayscale/matte surfaces separate from intentional glass/light emission.

Define directions, per-action states, frame size, pivots and tool contacts before
an NPC batch. Start with native room-scale verification and a minimal motion pilot.
Construction: propulsion/idle/build/repair; Mining: wheels/steering/mining;
Salvage: propulsion/idle/claw retrieval. These are next-session candidate states,
not completed coverage. The accepted study uses compositing, not articulated NPC
animation. Room skill owns docks and effects; character skill owns moving NPC
motion and identity. No automatic mirror of asymmetric tools or thrusters.

## Closeout
Separate selected sources, calibrated exports, previews, provenance, review and
rebuild tools in a versioned approved bundle. Preserve previous paths or rewrite
all consumers before moving. Inventory/hash all selected files and verify rebuild
inputs resolve. Reconcile owner acceptance explicitly by revision and scope.
Do not equate approval of a preview with runtime installation, world footprint,
pathfinding clearance or release evidence. Keep unknowns unverified. Update the
bible/workflow and maintained project skill references; sync only the same edited
reference/routing lines into installed skills. Never overwrite unrelated skill work.
