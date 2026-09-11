---
name: brinespace-room-pipeline
description: Use when generating, repairing, reviewing, or integrating BrineSpace room graphics, underwater terrain and scenery, wreckage, room-card art, doorway layouts, or functioning-room visual effects.
---

# BrineSpace room pipeline
For directional service counters, short finished-end sections and additive host
studies, read [fitted service lessons](references/fitted-service-lessons.md).


For matching station navigation artwork and UI integration, read
[navigation UI lessons](references/navigation-ui.md). Its material rules are
UI-specific; do not apply them universally to room props.

For corridor floors, department risers, default doors and opposite-facing corners,
read [the corridor/riser contract](references/corridor-riser-contract.md).

For layout-editor tray previews, drag optimization and water-rendering follow-up,
read [editor and water lessons](references/layout-editor-and-water.md).

For every new or revised prop, apply the owner-directed
[material and scale review](references/material-and-scale-review.md): matte
surfaces, restrained highlights and native-scale comparison are explicit gates.
Record verified corrections in the maintained workflow as each art task progresses.

For the fourteen-room continuous/split wall rollout, read
[wall-room rollout](references/wall-room-rollout.md).

For full-wall props, side-facing variants, enclosed cutout repairs and relocation,
read [full-wall installation lessons](references/full-wall-installations.md).

For session consolidation, paused production or a cross-room handoff, read
[handoff guidance](references/handoff.md). Use current selections and dated
evidence before carrying forward historical TODOs or package claims.

For underwater hull windows, wall-mounted props and related deck details, read
[the hull fitting workflow](references/underwater-hull-fittings.md). It separates
wall registration, floor collision, transparency cleanup and native style review.

Produce usable room assets, not just attractive images. Keep geometry authoritative
and distinguish **generated → cleaned → geometry-validated → integrated → verified**.
Track rejected candidates separately; counts at one stage never imply another.

For crew character design, sprite animation, or character-specific NPC integration,
use `skills/brinespace-character-pipeline/SKILL.md` in the active checkout. Use both
workflows when a task changes a character and its room/prop interaction. Existing
characters used to verify room clearance do not require a character redesign.

For underwater terrain, scenery, wreckage or blocker art, read
[references/environment.md](references/environment.md). It routes environment
geometry, source provenance and native review; room-specific door and card gates
below apply only when those consumers are in scope.

## Establish the contract

Locate the BrineSpace checkout from the active workspace; never assume a drive
path. When using an installed snapshot for production, compare it with
`skills/brinespace-room-pipeline` in that checkout using
`python <installed-skill>/scripts/check_source_sync.py --source <checkout-skill> --installed <installed-skill>`.
Use the maintained project references when a difference is reported; do not overwrite
project work from an older installed snapshot. Read its AGENTS.md and docs/DEVELOPMENT_NOTES.md. Get room IDs, footprints,
door masks and walkways from scripts/room_database.gd; inspect the renderer's
coordinate transforms before specifying pixel positions. Existing art can have
incorrect doors. Inspect actual PNGs, not filenames or thumbnails alone.

Read the checkout's docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md before room art
production or review. It owns department identity, condition, shared architecture
and the current south-facing/infill contract. Technical passes on older art do
not establish compliance with this bible.

Read [references/production.md](references/production.md) before production or
integration. It contains cleanup commands, evidence requirements and a manifest
example. Read [references/lessons.md](references/lessons.md) when revising the
pipeline or choosing generation/animation methods.
Read [references/art-direction.md](references/art-direction.md) before writing
room briefs, selecting art references, or reviewing visual consistency.
Read [references/layered-assets.md](references/layered-assets.md) for modular
hulls, separately registered props, directional views and layered animation.

## Generate against geometry

Use readable machinery silhouettes, quiet department-appropriate floors, maintained
department-specific materials and restrained lighting in the shared cutaway camera.
Do not apply ivory enamel and dark slate universally. Record primary department,
secondary functions and independent condition before selecting style references.
Preserve the requested scope; do not substitute recolors or count duplicates as
new rooms. Name every requested identity in a pack ledger before batching.
Keep construction consistent, not compositions identical. Give each room a
recognizable visual story and record its focal subject, material contrast,
surface condition and functioning-effect anchor before generating.

Separate references by role: style master, canonical layout, subject. A reactor
image is not a valid door template for a corner room. Prefer shared hull/door
templates with editable interior regions. If templates do not exist, author and
verify them before claiming geometry is locked. A prompt alone is not a lock.

Use the available imagegen skill/tool for generation. Make each room an individual
asset; assemble contact sheets afterward for comparison. Preserve raw outputs and
exact prompts. An illustration with an imitation checkerboard is opaque until
pixel inspection proves otherwise. The whole-room production target is 1280
square, not a universal prop or material size; record the
actual native dimensions and any normalization, rather than claiming the tool
honored the requested size.

## Repair and inspect

For a focused repair to integrated room art, read
[references/repair-loop.md](references/repair-loop.md). It keeps diagnostic,
gameplay-scale and revision-specific acceptance separate and explains how to
feed verified improvements back into this skill and the project's bible.

For a multi-room source batch, save each result immediately and audit its manifest
with `tools/audit_room_source_batch.py`. Record revisions without replacing source
hashes. Its contact sheet and alpha report are provenance/review aids, never a
geometry or runtime acceptance certificate.

Use the project's tools/room_art_pipeline.py for authorized local cleanup. It
removes only edge-connected light neutral background and fits without stretching;
it does not validate doors, remove every fringe, or guarantee pixel-grid fidelity.
Compare raw and cleaned images. Repair a failed region without changing accepted
regions where practical; save revisions to new paths. Never crop away wrong doors
and call the footprint correct.

Inspect at full resolution, actual gameplay zoom, and in a same-scale pack sheet.
Check each doorway, sealed side, route, machinery footprint, light hierarchy and
transparent exterior. Dimensional tests cannot prove these visual properties.

## Integrate the accepted result

Static interiors, stateful doors and machinery effects have separate roles.
Define effect anchors in room-local coordinates and transform them with the room.
Keep operation state separate from discovery knowledge: offline machinery stops;
unknown recipes remain hidden. Pause freezes continuing motion.

Update both station and card consumers, including alternate-art selection, without
rewriting unrelated gameplay. Preserve originals and player saves. Validate raster
staging through Git LFS and keep Godot script/UID pairs together.

Finish with native Godot evidence and relevant regression tests. Report what is
generated, rejected, integrated and verified, plus remaining work. A full-set
request is not finished when only a pilot is good. Do not install external apps,
purchase generation, publish, or push merely because this skill is active.

Reconcile furnishing coverage against the current RoomDatabase identities before reporting a catalog total; add newly introduced rooms to the ledger.

For decoration passes, follow the bible's Organic room composition section: author activity areas and physical supports before placement. Repeated paired accessories are a rejected composition, not a reusable template.

For supported furniture, use the project dressing helper where appropriate and see `docs/ORGANIC_ROOM_COMPOSITION.md`. Derive free circulation from each room's actual ports; do not reserve an unnecessary cross aisle in a single-door room. Validate composition profile hashes in packaged evidence alongside raster assets.

For true-alpha registration, use the read-only `tools/register_alpha_silhouette.py` and the supported-furniture lesson. Keep visual acceptance separate from route and packaged asset checks.

Before packaging profile-based furnishings, run `tools/audit_composition_dependencies.py` with the affected manifests; see the dependency audit lesson.

For all-room floor production and integration, read [floor coverage lessons](references/floor-coverage.md). Reconcile live identities and inherited floor owners; keep per-room source, placement, and native-acceptance stages separate.


## Build storage at closeout

For generated-package retention and disk cleanup, read
[storage retention](references/storage-retention.md). Preserve source art and
review evidence separately from disposable executable/package copies.

For sparse-room cleanup, source repaint integration and source-control closeout, read
[room materials and declutter](references/room-materials-and-declutter.md).
