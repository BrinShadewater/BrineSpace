# Project handoff

Updated: 2026-09-28 · Project: BrineSpace · Task: four large rooms and Moonbay missions

## Objective and acceptance

Deliver four rare 2×2 rooms with aligned perimeter doors and fixed large props; one later card per run, first four in the accepted order; ocean-facing Moonbay and Tidal Power Plant; assigned crew mini-sub missions for survey, recovery, and deep access.

## Accepted decisions and constraints

Hydroponics Farm is green, Storage Depot and Tidal Power Plant yellow, Moonbay cyan. All cost more than ordinary rooms. Moonbay's dry hangar uses a sealed floodable launch chamber. The player assigns crew and watches an automated mission. Preserve normal paid construction and the owner's save and Studio layouts.

## Current state

Branch `codex/large-rooms` in the managed `large-rooms` worktree. Foundation commits `091da8b9`, `fde7efc0`, `cd219f2a`, `684f1872`, and `a60ff8aa` add footprint/ports, atomic placement, exact connections and save, room art, and rare draft scheduling. Task 6 also fixes crew construction approaches for 2×2 perimeter ports. Four card PNGs are tracked through Git LFS. Native captures are under `output/large-room-review/` in this worktree. Moonbay missions are not yet implemented.

## Verification

- Focused `large-rooms` suite: 5/5 pass before the paid construction probe; the new paid probe passes with existing crew construction and Save/Continue tests (3/3).
- Existing construction, metal trickle, owner regressions, power, reliability, room cards, fire, flooding, and Save/Continue: 9/9 pass under scratch `APPDATA`.
- Native view/card renders cover all four rooms and four rotations. Native station captures show each room beside normal rooms. Native paid Farm construction passes, with `output/large-room-review/station/paid-hydroponics_farm.png` captured. Farm output and inputs appear in the live resource strip.
- The real owner folder's 2,679 non-log files match their before hashes. One task-completion wrapper was accidentally run without scratch `APPDATA`; Godot rotated five owner `logs` files. The progress save, checkpoint, profile, and Studio data were unchanged. All subsequent Godot runs explicitly set scratch `APPDATA`.
- Native runs emit missing-resource messages for several existing `brineui` and icon atlases in this isolated checkout, although the large-room views and paid construction render. Resolve import/cache state before treating those unrelated UI assets as a release check.

## Next action

Complete the companion [Moonbay mission plan](superpowers/plans/2026-09-28-moonbay-missions.md): state machine, crew assignment, launch visuals, persistence, paid native review, then update this handoff and current status with final results. Run the complete `large-rooms` suite including the paid probe, confirm the owner non-log fingerprint, and review the full branch before asking for merge or publication.
