# UI, characters and build session closeout

Updated: 2026-09-09 - BrineSpace

## Objective and acceptance
Close this session with accepted decisions, reusable workflow/asset lessons and a
current bible entry. No new generation, gameplay work, build, publication or cleanup.

## Accepted decisions and constraints
Prominent readable portraits matching peers; BRINE identity follows the supplied
reference, with softer shadows, restrained darkening and smaller animated bubbles.
Marsh is a blond humanoid android in a white suit with a metal head plate, recovered
through a powered white-fluid charging pod; charging replaces breathing as his
tradeoff. Four evenly spaced top badges; taller inspector; larger station controls;
TIME / CYCLE counter; no sidebar tutorial or visible Locate Room & Connections action.
Companion portraits match architect selector size. First-time character discoveries
join the loop recap and survive Continue. Preserve all later shared-checkout work.

## Current state
- Bible: added a current character/sidebar section and marked the old BRINE V8
  selection as historical. Current consumers govern selection, not old filenames.
- Skills: updated character comms-portraits and godot-integration, room navigation-ui
  and production, plus two character skill selection scenarios. Synced these five
  files to installed copies; unrelated differences remain untouched.
- Workflow: docs/RELEASE_WORKFLOW.md covers manifest-driven packaging, raw assets,
  runtime dependencies in tools/, safe loaders and release-stripped assertions,
  actual-release fixtures, camera initialization and evidence/retention. AGENTS.md
  routes future build work there. Reuse existing export/reliability tools; no new
  overlapping exporter or generator.
- Build history: this session produced builds/BrineSpace-2026-09-09 and fixed an
  export dependency plus unintended startup zoom. Later fixed/optimized releases
  supersede it. WINDOWS_BUILD_2026-09-09.md now explicitly records that limitation.
  Latest recorded optimized release is brinespace-7ffe90b527116109; its frozen scope
  predates subsequent animation/water work. Do not claim the current checkout has
  all been tested together in that executable.
- Other work: current code selects newer BRINE/lighting/background portraits and
  includes later room/companion changes. Their own handoffs govern acceptance;
  this closeout does not approve or revert them.

## Verification
Documentation-only closeout: structural skill validation, changed mirror byte
comparison, JSON parsing and local-link checks. Added scenarios are evaluation
inputs, not a newly executed behavioral trial. No gameplay/asset batches rerun.
Prior native/UI, recovery, Save/Continue and package checks remain scoped to their
dated reports; later actual-release evidence is in the Teegly/reliability handoffs.
Mixed-encoding bible/current-status files were edited as bytes to preserve existing
content rather than silently replacing undecodable characters.

## Next action
This session is closed. On renewed work, begin with CURRENT_STATUS.md and current
runtime bindings. Review pending newer artwork/motion with the owner and make a
fresh frozen release only when requested. Preserve current packages, sources,
prompts, rejection records and evidence; no cleanup or archival deletion performed.
