# Josh tread cleanup and blowtorch

Updated: September 9, 2026 · BrineSpace · Companion repair animation

## Objective and decisions
Owner requested another cleanup pass, removing blue from Josh's wheels, and more animations including blowtorch repair. This pass covers Josh's whole tracked base in locomotion and personality, plus four-direction deploy/weld/stow. Upper body remains muted bluish lavender. River and Margot retain the preceding extraction repair.

Josh now assists an existing paid crew hull-repair job. Implementation tuning: +25% progress while the torch is lit, nearby and on dry accessible floor. Architect ownership, normal Metal costs and completion stay in hull_repair.gd. He does not independently queue jobs, claim architect work or grant a passive bonus. This implements the newly requested repair capability beyond his former observer-only behavior.

## Current state
`character/josh-repair-v4` contains edited locomotion/personality sources and a new torch sheet, exact imagegen prompts/hashes, 8 base clips and 36 action/transition clips (12 added), and review GIFs/contact sheets. Treads, road wheels, hubs, fenders and front/rear lower chassis are neutral charcoal/gunmetal. Initial torch sheet retained but rejected because south flame crossed the body and chassis paint remained blue; torch-fixed.png is installed. Rear watch now uses its corrected authored rear-view frame instead of a duplicate.

`tools/build_josh_repair.py` packages those sources using the preceding cleanup helpers, shared 64-color palette, binary alpha and head registration for torch frames so flame width does not move the body. Added optional extraction gutter parameters defaulting to the preceding behavior. Source has narrow/uneven gutters; torch extraction permits boundary-adjacent ink, while final 92px exports retain unclipped bounds. Earlier packs remain intact.

`scripts/companion_repair.gd` (+UID) finds valid nearby paid jobs and gates assistance. `companion_npc.gd` routes Josh, serializes the new torch/pending state, plays deploy/loop/stow and extinguishes on invalidated work. `hull_repair.gd` applies the gated multiplier. Normal pause, flooding, cancelled/completed jobs, dead worker, range and stow disable assistance. The source checkout is installed; executable not rebuilt.

## Verification
Asset validators pass both manifests. Builder checks frame sizes, bounds, durations, binary alpha and palette. Agent inspected generated source corrections and final torch contact sheet; native sprite board captures all directions. GIF gallery preserves deploy/loop/stow for owner motion review; continuous visual acceptance remains owner-facing.

`tests/test_companion_repair.gd` (+UID) passes: actual paid HullRepair progress gets 1.25 seconds per lit second; deploy/stow, pause, doors, flooding, range and worker death suppress the bonus; completed job stows; normal costs/completion preserved; torch and pending snapshots validate and other companion identities reject them.

`tests/test_companion_personality.gd` adds a real-station route to a paid repair, active contribution at arrival, full checkpoint restore mid-torch and stow after job removal. Native test passes, including prior River/Margot/Josh personality checks. Generic action loop skips torch because the new paid-job section exercises it. Native `test_sprite_polish.gd` updated to the installed Josh pack and torch frames passes. Logs: `output/josh-repair/`. No global congestion or all-room occlusion claim.

## Next action
Owner review: `character/josh-repair-v4/review.html`. Balance the assistance rate after play feedback; broader companion actions and independent job ownership are separate scope. No executable export or commit.
