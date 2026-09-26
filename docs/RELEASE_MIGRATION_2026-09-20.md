# Runtime migration release handoff

Updated: September 20, 2026. Project: BrineSpace.

## Objective and acceptance

Verify migrated runtime artwork in a real Windows release before preparing Mac
testing. This is scoped launch/render/report acceptance, not broad gameplay or art
approval.

## Accepted decisions and constraints

Owner Mac testing hardware is Apple Silicon (M1 or newer). Preserve owner layouts
and library marks. No Higgsfield, publication or commits requested. Bill's generated
walk study remains unselected; room composition revision 02 awaits owner review.

## Current state

Validated package: `builds/BrineSpace-migration-2026-09-20-fixed/`, build ID
`brinespace-66abbef9bc1a8278`, source fingerprint
`66abbef9bc1a82789b5d19e7aa382a49d733bc9d38537af4802bcc31d9edab14`.
Includes EXE/PCK, build_info, README, NOTICE and SHA256SUMS.

The first candidate was rejected: its old custom template was actually Godot
4.6.1 and could not read the 4.7.2 PCK. `tools/export_release.ps1` now checks the
template binary version against the editor. Official 4.7.2 templates were verified
against published SHA512 sums and selected in `export_presets.cfg`.

`addons/brine_raw_export/plugin.gd` now excludes unselected raw files and sidecars;
`tools/audit_release_assets.gd` rejects unexpected raw files as well as missing or
changed dependencies. The rejected pack reproduced 2,189 unexpected files.

`tests/release_new_game_smoke.gd` now follows architect selection and waits for
observable dialogue/Continue state. A temporary probe established that the old
frame-count timeout expired during normal typing; it was not a game startup fault.

## Verification

- Five Python release manifest/assert-safety checks passed.
- Version mismatch preflight rejected the old template before export.
- Exact corrected pack: 15,085 checked, zero missing/changed/unexpected files.
- Actual release: New Game, simulation and F8 passed with zero failures and
  `debug=false`; 66 environment textures and five foundations loaded.
- Native game and report screenshots visually inspected. QA used a separate user
  profile; its external autoload override is disabled and absent from delivery.
- Static path-case audit found no tracked collisions or reference mismatches.

Evidence: `output/release-migration-2026-09-20/`, especially
`release-accepted.log`, `pack-audit-fixed.log`, `release-game.png` and
`release-report.png`. Older failed logs are retained as diagnostics.

## Next action

Follow `MAC_RELEASE_PLAN.md`: parameterize manifest preset selection, prepare the
Mac candidate, then test on the owner's Apple Silicon hardware. No Mac runtime,
signing or notarization acceptance exists yet. Bill identity-preserving body motion
and wider natural room decoration remain separate outstanding work.
