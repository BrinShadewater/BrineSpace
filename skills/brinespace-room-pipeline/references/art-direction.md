# Room art direction

The checkout's docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md is the current aesthetic
source. Read it before using this reference. Shared geometry does not imply
identical finishes: mostly clean describes condition, not a universal lab palette.
The older pale-enamel guidance below applies only where appropriate to the
selected department. Preserve Engineering steel/orange, Life Support grey/cyan/
green, warm habitation, and BRINE's exclusive pearl-white aquatic treatment.

The target is a shared station with distinct functions: readable large shapes,
selectively detailed, mostly clean machinery, and a quiet, slightly haunted atmosphere.
These are working art-direction criteria, not a claim that generation is reliable.

Current owner direction: the station is underwater and partly derelict. Newly
built/restored habitable interiors should remain mostly clean; discovered rooms
and exterior hulls may show localized decay, silt and biofouling. The bible's
underwater condition rules supersede any older whole-station cleanliness default.
Use intact pale enamel, clean glass, crisp metal and readable functional details.
Preserve richness through construction, recessed vents, fasteners and shading,
not blanket scratches, chipped paint or grime. Subtle handling marks are optional.
Treat heavier damage as an explicit variant, not the default. Older worn reference
images supply equipment design and depth, not mandatory surface deterioration.

## Shared construction, individual identity

Keep projection, hull thickness, doorway dimensions, equipment scale, light
direction, shadow treatment and pixel/detail density consistent with the approved
pack references. Geometry comes from the database and verified templates.

Vary the focal machinery, interior arrangement, material contrast, task-specific
wear and restrained accent color. A different hue alone is not a new identity.
Use symmetry when the function benefits from it (paired treatment beds, storage
banks); vary supporting furnishings and other rooms so the station does not become
repeated mirrored quadrants. Asymmetry must still preserve the required routes.

At gameplay scale the reading order should be: room silhouette and paths, primary
equipment, supporting equipment, then surface detail. Put fine wear around contact
points, heat sources, wet surfaces and repairs. Quiet floor areas separate shapes;
filling them with bolts does not make a room more interesting.

## Brief before prompt

First record primary department, localized secondary functions and independent
condition. Include department cladding/floor roles and service-routing endpoints,
not just equipment colours. Audit existing accepted candidates against the new
bible instead of treating prior approval as universal departmental style approval.

Record these fields in the room's production record; reference an existing brief
when it already supplies them:

- **Function/story:** one sentence explaining what physically happens here.
- **Focal subject and composition:** the shape that identifies the room without
  a label, plus its arrangement around the canonical clear paths.
- **Materials and wear:** dominant construction, contrasting material, and a
  small amount of wear that reveals use rather than uniform noise.
- **Color and value hierarchy:** restrained accent; equipment reads against the
  floor even without relying on hue alone.
- **State anchor:** where functioning motion/light belongs; what remains legible
  while offline. Visual cues suggest activity, not undiscovered recipe partners.
- **Reference roles:** what to inherit and what not to inherit from each image.

Example concept, not an approved layout template: Mycelium Nursery cultivates
fungal substrate in a broad tiered growth rack, with a smaller servicing bench
beside it. Soft pale growth contrasts with ribbed steel trays; condensation and
patched irrigation fittings explain its use. A localized irrigation pulse can
show operation. Its west/east/south routes stay open. Avoid turning the growth
rack into a glowing reactor merely because the reactor supplied material cues.

## Reference hygiene

A style reference supplies camera, materials and rendering treatment. A layout
reference supplies hull, doors and reserved walkways. A subject reference supplies
equipment design. Record these roles explicitly even when one image serves more
than one role. Inspect every referenced local image before use.

Use a compact set of approved style examples with different functions to judge
the pack. Do not serially use each newest candidate as the next style master:
unreviewed changes accumulate. A full reactor image can leak its amber lights,
radial composition and door trim even when the prompt says “style only.” If that
recurs, change the reference set or prepare focused material/layout references
through the authorized image-editing workflow. Text exclusions are not a guarantee.
Do not describe a proposed reference board or template as an existing asset.

## Visual review and repair

Review both individual images and same-scale comparisons:

- Can the room be recognized from its primary equipment without a label or glow?
- Does its construction belong to the same station as the accepted references?
- Is its composition meaningfully different from neighboring identities?
- Do paths stay quiet and clear, with no false doors or oversized furnishings?
- Does detail support the function at gameplay and card sizes, rather than only
  looking impressive at full resolution?
- Can functioning effects attach to visible equipment without obscuring it or
  exposing an unknown synergy? Is the offline base still believable?

Record art findings separately from geometry and runtime findings. Strong identity
does not excuse broken doors; a correct doorway does not prove good art. Preserve
successful candidates and repair specific weak regions. Whole-room regeneration
is appropriate when the composition itself fails, not automatically for a seam.

After using a changed reference strategy, compare the resulting images against
the prior batch at the same scale. Until that comparison and native inspection
exist, report the strategy as guidance awaiting visual validation, not a proven
quality improvement.

### Personal belongings need supports and an intended orientation
An operator's headset can hang from a chair hook and a flask or logbook can rest on a bolted side tray. Orient the seat toward its task rather than treating every object as a front-facing display. A north-facing chair may show its back to the camera. Keep the chart station's working face usable in every rotation; diagnose wall clearance separately from chair collision. Furniture alone does not establish a sitting interaction.

### Reuse furniture with its task relationship intact
A supported operator chair can be shared between command and listening work, provided its orientation, scale and spacing serve the local controls. Retain source provenance and distinguish reused furniture from newly generated art. Pair it with the relevant console rather than scattering chairs as filler. For profile-ownership changes that should preserve appearance, compare decoded native card pixels as well as checking that files load.


### Furnishing completion requires a stopping rule — 2026-09-06

Crew Lounge activity-v3 has been visually reviewed in its card and the functioning catalog40-v2 station capture. Reading, dining, refreshment and games areas have distinct supported objects, secondary furniture and appropriate standing lights, rugs, plants and coats. The clear middle serves circulation. Accept this composition rather than continually adding clutter; record exact card hash and station evidence in the rollout ledger. Technical tests alone never establish this decision, and agent acceptance does not imply owner sign-off.


### Hash-bound visual findings — 2026-09-06

The review board now exposes visual findings and the decision for the selected card. If visual_review.card_sha256 differs, it shows a stale-review warning and suppresses the old decision. Positive/current, stale and escaped-text fixture checks pass. Biodome and Hydroponics station-scale reviews now identify concrete remaining work: Biodome needs a restrained wall care detail; Hydroponics needs a small supported harvest/supply area and wall detail. A readable irrigation system is not by itself complete furnishing.


### Botanical wall care charts — 2026-09-06

Biodome and Hydroponics care-v1 add code-drawn sealed clipboards with simple schedule marks, mounted to north hull segments only when the full 28-unit width fits. They are decorative notices, not interactive systems. Keep this small common fixture subordinate to department props. Both native four-rotation route tours pass; Biodome q3 station capture confirms the mounting and scale. Biodome furnishing now passes native visual review; new package check pending. Hydroponics still needs its supported harvest/supply area.


### Medical review follow-up — 2026-09-06

Medical Center services-v1/profile-v3 connects imaging to diagnostics with a perimeter service run and flush east crossing cover. Four native route rotations pass; furniture/collision unchanged. Medical Office grouping is coherent in card and unpowered station view, but powered visual acceptance remains explicitly unproven. Record lighting state with visual findings instead of treating every station capture as equivalent.
