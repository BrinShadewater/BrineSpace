# Continued play and paid crew recovery

Updated: September 23, 2026. Project: BrineSpace.

## Objective and acceptance

Continue the normal expedition on current source, verify the Continue dialogue
repair during play, and exercise a real paid crew recovery. The observed Veld exit
identifies a remaining pod-lid handoff defect; that art transition is not fixed.

## Accepted decisions and constraints

Use normal costs, failures, resource production and simulation timers, isolated
profiles and disposable checkpoint copies. No supplied resources/rooms, manual
simulation steps, owner-layout changes or Higgsfield. Automated legal actions are
not human play or input-ergonomics acceptance. Preserve existing test packages.

## Current state

- Current source continuation from the preceding frozen cycle3 checkpoint runs
  120 seconds, reaches cycle9/seven rooms and saves successfully. Bill's opening
  wake line does not repeat. 355 cropped samples cover walking and north work.
- A second 120-second native run starts from that saved station and stops new
  building while accumulating the actual eight-Metal repair cost. The existing
  room layout connects the ward at (19,18), so the normal repair command can run.
  Payment is recorded as Metal8 ->0, with active/paid flags true.
- Hull repair, power-dependent thaw and Veld release complete without changing
  rules. The run ends at cycle14/eight rooms/two crew. Veld's wake line plays;
  Bill's already-delivered starter line stays suppressed. Normal power warnings
  and discovery messages are retained.
- Frozen next-review save: `output/continued-play-2026-09-23/two-crew-frozen.loop`.
  Work only on a copy when saving or concluding a future review.

## Verification and visual finding

- Both native source runs exit0 with zero captured engine/script errors; these are
  editor/native runs, not fresh executable-release acceptance. Costs/failures remain
  enabled. No performance, listening or native Mac claim.
- Checkpoint reader accepts the primary save, cycle14/two crew/Veld active, with
  `awake/veld` seen and `awake/bill` absent. Existing packages still predate the
  source Continue-dialogue fix; no rebuild this pass.
- Ninety correctly mapped recovery crops show Veld's thaw, emergence and departure.
  Agent inspected the eight-pose contact sheet and final room view. Exit poses use
  the final1.2seconds of the7second ward thaw. This is not blanket temporal or
  anatomical approval. `veld-thaw.gif` preserves sampled intervals and adds a
  600ms final hold; its looping boundary is a presentation edit.
- **Remaining defect:** the open pod becomes the closed empty-pod image immediately
  at recovery. `scripts/architect_cryo_art.gd` switches from occupied wake frame5
  to `empty_texture` in its recovered branch; there is no matching open-empty
  handoff or closing interval. Observed in Veld's normal recovery, independently
  of the already-corrected exit-pose timer. The renderer is shared by human pods.
  Do not stretch the entire thaw or change crew release timing to conceal it.
- Evidence: `output/continued-play-2026-09-23/`, including both `native.log` files,
  `recovery/events.json`, `recovery/motion.json`, `checkpoint-check.log`,
  `veld-thaw-contact.png`, `veld-thaw.gif` and the frozen save.

## Next action

Repair the open-to-empty pod handoff using matching pod art and a pause/save-safe
presentation sequence. Keep normal recovery timing, source character identity,
physical release position and owner layouts unchanged. Then use the preserved
two-crew expedition for further natural activity and room-interaction review.
