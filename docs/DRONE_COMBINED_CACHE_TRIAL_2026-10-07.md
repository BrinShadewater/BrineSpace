# Drone-only combined cache trial

Updated: October 7, 2026 Â· Project: BrineSpace Â· Task: performance and release readiness

## Objective and acceptance

Release stale ordinary and indexed drone textures under one budget without changing pixels, gameplay, active resource identity or scene ownership. Require matched workload evidence and clean native lifetime checks before admission. Original PC/Mac frame, memory, loading, bug and endurance gates remain mandatory.

## Accepted decisions and constraints

Keep normal crew playback and flood code. Preserve original art, user settings and owner saves. Protect recently used resources even when the visible working set exceeds the budget; do not force eviction to claim a budget pass. No normal source admission in this trial.

## Current state

Evidence: `output/drone-combined-2026-10-07/` (two-frame grace) and `output/drone-combined-grace-2026-10-07/` (32-frame grace). Both physical private providers have sixteen selected lossless sources. Oldest eligible entries from both backends participate in eviction; diagnostics retain at most 64 path records. Current control is the previous drone-only provider, **not** the original normal game.

Two-frame policy rejected: final reported textures 4131.23 â†’ 3946.46 MiB, but ordinary uploads 25 â†’ 31 and measured upload bytes increase by 144,506,892. Three substantial extra uploads are West steering, drive and stop sheets; other extra events are placeholders. Frames over 50 ms increase 3 â†’ 4; phase timings mixed.

32-frame policy is a memory candidate: six texture endpoint changes are 0, 0, âˆ’61.32, âˆ’61.32, âˆ’122.54, âˆ’91.76 MiB. Large upload events do not increase; the only additional observed ordinary upload is the four-byte empty placeholder (25 â†’ 26 uploads), indexed uploads remain 15. One frame over 50 ms in each lane; maxima 55.10 / 56.32 ms. Six p95 pairs remain approximately 38â€“45 ms with mixed changes; no FPS gate pass or consistent pacing improvement claimed. Final candidate reported textures 4039.47 MiB still fails the large-scene budget.

## Verification

Both matched 1920Ã—1080 native source pairs: 40-room mixed station, idle/pan at 1Ã—/2Ã—/4Ã—, 60 measured frames per phase, uncapped/VSync disabled. All six full crew/fleet/door/light/power/zoom states match; complete crew and room resource records match; zero missing art or selected ordinary duplicates. Source/editor trials, not actual debug=false release certification or three-run loading certification.

Each policy passes 17 actual allocation checks: oldest-first eviction, protected recent storage, exact bookkeeping, held references surviving lookup removal and last-owner release. The 32-frame provider additionally passes 2625 dock checks / 1300 exact native pairs and 446 full-room checks / 216 exact pairs, clean exits. Actual room and final station captures inspected.

The new drone-only New Game/Studio/save/title/Continue fixture uses **normal loading, flood and crew**; no prior private crew routing/hot reload. A title adapter retains the candidate across Continue; the original measured Main is preserved as `main-before-lifecycle.gd`, with only the return-title path changed afterward. Functional checks pass (142 with Studio, 140 without), including restored crew/fleet and released weak references/factory/jobs/caches. Nevertheless, exit diagnostics report four leaked RefCounted objects with Studio, two without. An otherwise normal two-cycle/no-Studio control passes 98 checks with **zero** leaks/warnings. This is an experimental integration admission blocker; functional checks alone do not close it.

All completed runs verify 2936 owner files unchanged. Full logs, reports, isolated profile locators and failure evidence retained.

## Next action

Later accepted attribution: see [cold-loading investigation](DRONE_LOADING_LEAK_ATTRIBUTION_2026-10-07.md). Runtime weak owners release; load-only reproduces the warning before gameplay. Synchronous-preparation lifecycle with/without Studio passes cleanly. Responsive production loading and actual compiled-package verification remain required; the historical next-action paragraph below preserves the earlier hypothesis and trial evidence.

Isolate the experimental lifetime defect. A separate `output/drone-named-sort-2026-10-07/` copy substitutes a named static comparator for the inline sort callback while preserving eviction policy; its 17 allocation checks pass. Its two-cycle/no-Studio diagnostic completes 140 functional checks but reports four leaks/one warning, so replacing the comparator does not solve the defect; the hypothesis is rejected. The separate original sixteen-source eviction-policy control in `output/drone-original-policy-lifetime-2026-10-07/` also completes 140 functional checks but reports three leaks/one warning. Thus combined eviction is **not required** to reproduce the lifetime defect; the drone-only integration differs from the clean normal control. Counts are not yet stable enough to infer per-cycle retained owners. All processes terminal, all owner fingerprints unchanged. Next record relevant provider/context/texture-pool object IDs and weak lifetimes at scene exit to identify the leaked instances; do not mask warnings or force-free reference-counted objects. Then complete provider/build admission, packaged measurement and sustained rendering optimization. No release upload or gate closure.
