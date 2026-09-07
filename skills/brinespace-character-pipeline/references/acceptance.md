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
