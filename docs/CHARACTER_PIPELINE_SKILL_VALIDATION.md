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
