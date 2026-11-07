# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: ordinary prop submissions normal admission

## Objective and acceptance

Reduce regular renderer work while preserving art/order/filter/materials and scoped lifetime. Original complete PC/Mac release gates remain active.

## Accepted decisions and constraints

Installed in normal scripts/room_content_canvas.gd:eligible unsplit library props combine ordered float-color body/shadow triangles, then original live output. Existing split path unchanged. Portable/custom/drone/aquarium paths remain original. Slot-owned cache releases hidden/unused/reclassified entries and excluded props. Internal --separate-ordinary-bases retains original comparison path; no user quality option. No new images/materials/nodes/global cache or art changes.

## Current state

Changed existing normal module (existing UID preserved); new tests/test_ordinary_prop_triangles.gd and test_ordinary_prop_triangle_cache.gd with paired unique UIDs/native render-perf index. Evidence output/ordinary-prop-triangles-2026-10-06/{composition,normal-cache,normal-art,normal-split,normal-large,normal-station} receipts/logs/JSON.

## Verification

Private actual LIVE composition12exactpairs(all40bounds/248visibleordinaryslots/activeBRINE signals) pass across3zooms×idle/flood/launch/return. Normal-source96exact nonblank artpairs/12currentsources pass(mirror/nearestlinear/flood). Normal30cachechecks/12exacttransitions/9builds pass includingstable/move/resize/mirror/pieces/texture/floor/hide/unused/reclassification/ownerrelease and excludedclass cache removal. Initial excludedportable fixture calledreal bounds with incomplete mocked portable metadata; corrected synthetic bounds handling before clean authoritative normal result. This tests classification cleanup, not new portable rendering.

Existing normal split-cache26checks/12pairs and large-room135checks/80pairs pass, zero errors/cleanexit. Unique pairedUID/index/whitespace checks pass. No unrelated full asset/test batches.

Installednormal matched physical40room six60sample phases, same current normal content modules and internal comparisonflag, both same private six-sheet drone/crew fixture. Positive157ordinaryholders/157→164builds/667→679callbacks verified. Allsix fullcrew/drone/door/light/power/zoom snapshots and texture endpoints identical; no engine/missingart errors. RendererCPUlower allsix by0.73–1.06ms; ~461–463fewerreported drawcalls. Prior prototype matchedpair also showedlowerCPUallsix .95–1.77ms; these establish local renderer benefit, not universalFPS.

Normal p95reference→candidate:1xidle45.902→46.710,1xpan49.474→49.363,2xidle45.958→44.757,2xpan47.910→46.923,4xidle50.954→51.352,4xpan55.974→54.962ms. Whole-frame results mixed/stillfail16.7ms; no normal memorysaving/loading/packaged/Mac acceptance. Privatetexturefinal2776.236MiBidentical. Every owner2936non-log fingerprint unchanged; all processes terminal. Normal-source hashes and verified comparison retained.

## Next action

Continue larger steady frame preparation (~22ms after explicitstep) and remaining renderer/backend work, preserving full-quality exact output. Profile remaining large-room base/seabed/line preparation before choosing another cache. Six-sheet indexed drone provider still private: actual Main title/save/Continue and complete dock/exterior/material lifetime remain before normal admission. Full normal texture/loading budget, original packagedbugs/endurance and Windows/Mac certification remain open.
