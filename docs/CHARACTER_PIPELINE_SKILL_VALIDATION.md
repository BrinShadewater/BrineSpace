# Character pipeline skill validation

Date: September 6, 2026. Scope: create and install the character workflow; no
character generation, game-code changes, or engine regression run in this task.

## Delivered

The maintained source is `skills/brinespace-character-pipeline/`. Its seven files
contain a 77-line entry point, UI metadata, four focused references, and evaluation
cases. An identical copy is installed in the user's Codex skills directory.
Automatic invocation remains enabled by default. The room skill has a narrow
cross-reference in both its project and installed copies; unrelated differences
between those room copies were preserved.

The skill supports concept, animation-pack/repair, and integrated-NPC scopes.
It reuses the shared visual bible and existing builders rather than duplicating
art standards or introducing a new renderer. Its design rationale is documented
in [the research report](CHARACTER_PIPELINE_RESEARCH.md).

## Completed checks

- Skill-creator `quick_validate.py`: project and installed character skills pass.
- Project and installed room skills still pass the skill validator.
- All relative Markdown links in the character skill resolve.
- All raw input paths in the three output evaluation cases exist.
- Evaluation JSON parses and contains three output cases and six selection cases.
- All seven installed character files match source hashes.
- The referenced generic sprite validator runs against Veld's existing manifest
  with zero errors and zero warnings; it does not certify motion or visual quality.
- Whitespace checks pass. Path inspection caught and corrected the layered-room
  renderer location to `rooms/whole-room/nursery_whole_view.gd`.

## Behavioral evidence and limits

An independent read-only trial used the skill for a request to inspect Veld's east
walk and propose a repair without editing. It selected animation-repair scope,
consulted the relevant references and raw project metadata/code, and made no edits
or generation calls. It distinguished distance-driven playback from preview timing
and refused to infer a visual defect from metadata alone.

The trial identified a concrete packaging hazard: Veld's builder recomputes the
whole pack palette, and `--partial` does not select one clip. The animation-contract
reference now documents this hazard and calls for checking unrelated frame pixels.
The updated reference was synchronized to the installed copy and revalidated.

The stored evaluation cases remain marked `specified_not_executed`: this planning
trial is not the complete output benchmark and does not establish automatic skill
selection. It provides evidence of scope discipline and useful code inspection,
not proof that an animation was fixed.

No with/without-skill quality comparison, generation benchmark, or live discovery
test has been performed. Existing Bill/Veld runtime tests are documented as tools
for future affected work, not rerun or claimed as new skill-validation evidence.

## September 9 companion closeout update

Added `references/companion-motion.md`, routed it from the maintained entrypoint,
and added inventory-aware handoff guidance. Lessons come from actual source-facing,
gutter, robot footprint and camera-focus failures corrected during this session.
Added a project active-asset registry and read-only binding audit; it reports nine
animation packs and eight portraits with zero errors. No unrelated art was rebuilt.

Maintained and installed skills both pass `quick_validate.py`; changed files match
byte-for-byte and their reference links resolve. The validator's missing PyYAML
dependency was installed only into the closeout output directory. Evidence:
`output/character-closeout/skill-validation.json` and `bindings.json`.
This was structural validation and a targeted lesson update, not a new independent
behavioral or comparative skill-effectiveness evaluation.

## September 29 human crew consistency closeout

Added crew-consistency.md from observed owner revisions: material/alpha spill,
idle-led identity, complete gait cycles, local breathing, resampling limits,
shared helmet/collar fit, action interior-frame continuity and parallel actor ownership.
Routed both maintained and installed character skills; preserved their pre-existing
engineering-note/formatting differences rather than replacing the whole installed skill.
Updated direct-video current-selection guidance and added underwater/handoff routing.
Three new regression cases are specified_not_executed in intent (the JSON field is
not_executed_fresh_context); no independent agent behavior benchmark was run.

Both quick_validate.py runs passed. New closeout/reference Markdown links and both
skill routing sets resolve; four updated mirrored resources match byte-for-byte.
Evaluation JSON parses with unique case IDs. Selected/staged inventory records
16 manifests and 3,106 frame references, with manifest and ordered per-state
content hashes. git diff --check passed for the changed tracked documentation/skill
scope (only line-ending notices). No art regeneration, provider spend, Godot test,
release export or owner-save mutation occurred for this documentation closeout.

See CREW_ANIMATION_SESSION_CLOSEOUT_2026-09-29.md and the three actor continuation
handoffs. Existing Bill 121/232 checks are previous candidate evidence, not new skill
behavior acceptance. Bill east idle-led-v3 remains staged and visually unaccepted.

## September 30 Marsh master-repair closeout

Added master-repair.md and routing to maintained/installed character skills:
master versus idle authority, frozen ordered selection, connected body/tool
sources, reflowed-sheet extraction/holds, shared poses and material grades,
protected white android fluid, advancing capture coverage and evidence limits.
Preserved existing differences between skill copies; only the new guidance and
three new regression cases were synchronized.

Both quick_validate.py runs passed. New reference copies match byte-for-byte;
three new cases match with unique IDs. Eight new Markdown links resolve. Closeout
snapshot verifies all 51 ordered body manifests and the selected runtime contract
(204 states / 1,058 slots). Scoped git diff --check passed with line-ending notices.
Cases remain not_executed_fresh_context; no independent behavior benchmark,
generation, Godot run, export or profile mutation was performed for this closeout.
See MARSH_SESSION_CLOSEOUT_2026-09-30.md for installed versus accepted scope.
