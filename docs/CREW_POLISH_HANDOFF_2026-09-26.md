# Project handoff

Updated: September 26, 2026 · Project: Brine Space · Task: crew animation cleanup

## Objective and acceptance
Improve cast consistency with the current visual bible, painted detail, clarity and
smoothness. Overall request is unfinished. Do not count preview studies as a full
replacement or owner acceptance.

## Accepted decisions and constraints
Preserve character identity, equipment handedness, world scale and existing gameplay.
Marsh remains helmet-free. Recent companion polish is separate. Authorization covers
reversible artwork work; no additional approval gate was introduced.

## Current state
All new work is under `character/crew-polish-v1/`: frozen catalog baseline, source
prompts/generations, reproducible extraction/build scripts and interactive comparison.
Twelve walk studies retain original pose/timing boundaries and recover 289 frames from
the preserved videos. Veld has 24 painted study poses, with a better-detail east V2
source. Bill south V1 is unselected for incoherent stride. No production bindings
or images changed. Preview: http://127.0.0.1:8791/character/crew-polish-v1/ .

## Verification
313 study frame references pass size/alpha/timing checks; 72 original walk poses
reproduce production pixels exactly. Twelve original cycle durations retained.
JS syntax, all twelve browser selections and selected visual views checked; no
console errors. Pause/step and scale controls work. No Godot execution or save access.
Native contact/equipment/transitions and complete art/motion acceptance are pending.

## Next action
Review the Veld east V2 proportions against idle; establish matching idle/work and
coherent motion before broad expansion. Retain rejected candidates and source hashes.
Finish remaining cast/action artwork, paired gear and isolated native verification
before promoting packs. Do not mistake the denser motion study for new detail.
