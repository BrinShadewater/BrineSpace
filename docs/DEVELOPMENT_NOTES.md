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
- Tune the draft mix so power, corridors, corners, and dead ends create interesting choices.
- Replace the test walker with eventual cryo and clone population systems.

## Known Prototype Limits

- Build costs are disabled during testing; fail conditions are also relaxed.
- The save/meta loop is intentionally lightweight while room and progression behavior are still changing.
- Some room variants and door placements need continued visual/layout verification.
- Resolution and borderless mode need real-window testing beyond headless validation.

## Working Agreements

- Keep room definitions data-driven in `scripts/room_database.gd`.
- Keep generated Godot imports, local backups, and audit exports out of version control.
- Commit art through Git LFS. Run `git lfs install` after cloning.
- Prefer small, tested gameplay changes over broad refactors while the prototype is taking shape.

## A Good Next Session

1. Play a few short station builds at normal speed.
2. Record where placement, card readability, or pathing feels confusing.
3. Fix the most visible station interaction problem first.
4. Add one meaningful system only after the existing loop is pleasant to use.

That keeps the project moving forward without turning BRINE into a control panel with a space station attached. 🛰️
