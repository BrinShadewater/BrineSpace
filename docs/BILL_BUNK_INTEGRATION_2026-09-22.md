# Bill bought-bunk integration

Updated: September 22, 2026. Project: BrineSpace.

## Objective and acceptance
Connect Bill's reviewed bare/equipped bunk motion to gameplay with the reduced
helmet fit, preserved body scale, save/restore and interruption behavior.
Working-tree integration is installed; broad goal and release acceptance remain open.

## Accepted decisions and constraints
Preserve owner layouts and existing generic crew movement. No Higgsfield, commits
or publication. Keep Bill-only presentation out of other crew's base controller.

## Current state
- scripts/major_bill_npc.gd extends the existing shared bill_npc.gd, following the
  existing Veld/Branforth profile pattern. main.gd instantiates it; run_save.gd uses
  its typed validator. Other crew keep the original shared base.
- crew_room_activity.gd registers Bill's reviewed bought-bunk profile and the shared
  destination-claim check includes it.
- tools/build_bill_bunk.py installs bare/equipped supplements in major-bill-v3;
  rebuild_bill_art.py invokes it after the ordinary canonical build.
- main.get_test_walker_state now reads active Bill's actual controller state.
  Native review caught the old cached standing pose after a paused restore even
  though direct texture checks passed. The test now exercises the production getter.
- tests/test_bill_bunk.gd covers normal choice/arrival, shared claims, fourteen
  disk restores and actual source pixels, pause, partial/service interruption,
  completion and invalid saves. It is indexed in the native crew lane.

## Verification
Evidence: output/layout-default-audit-2026-09-21/.
- bill-bunk-controller-render-final.log: zero failures, including production getter.
  Corrected native restored equipped sleeping image inspected in
  output/crew-activity/bill-bunk/restore-helmet-1700.png.
- sleep-interruption-after-bill-bunk.log: 507 checks, zero failures.
- marsh-berth-after-bill-bunk.log, veld-bunk-after-bill.log and
  branforth-bunk-after-bill.log: native regressions pass.
- bill-bunk-canonical-rebuild.log completes; bill-bunk-rebuild.json reports all 2431
  inventoried PNG/JSON files unchanged, including catalog, supplement and clearance.
- Focused whitespace check passes. Initial fixture run failed because it assumed
  Bill had a private RNG; the test now creates its own seeded RNG explicitly.
Full expedition, owner motion and packaged release validation remain separate.

## Next action
Finish Marsh's bought-bunk profile and broader autonomous multi-crew review, then
continue furnishing/performance and release work. Preserve Marsh's working legacy
berth behavior. Refresh packages and run actual release checks before claiming
Windows/Mac acceptance.

Godot generated UID pairs: major_bill_npc.gd = bucuukwry78yf;
test_bill_bunk.gd = bu0py3go4ll82.
