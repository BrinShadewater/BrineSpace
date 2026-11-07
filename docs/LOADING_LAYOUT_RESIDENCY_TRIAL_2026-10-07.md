# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: loading viewport/layout residency

## Objective and acceptance

Remove second-long startup preparation stalls without retaining unnecessary art or showing incomplete interactive rooms. Full original release gates remain open.

## Accepted decisions and constraints

Physical package66929cd10addc5b0 unchanged. Experimental external adapters only; no normal admission. Keep owner layouts, art, quality, runtime PNG loading and diagnostics. Single cache-uncontrolled comparisons do not certify loading gains. Reject all-ward preparation as a production selection policy.

## Current state

Bounded source-key snapshots (512 maximum per inventory, complete in the observed gaps) and actual viewport/ward lists added to the prior environment preparation fixture. New Game's largest1,140.355ms gap changes viewport from origin(0,0) to(5898,6102), size1328×920. The earlier ready-time viewport has no visible wards; after camera layout, river(20,18), josh(22,20), margot(20,22) enter view. That gap adds23 library source paths, no new whole-room source paths. Continue changes viewport size0×0→1328×920 at(9593,9593), with only josh/margot visible, adding20 library paths. Full source lists: output/drone-compiled-2026-10-07/loading-residency-summary.json.

RoomAssetLibrary.template loads raw PNG bytes directly rather than via SafeImage/ImagePrefetch. Consequently those late library loads do not use existing startup worker order or progress pumping. This is a specific preparation/loader integration gap, not a proof that every unexplained millisecond is PNG decode.

Diagnostic superset then calls existing bill_room_geometry for currently placed rooms and every uncleared companion ward before the first station presentation, servicing loading between rooms. New Game preparations: core210.618ms, salvage117.205ms, storage195.557ms, cryo71.670ms; total596.024ms including pumping. Continue total178.662ms. The current callback's lists contain core plus three wards in both cycles; do not assume this describes the restored station's complete room set. Production preparation must run after restoration and final camera layout, rather than use this ready-time superset.

Against residency control, New Game max1,140.355→629.151ms; elapsed12,276.723→12,379.470ms (no total gain). Continue max994.546→844.149ms; elapsed4,509.672→4,705.913ms (slower). Gaps>100ms increase79→82 and24→26; existing120ms pumping contributes. No loading gate closure.

At equivalent before-drone-exercise labels, reported texture memory increases11,184,808bytes in New Game and42,213,095bytes (~40.26MiB) in Continue; library source count35→35 and26→32 respectively. Counts alone do not prove equal backing storage. The extra six Continue sources and increased memory make this superset unsuitable for admission. Exact final-state visual/resource comparisons remain pending.

## Verification

Residency and layout-superset runs each pass142 actual debug=false lifecycle checks with zero failures/errors/leaks/warnings. All owner fingerprints2,936 files unchanged; processes terminal. Raw packaged-loading-residency and packaged-loading-layout-prewarm gaps/lifecycle/logs/owner JSON retained. Fixture identities and archived adapters in qa-helper; matched station adapter restored. No packaged runtime source was changed.

## Next action

Implement a private production-path trial after checkpoint restoration with explicit viewport settling and pause/input ownership. Select actual visible room/ward layout resources and integrate late library image loading with bounded startup decoding/progress. Compare decoded/source inventories and texture endpoints, complete native pixels/clock checks, then repeated packaged loading before admission. Preserve larger sustained renderer, memory, drone admission, original bugs, endurance and PC/Mac certification work.
