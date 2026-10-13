# Project handoff

Updated: 2026-09-29 · Project: BrineSpace · Task: human crew animation session closeout

## Objective and acceptance
Owner requested consolidating skills, workflow, bible and lessons, then ending this
session. They will open separate Veld, James and Bill sessions for remaining work.
This closes the session, not the unfinished animation feature. No new generation,
installation or gameplay change was made during documentation closeout.

## Accepted decisions and constraints
Humans use dark matte graphite cloth, muted silver hardware and linear sampling.
Bill: dark brown hair/sideburns/restrained beard, warm skin, burgundy patches.
Veld: balanced head, warm light skin, contained brown bun, blue patches.
James Branforth: same neutral suit family, distinct goggles/moustache, muted yellow
engineering patches. Shared helmets are graphite/silver with sealed glass and a
white lamp; yellow shell panels, facial glare and colour spill are rejected.
Marsh remains the facial-stylization reference; this work does not redesign him.

Colour-only corrections use deterministic masked remapping from preserved sources.
Keep complete alternating strides, restrained arm motion, natural bob and fixed
clip registration. Do not inflate frames or normalize every pose's height.
Review approximately 82/54/27px character heights plus diagnostic enlargements.
Routine authorized video uses direct MiniMax; historic price estimates are dated,
not verified current billing. Reserved Higgsfield Genjutsu remains reserved.

## Current state
At closeout the checkout is main, HEAD 92478eb4, with extensive existing working
edits and untracked art/builders. Do not reset or infer disk state from HEAD alone.
Installed selections are recorded in character/ACTIVE_ASSETS.json and loaded by
scripts/grid_canvas.gd. Snapshot: [crew manifest inventory](CREW_ANIMATION_CLOSEOUT_INVENTORY_2026-09-29.json).

| Actor | Installed | Remaining / staged |
| --- | --- | --- |
| Veld | Accepted bare idle/walk, shared helmet idle/walk, four-direction interact/kneel/repair/stand equipped overrides; west/south/north bare companion overrides | Audit remaining retained actions, fitting/handling, water and special states against current identity; no claim they are all revised |
| James / branforth | Accepted bare idle/walk and shared helmet idle/walk in four directions | Retained equipped action library still needs shared-helmet/body/material audit; side cadence was provisionally accepted as better, not perfect |
| Bill | Accepted bare idle/walk and shared helmet idle/walk in four directions | East matte idle/walk and matched bare/equipped action candidates remain staged; latest idle-led-v3 has no owner visual acceptance yet; other retained actions still need audit |

Current Bill review: [east idle-led-v3](http://127.0.0.1:8791/character/bill-shared-helmet-actions-east-v1/?v=idle-led-v3).
No candidate was installed merely because checks passed. Older dated next-action
lists may be superseded by later acceptance; use this snapshot and current loaders.

Updated files: docs/CURRENT_STATUS.md, docs/DEVELOPMENT_NOTES.md,
docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md, docs/ASSET_PIPELINE_AND_WORKFLOW.md,
character/ANIMATION_PIPELINE.md, character skill entrypoint and direct-video,
underwater-equipment, handoff and crew-consistency references, plus three specified
evaluation cases. Installed skill received targeted mirrors; pre-existing source
engineering notes and installed formatting differences were preserved.

Reusable lessons now live in [crew consistency skill reference](../skills/brinespace-character-pipeline/references/crew-consistency.md),
linked from the maintained and installed character skills, asset workflow, animation
pipeline and bible. The previous [shared helmet handoff](CREW_SHARED_HELMET_HANDOFF_2026-09-29.md)
retains detailed revision/test history. Actor continuation documents below contain
the first useful next action and affected paths.

## Verification
Latest Bill east staged candidate: Python 121 checks/0 failures; isolated Godot
232 checks/0 failures. All 24 action frames and interact transition crops inspected;
review page refreshed with new cache key. Latest Godot run used scratch APPDATA;
real-profile fingerprint unchanged. Earlier windows had concurrent profile deltas,
preserved in the shared-helmet handoff rather than rewritten as clean.
Veld's last recorded pass: east 90, west/south/north 122 each, crew walk 5,732,
native north 15 captures/0 failures; those are dated evidence, not new closeout tests.
Both maintained/installed skill structural validators passed. New Markdown links
and skill routes resolve, JSON parses with unique case IDs, four mirrored resources
match exactly, and scoped git diff --check passed (line-ending notices only).
The inventory hashes 16 manifests and 3,106 frame references. See
[skill validation record](CHARACTER_PIPELINE_SKILL_VALIDATION.md). Newly added
skill cases are specified but not executed as independent behavior evaluations.
No Godot/art regeneration is required for this documentation-only closeout.

## Next action
Open one actor session using its handoff:
[Veld](VELD_ANIMATION_CONTINUATION_2026-09-29.md),
[James](JAMES_ANIMATION_CONTINUATION_2026-09-29.md),
[Bill](BILL_ANIMATION_CONTINUATION_2026-09-29.md).
Each owns its actor files; shared code/registry/standards edits must be coordinated
and serialized. Keep shared helmet sources read-only and do not run another actor's
whole-pack builder. Preserve owner saves/layouts and isolate every Godot fixture.
No further work or spending is scheduled from this closed session.
