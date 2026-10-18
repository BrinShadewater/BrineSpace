# Live look audition â€” October 18, 2026

The owner requested an in-game comparison after trying screenshot pixel/tilt-shift previews. This is an experimental, session-only source feature; no permanent visual direction is accepted.

- **F10:** toggle the preview on/off. Starts off each scene.
- **Shift+F10:** toggle a 2 px grid blended at 60%, enabling the preview.
- Default preview: no pixelation, 0.5 px maximum tilt-shift sampling radius, focus band at 25% of the station viewport height, original colours. These follow the owner's latest screenshot selections. The native weighted blur approximates the screenshot Gaussian blur.
- HUD, card hand and inspector remain outside the effect. F6 atmosphere comparison remains available. Nothing is written to saved visual preferences.

`scripts/look_audition.gd` is attached by two lines in `scripts/screen_atmosphere.gd`. When off, both the effect rectangle and screen copy are hidden. GPU comparison proves the off image returns exactly to the original after the notification disappears. The effect is positioned inside the station frame and follows its normal resize/layout anchors.

Validation: `python tools/run_tests.py --only test_look_audition --native` passes 12 checks (input, repeat suppression, defaults, sharp focus/interface, defocus and exact off restoration). Existing atmosphere mask test passes. Actual source gameplay restored a twelve-room QA checkpoint under scratch APPDATA; off/tilt/pixel+tilt captures visually reviewed. Both active modes change station pixels and zero pixels outside its bounds. All 2,958 real profile files fingerprinted unchanged.

An isolated playable launcher is at `output/pixel-audition-20261018/Play look audition.cmd`. It opens actual source gameplay directly, bypassing the title loader, with a scratch copy of profile/layout data and the existing QA checkpoint. Starts paused for comparison; Space resumes. Normal source launches also have F10. Existing exported executables have not been rebuilt. No performance or platform acceptance is claimed.

Evidence and continuation: `output/pixel-audition-20261018/LIVE_HANDOFF.md`, native test logs, `live-render-verification.json` and three `live-*.png` captures. Source follow-up is published on `codex/look-audition-20261018`, based on the reconciled Windows/Mac/iPad review branch. No export or main merge. Fresh publication checks reran both native tests successfully and verified all 2,958 real profile files unchanged. Apple/platform and performance acceptance remain pending.
