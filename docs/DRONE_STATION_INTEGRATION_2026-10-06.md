# Project handoff

Updated: October 6, 2026 · BrineSpace · First ordered palette station comparison

## Objective and acceptance
Reduce actual station texture residency/upload stalls while preserving complete
rendering and gameplay. First integration is experimental and not accepted.

## Accepted decisions and constraints
Private physical source copies only. Normal game/art/settings untouched; all
2,936 owner non-log files unchanged under verified isolated profiles. No release.

## Current state
`output/drone-coordinate-2026-10-06/prepare-station.py` creates private Main/Grid/
crew/benchmark copies in `station/`. Original exterior pass remains baseline;
`--palette` uses ordered harvest/scrap/construction before, complete fleet dust/body
commands, then admin/survey after. Provider session attaches to Grid lifetime,
not temporarily empty fleet. Actual normal dust and survey/harvest/construction
code called without editing those scripts. Copies include current card scan/raw
region functions. Other frozen inputs retain their fixture revision.

## Verification
One native development-runtime pair: deterministic 40 rooms, Veld/James/Marsh,
180 warm-up frames, 60 measured frames each idle/pan at 1/2/4x, 1920x1080,
VSync disabled, RTX 4070 Ti, Godot 4.7.2 Compatibility. Both processes terminal,
zero logged engine errors, empty SafeImage failures, clean exits.
All six complete crew snapshots and drone dictionaries equal, equal warm-up count.
This does not prove complete scene pixel equivalence or release performance.

Baseline texture end 3168.484 MiB; candidate 3382.873 MiB (+214.388).
Per-phase deltas +122.455 MiB in first four, +30.638 during indexed South mining,
then +214.388 after moving to other atlases. Indexed draws 52 then 87 cumulative,
zero linear/material fallback draws. Candidate has 48 command slots.
Normal cache remains 96,996,820 source-data bytes while copied exterior cache
also loads ordinary atlases. Bank holds the indexed South atlas after usage;
residency therefore grows again after source eviction. These measurements reveal
integration ownership costs; they do not disprove lossless atlas storage savings.

Baseline p95 40.889–49.854 ms; candidate 39.157–52.817 ms. Both fail 16.7 ms gate.
No FPS improvement established. Loading 13.787 vs 12.789 seconds is one uncontrolled
cache-order pair and not an accepted loading improvement. Full logs/results and
six-phase comparisons retained. Draw-call averages differ slightly; full scene
raster/order validation remains required before accepting appearance.

## Next action
Eliminate duplicate ordinary atlas storage across original and private exterior
consumers; avoid independent long-lived GPU banks. Make indexed storage follow
actual cache/command ownership rather than keeping the last atlas for the whole
scene. Validate identity/eviction/held commands before repeating matched station
workload. Also include slot drawing in CPU attribution (current host timing covers
section/command preparation but not every slot callback). Avoid claiming normal
memory reductions until these costs and complete scene visuals are verified.
All original performance, packaged Windows/Mac, endurance and release gates remain.
