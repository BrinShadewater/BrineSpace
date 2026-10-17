# Native Apple validation evidence — 2026-10-17

See [handoff](../MAC_IPAD_NATIVE_VALIDATION_HANDOFF_2026-10-17.md) and [performance](PERFORMANCE.md). This evidence validates the exact integration585111ca3, without game-source changes. Native Mac fixtures, a QA clone of a maintained release export, and physical iPad acceptance are separate lanes. Physical iPad acceptance is **BLOCKED**.

- `build-and-platform.json`, `hydration.json`, `parent-runtime-verification.json`, package/source audit logs: identities and export scope.
- `python-tests.json`, four Python logs, `headless/`, `native-tests.json` and native test logs: focused source lanes.
- `mac-deep-*.log`, deep-home journey JSON: ordinary release New/Continue, 76 checks; earlier home4 journey JSON is supplementary, not additional unique coverage.
- `native-desktop-input.json`, `native-f8-local-save.png` (if present): native UI keyboard/local report interaction. No report upload.
- `balanced/`, `balanced-analysis.json`: six source/editor ABBAAB visits; A=Mac parent, B=integration.
- `release-benchmark/`, `release-benchmark-analysis.json`: three separate actual release-template visits. JSON contains frame samples and phase summaries; logs retain time/memory output.
- `game-continue.png`, `title-new.png`: real Mac release captures. `forced-tablet-*.png` are **Mac tablet-mode fixtures**, not iPad captures.
- `preservation.json`: before/after exceptions; preservation is not an unconditional PASS.
- `review.md`: static integration review and explicit failures/limits.
- `reproduction/`: external QA helpers used for this dated run, not production changes. `.gd.txt` files intentionally are not imported game scripts. Python drivers contain local absolute paths; adapt them to your scratch worktrees/SDKs. Recreate the guarded QA override and scratch HOME before invoking any helper. Never run them against an owner profile. The normal maintained tools remain in `tools/`.

The full local archive is `/Users/Shared/BrineSpace-native-validation-evidence-20261017`. Failed exports/setup runs, full report ZIPs, app/PCK/ZIP outputs, profiles and crash IPS remain there. They are not uploaded. Portable evidence intentionally excludes saves, signing material, SDKs and owner profiles. Logs have dated local paths for provenance.

Portable text copies normalize trailing whitespace; original logs remain in the local archive.
