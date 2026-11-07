# Marsh movement handoff

Updated: September 12, 2026. Project: Brine Space.

## Objective and acceptance
Replace owner-rejected stiff-torso walks with whole-body articulation and credible foot contact; continue broader animation/movement polish. Selected playback checks and live visual review are bounded evidence, not owner acceptance or completion of the full goal.

## Accepted decisions and constraints
Marsh is a human-looking blond male android in an ivory/slate suit with sage shoulders, full gloves and no helmet. Canonical identity: character/marsh-portrait-v3/portrait.png. His implant is on anatomical RIGHT: visible east, hidden west, viewer left in front and viewer right in rear. Bill remains unchanged. Preserve real battery behavior.

## Current state
All four walk directions are selected through tools/veld_scanner_revision.py and tools/rebuild_human_crew_art.py, exported by tools/rebuild_marsh_art.py. Tests: tests/playtest_crew_walk.gd and tests/playtest_marsh_walk.gd with paired UID. Sources, exact prompts, durable jobs, recipes and review images live in character/marsh-motion-polish-v1/.

East video 01: 97 frames, 24 fps, 1248x1664; cycle 36-64, slots 36/41/45/50/55/59, fixed scale 147/1380 and position [62,59]. West video 01: same metadata; cycle 28-52, slots 28/32/36/40/44/48, scale 147/1440 and position [64,64]. Both use six 150-ms holds, canvas 256 square, pivot [128,224]. Dense strides: east 96, west 126. Heel boundary trials and uncertainty are preserved with each cycle; these are not continuous foot-lock proofs.

North and south references and videos 01 are preserved with exact prompts/jobs. Each video has 97 frames at 24 fps, 1248x1664. North: cycle 24-44, slots 24/27/31/34/37/41, scale 147/1300, position [57,54]. South: cycle 28-54, slots 28/32/37/41/45/50, scale 147/1540, position [68,68]. Both selected with six 150-ms holds and axial stride 0.128 cells. Axial screen foot movement is foreshortened, so the stride is evaluated in the live fixture rather than calculated directly from sole pixels. No active generation or test jobs.

## Verification
East/west art validation passes; each selected native walk passed 60 samples. Live east: 32 samples through north kneel, battery 92.90. Live west: 25 samples through north kneel, battery 96.03. Both source and live contact sheets reviewed. Evidence: output/crew-replacement-2026-09-12/marsh/{east,west}-video-walk-{validation,selected-native,live}.log and live-walk-review-{east,west}-padded/. Fixture retains real battery drain and rejects helmets; automatic processing is disabled while an explicit unpaused clock advances Marsh.

North/south art validation and 60 selected native samples each pass. Live north: 29 samples into north kneel, battery 99.03; south: 33 into south kneel, battery 95.87. Source and live contact sheets reviewed. South kneel is partly hidden by machinery and is not visually accepted by this walk test. Combined packs: 19,259 checks, zero failures. Four-direction preview: review/all-direction-walks.gif.

Ledger: all 20 targeted walk variants have bounded review. Broader run/carry/actions, transitions and identity work remain open.

## Next action
Review the new walks alongside idle, turn, start/stop, run, carry and action transitions. The full replacement/polish goal and owner acceptance remain open; do not interpret 20 walk rows as completion of the 808-clip ledger. Prioritize visible discontinuities and Veld identity/seated review, retaining Bill and Marsh invariants.
