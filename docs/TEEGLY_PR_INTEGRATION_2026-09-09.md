# Teegly PR integration

Updated: September 9, 2026 · Project: BrineSpace · Task: review and integrate PRs #7 and #8

## Objective and acceptance
Review Teegly's release crash fix and bug-report feature, retain newer art/gameplay, merge on GitHub, and verify an actual release executable starts New Game.

## Accepted decisions and constraints
Preserve normal paid gameplay and all unrelated local edits. Retain Teegly's commits through merge ancestry. Reports are saved locally; nothing is uploaded or sent automatically. Existing saves and current art/layout work remain intact.

## Current state
- PR #7: moved image decoding outside release-stripped assertions. Resolved 15 merge conflicts against current artwork; extended the same correction to newer loaders. Three additional loaders in local art work are fixed locally without publishing that unrelated art.
- PR #8: F8 report ZIPs include logs, last on-disk saves, screenshot, tester note and system details. Unclean-session detection collects prior diagnostics and available bounded Windows dumps.
- Follow-up: reporter processes while paused, pauses the scene tree while open and restores its previous state, reserves F8 in controls, makes report names unique, rejects partial folder writes, removes failed ZIPs, discloses dumps in folder fallback, and avoids claiming an active second process crashed.
- `.github/workflows/ci.yml` runs `tests/test_release_assert_safety.py` to catch future runtime loads inside assertions, including multiline calls.
- Fixtures: `tests/test_bug_report.gd`, `tests/release_new_game_smoke.gd`, paired UIDs and the Python guard. Runtime changes span the image loaders, `project.godot`, `scripts/bug_report.gd`, `scripts/settings_panel.gd` and `scripts/title_settings.gd`.
- New local Windows release: `builds/BrineSpace-2026-09-09-fixed/`. This packages the current local art as well as the fixes; the source integration commits contain only the PRs and relevant follow-up work. The older executable is unchanged.

## Verification
- Python guard: two tests pass, including multiline detection and all runtime GDScript sources.
- Isolated native reporter fixture: zero failures. Checks F8/screenshots, pause restoration, unique archives, tester note, save inclusion, 2 MiB newest-log tail, previous log, partial-folder failure, folder dump disclosure, stale-session reporting and lock removal. Native overlay reviewed at 960x540.
- Actual release executable: `release-accepted.log` reports zero failures and `debug=false`, with no engine/runtime errors. Uses the configured title, New Game, transmission Continue, normal Resume, 240 running frames, visible station and F8 report creation. Checks use explicit branches, not release-stripped assertions. Prior fixture iterations exposed the deliberate paused opening and dialogue pauses; the final fixture presses Resume and verifies simulation time advances without changing game behavior. Native 1600x900 station/report captures reviewed. Test override removed from the deliverable; EXE/PCK SHA-256 hashes saved.
- Export completed; pre-import emitted three `get_multiple_md5` / `f.is_null()` errors while reimporting numbered PNGs. These were not script parse failures. Final runtime evidence is assessed separately; this is not blanket acceptance of every packaged asset.
- Evidence: `output/pr-review/` contains merge logs, original diffs, local-overlap backups, native/release logs and reviewed captures.

Reproduce reporter fixture in a small isolated project: copy `scripts/bug_report.gd` as `res://bug_report.gd`, copy the fixture, set a unique application name, then run Godot 4.6.1 with `--path <fixture-project> --script res://test_bug_report.gd`. Its screenshot is written to that project's `user://`.

Reproduce release test beside a copy of the EXE/PCK: temporarily add `override.cfg` with `[application] config/name="BrineSpaceReleasePRFixture"` and `[autoload] ReleaseSmoke="*<absolute-path-to-tests/release_new_game_smoke.gd>"`. Run the release EXE with a log path, then remove that override. Screenshots go to isolated `user://`; do not ship the override.

## Next action
Use the fixed local executable for further playtesting. Native diagnostics and the opening release journey are covered; this is not a full expedition/balance acceptance. Missing/corrupt-image fallback behavior remains a separate improvement: the PR logs decode errors but does not provide replacement artwork.
