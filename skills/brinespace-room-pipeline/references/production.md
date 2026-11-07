# Production contract and verification

All paths below are relative to the active BrineSpace checkout, not this skill.
Keep project tools as the single executable source; do not fork copies into skills.

## Source ownership

- `scripts/room_database.gd`: canonical ID, footprint, layout and door masks.
- `scripts/room_card_art.gd`: current card PNG mapping; also inspect variant and
  aspect-fit selection in `scripts/main.gd`. Consumer locations can change.
- `scripts/grid_canvas.gd`: station PNG/variant mappings, crop/rotation and effects.
- `tools/room_art_pipeline.py`: Pillow cleanup and normalization (inspect `--help`).
- `tests/test_room_art_pipeline.py`: cleanup behavior tests.
- `docs/ROOM_ART_PRODUCTION.md`: production evidence and correction queue.
- `rooms/hybrid/`: current working images, not automatically accepted images.

## Per-room record

Record full prompts, reference roles, source/output hashes, actual dimensions,
processing settings and separate review findings. Use one pack index referencing
room records; the expected-ID set comes from the requested scope and current
database, including approved new IDs not yet added to the database.

Example review record for a currently blocked candidate:

```json
{
  "id": "corner",
  "path": "rooms/hybrid/corner.png",
  "stage": "cleaned",
  "geometry": {
    "expected_doors": ["west", "south"],
    "verdict": "fail",
    "findings": ["Door trim is present but actual west/south openings are missing"]
  },
  "integration": {"station": false, "cards": false},
  "verification": {"native_capture": null, "regression_log": null}
}
```

Do not mark absent evidence as passed. Existing `.provenance.json` files have a
lighter schema; read them as historical records, not full validation certificates.
Introducing a manifest or template generator is implementation work, not something
this reference claims already exists.

## Cleanup

The owner has authorized local background removal and margin normalization for
this room expansion. For other tasks, respect the current user's editing scope.
Use new destinations; the script refuses overwrite:

```powershell
python tools/room_art_pipeline.py output/room-art-pilot/hydroponics-candidate.png output/room-art-review/hydroponics-v2.png
python -m unittest discover -s tests -p test_room_art_pipeline.py
```

Pillow is required. Check availability before running. Cleanup preserves enclosed
light details, but light artwork connected to the exterior can still be removed.
Black backgrounds are not safely removable with a universal dark-color threshold:
station floors and shadows are dark too. Use an explicit mask or targeted edit.

Aspect-preserving bounding-box fitting can leave different side margins and does
not align door anchors. Non-integer nearest-neighbor resizing also changes pixel
cluster widths. Record those tradeoffs and inspect actual-scale output. After
anchors are established, use a shared template transform, not independent tight
cropping on every revision or animation frame.

## Geometry and state checks

For every room, inspect all four sides against the canonical door mask. Verify
openings are centered, widths agree at seams, and closed sides lack false door
trim. Walk the specified paths visually: a conveyor across an aisle is a failure
even if the simulation permits walking through it. Review rotations and adjacent
room pairs, not only a single upright room.

Define interior effect rectangles and pivots in normalized room-local coordinates.
Use the same transform for art and overlays. Do not bake active-only glow into
the sole static texture and call an offline tint a full operating-state system.
Do not infer new collision or resource mechanics from an illustration.

## Native acceptance

Use isolated-save harnesses, never the player's `user://brine_save.json`.
Adapt `tests/playtest_polish.gd` for paid builds, cards, rotation, connected doors,
operation, suspension, pause and discovery states. Inspect native viewport images
at 1280x720, 1600x900 and 2560x1440, plus mature-station zoom. Use paired frames to
prove motion/freeze behavior; a single screenshot cannot prove animation.

Run affected tests, the existing gameplay suites and main-scene smoke. Locate the
configured Godot 4.6 executable rather than hardcoding a user's Desktop path.
Inspect logs for `SCRIPT ERROR:` and `ERROR:` even with exit code zero.
For an existing-package dependency probe, use an empty project directory, not
only an external working directory with `--path` still pointing at the checkout.
Godot resource-pack mounting can fall back to local files and falsely establish
that a missing profile was packaged. `tools/inspect_pack_profile.gd` diagnoses
profile presence/hash/JSON or raw PNG presence/hash/decode under that isolation;
it does not certify room art. Register shared runtime atlases in each affected
room's component assets, not only its original source and card. Older room-state
evidence does not approve a newly substituted prop renderer.
For a new raw-PNG asset directory, check the explicit roots in
`addons/brine_raw_export/plugin.gd`. A `*.png` export filter can retain only
the imported texture and its remap; that does not satisfy FileAccess PNG-byte
loading. Verify the original path and hash from an isolated package after
extending the raw-export roots.
Room JSON is also read dynamically. A valid local profile and a `*.json` filter
do not prove package inclusion, especially during concurrent additions. The raw
export plugin includes JSON beneath `res://rooms` explicitly; verify new profiles
by isolated packaged presence, hash and parse checks. Do not interpret an empty
missing-file read as malformed source JSON or replace the source to silence it.
The current suites are test_synergy_manager.gd, test_discovery_progression.gd,
test_polish_gameplay.gd, test_run_balance.gd and playtest_polish.gd under tests/.

Before an authorized commit, check `git check-attr filter -- <PNG paths>` and
confirm staged PNG blobs are LFS pointers. Stage exact intended files only.

## Retry policy

After the same generation defect repeats, improve the input contract or use an
authorized deterministic repair instead of repeating identical prompts. Keep
structurally invalid candidates in the correction queue. Continue independent
in-scope work; ask only when the repair genuinely needs new authority or design.


For a baked checkerboard inside an open shelf or machine gap, an exterior flood alone is insufficient. After inspecting the source, use repeatable `--clear-gap X Y` seeds with `tools/room_art_pipeline.py`; only light-neutral pixels connected to those seeds are removed. `--keep-canvas` preserves registration coordinates. Record every seed, preserve the source, and inspect internal openings and bright trim. Never seed a lamp or pale material merely because it is enclosed. The four cleanup tests include a selected gap beside an unselected bright interior detail.


For small task furniture, brief the supported object and its support explicitly (for example a cutter in saddles, or recovered parts inside a tray). Avoid requesting generic additional machinery. Record raw alpha before cleanup; register existing alpha without rewriting the source. After integration, capture the task surface at normal station zoom as well as the depth diagnostic. A readable small asset is progress, not approval of an otherwise sparse room.


Before a full-catalog review, run tools/audit_room_review_inventory.gd headlessly and save its stdout. It compares the current RoomDatabase, selected card bytes and rollout ledger, exiting nonzero on omissions. Then run python tools/build_room_composition_review.py <inventory-log> docs/room-composition-review.html. The board rejects failed inventory or card hashes changed since the audit; it does not establish station-scale visual acceptance. Reconcile export entries too when new identities appear.

### Use mounted backboards where thin hulls cannot support large fittings
A bench-owned backboard can carry meters, hooks and leads without inventing a room-wide raised wall. Keep visible brackets and tabletop/shelf support; distinguish this freestanding furniture from hull attachments. Battery Array's test bench is the current example. Check full silhouettes before integration: requested transparent margins may still return clipped hardware, and reframing may replace alpha with a baked checkerboard. Preserve rejected sources and inspect cleanup gaps independently of cream meter faces and lamps.

### Explain floor-service crossings
A visual transfer run crossing a crew aisle must read as recessed or covered. Use a flush access plate or grate at the crossing and retain the floor-only rendering layer. Connect runs to registered machine endpoints, leave working faces accessible, and review all rotations. Do not imply new simulation behavior from a decorative connection. Ore Refinery's crusher/vessel transfer cover is an example.

### Separate buried services from exposed leads
Use routes below floor finishes for buried services and surface_routes above decals for exposed leads resting on the deck. Both resolve machine endpoints and remain floor-only. A surface route must not draw over a cover that should conceal it: split the route or use the buried layer there. Audit hosts in both categories. Obtain canonical door directions from current RoomDatabase/manifest before positioning an entrance fixture; names such as Quarantine do not imply dead-end geometry.

### Keep new identities visible while integration is incomplete
The current catalog may grow during a furnishing pass. Inventory v6 contains 40 rooms; three new rare rooms have no selected cards yet. Add their identities to the furnishing ledger immediately. The review-board generator's --include-incomplete mode displays missing-art entries and the inventory errors; it never substitutes another room's card. Default strict mode still rejects the same inventory, and changed hashes remain errors even in report mode. A successful 33-profile dependency audit covers declared assets only and does not prove all 40 rooms are integrated.
Command: python tools/build_room_composition_review.py output/room-review-inventory-v6.log docs/room-composition-review.html --include-incomplete

### Author new room placements by identity
Replace modulo-indexed sockets with explicit prop-ID placements when giving a new room its own composition. This prevents array-order changes from silently moving equipment into a different work area. Give inherited machinery its own service-routing profile; inherited endpoint positions can create long diagonal aisle crossings after relocation. Isolation Vault's local arrangement and perimeter services are the current example. Preserve honest provenance when reusing existing banks and tools.

### Profile ownership follows the new room
When a derived room adopts its own dressing profile, remove inherited dressing registrations before constructing the replacement helper. This loads the local profile's textures and avoids duplicate small furniture. Do not merely replace the helper's profile dictionary while leaving texture ownership tied to whichever profile its parent happens to select later. Pressure Control's ready sequence demonstrates this boundary. Check all objects: seven props cannot safely wrap around six generic sockets.

### Full 40-room packaged baseline
windows-catalog40-v1 passes 40 selected sources, 80 source/card PNG decodes, 68 component records and 36 composition profiles. The Windows controlled tour visits 60 placed rooms across 162 transitions and 12,525 movement samples. All 40 focused captures decode at 1600x900; hashes are in focused-capture-decode.json. Pack SHA-256: 58270AC6D6C83ADE1BD7C8E35EDC6549071763AC0424788D33CBE9E14AA66E9A. The ledger preserves the earlier package as historical. This is technical coverage, not full visual acceptance.
The floor-hook auditor now counts surface_routes as floor detail alongside mats, buried routes and decals. catalog40-floor-hooks-v2 covers all 36 current profiles without errors. This audit-only change postdates the package and changes no runtime art. Continue room-by-room visual review at actual station scale; a complete asset inventory does not establish natural composition.


### Holographic Core grouping follow-up — 2026-09-06

Offset the supported calibration cart beside its machine, raise the opposite terminal, and connect equipment with perimeter service runs. Reject the first placement: front-access probes passed but the machine interrupted a side entrance. Final depth review has 60 poses and 20 accessible fronts; current-route tour passes all four rotations (`output/holo-group-depth-v2`, `output/holo-group-routes-v2`). This illustrates why local prop access cannot substitute for doorway movement. The selected card is group-v1/profile-v3; the prior 40-room packaged baseline predates this change. Further wall and surface dressing remains a visual task.


### Hull repair preparation surface — 2026-09-06

Shield Generator now has a low clamped panel cradle, supported sealant gun/rag tray and contained hose between monitoring and compound injection. A distinct low support height helps the room avoid a row of repeated electronics benches. Reject the diagonal-camera first source; the second source needed explicit checkerboard cleanup including its enclosed leg opening. Preserve both generation prompts and cleanup seed in panel-cradle-provenance-v2.json. Native card panel-v1 was inspected; 72 depth poses, 24 accessible fronts and all four current doorway rotations pass (`output/shield-panel-depth-v1`, `output/shield-panel-routes-v1`). Catalog40-v1 export predates this revision; package verification remains due.


### Radio listening workstation — 2026-09-06

Radio Lab operator-v1/profile-v3 places an existing operator chair at the listening console, staggers the lower machinery around the supported electronics bench, and adds perimeter signal services with a flush covered doorway crossing. Reuse furniture when its activity fits; avoid copying an entire room accessory set. Final native depth review: 72 poses, 24 accessible fronts, no ordering failures. Current east/west routes pass all four rotations (`output/radio-operator-depth-v1`, `output/radio-operator-routes-v1`). The strict 40-room review board was refreshed from inventory-v8; it includes Holographic Core group-v1 and Shield Generator panel-v1. These three revisions postdate the packaged baseline.


### Review board revision visibility — 2026-09-06

The composition board now displays each ledger entry’s composition_revision alongside its limitations. Regenerate after selecting a card; a correct image hash with an old generic note is insufficient review context. Inventory-v8 rebuild contains all 40 identities and the three latest Holo/Shield/Radio revision notes. This reports recorded work, never automatic visual approval.


### Current 40-room packaged check — 2026-09-06

windows-catalog40-v2 includes Holo group-v1, Shield panel-v1 and Radio operator-v1. Exported Windows runtime passes 40 source/80 source-card decodes, 70 component records, 36 profiles, 60 arrivals, 162 transitions and 12,525 movement samples. All 40 focused PNGs decode at 1600×900. Shield station capture confirms the low cradle is present with clear central circulation; offline lighting limits fine detail. This is packaged integration evidence, not full furnishing approval. Verification: output/room-rollout/windows-catalog40-v2/verification.json.


### Maintenance service connection — 2026-09-06

Maintenance services-v2/profile-v3 adds a diagnostic lead to the parts trolley with a covered central crossing. Keep this run in routes below decals; surface_routes would incorrectly draw it over its own cover (rejected card-services-v1). Native four-rotation route fixture passes; furniture geometry is unchanged. Package catalog40-v2 predates this floor-only revision.


### Nursery substrate preparation — 2026-09-06

Nursery substrate-v1 adds a generated low wheeled stand with supply bags below and measuring tools above. Preserve original RGBA and source provenance; alpha registration uses 11 polygons. Canonical placement alone was insufficient because nursery machinery has authored quarter-specific positions: initial q1/q3 access failed, corrected explicit stand centers pass 72 depth poses with 24 accessible fronts and all four current routes. Evidence: output/nursery-substrate-depth-v2 and output/nursery-substrate-routes-v1. This revision postdates catalog40-v2; visual acceptance and package refresh remain separate.


### Hydroponics harvest stand — 2026-09-06

Harvest-v1/profile-v3 adds a low produce-crate dolly with packing paper and a supported shears/tags tray beside nutrients. Image revisions rejected a backdrop and a clipped handle before source-v3 cleanup; exact prompts, revisions and reviewed gap seeds are in hydro-harvest-provenance-v3.json. Native card inspected; 72 depth poses/24 accessible fronts and four route rotations pass. Updated station-scale visual and package review remain.


## Editor thumbnail consumer

Material replacement consumer audit: check inherited hull/cap UV donors, shared
dressing and common-tray entries, occupied and empty animation states, and both
card consumers. Replacing a default-room texture does not update these implicitly.
Keep diagnostic all-port captures separate from sealed production card bakes.
Preserve atlas cells and pivots when repainting animations; inspect actual alpha
and render explicit states. A fixture label does not prove its intended state.
Project example: docs/ART_MATERIAL_SESSION_CLOSEOUT_2026-09-08.md.

See [editor and water lessons](layout-editor-and-water.md): the tray must render
registered cutouts on transparency, never expose raw source-sheet backgrounds.
Native tray review is separate from source-art, card and in-room acceptance.


## Generated-package retention

Apply [storage retention](storage-retention.md) when exporting or closing a batch.
Record which binaries must remain replayable; preserve raw art, source snapshots,
manifests, captures and failure explanations independently. Temporary isolated
copies need an explicit lifecycle; the existing environment-export tool still
leaves them behind until its cleanup behavior is implemented.


## Playable package verification

When building or certifying an exported asset set, read the checkout's
`docs/RELEASE_WORKFLOW.md`. Follow runtime dependencies rather than excluding
folders by name: `tools/modular_room_geometry.gd` is used by gameplay and Studio.
Preserve raw PNG/JSON reads through the release manifest/export plugin; an
imported texture or clean editor import does not prove the raw file is packaged.
Keep generated sources and rejected candidates outside the shipped dependency
set without deleting them from the source archive. Use the current manifest tool
rather than rebuilding a broad all-resources preset from historical instructions.
