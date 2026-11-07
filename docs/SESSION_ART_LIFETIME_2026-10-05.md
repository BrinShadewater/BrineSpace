# Project handoff

Updated: October 5, 2026 · BrineSpace · Unused session artwork cleanup

## Objective and acceptance

Release unused artwork after gameplay/Studio exits, preserving live drawing owners,
selected source pixels, owner layouts and re-entry. Measure matched transitions
and equivalent settled memory; do not evict active animation states.

## Accepted decisions and constraints

Old crew players already release after leaving gameplay. Strong factory lookups
and derived prop templates retain other images beyond their users' lifetime.
Clean only after the last registered owner leaves the tree. Main and Studio lease
resources; Studio also leases the current scene root (or its backdrop in script
fixtures), preserving standalone previews and avoiding leases on persistent report
overlays. Normal active-scene caches, filtering, PNG loading and animation unchanged.
Owner data/catalog descriptions, favourites, aliases and layouts remain intact.

## Current state

New `scripts/session_art_cache.gd` and paired UID use weak owner registrations and
one-shot exit callbacks. Last-owner cleanup joins pending library/drone decodes,
drops unused results, releases portable views, derived library templates/source
images/bunk layers, original room-source lookups, both floor mesh generations and
their images, environment lookups and drone cache bookkeeping. Lightweight art
definitions/settings remain. Existing Main/Studio pending-job drains still execute.
`scripts/main.gd` and `scripts/room_layout_editor.gd` register owners in `_ready`.
Reference switch: `--reference-session-art-cache`. No art/save schema/export changes.

New `tests/test_session_art_cache.gd` and UID are registered in the native
performance lane. Evidence/runners/full logs/source hashes:
`output/session-texture-lifetime-2026-10-05/`.

## Verification

Godot 4.7.2 native Compatibility / RTX 4070 Ti, isolated profiles with copied owner
layouts and a scratch checkpoint. Resolved user directory checked before writes.
18 focused checks pass: duplicate/overlapping leases, surviving retained pixels,
retired floor generations, weak image release, derived template removal, both
pending worker queues, exact reloaded source/floor/prop pixels and prop registration,
plus reference behavior. These are source/floor/prop passes, not full motion review.

Three alternating matched reference/candidate pairs each execute two actual
Title Continue → gameplay → menu save → title cycles. Studio opens/closes during
the first gameplay entry; its closure keeps Main's lease and artwork. Dialogue
typing skipped in the fixture; production/code otherwise follows normal routes.

| Raw engine texture counter, MiB | Reference | Candidate |
|---|---:|---:|
| Initial title | 47.00 | 47.00 |
| First gameplay after Studio | 3,446.20 | 3,446.20 |
| Settled title after exit | 682.40 | 383.46 |
| Following gameplay entry | 3,629.99 | 3,473.92 |

All three pairs reproduce these allocation figures. Removing only source-image
lookups was insufficient because the catalog's derived templates also owned
images; clearing those derived entries is included in the final candidate.
The earlier 80 MiB prototype saving is superseded by this final comparison.
This reduces retained images and next-entry pressure; it does not bring active
gameplay under the existing memory budget or measure driver residency.

First-profile measured startup-stage median: reference 15.376 s, candidate
15.421 s. Repeated Continue median: 4.767→5.040 s; candidate samples 4.712–5.578 s.
The cleanup trades about 273 ms median reload work for reclaimed storage.
OS/driver caches uncontrolled; first-profile is not certified cold. Neither these
stage sums nor the fixture's editor executable certify packaged loading gates.

Final enabled-default ten-cycle native run includes Studio ownership checks and
normal menu saves/Continue. Settled title 383.46→383.82 MiB (~0.094% growth);
comparable later gameplay 3,473.92→3,474.24 MiB (~0.009%). Old main scene and Veld
player release on each exit; obsolete leases/lookups are empty at title. No failures
or engine errors. Earlier short reference/candidate fixtures each emit one common
ObjectDB shutdown warning; the final verbose ten-cycle run does not reproduce it.
Its cause is unassigned; no general clean-shutdown fix is claimed. Initial probe
method-name and focused-test native-class-name setup errors were corrected before
accepted runs. All batches preserve 2,936 owner non-log files. Scoped diff/index
checks pass. No two-hour soak, active large-fleet transitions or native Mac run.

## Next action

Keep this cleanup enabled within its measured scope. Audit remaining title-resident
image owners using explicit bounded roots, especially room material/window caches.
Do not clear data-driven owner marks or introduce active-state reload misses.
The reported station still exceeds 2 GiB and the active large-fleet budget remains
unresolved. First-profile loading, long stalls, two-hour large-station endurance,
minimum hardware and packaged Windows/Mac/signing gates stay open. Frozen release
inputs remain unchanged.
