# Project handoff

Updated: September 26, 2026 - Project: C:/Users/Alex/Documents/Brine Space
Task: Production wall, door and airlock artwork rollout

## Objective and acceptance
Apply the latest risers, caps, department doors and hatch motion to the existing
47 rooms and the 28 additions. Owner authorized continuation after learning these
were still preview-only. Integration is complete; visual owner acceptance remains.

## Accepted decisions and constraints
Use the reviewed painted industrial art and existing room geometry. New room
families inherit an explicit matching source; this does not claim 28 new wall masters.
Keep owner layouts/marks, optional wall materials and utility/observation corridor
finishes. Preserve pressure-cycle logic, crew movement and the 72-unit station-door
navigation aperture. The ocean hatch has the reviewed 56-unit right-hinged leaf.
No balance changes, save migrations, playable export, commit or push.

## Current state
- assets/architecture-rollout-2026-09-26/{walls,doors}.json register all 75 rooms.
- rooms/whole-room/painted_shell.gd installs faces, caps, mitres and doorway reserves.
  nursery_whole_view.gd draws caps before props/crew; north_wall.gd shares this shell
  and positions BRINE's subtle live traces inside the revised monitors.
- rooms/doors/painted_door.gd supplies nine cached department skins and rigid eased
  leaf travel. door_finish.gd and department_door.gd route production doors through it.
- corridor_wall_art.gd/corridor_dressing.gd fit the three actual hull shapes, preserve
  optional finishes, cull shared seams and dim their fittings with the room.
- rooms/doors/ocean_hatch.gd, airlock-v1/airlock_view.gd and grid_canvas.gd connect the
  right-hinged outward hatch to the existing flood/equalize/open/seal/drain cycle.
  Raised north uses a clear aperture; other directions use overhead hinge geometry.
- All 75 registered cards refreshed. Furnished gallery captures and live probe/aquarium
  states refreshed. The card bakers now preserve shell-before-prop ordering.
- New tools: review_architecture_rollout.gd, review_architecture_live.gd,
  review_architecture_doors.gd, build_architecture_gallery.py. New scripts have UID pairs.
- Test corridor catalog expectation updated from six to nine shape/finish registrations.

Review: http://127.0.0.1:8780/architecture-rollout-2026-09-26/
The furnished additions page links to it. Desktop collection has an 08 architecture
folder with the referenced source art, manifests, captures and this handoff.

## Verification
- 300 native room views (75 x four orientations); representative BRINE, aquarium,
  probe, airlock, corridor and T-junction renders visually inspected.
- Furnished additions: 112 views, 17,920 walking samples, zero failures.
- 28 live-game airlock phase/direction captures; nine door families at 19 sampled
  raised/low poses. Native probe/aquarium captures refreshed (36 + five states).
- Headless: airlock (1,333 travel samples), airlock clearance, door polish (100
  aperture states), and new-room expansion pass.
- Native: airlock actor visibility, exterior hatch, Studio, riser adjacency and
  corridor variants pass. The first corridor run stopped on its old six-record
  assertion; after updating the expectation it passed, including 72 rotated
  raised/low captures, finish distinctions, neighbor culling and dark response.
- Gallery browser checks: 300 room images, 28 airlock states, 19 door poses, working
  furnished-page link, zero page errors. These are sampled native captures, not
  a claim of continuous native video review or a released build.
- Both registries resolve all 112 referenced image paths; no absent/LFS-pointer
  sources. Owner room_layouts.json and all four library mark files byte-identical
  to the pre-install snapshot. Evidence/logs are in the architecture assets folder.

## Next action
Owner reviews the installed artwork in the gallery and game. Room-specific behavior,
new-room economics, outdoor aquatic spawning, drone/Margot preview integration and
playable release packaging remain separate work. Do not overwrite concurrent art work.
