# Selected animation loading

Updated: October 4, 2026 · BrineSpace · Performance follow-up

## Objective and acceptance

Owner approved auditing layered animation loading and loading only the surviving
images. Preserve current art, timing, equipment validation, saved animation banks
and readiness before gameplay. Compare the same native startup workload.

## Accepted decisions and constraints

This changes loading, not character selection or gameplay. Retained historical
banks (including Bill's supported carry bindings) remain loaded. Mirrors and
legacy helmet fitting still decode their dependencies when needed. Direct manifest
loads outside the explicitly batched station setup remain immediate. All native
runs used scratch APPDATA and copied layouts/checkpoints; restored autosave paths
were reset to scratch. No owner data, art, exports or commits changed.

## Current state

- `scripts/crew_texture_batch.gd` (+ UID): weak references to pending textures let
  overwritten frames expire. Materializes all surviving references before finish;
  computes the same alpha bounds on both raw and filtered textures.
- `scripts/crew_sprite_player.gd`: opt-in batching; equipment variants share the
  batch while retaining existing intermediate validation and stride snapshots.
  Mirroring explicitly resolves pixels before use.
- `scripts/swim_helmet_fit.gd`: resolves fitting inputs before composition.
- `scripts/grid_canvas.gd`: brackets the four normal crew loaders; finishes before
  publishing each player. Historical banks and derived bridge references keep
  their original texture identities.
- `tests/test_crew_texture_batch.gd` (+ UID), `tests/index.json`: 76 checks, native
  lane override, performance-diagnostics registration.

Audit counts represent frame allocations, including equipment; repeated source
files remain separate textures to preserve per-frame metadata and identity.

| Actor | Requested frames | Retained/loaded | Replaced/skipped |
| --- | ---: | ---: | ---: |
| James/Branforth | 14,668 | 8,056 | 6,612 |
| Bill | 7,404 | 3,624 | 3,780 |
| Marsh | 4,093 | 1,190 | 2,903 |
| Veld | 5,098 | 3,186 | 1,912 |
| Total | 31,263 | 16,056 | 15,207 |

## Verification

Evidence: `output/selected-animation-pass-2026-10-04/` (baseline source copies,
scoped diffs, probe/runner, native logs, bank signatures, screenshots, audit,
verification.json and owner fingerprints).

- Same restored station, layouts, 2560×1440 viewport and copied prior prefetch
  manifest. Native ready time **11,424.642 → 8,309.968 ms (27.3% faster)**.
  Entire startup PNG requests **32,169 → 16,962 (47.3% fewer)**. This is a local
  before/after observation, not a release benchmark or repeated statistical study.
- All 16,056 retained texture signatures match: full pixels, dimensions, formats,
  metadata, wrapper/filter; body/equipment timing, strides, gait groups and Bill's
  retained carry banks also exact. Frozen startup screenshots are pixel-identical
  and visually reviewed. They establish startup parity, not every live room state.
- Final reported texture memory unchanged at **5,249.95 MiB (~5.1 GiB)**. This
  eliminates redundant work; it does not claim improved gameplay FPS or lower
  steady-state texture memory.
- Native focused regression **76 checks, zero failures**: overwritten and retained
  frames, reset loads, intermediate equipment rejection, stride snapshots,
  filtering/alpha bounds, mirrors and real legacy helmet composition.
  Initial fixture expected the rejected mirrored variant to skip pixels; diagnostic
  state showed it correctly materializes before validation. Corrected expectations;
  failure and diagnostic logs retained.
- Native `test_loading_transition.gd`: **PASS**, new run and Continue.
- Scoped whitespace check passed. All **2,936 owner non-log files unchanged**.

## Next action

This loading change is complete in source. Release/export acceptance is separate.
For another performance pass, measure retained texture duplication/memory and live
room redraw bursts independently; neither is reduced by this change. Preserve
per-frame metadata, filter settings and identity when considering texture sharing.
