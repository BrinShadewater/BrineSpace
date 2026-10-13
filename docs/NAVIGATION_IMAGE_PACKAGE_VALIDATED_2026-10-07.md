# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: packaged navigation image cleanup

## Objective and acceptance

Verify accepted scene-exit image cleanup in a real release executable and repeated large-station save/Continue transitions. Full original PC/Mac release targets remain active; this milestone proves one resource-lifetime fix.

## Accepted decisions and constraints

Preserve cached navigation geometry, collision/activity metadata, selected art and owner saves/layouts. No automatic quality reduction, broad refactor or public upload. Trials remain private until their source admission and release gates are covered. Reported texture memory is not physical VRAM; unavailable static-memory monitoring is not zero RAM.

## Current state

Candidate `output/drone-compiled-2026-10-07/navigation-images-release/BrineSpace.exe` is maintained export **brinespace-ae9fca1ccceaceb6**. Source SHA ae9fca1ccceaceb6bafdec644e62c275af4fe80631b96eb8a6b974d403c61df6; PCK SHA 4b1b668dcba7030d4de9e33519f14074e7ca7e5b6de70987b654dec3437b416d; EXE SHA 7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76. It includes the accepted normal SessionArtCache cleanup plus private navigation-edge, drone-storage and loading trials from physically frozen inputs. Normal Bill/provider source admission remains pending. Export restores temporary frozen Bill/Scope changes. Previous navigation-edges deliverable retained.

QA `qa-cold-hints` identity now names this candidate; exact old PCK duplicate replaced only after inactive check and hash match with retained old deliverable. One separate obsolete `qa-startup-window32` PCK duplicate was likewise removed after verification to make export space; retained startup-window32 deliverable unchanged. Records: `navigation-images-qa-replacement.json`, `navigation-images-qa-space.json`. Do not run these old QA folders without restoring their packs.

## Verification

- Export exits0; outside-checkout audit:36,288 files,55 remaps, zero missing/changed/unexpected. Saved expected manifest corresponds to frozen selected source, not restored source.
- Actual debug=false ten-cycle isolated40-room/title/Continue:825 checks,0 failures/errors/warnings/leaked-instance reports. Includes normal save path, full crew needs/RNG/foot/activity restore, fleet restore, Studio overlapping art ownership, indexed drone ownership/release, scene release and67,121 local-edge parity comparisons. It uses fixture-only free building/failure suppression and typing skip; it does not certify normal balance or full gameplay endurance.
- Read-only navigation inventory:0 images at all10 settled title returns; cache keys remain4 then59. No lazy getter/readback/truncation. Later restores reuse image-free snapshots while drawing views reload their own images.
- Reported settled title textures:250.985,254.088,254.623,254.658,254.693,254.728,254.763,254.798,254.834,254.869MiB. Cycle2→9 growth257,880bytes/0.0966%; constant36,840bytes per later transition remains unassigned. Do not claim no sustained growth or explain this without evidence.
- Large gameplay reported textures3.767–4.329GiB, still fail3GiB budget. First New Game6.932s, first large Continue6.905s, later4.920–5.070s. Cache uncontrolled/one process/fixture dialogue skip; no three-run cold/warm acceptance. Maximum loading draw gap403.801ms remains a responsiveness concern, not a measured gameplay stall.
- Final saved station capture inspected: room props/floors, compact needs bars and card/resource UI visibly present. Still-image inspection does not close original bug list, animation joins or all scaling checks. Captures retained as `navigation-images-ten-station-0.png` and `-9.png`.
- Owner2,936 non-log files unchanged across export, audit and native run. QA adapter restored byte-exactly; export frozen sources restored. All current validation processes terminal.

Evidence under `output/drone-compiled-2026-10-07`: `navigation-images-release-identity.json`, `navigation-images-expected-manifest.json`, export/audit logs and owner records; `navigation-images-ten-{summary,inventory,session-lifetime,loading-gaps,owner}.json` and native log. Summary generator explicitly asserts10 zero-image title inventories, no leases/jobs/library images and clean engine log.

## Next action

Prioritize remaining retained/duplicate GPU storage and measured rendering costs; finish navigation fallback/layout/invalidation admission before normal Bill installation. Attribute small residual title growth only with bounded read-only evidence. Complete original gameplay p95/p99, memory, responsive loading, original nine bugs, UI/motion, two-hour native soak, longer simulation, target PC and native Mac/signing/notarization gates. Current package is a private candidate, not certified for publication.
