# Project handoff

Updated: 2026-10-15 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: bulk navigation construction

## Objective and acceptance

Reduce graph construction cost without appearance or crew behavior changes;
benchmark average FPS and 4× placement action/following-frame hitches.

## Accepted decisions and constraints

Both native trials remain private. Preserve installed Bill/Synergy, graph identity,
IDs/link order/weights/locks/water policy, routing and synchronous schedule. No
quality, renderer, art, gameplay or export change. Use scratch APPDATA plus the
test user-dir override for every Godot invocation and fingerprint the owner folder.

## Current state

Only this report/handoff and CURRENT_STATUS are added/updated in project source.
Private C++/DLLs, candidate Bill overlays, frozen packs, raw logs and final audit:
`C:/bs-bulk-nav-20261015/`. Helpers: `output/bulk-nav-20261015/`.
V1 uses per-room batches; V2 batches the whole rebuilt suffix. SDK pinned to
`1e7926375b62b445fa79db6851f7105b644831f2`; V1 binary/source preserved separately.
No commit, new export, installed extension or Mac binary.

## Verification

V2 middle-suffix rebuild 13.319→12.367 ms / ~7.1% faster in isolation; warm and
append effectively flat. Two guarded release series: 3,840 frames, sixteen exact
state/camera/path pairs, 0/16 60 FPS gates. V2 normal idle 51.35→48.24 FPS; 4× action
68.306/70.146→71.624/72.386 ms. Following-sixty-frame mean/p95 worsen both orders,
>50 ms counts 1→2 and 1→3. V1 has mixed action savings and worse following means/p95.

V2 oracle 9,425 checks / 269,812 ordered records / 2,352 routes passes; native
primitive 346+226 and extension-absent fallback 1,488 checks pass. Seventeen
cross-process image pairs plus twelve repeat pairs exact. One intermediate harness
script error was rejected and corrected; do not count that run as passing.
All 28 profile guards clean; final 2,948 files equal task-initial and prior
post-recovery baseline. Source/UID hashes unchanged; only owner editor PID 46624
remains. Earlier [profile incident](TEST_PROFILE_INCIDENT_2026-10-15.md) still applies.

## Next action

Investigate large suffix invalidation in the two companion graph rebuilds; separate
script preparation from native mutation before choosing another prototype.
Prove additional retention with exact graph/route/water/lock oracles, then run one
guarded forward/reverse full-game comparison. Do not repeat unchanged trials.
Native shipping would additionally need Windows/Mac packaging and release checks.
See [full results](BULK_NAV_PERFORMANCE_2026-10-15.md).
