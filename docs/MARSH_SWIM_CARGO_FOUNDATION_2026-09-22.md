# Marsh loaded swimming foundation

Updated: September 22, 2026. Project: BrineSpace. Task: continue cargo animations.

## Objective and acceptance

Make loaded swimming visibly retain cargo before adding the twelve missing turns.
This pass discovers an underlying base-animation defect and prepares a candidate;
no new animation is installed or visually accepted.

## Accepted decisions and constraints

No Higgsfield. Built-in generation for new art; local extraction for registration.
Preserve working dry-carry/swimming turns and original sources. No gameplay change.

## Current state

Inspected current `swim-carry-east/000.png`: upright empty-handed pose. North frame
has spread hands. `_get_marsh_frame` in grid_canvas renders the selected player
texture directly; there is no separate case added by this path. Crew expedition
state selects swim-carry when returning with cargo underwater. Current state names
and count alone therefore overstate visual completion of loaded swimming.

New source/prompt: `character/marsh-swim-cargo-v1/sources/east-loop-01.*`.
`tools/prepare_marsh_swim_cargo.py` builds four review frames of a prone east-facing
swimmer holding the case, with registered shoulders and restrained kick poses.
Review GIF/contact: `character/marsh-swim-cargo-v1/review/east-loop-01/`.
Canvas224x208/pivot112,172 provides20px horizontal padding on either side of the
184-wide profile. .32 source scale. These are candidate extraction values, not
an installed animation contract. Initial184-wide trial clipped the trailing boot;
transparent padding fixed it without changing anatomical scale.

## Verification

Four frames extracted with binary alpha and no border touches. Agent inspected
the registered contact sheet for connected body and visible case. Source and exact
prompt saved. Runtime and original art unchanged; no native or release test claimed.
Candidate's small kick variation still needs motion review and comparison against
current actor scale. No full four-direction base audit or human loaded-swim visual
acceptance was established by this pass.

## Next action

Inspect all current loaded-swim frames and their pickup/unload joins. Refine the
candidate if needed, finish directional base repairs and integrate with canonical
rebuild, clearance, source contracts and native cargo transport checks. Then build
twelve turn clips from corrected endpoints. Earlier sixteen-to-twelve count only
covered missing turns; newly discovered base defects are additional work.
