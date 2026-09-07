# Underwater hull attachment workflow

Full-pack style revisions: preserve a ledger of every original identity and map
each to a new export. Atlas edits can shift coordinates despite preservation
instructions, so re-register and visually review connectors rather than reusing
old anchors blindly. Scope subject instructions to the matching asset family:
ocean-window language accidentally turned a floor drip tray into a window during
the 85-asset refresh. Reject that region and generate a separate correct subject.
Use consistent material references across the entire collection, including pieces
previously retained after a partial review. See `output/art-style-refresh`.

Style review follow-up: judge wall decorations beside furnished room references,
not only previous isolated packs. Tiny highlights, saturated readouts and rust
speckling can make individually attractive sprites distract from room machinery.
Revise the outliers with explicit room material references and compare at equal
mounting heights. Keep sprite style acceptance separate from wall geometry:
48-unit demonstration strips do not supersede the owner's current low-wall rule.
See `assets/wall-dressing-style-v1` for 24-piece review and six focused revisions.

Everyday wall dressing: mix functional time/communication fixtures with a few
paper or framed personal objects, keeping common station mounting hardware.
Prefer large graphic motifs over tiny poster text. Check actual generated clock
digits before documenting them; static artwork is not a timekeeping system.
True-alpha sources may still carry faint exterior haze: review a thresholded
registration on dark hulls, record the threshold, and retain untouched sources.
See `assets/wall-dressing-v1` for the reviewed alpha-128 export and native samples.

The owner retained the current low wall height everywhere, including exposed
north edges. The riser studies below preserve asset-production lessons, not
permission to raise a room's hull. A room-specific renderer bypassing the global
setting is still a contract violation. Reconcile its wall, hatch and mounted
fittings as one assembly; disabling the backdrop alone can leave floating art.
Review standalone and shared-edge views in all rotations, then update cards and
package evidence. Preserve unused tall fittings as source assets, not exceptions.

For a low cutaway exterior hatch, inspect the fully open state: retracting leaves
can expose an uncut solid hull strip behind them. Split only the authoritative
aperture, retain a supported threshold across the wall depth, and verify that
the chamber reaches the exterior in every rotation. Recheck nearby machinery
when extending a previously shortened rotated chamber. Keep visual wall pieces
separate from crew-access and pressure-interlock rules; an open image does not
authorize exterior travel. Airlock's low-cutaway record contains native and
packaged checks, with old raised art preserved rather than overwritten.

Riser window follow-up: request explicit small, medium, panoramic and tall
silhouettes, then record the actual generated proportions. Fit attachments by
height inside the riser and preserve width through uniform scaling. Keep the
painted ocean opaque inside the glass while clearing only the exterior. Review
window, plating and screen combinations on native hull strips with a reserved
door bay. Static screen pixels and ocean paintings do not imply powered states
or animation. See `assets/riser-wall-kit-v1`.

Reusable floor dressing: store department and intended host/activity with each
sprite, not just a color label. Rugs belong to furniture groups, drip trays to
plants and access markings to service areas. For hollow decals, verify every
enclosed background component: tabs can divide a double-ring band into four
separate sectors. A center-only alpha test will miss opaque white wedges. Inspect
the native cutout on a dark deck as well as checking alpha ranges and hashes.

Floor utility follow-up: author top-down low-profile variants explicitly rather
than laying an upright wall sprite on the deck. Distinguish clipped thin wires,
armored cables, protective rubber mats, shallow pipe saddles and flush service
channels. Draw them beneath props and crew, with no inferred collision or utility
simulation. Check sample routes on an actual-scale deck. An opaque black atlas
must not be black-keyed when the subjects themselves are black rubber or dark
metal; preserve the failed source and request a clean background revision before
using the existing neutral-background cleanup. See `assets/floor-utilities-v1`.

Utility-kit follow-up: separate pressure pipes, ventilation ducts, flexible tubing,
armored power cables and thin signal wires by construction and restrained coding.
Request explicit straight/bend/junction/terminal pieces, but record actual exits
and source regions: generation can reverse a bend or ignore equal atlas cells.
Preserve family scales and connector anchors in the manifest. Review joined runs
at native scale before calling a pack reusable; visible paired flanges are not a
seamless autotile guarantee. Preserve real alpha, and use reviewed gap seeds only
for enclosed background in coils or valve wheels. See `assets/utility-kit-v1`.

Separate hull windows and wall equipment from floor furniture. Record reference
roles: department materials, pixel rendering, subject function and authoritative
door layout. Ocean windows look outside into submerged terrain, not an aquarium
or starfield. Use protected controls, manifolds, sealed glands, shielded lamps
and flush drains appropriate to an underwater station.

Register wall fittings in a profile with a riser envelope and reserved door bay.
Keep upright art in screen-facing hull space; rotation of a floor plan does not
turn windows into floor decals. A post controller needs a visible support. Drains
stay floor-only. Do not clamp wall art into furniture's floor envelope: that
previously dragged the airlock hatch down from the riser. Suppress shared-edge
risers beside occupied north cells, and distinguish a room-specific authored hull
from a retired global wall experiment.

The airlock atlas returned 1254-square RGB with a baked checkerboard rather than
requested 1536-square transparency; the wide window returned nearly square.
Preserve the source and actual dimensions. Inspect alpha, use reviewed regions
and the existing connected-background cleanup, and retain aspect ratio. Never
stretch a failed proportion into compliance. Check bright trim and enclosed gaps.
Detail at source scale does not prove readability at a 35–46-unit hull window.

Run `tools/audit_wall_fittings.py` on the wall profile for actual alpha, independent
wall bounds and hatch clearance. Exercise a negative control in the hatch bay.
Include wall profiles and all their textures in the composition dependency
manifest. Review native room/card views beside existing rooms at matching scale;
dimensional audits do not certify style, catalog completeness or packaged loading.
Airlock evidence and limitations: `rooms/underwater/airlock-v4/README.md`.


### Shared-wall fitting visibility — 2026-09-06

A fitting drawn only inside draw_wall can disappear when the station owns the shared wall between connected rooms. Botanical charts now draw as room detail at their fixed hull mount, outside the 72-unit door bay, while the station retains shell ownership. Closed card previews did not reveal this. Add a connected-neighbor station capture to fitting review. Moving the mount alone did not resolve the handoff and placed it behind foliage; retain rejected v2/v3 cards as diagnostic evidence. Selected cards are care-v4/harvest-v4.


### Reusable decoration integration — 2026-09-06

Use the style-v2 libraries at existing physical mounts before adding furniture.
`rooms/whole-room/decoration_props.gd` fits art without stretching into approved
floor pads and low north-wall segments. Floor services tile between authored
endpoints. Do not draw upright wall art as a rotated floor decal. Low wall strips
cannot accommodate full-size posters: retain the low hull contract and fit only
appropriate details. Shared exterior windows disappear with the omitted hull.

Audit the current database, not a stale rollout count. The integration inventory
covers 40 identities, 37 furnished views and three procedural corridors. Rare
q0 baked views suppress their old dressing helpers; record the exception rather
than reporting missing live hosts, and inspect their separate floor additions.
Clear a capture canvas before freeing room mesh caches; queued draw commands can
otherwise reference released meshes. Bake cards and corridor variants through
the changed renderer, and keep raw PNG/JSON dependencies covered by export.
See `rooms/decoration-integration/README.md` for this pass's evidence and limits.
