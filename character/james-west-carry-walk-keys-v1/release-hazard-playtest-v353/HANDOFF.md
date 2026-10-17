# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James survival handoffs

## Objective and acceptance
Finish James and prepare the next playable version. Survival-triggered animation
handoffs tested in the existing package; full visual closeout remains open.

## Accepted decisions and constraints
Accepted art and gameplay rules preserved; tests use scratch APPDATA. No new
artwork, production edits, executable rebuild or publication in this milestone.

## Current state
V353 fixture/UID, preparation/run/media/closeout helpers and twenty LFS raster
outputs. Exact tested package remains V351 brinespace-5024faab0e485c1a.

## Verification
### James packaged survival handoffs — October 4, 2026

V353 unchanged V351 Windows package: 2290 checks, zero failures, sixteen
cases across four directions/both gear variants and recovery/fatal outcomes.
Actual RoomFlooding.step_crew plus normal actor updates dispatched swim distress,
finite recovery after breathable air returned, and water death after air exhausted.
No direct die() or recovery-pose invocation. 1120 native 10Hz captures,
sixteen lossless animated PNG playbacks and four chronology boards. Four boards
visually reviewed; no obvious cut-off or missing-body transition in sampled poses.
Owner profile unchanged under scratch APPDATA; temporary QA override removed.
Exact package hashes in output/james-hazard-playtest-v353/validation.json.

Scope: scripted low initial reserves, fully flooded authored rooms and scheduled
drain for recovery; fixed60Hz survival/actor updates with normal packaged renderer.
Initial technically passing run obscured by expedition summary after James death;
excluded from visual acceptance. Diagnostic reruns preserved in output subfolders.
The fixture repeatedly stepped survival on the already-dead actor, unlike normal
RoomFlooding.advance, exhausting crew_count. Final fixture follows the live dead-
actor guard, retains another survivor and asserts summary_layer hidden for every
native capture. A child-panel visibility assertion was also corrected. Production
failure rules remain active; no runtime fix was needed.
This establishes survival-triggered animation handoffs, not autonomous refuge
routing, exterior excursions or full-game water propagation. Animated playbacks
supplied for review, not continuously observed by the agent. No production changes
or rebuild. Cargo quilt/North unload stance remain polish; final autonomous water/
exterior playtest and continuous selected-clip acceptance remain open.

## Next action
Complete autonomous water/exterior review and continuous game-scale acceptance.
Avoid further stationary water studies. Keep known cargo material/stance polish
explicit; do not claim it fixed or all animations accepted.
