# Resolved furnishing-host audit

V32 exposed a renderer-inheritance defect: Bio Lab replaced Biodome's machinery
but retained its furnishing routes. Asset hashes and JSON parsing passed because
the files were valid; runtime host identities were not. Bio Lab now clears the
inherited profile before replacing hosts and retains its new child-owned profile.

`tools/audit_room_dressing_hosts.gd` instantiates the views named in the production,
batch-two and foundation manifests, deduplicates view paths, and resolves mat,
supported-object and route endpoint hosts after all four native rotations.
The first clean run covers 26 views, 22 active profiles and 192 references.
The negative control adds one nonexistent endpoint to the audit only and exits 1
with precisely that missing-host report. It does not mutate a production profile.
Logs: `output/dressing-host-audit-{positive,negative}-v1.*`.

The export helper now runs this audit after import and rejects process or engine
errors before packaging. This new orchestration hook still needs a complete
export invocation; its underlying command and negative control pass/fail as
expected. Both workflow copies document the gate and validate with matching hashes.
This is identity validation, not furniture support height, route artwork,
walkability, occlusion or full-catalog visual acceptance.

## V33 package evidence

PCK SHA256: `7d75bc7149d38c2050ce3f4e02712733aa14e3dced57370e33874daf620cfb72`.
V33 predates the new audit hook. It passes 20 selected source hashes, 40 raw PNG
decodes, 26 component checks and 17 composition checks without the old furnishing
errors. The full tour is nevertheless rejected: after seven completed legs,
crew traffic stalls en route to Crew Lounge `(25,19)`. The target is `(9792,7488)`;
Bill remains at approximately `(9782.36,7671.25)` beside an active peer at
`(9767.98,7655.73)`. This is not fixed by successful room-art tests.

Individual Bio Lab packaged tests are recorded separately in
`output/batch-two/bio-isolation-export-{1280,1600,2560}-v1/`.
All three pass against the same PCK, with input isolation and 69 full-frame
dimension checks per run (207 total), four rotations and the five actual economy
states including restoration. No runtime engine errors were logged in these runs.
The 1600 restored q1 frame was reviewed: the lab and its own supported fixture
render with clear machinery silhouettes; this single frame is not full visual
acceptance or movement coverage. No bible aesthetic rule changes in this pass.

V34 executes the new audit hook successfully before export (26 views, 22 profiles,
192 references). Its tour completes after the crew graph-join repair, but the
build is rejected for a Hull Integrity profile JSON-loading error. See
`LOUNGE_TRAFFIC_JOIN_REPAIR.md`; native host resolution does not prove that every
profile is included in the package.

## Explicit room JSON export: V37

An isolated V34 probe confirms Hull Integrity's profile was absent (zero bytes),
not malformed. The current local JSON validates. `addons/brine_raw_export/plugin.gd`
now includes JSON under `res://rooms` explicitly alongside existing raw PNGs.
Player saves and unrelated filesystem locations are not included by this rule.

V35/V36 stopped at import during concurrent Thermal Control edits: duplicate
`rebuild` definitions prevented parsing. The other edit was corrected, then an
explicit check-only invocation passed before V37. These failed builds remain.

V37 passes import, resolved-host gate, export and standalone controlled tour
without engine errors: 30 arrivals, 84 reciprocal transitions, 6365 movement
samples. PCK SHA256:
`a18df340e459e054ae27b08bec4e842069db80b1c15f83528bfe6c103f849a81`.
An empty-project isolated probe reads all 46134 bytes of Hull Integrity's JSON,
parses successfully and matches local SHA256
`0250f9ab2d9c4c1cc6fa4b7bcb481778f66d7cb581addd126451277e8ee646f0`.
Evidence: `output/hull-profile-v37-probe.log` and
`output/batch-two/windows-validation-v37/verification.json`.
This establishes this debug package's loading and controlled traversal, not
release, autonomous destination-choice, or complete room-art acceptance.

## Live-catalog coverage

The audit now uses `RoomDatabase.all_rooms()` and the station's actual
`_bill_room_view` dispatch instead of the three batch manifests. The current
catalog contains 35 identities: 33 distinct room renderers and two explicitly
reported procedural corridor types (corridor and corner). Of those renderers,
29 have dressing profiles; 276 host references resolve across four rotations.
The audit does not require a dressing profile where the renderer does not use one.

`output/dressing-catalog-positive-v1.log` exits 0 with no failures. The
`missing-host` and `unmapped-room` negative-control runs both exit 1 with exactly
their intended failure: a nonexistent host and a room silently resolving to the
nursery fallback. All three stderr logs have no ERROR or SCRIPT ERROR entries;
existing raw-image loading warnings remain. No main gameplay scene or save is used.

The existing export hook invokes this expanded audit automatically; no new export
was produced in this pass. These checks establish catalog coverage and resolved
identities, not visual, movement, procedural corridor geometry, or package approval.
The workflow skill now records this coverage rule in both copies. The bible's
visual direction is unchanged.
