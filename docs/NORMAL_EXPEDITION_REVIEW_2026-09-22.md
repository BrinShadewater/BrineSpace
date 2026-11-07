# Normal-clock opening and conclusion review

Updated September22,2026. Broad goal remains unfinished.

## Objective and constraints
Exercise the current native opening with the actual dealt hand, normal room costs
and failure rules, normal process/cycle timers, comms pauses, save and conclusion.
Use a fresh isolated profile; preserve owner saves, layouts and library marks.

## Method
output/normal-expedition-2026-09-22/review.gd loads main.tscn with process-specific
meta, loop and preferences paths. No blueprint/resource injection, manual simulation
steps, free building or failure suppression. Automated choices use ordinary card
selection/grid-click methods and legal placement checks. Comms advances every four
seconds while visible; construction is considered every five seconds. The fixed
priority list is an automated strategy, not human gameplay. No native mouse/title
navigation, audio listening or input ergonomics claim.

## Results
Native exit0, no logged script errors.120wall-clock seconds after startup; reached
cycle4, survived and displayed End Expedition's report. Five completed rooms total
at conclusion. Clicked orders: Solar Array, Mining Drone Bay, Hydroponics, Corridor,
Life Support; an order click does not imply immediate completion. Starting resources
were spent normally. Bill's sampled states include idle, weld and walk.

At90seconds, _save_active_loop returned true. This run did not restore that save;
concluding a loop ends the active expedition, so save success is not resume proof.
Prior bounded restore evidence remains separate. Final sampled resources include
metal0, power3, oxygen10, food12, integrity100. Metal constrained choices but later
mining income funded Life Support; no balance change follows from this strategy.
The report showed4cycles,1crew and0banked Data/no patterns. UI screenshot inspected.

Comms pauses are retained: two of12ten-second state samples were paused; each
advance records its actual line. The opening explains construction takes time.
This sample did not expose an early completion announcement. Four second intervals
can require two advances per line (finish typing, then next); do not misclassify that
as duplicated transmissions.

Evidence: events.json, native.log, view-000/030/060/090.png and conclusion.png in
the output folder. Native active station and conclusion captures inspected. The
unmoved native cursor leaves an out-of-grid placement preview while the harness
selects cards; this is a capture/input limitation, not a newly diagnosed placement bug.

## Next action
Extend this real-clock/dealt-hand journey through disk restore and subsequent play,
with frame/state evidence for repaired actions. Audio mix and owner pacing/motion
judgment remain open, as do native Apple Silicon execution and longer expeditions.
No runtime, art or owner-layout changes were justified by this run.
