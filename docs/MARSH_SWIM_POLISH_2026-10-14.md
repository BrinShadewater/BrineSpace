# Project handoff

Updated: October 14, 2026 · Project: Brine Space · Task: latest-report Marsh animation polish

## Objective and acceptance

Owner reopened Marsh polish. Address the latest report's 12 swim-turn endpoint
failures and possible doubled north head. Review the changed drawings and joins,
retain unrelated accepted animation, and install a reproducible source revision.

## Accepted decisions and constraints

Reuse coherent complete selected bodies. No anatomy stamping, generation, grade,
silhouette, pivot, timing, controller, equipment or gameplay change. Older sources
and reports remain historical evidence. No release export or publication requested.

## Current state

`character/marsh-swim-joins-v1/manifest.json` is appended to Marsh's ordered catalog.
North swim slot 0 now uses the complete selected east-to-north turn endpoint;
only transparent bottom padding is removed for the loop canvas. Its alpha is exact
to the previous loop pose, with the doubled interior head removed. All 12 turns
reference complete loop-slot-0 bodies at entry and exit, with transparent bottom
padding for their original canvases. Five packaged PNGs; 13 clips / 19 frame slots
change. All turn interiors and remaining loop drawings retain their original paths.

`tools/polish_marsh_swim_joins.py --install` builds this narrow override; the
maintained `rebuild_marsh_art.py` invokes it after the older installers. The crew
art baseline is refreshed. `test_marsh_swim_join_polish.gd` and paired UID provide
native source-clock/capture coverage; `tests/index.json` registers its native lane.

[Animated review](../character/marsh-swim-joins-v1/review/index.html) includes all
13 clips and native boards. Each turn continues into two destination swim cycles;
the labelled replay reset is viewer behavior. The north before/after is lossless.
These previews reconstruct authored source holds; they are not station-world video.

## Verification

- Before: carry-turn handoff fails 12 of 72 cases. After: all 72 pass, including
  saved/paused turn restoration, exact destination pixels and resumed phase.
- Native: 106 checks, zero failures; all 13 chronology boards captured at 1x/0.5x.
  Complete full-size chronology reviewed, including all nine holds of half turns.
  No doubled head remains; the final turn/first loop drawings match exactly.
- Crew complete packs: 4,832 checks; walk: 234 checks; swim packs: zero failures.
- Scope audit: only 13 Marsh clips differ in the full baseline; other actor/body,
  equipment and strides match. Changed frame metadata, dimensions, alpha, pivots,
  filtering and clip timing remain exact. No exact doubled-head aliases remain.
- Narrow rebuild is byte-identical. Scratch APPDATA throughout; all 2,948 real
  non-log owner-profile fingerprints match before/after. Task Godot processes exited.

Evidence: `output/marsh-swim-polish-2026-10-14/`, including scope audit, fingerprints,
before/after test receipts and native captures. Successful runner logs:
`20261014-194207-headless`, `20261014-194407-headless`, and the final native receipt
recorded in that output folder. Initial native attempt exposed stale viewport
captures; a rendered marker now guards readiness. The next capture omitted later
half-turn holds beyond the window; two-row layout fixes containment. Both incomplete
capture sets are retained and superseded by `native/` and `native-complete-*` boards.

## Next action

Reported swim defects are repaired in source. Owner visual acceptance, natural
world travel/occlusion review and a rebuilt playable release remain separate.
No claim of a full-library visual reapproval or new in-between artwork.
