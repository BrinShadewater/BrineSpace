> Full-wall exception: current owner-directed wall installations use authored inward-facing views. See wall-room-rollout.md and full-wall-installations.md; the general south-facing default below applies to other upright props.

# Layered, rotatable room assets

Current owner contract: large props always face south. Rotate sockets and prop
centers, not the artwork or its footprint orientation; retain height screen-up,
recompute depth, and translate host effects. Reroute inter-machine services.
The directional-view discussion below is historical/exception guidance, not a
requirement to generate side/rear art for the current room rollout.

Unused sockets need flush wall infill matching the host department over shared
structure. Do not show an opening until both sides form a valid connection.
Connected closed doors remain doors; offline/suspended rooms do not gain infill.
Cards and finished previews show sealed potential sockets with markings/UI port
indicators; exposed-port technical fixtures must be labeled. Follow the bible's
section 23 for retained consumer rules and current implementation gaps. Validate seam
pixels as well as collision, including disconnect and incompatible-neighbor cases.

Read this for modular hulls, prop assemblies, directional art and animation.
Use the checkout's docs/MODULAR_ROOM_PILOT.md for current experiment status.

## Separate geometry from appearance

Own cell spacing, wall thickness, door centers, clear aperture and collision in
code or an authored dimensional source. Adjacent rooms share one edge assembly;
two independently painted doors must not decide the seam. Render directional
wall faces for the fixed camera rather than rotating a completed room bitmap.

Classify each component before generation:

- Surface: floor or enamel swatch mapped onto authoritative polygons.
- Upright reusable sprite: growth or approximately radial vessel. Record any
  asymmetric wear or silhouette that makes reuse an approximation.
- Directional prop: microscope, console or asymmetric chassis. Requires coherent
  views or a dimensional source; a mirrored front is not a rear view.

Rotate ground positions and local effect anchors. Vertical height remains
screen-up. Preserve ground contact, collision footprint and depth sorting
independently from each image's transparent canvas.

## Registration is not geometry repair

Inspect native dimensions and alpha. A requested transparent background can be
an opaque imitation checkerboard. Preserve originals; use authorized cleanup
only after checking which pixels are background.
Faint exterior alpha specks displaced anchors in the component trial. An
alpha>=128 display region with two pixels of margin helped that trial without
altering source alpha. Inspect faint intended detail before adopting that
threshold elsewhere; do not independently normalize directions by tight bounds
and assume physical scale is preserved.

Record native canvas, display region, ground pivot, world dimensions, direction,
source hash, exact prompt, reference roles, processing and acceptance separately.
An enabled texture or a successful file load is not visual acceptance.

## Directional review

Compare stable landmarks: front ocular opening, rear support, service panel,
knob side, base axis and occlusion. Keep camera and lighting fixed. Text-only yaw
requests in the microscope trial retained front features in requested rear views.
Rack geometry guides improved one footprint but did not preserve upright growth.
These trials support using a deterministic chassis plus independent details;
they do not establish that image references lock geometry.

After a failed directional batch, identify the missing geometric constraint.
Prefer an authored proxy with matching views or explicit reconstruction over
repeating equivalent prompts. Preserve rejected candidates outside active
registration. Missing views may use a visible prototype fallback, but the room
must remain marked incomplete.

One later microscope trial succeeded more clearly when each paintover used an
actual shared-model view as its first image and a separate material-style image.
The rear support occluded the stage correctly; all four views reached the native
pilot. The generated outlines still drifted, and alpha still required cleanup.
Treat this as improved directional guidance, not pixel-locked reconstruction.
Keep the full guide-relative canvas and ground pivot through registration; use
native contact/scale review to decide whether residual drift is acceptable.

## Native evidence

Check all four rotations at the same scale in the actual renderer. Include
adjacent-room seams, character behind and in front of every tall prop, traversable
routes, active/offline/pause behavior and target viewport sizes. Per-room pixel
changes prove only that something animated, not that every machine functions.

Keep geometry tests, directional coverage and visual acceptance separate.
The pilot's --require-directional-art check currently guards microscope coverage;
it is not an exhaustive room-completion certificate. Main-game integration is a
separate acceptance stage from an isolated pilot.
Walls and door jambs can occlude crew too: include their ground-depth bounds in
layer ordering rather than painting every wall after the character. Keep floor
labels below characters. Check continuous input-driven circuits around prop
corners as well as static front/behind poses; collision samples alone do not
exercise the movement controller. Preserve native capture pixels in review sheets.

Use separate crew and machinery clocks: loss of room power stops operating
effects, not walking, while pause freezes both. Inventory existing directional
animation files before promising coverage; a static diagonal idle is not a
missing breathing animation to invent or silently claim as animated.

 
For mixed legacy/modular stations, draw legacy rooms, then all modular floors,
then modular props and shared structures. Interleaving complete rooms let a
neighbor floor erase half a shared wall. Suppress legacy door overlays on edges
owned by the modular renderer. If legacy crop margins leave a void, bridge only
the connected canonical aperture; do not widen the door or paint over sealed sides.

Native screenshot crops must include viewport stretch as well as the CanvasItem
transform. Save and inspect the cropped region before trusting motion comparisons:
the station trial produced false animation failures when crops missed their room
at different window sizes. Preserve failed evidence and identify the corrected run.


## Optional raised-wall layer: verified practice
Keep screen-facing rear walls separate from floor registration and door geometry.
Suppress extensions at occupied north cells so decoration cannot obscure a neighbor.
Use stable room/cell variation for occasional windows; do not randomize on redraw.
Reserve a separate wall bay for windows to avoid collisions with department fittings.
Show depth through mounting shadows, bevels and functional details at gameplay scale.
For a visual preference, test the real settings control, saved value, reload, and
both rendered states using an isolated settings path. Restore defaults explicitly.
Capture a connected pair as well as single-room rotations. State which consumers
are covered: station layers do not automatically update baked cards or study scenes.
Keep before/after evidence and add concrete lessons after each accepted iteration.
