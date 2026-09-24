# Acceptance and workflow evaluation

## Select evidence for the requested result

| Scope | Mechanical evidence | Visual evidence |
|---|---|---|
| Concept | Source saved; reference/provenance identified | Identity, silhouette, department, same-scale room context |
| Animation pack/repair | Required coverage, frame paths, dimensions, alpha, pivot, timing, exports | All changed clips in motion; endpoints; full-size and gameplay-scale appearance |
| Integrated NPC | Relevant loading, behavior, navigation, pause, save tests | Native room/prop/door occlusion and applicable crew interaction |

Use actual pixel alpha inspection; a painted checkerboard is not transparency.
Check unintended opaque backgrounds, fringe, clipped limbs, identity drift,
equipment swapping sides, registration jitter, foot sliding, and transition jumps.
Palette size and frame counts alone cannot settle those judgments. A still contact
sheet does not establish temporal smoothness; disclose when motion review is missing.

Report generated, packaged, integrated, and verified status independently. Attach
evidence paths to the revision being assessed. Record visual reviewer and observed
limitations; do not call agent visual inspection owner approval. Preserve earlier
source hashes and rejected candidates when revising, and invalidate relevant prior
evidence after a source or contract change.

Completion is proportional to scope. Concept work does not require a Godot test;
pack work does require animation review; runtime work requires the affected native
and regression checks. Preserve existing user authorization and continue reversible
corrections without asking for approval at every stage.

## Evaluate the skill when changing its behavior

Use `evals/cases.json` relative to the skill root. These are representative prompts
and observable outcomes, not claims of completed tests. Inspect the current raw
fixtures before each evaluation; copy mutable inputs to an isolated workspace.

Compare a new skill version against the previous workflow in fresh contexts with
the same inputs. Keep model and available tools comparable. Do not supply expected
answers to the executing agent. Keep costly generation or runtime modifications
within the authorized evaluation scope. A read-only planning trial can check scope
and decisions, but cannot establish animation quality or runtime correctness.

Evaluate skill selection separately from output quality: include near misses and
mixed room/character requests. Record actual loaded skills, unrequested work,
mechanical failures, visual defects, corrections, and time/retries where measured.
Repeat a case when variable behavior affects the conclusion; do not claim a pass
rate from a single trial or historical Bill/Veld results.

Use narrowly targeted corrections from observed failures. Retain the baseline and
evaluation results in a project validation record, outside production asset paths.
The rationale and external sources are in `docs/CHARACTER_PIPELINE_RESEARCH.md` in
the checkout. No new generation service, umbrella skill, or studio asset server
is required to evaluate this workflow.


For autonomous station captures, log advancing simulation and pause state. Queued
crew dialogue can pause after setup; dismiss it through normal UI methods rather
than forcing actor needs or disabling resource rules. Confirm the actor and work
area are inside the captured viewport and clear unrelated build previews before
calling a sequence visual evidence. A completed offscreen action is behavior
evidence only. Camera-follow fixtures are not startup-camera acceptance.

For native NPC crops, use the consumer's screen-position helper rather than raw
room-space feet; the grid scale changes the mapping. Record a capture index on each
sample only after saving its image, and record skipped crops explicitly. Missing
crops otherwise break exact phase-to-image alignment. Autonomous observation does
not guarantee work-state coverage; report the states actually selected.

With canvas_items stretching, also apply the viewport final transform and the
grid canvas global transform before cropping its captured texture. A 1920x1080
logical viewport can render a 1600x900 image: the untransformed helper position
then produces an offset crop. Verify one full-screen/crop pair before collecting
the sequence; preserve rejected captures separately from accepted visual evidence.

For walk-to-work review, retain a short rolling approach buffer before the first
kneel; starting capture at the action omits the gait handoff. Record sample rates
when combining sparse approach and per-frame action logs. Sample renderer phase
after frame_post_draw if asserting same-frame playback; controller position and
pre-draw playback metadata cannot establish anatomical foot lock.


Directional capture gate: one nominal facing frame can precede travel in a different
direction. Require sustained target-direction travel and enough target samples in
the completion predicate. For actor-follow reviews, center continuously on the foot
rather than jumping between room centers; validate crop containment and retain full
station context frames. Do not label a clipped or wrong-direction run as coverage.
GIF timing is quantized to centiseconds; record conversion from simulation cadence.

Distance-driven phase and correct stance anchors at pose boundaries do not prove
foot planting between those boundaries. Measure root travel while the same texture
is held, using stride * duration / cycle / source-pixel-scale-in-cells. Bill's
six-pose side walk permits17.38source pixels of within-hold movement. A denser
candidate must preserve key poses/timing and also pass anatomical contact, loop,
contour and native-scale visual review; reducing the hold metric alone is not
acceptance. Distinguish room-local384-unit coordinates from scaled station units.

If the owner reports disconnected joints, compare original whole-limb poses against
the current repair and unaffected cast before adding inbetweens. Numerical foot
slide improvements cannot accept broken ankle silhouettes. Preserving current key
poses is not a virtue when those poses contain the reported defect. Restoring a boot
by its rectangular bounds can also restore neighboring old leg pixels; inspect the
composite, not only the boot or replacement limb in isolation.

Bill's dry frame tables can retain cached arrays after a candidate is appended to
CrewSpritePlayer. Candidate station fixtures must update the grid's dry tables too
and assert _get_human_frame_source selects candidate textures during the actual
action. Loader equality alone missed a mixed review showing old bare/new equipped
art. Keep failed capture evidence and label the corrected rerun explicitly.


At action departure, distinguish queued navigation from actual movement. Selecting
walk before move() resolves travel facing can flash one stationary pose in the old
work direction. Log adjacent state, foot and facing samples; verify route selection
and actual movement separately. Autonomous before/after captures may choose different
work targets: disclose that instead of calling them matched motion or pixel parity.
Keep root stability separate from visible stand-to-idle body proportions.


Direction-specific station captures must require nonzero captured samples in the
requested direction and changed states. An unrelated stand/departure is not a pass.
Wait for wake/transient states to finish before assigning a controlled service target;
report explicit target selection separately from unforced autonomous goal choice.
Preserve failed fixture setup logs separately from the final acceptance record.


A placed room is not necessarily an available service. Before assigning a controlled
maintenance review target, wait for the actor's normal service_available() condition;
otherwise normal construction/power gating may immediately cancel it. Require the
requested direction AND selected point when claiming that target was exercised.
Trace goal/state/stage, service availability and route before editing the fixture.
Do not disable resource failures or mutate game rules to make a capture succeed.

For repeated actor/rotation action captures, include actor, rotation and action in
both image and trace filenames; otherwise later passes overwrite earlier evidence.
Review equip and remove alongside the selected standing endpoints: stable feet,
correct event timing and completed service do not establish matching suit, face or
equipment identity across separately authored clips.

When staging precomposed equipment actions, trace the renderer's selected body or
equipment collection for each state. Replacing only bare rows can preview a new
equip action beside an unchanged equipped removal action. Verify both routes
before treating the candidate's paired motion as reviewed.

When an accepted supplement extends an older frozen inventory, validate its own
explicit state, timing, canvas, depth and source-pixel contract as well. Do not
silently exclude it from full-revision validation or rewrite the old source ledger.

Inspect empty carried or raised helmets for accidentally generated duplicate faces.
Preserve the raw source and record cleanup masks before extraction. Check the result
at source and game scale, including the transition to an actually worn helmet.

Resolve moved authoring inputs through their explicit archived locations and retain
the frozen original hashes. Avoid direct truncating PNG writes during rebuilds;
use the maintained atomic write-if-changed helper and compare unrelated runtime
files after the completed build. A failed partial build is not an accepted revision.
