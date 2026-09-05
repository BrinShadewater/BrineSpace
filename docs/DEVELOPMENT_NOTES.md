# BrineSpace Development Notes

## Prototype North Star

BrineSpace should feel like restoring a silent machine in orbit: build a little, watch the systems find their rhythm, notice a strange connection, and decide whether to risk one more room before the next reboot. The interesting pressure should come from the station's interlocking needs, not from click speed.

> **BRINE // DIAGNOSTIC**
>
> *"I have mapped thirty-seven ways to run out of oxygen. I recommend none of them."* ⚠️

## Current Focus

The full-run follow-up is now on local `main`, alongside the remote documentation and CI changes. A matched 30-run automated sweep improved from 12 to 21 completions after adding slow draft recovery, with at least one completed run per doctrine pair. See [Balance Report](BALANCE_REPORT.md) for the full comparison and the remaining discovery droughts; these are bot results, not human completion-rate targets.

Rerolls rebuild one charge every four cycles below a bank of three, and the draft button shows the wait. Directive reward overflow is preserved. A full-run screenshot also exposed the old 22% minimum zoom clipping mature stations; Fit Station now supports a wider overview range.

The September discovery/polish pass completes the 12-foundation → 30-blueprint graph with 25 patterns. Rooms teach their relationships through functioning effects; the journal records knowledge after discovery, never before. Progress and rewards persist independently of winning a run.

Implemented in this pass:

- Three consecutive functioning cycles stabilize a recipe once; duplicate links stack output but do not accelerate discovery.
- Closed Air Loop reclaims Water so its Biodome prototype is affordable; Biodome Atmosphere recycles Water for the next bio branch.
- Every doctrine pair gets food and oxygen foundations; selected doctrines retain stronger card weighting.
- Shared per-cycle input budgets, operation-aware forecasts, limited recovery berths, and an actual corruption-cleaning Containment Sector.
- Click-to-inspect room suspension, a pausing spoiler-safe journal, a two-row resource HUD, compact cards, fit-station control and scrollable inspector/summary.
- Optional open expeditions after victory, with a menu cash-out and one-time victory/mastery rewards.
- Updated/old saves retain existing discoveries and blueprints. Old orbital events no longer shortcut blueprint decryption.

Verification: three headless regression suites plus a real-scene deterministic paid-build playtest pass. The native renderer was inspected at 1280×720, 1600×900, 1920×1080 and 2560×1440, including all six effect profiles, successive motion frames, unknown/discovered/stabilizing/dormant states, journal, prototype and victory screens. The full discovery sequence was captured at both 1600×900 and 2560×1440. See `tests/playtest_polish.gd` for reproduction; generated images/logs are not committed.

Remaining priorities:

- Make room door layouts and character paths match the production layout guide.
- Keep placement previews, door connections, and synergy feedback immediately readable.
- Improve the inspector, cards, and objective panels without obscuring the station art.
- Tune each doctrine pair's finite deck so power, metal, corridors, corners, and dead ends create interesting choices.
- Tune Resonance thresholds and cascade pulses through short runs; the intended delight is finding one placement that closes several useful links.
- Play full three-directive runs and tune targets, deadlines, resource rewards, reroll supply, and the 20-second base cycle.
- Expand the directive pool beyond the current doctrine-pair stage with goals that reward specific spatial patterns and orbital preparation without forcing a single solution.
- Make doctrine mastery choices more expressive after the starting-resource rank bonuses have useful playtest data.
- Replace the test walker with eventual cryo and clone population systems.

## Known Prototype Limits

- The save/meta loop is intentionally lightweight while room and progression behavior are still changing.
- Some room variants and door placements need continued visual/layout verification.
- Resonance, doctrine mastery, directives, and reroll rewards are first-pass values and need balance data from complete runs.
- Directives currently measure room count, active links, distinct active patterns, total Resonance, or balanced development of the selected doctrine pair; orbital and geometric pattern-shape goals are not implemented yet.
- Borderless mode and unusual aspect ratios still need broader hardware testing. Standard 16:9 layouts have native-render screenshot coverage.
- The two-step discovery playtest uses a controlled draft order. The full-run sweep uses seeded random decks, but its automated player does not strategically suspend rooms or represent a human discovering the game at normal speed. Human pacing data is still needed.
- Population sprites still use Major Bill's test walker rather than representing every recovered survivor.
- Motion profiles are procedural and distinguish system families, not bespoke machinery animations for every room.
- Colorblind and reduced-motion options are not implemented yet. Status text supplements color, but does not replace that accessibility work.
- Terminal patterns award Research rather than room variants. Three-cycle stabilization and terminal Research rewards still need full-run balance data.

## Working Agreements

- Keep room definitions data-driven in `scripts/room_database.gd`.
- Keep generated Godot imports, local backups, and audit exports out of version control.
- Commit art through Git LFS. Run `git lfs install` after cloning.
- Prefer small, tested gameplay changes over broad refactors while the prototype is taking shape.

## A Good Next Session

1. Complete at least one run with each doctrine pair at normal speed.
2. Record the cycle reached, directive outcome, rerolls remaining, Resonance, and the resource that caused any failure.
3. Adjust the largest repeated frustration before adding another system.
4. Add doctrine-specific directives only after every pair can reliably reach the second stage.

That keeps the project moving forward without turning BRINE into a control panel with a space station attached. 🛰️
