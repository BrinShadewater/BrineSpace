# Project handoff

Updated: 2026-09-26 · BRINE crew-family style pass

## Objective and acceptance
Improve BRINE to match Bill, Veld and Marsh's currently selected animated sprites, retaining the simple blue suit and suspended pose.

## Accepted decisions and constraints
Current idle-south/000.png from major-bill-v3, dr-veld-v2 and marsh-v2 are authoritative style references. The old BRINE-derived head and eyes were too cartoon-like. Preserve existing float timing, tube, crew assets and saved layouts.

## Current state
Selected second imagegen attempt uses only the three current crew frames as image references, with BRINE's identity/costume described in the prompt. Smaller mature face, darker blue-gray suit, selective contours and stronger painted folds. First attempt retained too much previous stylization and is preserved as attempt-1.png. production.json describes that attempt; selected-production.json governs the chosen clean-master.png.

63x168 transparent export, original eight-second mesh rig and native room preview. build.py generates body export and hashes; build_review.py creates an equal-148px-height crew comparison, GIF and motion sheet from native captures. Comparison normalizes visual height for style review and is not an in-world scale proof. Shared preview launcher selects this revision. No production character registry changes.

## Verification
Viewed all three original crew frames, body export, crew comparison and eight native motion phases. BRINE now has a more compact face and muted shaded costume; unarmored silhouette remains slimmer and exposed skin less textured than armored crew. Owner acceptance pending. 32 native samples and endpoint loop assertion passed without logged script errors; owner save fingerprints unchanged (session-8b08ff6bc023447d9a3e585077ef799e). Frame/mesh technique is unchanged from prior float study, not a new painted-frame animation pack.

## Next action
Review comparison and live animation. Preserve earlier versions; production integration remains a separate uncompleted step.
