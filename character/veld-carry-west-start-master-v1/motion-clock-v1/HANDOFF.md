# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld cargo simulation clocks

## Objective and acceptance
Full master-matched Veld animation set, followed by cross-library polish. Active/incomplete.

## Accepted decisions and constraints
Whole original staged master sources and unchanged helmets/grade, real room route, normal update priorities, scratch saves.

## Current state
New staged direct VeldNpc subclass, actual-route test+UID/runner, native-source boards and review evidence. No normal adoption.

## Verification
## Veld cargo transitions use simulation clocks without skipping normal updates — October 2, 2026

Staged character/veld-carry-west-start-master-v1/motion-clock-v1 extends VeldNpc
 directly, replacing the older authoring arrival early-return. East-West and
West-North planted turns, West firststep and phase2 stopping use simulation delta.
Grid action_elapsed selects the exact whole master clip; no frame() side-effect
sampling, new raster, proportion/helmet/grade or normal selection changes.
A consumed real endpoint remains through final stop/arrival hold so inherited
update continues needs, service and safety priority. Start/stop clocks freeze
on blocked attempted travel; full traffic behavior remains to be proven.

Actual main/default workshop fixture5763checks0/104.22s,237targeted inputs unchanged;
all2931owner non-log files unchanged under scratchAPPDATA. Both gears complete
master route, source joins and independent-case departure. Display clock6x,
turn duration follows60Hz simulation; zero delta preserves turn/foot; hunger
advances throughout arrival. Reconstructed actual endpoint service-loss cancels
stale turn through normal controller; gear/medium/death invalidate private pose.
Two26pair native/source boards reviewed,52pairs. These guards are scoped tests,
not full fire/flood/traffic/naturalchooser/checkpoint/freshContinue acceptance.

No normal adoption; new private motion has no checkpoint serialization yet.
Next: guarded checkpoint restoration and real interruption/traffic fixtures,
generic phases/cardinalstarts, North fullidle/case lifetime/South masters,
furniture/swimming and full cross-library consistency/polish. Full goal active.
Lesson: retain normal update priorities during finite visual holds; bind clocks
 to simulation progress and use action_elapsed for authored turns. A passing
paused/needs/service probe does not certify every priority or lifecycle path.
Handoff: character/veld-carry-west-start-master-v1/motion-clock-v1/HANDOFF.md.

## Next action
Checkpoint serialization/guarded restoration; real fire/flood/traffic and interruption paths; other starts/stops and remaining full visual library.
