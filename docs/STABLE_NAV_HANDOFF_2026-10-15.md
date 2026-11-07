# Project handoff

Updated: October 15, 2026 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: stable navigation IDs prototype

## Objective and acceptance

Prototype navigation without global node renumbering; preserve game appearance
and crew behavior. Compare large-station average FPS and 4× placement hitches.
Prototype and requested comparison are complete. No normal-runtime integration.

## Accepted decisions and constraints

Each actor keeps its own ordinary AStar2D. Stable 1,024-ID cell blocks retain
unchanged cells, replay seams in original order and use existing sparse-safe
detour reachability. Scheduling, route resets, restrictions and simulation stay
unchanged. Full revisions, staged/reference modes, missing extension or rejected
plans fall back to canonical script assembly. Helper assumes sole structural
ownership; external same-size graph/lookup edits require reset. Exact-distance
`get_closest_point` numeric ties can differ, so the preview tool is outside scope.

## Current state

Private Windows V3 source/DLL, frozen reference/three candidates and evidence:
`C:/bs-stable-nav-20261015/`. Helpers: `output/stable-nav-20261015/`.
Among 22 frozen scripts only Bill differs. Native API revision 3 uses
`native/bin/brine_stable_v3.dll`; V1/V2 remain immutable and archived. No normal
runtime, UID, art, export, renderer, Mac package, commit or upload changed.

Documentation added: [results](STABLE_NAV_PERFORMANCE_2026-10-15.md), this handoff;
`CURRENT_STATUS.md` records the milestone. Keep the current chat/context.

## Verification

- Connected rebuild: 9.894→4.913 ms per actor; warm/simple rebuilds ~0.4–0.5 ms slower.
- Live 4× placement: 68.418/68.161→58.479/57.549 ms in opposite orders; crew phase ~26.3→15.1–15.4 ms. Final helper call retains 14,075 nodes across 52 cells.
- Normal idle 51.86→52.37 FPS; 4× idle 46.52→44.63. 4× placement phase 42.91→43.68 FPS. No dependable steady gain; 0/8 mean/p95 60 FPS gates.
- 1,920 guarded release frames, eight exact state/camera/path pairs. Subsequent sixty-frame placement windows improve; other hitches remain.
- 3,157 native assertions, 2,530 integrated graph checks / 2,872 routes, 2,216 extension-absent checks pass. Ordered physical maps/neighbors/seams, flooded/swim/traffic/fire paths and fallbacks covered.
- Seventeen cross-process image pairs and twelve repeat pairs pixel-exact; fitted station visually inspected.
- All 24 owner guards / eleven binary guards clean. Final 2,948-file fingerprint equals initial and prior protected baseline; installed sources/UIDs/test unchanged. Only owner editor PID 46624 remains.

The [earlier profile incident](TEST_PROFILE_INCIDENT_2026-10-15.md) caveat persists.
`final-audit.json`, `focused1-analysis.json`, `stable-micro3-analysis.json` and
`crew-phase-analysis.json` retain evidence. Native SDK pin/build identity is in
the report; no Mac or normal-export acceptance has been attempted. Long-session
memory high-water usage is unmeasured.

## Next action

Keep this promising placement prototype private. Investigate the mixed idle
result and isolate sparse detour reachability cost before integration; current
crew counters do not explain the whole-frame 4× idle difference. Then validate
bounded memory and Windows/Mac native packaging, retain physical routing oracles,
and handle numeric-tie-sensitive preview APIs separately if ever adopted there.
