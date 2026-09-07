# Character pipelines and agent skills: research for BrineSpace

**Research date:** September 6, 2026  
**Audience:** Alex and contributors working on BrineSpace  
**Decision:** How to organize a reusable character creation workflow beside the existing room pipeline.  
**Scope:** Agent skill design, sprite and animation production, and the handoff into Godot 4.6. This is a research recommendation, not an implemented skill or a new tool purchase proposal.

## Recommendation

Create a focused `brinespace-character-pipeline` skill with three modes: character concept, animation pack, and integrated NPC. Keep the room pipeline as a sibling. Share the visual bible and project conventions, and reuse the existing sprite tooling through explicit references. Put detailed animation and integration procedures in references that load only when needed.

This fits the Agent Skills guidance to organize around coherent tasks: overly broad skills become difficult to select, while excessively narrow skills add loading overhead and conflicting instructions. The same guidance favors knowledge extracted from actual work and corrections. Bill and Veld therefore provide better starting material than a generic character-production checklist. [Agent Skills: best practices](https://agentskills.io/skill-creation/best-practices)

The research also changes the emphasis of the proposed workflow: its core should be a stable asset contract, cheap revision, and evidence of acceptance. Image generation is one authoring method within that workflow. It should not define every future character's production method.

## What others do, and what transfers

### 1. Package expertise separately from reusable mechanics

OpenAI documents skills as instruction bundles with optional scripts, references, and assets. Selection begins with metadata, with the full instructions loaded when a skill applies. It specifically recommends concise descriptions with clear scope. This supports a small entry point and explicit mode-specific references. [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)

**BrineSpace application:** the character skill owns decisions such as which actions are required, what distinguishes the character, and what constitutes a finished NPC. The sprite builder owns reproducible transformations. The visual bible owns department appearance. Avoid copying those responsibilities into several independently maintained documents.

A skill reference is not an automatic package dependency. Its instructions should locate the active checkout and explicitly identify required files and available tools. If the generic sprite skill is unavailable, use documented project helpers for packaging; report missing generation capability rather than assuming it exists.

### 2. Treat metadata as part of the animation asset

Aseprite can export both a texture atlas and JSON metadata, including animation tags and slices; its CLI supports batch processing, frame selection, and export configuration. These facilities make named animations and registration data explicit instead of leaving the engine to infer them from filenames. [Aseprite: command-line interface](https://www.aseprite.org/docs/cli/)

**BrineSpace application:** one character contract should specify state IDs, directions, frame order, durations, loops, foot anchor, and action meaning. Generate previews and runtime exports from the same data. Do not maintain a separate hand-edited timing list for each consumer.

Our current Veld manifest already records much of this, including the distinction between the controller state `repair` and its character-specific meaning, sample inspection. Her pack has 72 frames, 92 × 92 canvases, pivot (46, 86), and four-direction idle/walk coverage. These are local facts and compatibility defaults, not industry standards. [Veld pack documentation](../character/dr-veld-v1/README.md) · [Current manifest](../character/dr-veld-v1/final/manifest.json)

### 3. Preserve sources and make exports repeatable

Spine recommends automated exports and keeping project sources safe so assets can be re-exported when its runtime version changes. It also supports saved export settings. The particular version-matching requirement is Spine-specific; the transferable practice is preserving editable sources and the configuration that transforms them into runtime assets. [Spine: Export](https://us.esotericsoftware.com/spine-export/)

**BrineSpace application:** retain generated source rows, exact prompts and references, accepted revisions, build settings, derived frames, and validation evidence. Record tool versions and source hashes. Rebuilding an accepted pack should use local sources without calling an image service.

This separates two different claims: generation is variable; processing accepted source files can be tested for reproducibility. Reusing the same prompt does not guarantee the same sprite. Nor do batch-export capabilities alone prove byte-identical output across tool versions.

### 4. Separate candidates from production-ready assets

AYON describes an explicit publishing sequence: collect data, validate it, extract to staging, then integrate into the production location. Product types carry different validation expectations. Here, publishing means an internal production handoff, not public release. [AYON: About the pipeline](https://help.ayon.app/en/articles/7070980-about-ayon-pipeline)

**BrineSpace application:** use a lightweight manifest and candidate output directory instead of installing a studio asset server. A generated sheet is a candidate; a packaged sheet has passed structural checks; an integrated character has passed relevant runtime checks. Keep those statuses distinct.

Our room skill already distinguishes generated, cleaned, geometry-validated, integrated, and verified assets. Preserve that principle while using character-specific checks. An automatic validator must not silently promote artistic acceptance, and existing user approval should not be replaced with repeated permission prompts. [Existing room workflow](../skills/brinespace-room-pipeline/SKILL.md)

### 5. Optimize the workflow for retakes

In his January 25, 2018 first-person account, Motion Twin artist Thomas Vasseur describes a Dead Cells workflow using a 2D model sheet, simple 3D characters and rigs, and rendered PNG animation frames. He emphasizes revising poses and timing as gameplay changes. He also describes establishing convincing key poses and timing before adding more frames. This is a historical production case, not an AI workflow or a universal animation prescription. [Thomas Vasseur: Dead Cells art pipeline](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)

**BrineSpace application:** prove one idle, one walk, and the distinctive role action before producing the whole matrix. Measure how expensive a requested change is after packaging. More frames should solve an observed motion problem, rather than serve as a default definition of quality.

Keep generated sprite rows as the current default. If recurring pose drift or equipment changes make revisions costly, compare a small hand-authored or rig-rendered pilot against that default. Do not migrate the whole project based on another game's success.

### 6. Evaluate characters at their actual display size

Riot's character-art education emphasizes proportion, likeness, and readability even in a tiny game model, and recommends rapid proportion prototypes. Its material concerns 3D character art; the relevant principle is that the final viewing conditions should shape authoring decisions. [Riot Games: Character Art](https://www.riotgames.com/en/artedu/character-art)

**BrineSpace application:** review new crew beside Bill and Veld at the same scale inside a room. Check silhouette, department distinction, face and equipment readability, foot placement, and occlusion. A large concept sheet can pass while the character becomes indistinct at station zoom.

## Godot-specific implications

Godot 4.6 `SpriteFrames` stores animation speed, loop settings, and relative frame durations. Absolute frame duration depends on relative duration, animation FPS, and playing speed. A converter must preserve actual timing, rather than copying millisecond values into a field with different units. [Godot 4.6: SpriteFrames](https://docs.godotengine.org/en/4.6/classes/class_spriteframes.html)

Godot also separates authored animations in `AnimationPlayer` from advanced playback and transition control in `AnimationTree`. This supports distinguishing asset data from playback state, but it does not require replacing BrineSpace's existing renderer or sprite player. [Godot 4.6: AnimationTree](https://docs.godotengine.org/en/4.6/tutorials/animation/animation_tree.html)

Texture appearance depends on the loading and rendering path. Godot documents alpha-border processing for bilinear filtering and advises enabling 2D mipmaps when the project visibly benefits. Avoid universal texture-setting rules detached from station zoom and the actual loader. [Godot 4.6: Importing images](https://docs.godotengine.org/en/4.6/tutorials/assets_pipeline/importing_images.html)

For integrated NPC work, the project-specific reference should cover independent playback clocks, distance-driven locomotion, action transitions, pause and speed changes, feet-based depth sorting, door approaches, collision footprints, crew avoidance, and save restoration. These come from our implementation and its known limits. Existing tests are useful regression fixtures; this research did not rerun them or certify new assets. [Veld integration and verification](../character/dr-veld-v1/README.md) · [Current development scope](DEVELOPMENT_NOTES.md)

## Proposed skill structure

This is a proposed layout. No folders below were created as part of this research.

```text
skills/
  brinespace-room-pipeline/          existing room workflow
  brinespace-character-pipeline/
    SKILL.md                       scope, modes, essential checks
    references/
      character-direction.md       identity and reference selection
      animation-contract.md        coverage, registration, timing, packaging
      godot-integration.md         runtime consumers and NPC verification
      acceptance.md                visual checks and evidence requirements
    evals/
      cases.json                   representative task and boundary cases
```

Keep the visual bible in its existing project location. Add a shared production reference only for rules that are truly common and otherwise duplicated. Keep reusable code in the project tools or existing sprite tooling; add a skill script only when it has a concrete function. No new umbrella skill is necessary for two workflows.

The repository should be the authoritative source for the project skill. If an installed copy is needed, use a deliberate sync/check process. Host discovery paths are version-dependent: current OpenAI documentation describes repository `.agents/skills` and warns that duplicate skill names are not merged. Preserve our working installation convention until its actual discovery behavior is verified; do not relocate existing skills merely to match a documentation example. [OpenAI: local skill loading](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)

### Modes and completion evidence

| Requested work | Required result | Completion evidence |
|---|---|---|
| Concept | Distinct character in the approved visual family | Reference identity and same-scale comparison |
| Animation pack | Contract-complete frames and exports | Manifest checks, contact sheet, motion and transition review |
| Integrated NPC | Pack connected to authorized behavior | Native room/corridor review and relevant gameplay regressions |

Select the mode from the user's request and existing context. A concept task can finish without implementing needs or saves. Animation cleanup can finish without inventing additional actions. A full NPC request must include the runtime checks relevant to its behavior.

### Proposed production stages

1. **Define:** identity, role, camera, technical profile, required states, and scope.
2. **Pilot:** establish the character at gameplay scale and prove representative motion.
3. **Produce:** complete the required state/direction matrix while preserving sources.
4. **Package:** apply deterministic cleanup, registration, timing, and export rules.
5. **Review:** check structural validity and visual quality separately.
6. **Integrate, when requested:** connect playback and behavior, then verify in Godot.

At every stage, retain accepted work and revise failed portions where practical. Track rejected, missing, and intentionally omitted states separately. If the contract changes, identify affected consumers and evidence before calling the new revision compatible. These are proposed BrineSpace rules informed by the sources above.

## Test the skill as well as the assets

Agent Skills recommends comparing realistic tasks with and without a skill, or against its previous version, in fresh contexts. It distinguishes mechanical assertions from human review and suggests recording time and token costs. [Agent Skills: Evaluating output quality](https://agentskills.io/skill-creation/evaluating-skills)

Its description guidance separately tests activation with positive prompts and near-miss negative prompts. Repeated trials expose variable selection behavior. We should use that distinction without automatically adopting its full suggested benchmark size for this small project. [Agent Skills: Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)

Start with three output cases:

- **New crew concept:** preserve the shared suit family while giving the officer a distinct silhouette and department identity. No unsolicited gameplay changes.
- **Repair Veld's walk:** correct a supplied defect, preserve unrelated accepted frames, rebuild reproducibly, and produce motion evidence.
- **Integrate a prepared NPC pack:** reuse existing navigation and playback interfaces, verify relevant transitions and persistence, and preserve prototype economy rules.

Add selection cases such as “animate the research room machinery” for the room skill and “make an unrelated game's sprite sheet” for the generic sprite workflow. Also test a request spanning both workflows, such as a new officer interacting with newly added laboratory equipment: both may legitimately apply.

Measure structural failures, missing required states, unintended edits, visual defects, manual corrections, generation retries, and time to an accepted result. Track selection and output quality separately. A file-format check cannot establish likeness, and an attractive preview cannot establish collision safety. These cases and measures are proposals; no new skill benchmark has been run.

## What to adopt now and what to defer

**Adopt now:** the sibling skill, three scope modes, explicit references to existing tools, one animation contract, a representative-motion pilot, source preservation, separate technical and visual acceptance, and a small evaluation set.

**Defer:** a studio asset server, an umbrella router, migration to skeletal or 3D authoring, and a generalized crowd simulation. None is necessary to capture the lessons from Bill and Veld. Consider larger tooling only when repeated failures or revision costs justify it.

The existing room workflow is already strong on provenance and evidence. The biggest opportunity is to make character-specific knowledge repeatable while keeping the amount of required procedure proportional to the requested work.

## Confidence and research limits

Confidence is high that focused skills, explicit asset metadata, retained sources, and staged validation are documented practices. Confidence is moderate that this exact proposed structure is the best fit for BrineSpace: that is an architectural judgment requiring real-task evaluation.

The sources comprise current first-party technical documentation, official game-art education, and a historical artist-authored production account. They do not establish industry-wide adoption rates or prove that generated sprite rows outperform hand-drawn or rig-rendered animation. No reliable comparative production benchmark for our exact AI-assisted Godot workflow was established.

Godot claims use version 4.6 documentation. Other documentation is living and had no visible publication date in the reviewed passages; it was accessed September 6, 2026. The Dead Cells article is dated January 25, 2018. Blender Studio material was explored but direct access was incomplete, so no recommendation depends on its inaccessible details. No paid software was installed and no character, game code, or existing skill was changed.
