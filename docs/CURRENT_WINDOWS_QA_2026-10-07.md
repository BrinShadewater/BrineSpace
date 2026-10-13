# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: refreshed actual Windows release baseline

## Objective and acceptance

Continue full PC/Mac release readiness. Freeze latest accepted normal inputs, export with the maintained Windows workflow, audit the PCK outside the checkout and measure actual debug=false gameplay. This is a QA baseline, not public release certification.

## Accepted decisions and constraints

Build `brinespace-1a4d5f698ed2d862`. Source aggregate SHA256 `1a4d5f698ed2d862acd7d364733ee0ba1262f9fb905ddd5044d623049772bb32`; metadata records current HEAD and dirty selection. Accepted normal image/geometry/preparation changes included; private crew/drone storage and connection prototypes excluded. No normal runtime changes or itch action in this turn. Previous query/calibration turn was evidence progress, not an accepted optimization.

## Current state

Physical selected inputs: `C:/Users/Alex/AppData/Local/Temp/bs-current-release-lvv9u8p4`. Shared Git metadata only; selected runtime/build bytes physically copied and verified against current source after copying. Index35,585 equals HEAD tree, freeze36,651 files including source UID pairs and maintained exporter/plugin/templates. Runtime collector36,244 files/3,593,466,291 bytes; generated manifest36,245 rows includes export plugin. No LFS pointers accepted.

Evidence `output/current-release-2026-10-07/`: inventory, input hashes, export/audit logs, expected manifest, unmodified deliverable in `release/`, isolated physical EXE/PCK copy and guarded autoload harness in `qa/`, gameplay JSON/capture, hitch attribution and readiness scope. EXE109,283,328 bytes/PCK3,623,006,806 bytes. QA identity records EXE/PCK hashes; deliverable hashes verified unchanged after gameplay. Previous build preserved.

## Verification

Maintained Godot4.7.2 export clean. Outside-checkout exact audit:35,779 checked,0missing/changed/remapped/unexpected. Source Python checks:10manifest tests and2release-assertion tests pass. Template/editor versions matched. All owner fingerprints2,936 before/after, zero changes.

Actual release,1920×1080 deterministic mixed40,60 measured frames each idle/pan at1×/2×/4×:360 frames. Explicit debug=false; no missing-art records, logged errors, warnings or leaks. Station capture inspected. Ready9,113.565ms, excluding dialogue/direct gameplay fixture; OS file-cache cold/warm status not controlled, single run cannot certify loading gate. p95 by six phases36.518/37.138/32.631/36.678/50.429/47.063ms; p9940.688/46.167/37.582/39.935/65.336/75.857ms. Every frame gate fails. Engine textures3.63–4.29GiB; prior mipmap-accounting calibration does not justify global conversion or close memory gate. Current machine4070Ti, not working1650/M1 targets.

Seven measured>50ms frames investigated: all4×, max75.857ms. Latest upload records correspond to drawing work one process-frame ID behind post-draw sample ID. Current-frame counter zero is not evidence of no upload. Payload96–241MB, upload7.05–29.01ms; exterior actor callback15.69–42.54ms, versus simulation3.62–5.41ms and render signals10.76–12.55ms. South/West mining body/effects dominate; South collection cargo, North start/wheels and West steering also appear. Scopes overlap, not additive causal accounting. All seven coincide with uploads, not proof they explain every millisecond. Normal auto capture enabled and saved one report; its own overhead still needs separate assessment.

Harness correction: comparison fixture had unconditionally hot-reloaded a private flood adapter. This adapter adds a draw_crew indexed-display resolution branch plus a comment encoding difference; diff preserved. Earlier paired trials applied the same adapter to both backends, so their relative comparisons remain paired evidence but must not be called entirely unmodified-normal baseline certification. Existing independently installed native visual tests retain their recorded scopes. New release harness removes hot reload, contains no private runtime res paths and uses packaged normal flood code. Do not reuse old fixture unchanged for certification.

All build/audit/test/gameplay handles terminal. No three-run benchmark matrix, fresh/reported workloads, other actions/resolutions, packaged original nine bug closure, full New Game/dialogue/save/Continue, endurance, target hardware or Mac signing/gameplay acceptance yet.

## Next action

Complete lossless shared drone-provider admission against this packaged baseline: actual room/dock flip/type/reuse, fallback filtering/materials, full lifecycle and residency. Keep original pixels/frames/metadata/default quality and Bill save identity. Include newly observed North start/wheel uploads in inventory rather than assuming current16-source provider covers them. Address steady rendering separately; no cache grace increase admitted. Preserve candidate for rollback/comparison, then broaden actual release workloads and three cold/warm runs, original issues/endurance and Windows/Mac certification. Release remains blocked by performance/memory gates, no public upload.
