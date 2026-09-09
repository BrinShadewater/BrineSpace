# Door art polish and flooded closing

Updated September 8, 2026 · BrineSpace

## Objective and accepted direction

Owner requested another art pass across all doors, with artwork for doors closing during flooding. Preserve shared aperture, crew safety, connections and water simulation. Keep maintained matte materials and department identity.

## Current state

Two original generated sources and exact prompts are preserved in `assets/door-polish-v1`. Registered rigid skins now serve low front/side doors, raised north doors, BRINE default sockets and both airlock pressure hatches. Inset latches, locking dogs, service plates, gaskets, drain details and status jambs replace the flatter surfaces. Five tint families cover bio, life-support/clinical, engineering, generic and BRINE. Mixed-room connections retain generic finish.

`door_finish.gd` owns shared skin registration. `department_door.gd`, `room_door.gd`, `north_wall.gd`, BRINE and airlock renderers consume it. `door_water.gd` supplies visual closing state, amber indicators, wet seals, aperture-limited wash/foam and compression ripples. `flood_visuals.gd` drives connected-door effects from actual water and door frame; airlock effects follow cycle state. Closed doors never depict water crossing. Dry pairs skip the added door lookup. New loops and Continue clear cosmetic history; rewind and pause are supported. No flood rules or timing were changed.

Forty-four furnished-room cards refreshed and both consumers updated. Three corridor card silhouettes retained. The review at `output/door-polish-v1/index.html` includes five finishes in three geometries, dry frame sliders, two animated flooded closures, BRINE and an actual station capture, plus local notes/export.

## Verification

- Native review: 150 dry frames and 40 wet closure frames exported; representative closed/partial/open front/side/raised views, BRINE card and actual flooded station visually inspected.
- Logic: closing detection, pause hold, opening cancellation, timeout/rewind and 100 monotonic aperture states pass.
- Production wet-door integration: real aperture drives closing; native pixels change and pause holds. Pass.
- Flood physics and retained flood-render checks pass. BRINE routes pass four rotations, sixteen entries/returns and 3,827 movement samples. Airlock passes three architects, four rotations, 1,039 travel samples, ten interlock phases, pause/power and disk saves.
- All 47 card identities agree across consumers and decode. New raster paths use LFS. Source hashes recorded. No owner layout file was written by the art tooling; concurrent owner edits are retained.

Some older fixture runs emit resource cleanup warnings at shutdown after their PASS; these are not claimed as clean exits. The visual-only flooded station setup uses two BRINE rooms to expose the connecting door. It is a fixture, not an authored layout change.

## Next action

Owner visual review of detail density and wet closure readability at normal game zoom. No publication, commit or personal layout replacement performed.
