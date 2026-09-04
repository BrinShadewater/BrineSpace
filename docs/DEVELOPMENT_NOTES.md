# BrineSpace Development Notes

## Prototype North Star

BrineSpace should feel like restoring a silent machine in orbit: build a little, watch the systems find their rhythm, notice a strange connection, and decide whether to risk one more room before the next reboot. The interesting pressure should come from the station's interlocking needs, not from click speed.

> **BRINE // DIAGNOSTIC**
>
> *"I have mapped thirty-seven ways to run out of oxygen. I recommend none of them."* ⚠️

## Current Focus

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
- Resolution and borderless mode need real-window testing beyond headless validation.

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
