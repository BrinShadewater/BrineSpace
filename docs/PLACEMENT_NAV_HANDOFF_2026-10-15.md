# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: placement/navigation CPU

## Objective and acceptance

Reduce remaining placement/navigation cost without visual or gameplay changes;
benchmark average FPS, action peaks and following windows against the latest
frozen one-spare private LOD candidate. Normal source and private QA remain separate.

## Accepted decisions and constraints

Keep clocks, geometry, routes, graph order/IDs, lock policy, bonuses and discovery
semantics. No art, renderer, quality, export or source-wide refactor. Native timing
serial and visible on secondary display; owner confirmed other runs paused.

## Current state

`scripts/synergy_manager.gd`: evaluate-local room-ID presence skips impossible pair
and pattern scans; passage and tagged-medical Cryo paths unchanged.
`scripts/bill_npc.gd`: retain canonical seam connections only within proven unchanged
prefix geometry and identical hardware/room-lock policy. Staged/layout/policy changes
take the original path. Per-actor bookkeeping is replaced each rebuild.
`tests/test_navigation_prefix.gd` adds connected row/column partial-prefix ordering
coverage; new synergy parity test/UID registered in tests/index.json. Script UIDs
preserved. Installed implementation matches private candidate.

`tools/run_tests.py` now selects scratch storage by default and refuses real-profile
redirects; four fake-engine isolation tests pass. This follows an actual isolation
mistake: progression restored from untouched backup, two legacy test metadata files
remain changed. See [incident](TEST_PROFILE_INCIDENT_2026-10-15.md); do not claim the
whole owner folder was untouched.

## Verification

Private graph oracle: 1,488 checks, 259,265 ordered records, 2,328 routes exact.
Synergy: 8,043 checks / 1,188 cases across 112 authored recipes, ordered links,
bonuses, mutations and input ownership exact. Eleven installed source regressions
pass under scratch profiles with zero skips; corrected owner guard unchanged from
post-recovery baseline. Independent source and runner review completed.
Release diagnostic: synergy evaluation about 7→1 ms. Controlled actual-release
navigation saves 0.57–0.73 ms per actor across warm/append/middle-edit cases,
both order subsets, exact graphs. Clean `focused1`: 1,920 release frames, eight
exact state/camera/path pairs; normal placement 52.852/54.871→46.237/51.717 ms.
4× 79.374/76.126→71.810/78.696 ms remains mixed. Idle 49.57→49.96 FPS, essentially
flat; 0/8 60 FPS gates. Seventeen cross-process station/first-placement image pairs
exact, plus twelve repeat pairs. Thirty-five clean owner guards, one incident;
current fingerprints equal post-recovery baseline. No task-owned game remains.

## Next action

No further unchanged timing needed. Investigate large suffix point/link rebuilding
at 4× or steady live rendering/exterior/atlas costs. Private LOD stays private;
normal source improvements are installed, with no new export or commit. See
[results](PLACEMENT_NAV_PERFORMANCE_2026-10-15.md) and preserve the profile-incident
caveat. Evidence: `C:/bs-placement-nav-20261015/`; helpers:
`output/placement-nav-20261015/`.
