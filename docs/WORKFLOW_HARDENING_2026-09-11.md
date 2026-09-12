# Workflow hardening and placement envelope — September 11, 2026

Track 4 of the audited plan, plus the placement-envelope unification the owner
approved during the session. Source and tests only; no executable rebuilt, no
art or registration touched. Everything below is on `main` and merged to
`godot-4.8-preview`.

## What landed

| commit | change |
|---|---|
| `9a87908b` | Skill sync repairs, `--ignore-eol` / `--expected` in `check_source_sync.py`, character bindings 4 → 16, portrait cross-check, bible correction |
| `94678923` + `4350ac84` | `tests/test_layout_keys.py` layout-key guard, wired into CI |
| `1eb3a460` | `push_warning` instead of a silent out-of-envelope prop reset |
| `2f10ae2e`, `9183d928`, `9ea18cc7` | Three stale native tests matched to owner decisions |
| `f60e8bc2` | One shared placement envelope for Studio and the live game |
| `7cfa1dc5` | `test_run_save` scene-swap flake fix |

## Verification

- Headless suite (run `20260911-171234-headless`): **112 PASS, 1 SKIP, 54
  SKIP-NATIVE, 0 FAIL**.
- Native layout lane (run `20260911-163810-native`): **7 PASS, 1 SKIP-HEADLESS**.
- `test_run_save` after the flake fix: four runs, one deliberately overlapped
  with a native lane — 31.3s, 31.4s, 31.7s, 31.6s, all PASS.
- Character bindings audit: 16 bindings, 9 packs, 355 clips, 8 portraits, 0 errors.
- Layout-key guard: 188 authored layouts, 0 problems; owner's saved layouts
  checked read-only from a copy, 0 problems.

## Placement envelope — what changed and why

Studio allowed 360×360 (368×390 wall-mounted, 368×444 movable-region) while the
running station enforced 360×378 and a full cell (400×400) for wall mounts, so a
placement could look legal in Studio and be reset in game. Both sides now call
`RoomLayoutStore.envelope_for()` and `RoomLayoutStore.door_lane()`; the live
values are the truth. A wall-mounted prop that also carries a movable region now
gets the taller movable box in game, matching Studio.

Measured impact across 47 rooms × 4 rotations: **30 placements change status, 29
of them Studio relaxing to match the game.** Only constrained layouts are
affected — 0 of 188 authored layouts and 1 owner layout
(`cryo-support-wall/0`) are in constrained mode; free placement skips the checks
entirely.

## Open items

1. **`battery_array/1` `full_wall_battery-wall_cells` is reset in game.** Its
   bounds sit ~4 units above the wall-mount envelope, so `apply()` snaps it back
   on every draw. Since `1eb3a460` this emits a named `push_warning`. Likely a
   registration or y-offset correction; do not widen the shared envelope without
   owner approval.
2. **`test_camera_pixel_stability` fails 2/64 at 960px, zoom 0.6.** Pre-existing:
   it reproduces at session-start commit `59c1e95a` and on both 4.6.1 and
   4.8-dev5. Cause unknown, not investigated.
3. **Fixed-duration waits elsewhere in fixtures.** `test_run_save` is fixed; the
   same pattern (a fixed wait after a scene swap, then an assertion) may sit in
   other fixtures and is the likeliest source of future flakes.

## Owner-gated, unchanged this session

Itch upload of the slim build (`builds/BrineSpace-2026-09-11-slim/`, procedure in
[ITCH_UPLOAD_WORKFLOW.md](ITCH_UPLOAD_WORKFLOW.md)); deleting the holding folder
`C:\Users\Alex\BrineSpace-to-delete` (its `MOVES.tsv` is the undo log) and the
`git worktree prune` that follows; the Higgsfield pilot, which needs an owner
login.
