# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: texture allocation and transparent animation upload trial

## Objective and acceptance

Continue the full PC/Mac performance and release plan. Preserve selected pixels,
animation clocks, filtering, ownership, saves and layouts. These private matched
trials do not certify the full current-checkout release or the target hardware.

## Accepted decisions and constraints

No art downscaling, reduced animation frames, automatic quality or broad refactor.
Normal gameplay source is unchanged in this pass. Keep both prototypes private.
The allocation pool is rejected as a performance remedy; transparent upload deferral
has mixed pacing and is not admitted. No public release action.

## Current state

Artifacts: D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/:
`drone-stall-image-inventory`, `drone-allocation-pool`,
`transparent-atlas-preparation`, `transparent-atlas-runtime`,
`transparent-atlas-reverse`, and `transparent-atlas-comparison.json`.
Reproducible private helpers live under output/renderdoc-tools-2026-10-08/;
no new normal gameplay scripts or authored art were changed.

Four actual large stall PNGs have distinct RGBA storage and visible colored pixels;
these four do not permit lossless grayscale/opaque conversion or duplicate sharing.
A weak-lease texture allocation pool protects live owners and clones, but the native
large-image microbenchmark is slower: fresh creation median14.206ms versus
reuse15.479ms, both alternating orders. Do not integrate that pool.

Transparent candidate starts PNG decoding on the original initial selected frame,
touches existing textures normally, and defers first GPU creation until a selected
cell is not in verified emptyFrameRanges. Clocks and authored files are unchanged.
Runtime uses one compiled module and a flag; semantic retention1 and low water
priority are common controls. These shared private controls limit certification scope.

## Verification

Pool ownership9checks/0; proxy drawing/duplicate ownership199checks/0 including
192 raster pairs. Allocation-only benchmark10 measured samples/lane after4 warm
iterations; not rendered gameplay. Official APIs reviewed:
https://docs.godotengine.org/en/stable/classes/class_texture2d.html and
https://docs.godotengine.org/en/stable/classes/class_imagetexture.html#class-imagetexture-method-update

Transparent synthetic native reference7checks/1 expected failure -> candidate7/0.
Real mining-effect native364checks/0, all180 selected frames pixel-identical;
both initial decode requests start, candidate upload count remains0 through frame44,
becomes1 at45, both jobs consumed. No timing clock rewrite.

Actual debug=false1080p40room idle,1000frames at each1x/2x/4x, both orders:

| Order/lane | Mean ms 1x/2x/4x | p99 ms 1x/2x/4x | Max ms 1x/2x/4x |
|---|---|---|---|
| Reference first | 38.696 /39.413 /40.297 | 56.351 /63.042 /73.408 | 100.025 /90.865 /122.243 |
| Candidate second | 38.313 /39.788 /40.553 | 54.103 /65.706 /76.514 | 79.772 /85.034 /110.675 |
| Candidate first | 38.906 /39.180 /40.021 | 56.751 /60.547 /72.948 | 102.079 /86.117 /107.847 |
| Reference second | 38.476 /38.939 /40.416 | 57.742 /60.427 /68.945 | 108.270 /98.105 /143.874 |

Maxima improve6/6, means and tails mixed; release FPS/stutter gates still fail.
Visible atlas calls30672/transparent524 each; visible misses ref735/737 versus
candidate737/737. Broader ready-miss reduction includes transparent cells and cannot
prove improved visible availability. Candidate peak2345.361MiB versus2345.481MiB,
only0.121MiB lower; this is not a substantial memory remedy. Drone uploads486->485
in both pairs: the difference is the all-empty completion empty-60.png placeholder,
not removed visible mining-effect uploads. Crew4074 uploads each is a separate counter.
Final mission histories/resources match; analyzed first-pair phase crew/drone/mission
endpoints match. Pending jobs3 before exit ->0 after actual exit; texture exit228.259MiB
each. Owner2936 files unchanged in each pair/native run; logs clean; processes terminal
and adapters restored. Completed decoded-image CPU retention is not fully inventoried.

## Next action

Do not promote either prototype on these results. Continue measured room-render
preparation/retained-command investigation. Reverse candidate stage samples average
live_rooms10.718ms, setup_large_child_base5.477ms, moonbay base4.706ms,
actors_effects1.729ms, environment1.477ms, door_light_validation1.445ms.
Scopes overlap: do not sum these values. Preserve current-frame output and full
invalidation/visibility/exit behavior; prove gains with matched actual release work.
Full original bugs, workloads, memory/loading/endurance and Windows/Mac certification
remain open. Any future transparent deferral admission also needs bounded decoded CPU
retention, more availability/workload evidence and consistent pacing benefit.
