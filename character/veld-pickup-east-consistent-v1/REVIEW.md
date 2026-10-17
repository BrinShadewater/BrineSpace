# Project handoff

Updated: 2026-09-29 · Project: BrineSpace · Task: Veld east pickup

## Objective and acceptance
Owner requested lighter unload and continued cargo work. Pickup derived-v1 is
staged for review alongside unload palette-v2; both now installed.

## Accepted decisions and constraints
Carry palette-v10 remains installed. Preserve motion/anatomy and shared helmet.
Pickup retains original520ms non-loop metadata,256canvas,pivot128/224,standing148.

## Current state
Owner accepted continuing from pickup derived-v1/unload palette-v2. Both paired
states installed in grid loader and ACTIVE_ASSETS. Builder statuses updated;
fixture now tests actual installed loader:58 checks/0 failures. 2751 real
profile files observed delta ['lagprobe.json', 'lagprobe.json.bak']; attribution unknown under scratch APPDATA.
Unload cloth lifted with one fixed10-level midtone curve; all12 alpha planes and
case regions exact. Pickup reuses those12 frames in reverse order5/4/3/2/1/0,
without new authored pixels. Source reverse/provenance hashes in checks.json;
reproducible builder, paired manifests/GIFs/contact/preview and native fixture
added. Preview slowed for inspection. Starting body equals accepted idle plus
floor case; ending body holds the case in a planted stance.

## Verification
All12 pickup frames match reversed unload pixels. Original520ms timing preserved.
Native59 checks/0 failures with scratch APPDATA. 2751 real profile files unchanged.
Source/contact/native reviewed; motion, grip/occlusion and palette acceptance
remain the owner's next review.

## Next action
Review derived-v1 pickup and palette-v2 unload together, then promote accepted
paired states. Carry turns and remaining directions remain separate.
