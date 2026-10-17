# Project handoff

Updated: October 14, 2026 · BrineSpace · Krusher Dom animation asset set

## Objective and acceptance
Complete reviewable asset candidate: `character/krusher-animation-package-v8`, 338 bare + 248 helmet states, 8,058 frame holds, 3,486 unique portable PNGs. Current likeness/collar now covers work, cargo, seated, meals, equipment, rest, recovery, death and water families. Technical checks and agent review do not constitute owner visual acceptance or ordinary crew-roster integration.

## Accepted decisions and constraints
Krusher Dom / System Administrator / AI & Robotics / James utility body / matte muted cyan #527C80. Original body poses, tools, shells, density, clocks, pivots and profiles retained. Canonical-v9 preserves the prior V6 collar repair. Owner-selected crew remain selected. Every native run uses scratch APPDATA with real-profile fingerprints before/after.

## Current state
Four new built-in generated sheets supply matching pitch, quarter, rest and rear heads. Raw images, exact prompts (`prompts.json`), extraction hashes and shared uniform scales are retained here. Family builders/validators are maintained locally; `prepare_pipeline.py` and `prepare_reviews.py` are historical bootstraps, not rebuild commands.

`krusher-coherent-bank-v2` records cyan finishing, including observed yellow-green suit lettering. Authored head silhouettes and recorded foregrounds are protected; alpha and all other pixels remain exact. `krusher-coherent-bank-v3` consolidates 87 shared-pose groups / 343 derivative slots onto their canonical or parent drawing. Final audit: 8,058 slots / 3,487 historical registered-pose groups / zero inconsistent groups.

`checkpoint_floor_state_v2.gd` adds only two exact release-cue hashes; paired UID preserved. `floor-cue-proof.json` establishes unchanged pixels outside declared head/colour edits and exact case/lower-body alpha. Historical James/Krusher admissions and altered-cue rejection remain strict. No roster, perks, resource rules or save schema changes.

## Verification
Final package: 16,790 checks, zero errors; every required state/source byte, timing/profile and indexed PNG. Revision-specific status prose is excluded from root-profile equality.

Final native loader: 57,025 checks across every slot at start/middle/end, original pixels, clocks, canvas, pivot, ruler and filter. Fresh final-package station fixtures: repair 8,951 checks / 120 captures / eight cases; bunk 240 / 30; water 6,399 / 104 / eight furnished routes; West floor-case 383 / 98 / 14 cases, including original James admission and mutated-cue rejection. Total native checks 72,998; zero failures/errors/warnings/leaks. Five zero engine exits; all 2,947 owner non-log files unchanged in every run. Native processes terminal.

Agent review: 256 family/cardinal/gear midpose samples, head/collar detail boards, selected actual repair/bunk/water/West views and interactive motion phases. These are sampled evidence, not continuous video proof of every clip/layout. Initial bunk fixture incorrectly compared V4 filenames and failed 30 source checks; failed evidence retained in `review/bunk-stale-v4-expectations`. Final scope uses V8 with original clocks unchanged. Intermediate revisions retain their original scopes; V8 is the deliverable.

Private browser: https://krusher-dom-preview.brinshadewater.chatgpt.site/animations/ . All 586 states / 8,058 holds; 3,486 WebPs decode pixel-exactly to V8 PNGs. Search, gear switching, playback, pause and scrubbing exercised locally. Existing Site identity/owner-only audience retained; successful deployment recorded in `remote-preview.json`. Owner-device rendering remains their check.

## Next action
Asset-set source coverage is complete and ready for owner review; no missing states or failed final checks remain. Further likeness/gait/contact edits should target the reported clip. Ordinary roster integration and additional world/lifecycle coverage remain separate work. No game export or game-repository commit performed.

Rebuild from local saved sources without generation: `python character/krusher-head-fit-v7/rebuild_all.py` (`--native` adds isolated full-bank checks). Re-admit proven cue hashes with `admit_floor_cues.py` if pixels change; refresh bunk scope before station tests. Fixtures: `run_repair.py`, `run_bunk.py`, `run_water.py`, `run_west.py`.
