# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: work transitions and collection jobs

## Objective and acceptance
Owner approved continuing with reach/stow transitions and a complete collection
sequence after the cardinal action review. New sequences cover N/E/S/W. Agent
review and technical checks are recorded below; owner acceptance remains pending.

## Accepted decisions and constraints
Keep the endorsed muted steel/cyan, asymmetric equipment, .34 world units/pixel,
northwest arm revision, eight travel headings and independent status pulse.
Existing sources, travel clips, work loops and accepted v10 remain available.
This is an animation review pack; no gameplay roles, saves or runtime code changed.

## Current state
Same bundle: `assets/drone-motion-v2-2026-09-26/`. Added sixteen single-shot jobs:
12 reach → work → withdraw/stow jobs, plus four Ready → Reach → Grip → Lift →
Carry → Lower → Release → Withdraw → Complete collection sequences. Each has
a 51-frame final hover cycle while the job remains completed. Replay explicitly
resets the fixture. No automatic cargo reappearance at the pickup point.

New `build_job_sequences.py` rigs preserved arm pixels and a generated empty-claw
source; only the four gripper crops are selected from that generation. Its altered
east tool is excluded. Original body/propeller/tool artwork remains in use.
Cargo is a separate layer with same-position attach/detach events. Root offsets
show travel to the drop point and clearance after release. Welding/repair hold
the workpiece stable while the tool withdraws. Native tool-only masks exclude
the plate/bracket pixels, avoiding fragments moving with the tool.

`manifest.json` now has 48 clips, including 16 jobs; 6084 body, 5268 effect,
3636 cargo and 153 status frame references; 99 atlases. Many blank effect/cargo
frames are packaging references, not new authored art. `jobs`, `phases`,
`rootOffsets`, `cargoState`, `cargoEvents` and `holdStart` describe playback.
The preview adds Complete job / Work loop and Replay job controls.
Sources and exact built-in imagegen prompt are preserved beside the builder.

## Verification
`validate_jobs.py`: required phases, cargo ownership, identical cargo pixels and
world contact at transfers, bounded root steps, exact reach/work and work/stow
body joins outside the rotating blades, and 51-frame completed hover.
`validate_pack.py`: paths, RGBA, dimensions, body borders, 288 atlas parity samples,
source hashes and three lamp brightness curves. Latest reports are in `review/`.
Visual evidence: collection-jobs.gif, collection-storyboard.png, job-transitions.png,
tool-isolation-check.png and browser job captures. Godot was not run.
Final north/south repair mask correction is shown in `review/repair-mask-final.png`;
it removes leftover brace slivers without moving the held bracket. Job rebuilds
write PNGs/manifest atomically and retain known atlas references during regeneration.
All sixteen jobs reached their Complete phase in browser playback; sixty phase
observations are in `review/job-browser-checks.json`. Collection's final empty-claw
and deposited-ore state was inspected, with continuous completed-hover playback.
Pause held the exact carry frame and clock; resume and explicit replay returned
the sequence to Ready. Evidence: `review/job-controls-check.json`.

## Next action
Owner motion review. These jobs begin/end in a job-ready equipment pose; automatic
travel-to-job-ready blending, world target assignment, inventory changes, docking,
start/stop travel and runtime save/interrupt handling remain integration work.
Welding/repair use held demonstration pieces, not live station repair targets.
Preserve that scope when wiring the sequences into the actual drone controller.
