# Portrait session handoff

Updated: 2026-09-27 · Project: Brine Space · Task: matching portrait masters

## Objective and acceptance
Owner accepted and requested installation of Bill, Veld, Branforth, Marsh, Margot,
Josh and River portraits matching BRINE. Session closed at owner request.

## Accepted decisions and constraints
Full-resolution PNG masters: `character/portraits-brine-style-v1/`. BRINE reference:
`character/brine-comms-v14/portrait.png`. Preserve masters and old sources; later
passes use new versions. Fine painted realism, soft cool light, restrained contrast,
quiet role backgrounds, distinctive identities and close square framing.

## Current state
All seven are bound in scripts/architects.gd and scripts/companions.gd; selection
and applicable comms share these loaders. installed-portraits.json and pack manifest
record acceptance. Exact prompts, hashes, comparison page and pack HANDOFF retained.
Updated maintained/installed character skill portrait reference and entrypoint,
docs/ASSET_PIPELINE_AND_WORKFLOW.md and CURRENT_STATUS.md for future matching work.
No new images, runtime edits, commit or export during this closeout.

## Verification
Prior native Godot 4.7.2 checks passed four crew comms portraits at 1600x900 and
960x540, and three companion textures at 160x170. Agent inspected companion sheet
and Marsh capture; full selector layout was not verified. All seven source hashes
matched the reviewed outputs; LFS coverage was checked. Evidence remains under
output/portrait-masters-2026-09-26/.

Safety correction: those checks were not isolated and overwrote
brine_loop.save.comms.json. Owner project instructions record restoration from an
F8 bug-report zip; this session did not independently reverify recovery. The old
probe is not safe to reuse without scratch APPDATA and before/after fingerprints.
Documentation closeout uses skill validation and reference checks only, no Godot.

## Next action
No remaining portrait work. For future portraits start with the maintained
skills/brinespace-character-pipeline/references/comms-portraits.md and accepted pack.
Existing executable packages require a fresh export to receive these images.

Closeout checks: maintained and installed skills both pass quick_validate.py;
portrait guidance copies have identical hashes; referenced workflow/master files
exist and targeted diff whitespace checks pass. No Godot process was launched.
