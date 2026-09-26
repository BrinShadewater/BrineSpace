# Marsh bought-bunk integration

Updated: September 22, 2026. Project: BrineSpace.

## Objective and acceptance
Integrate Marsh's bought lower-bunk motion while preserving the legacy berth,
charging behavior and movement clearance. All four cast now have a profile for
the reviewed unmirrored bunk, but broad autonomous and release acceptance are open.

## Accepted decisions and constraints
No helmet variant, owner layout edits, Higgsfield, commits or publication. Bought
bunk and legacy berth contact are mutually exclusive saved profiles.

## Current state
scripts/marsh_npc.gd owns the 1.84s bought-bunk entry/rest/rise and contact offsets.
Its low-battery path finishes rising before charging travel. Shared validator timing
accepts the nonhuman bunk duration; Marsh validates anchors and rejects conflicting
profiles. crew_room_activity.gd registers the actor-specific station; shared bunk
claims include Marsh. tools/build_marsh_bunk.py installs the supplement through
rebuild_marsh_art.py. finalize_crew_art.py excludes bunk contact from his shared
movement envelope, as it already does for the legacy berth. The native indexed
test tests/test_marsh_bunk.gd has Godot-generated UID dimeen7n2yud2.

## Verification
Evidence: output/layout-default-audit-2026-09-21/.
- marsh-bunk-controller-final.log: normal chooser/arrival, seven disk restores,
  exact source pixels, pause, reversal/service interruption, completion, shared
  claim, invalid/conflicting saves and low-battery rise-before-recharge; zero failures.
- marsh-legacy-after-bunk.log: existing native berth regression passes.
- marsh-battery-after-bunk.log: battery test passes, 93 route samples.
- sleep-interruption-after-marsh-bunk.log: 507 checks, zero failures.
- marsh-bunk-rebuild.json: all 52 inventoried catalog/clearance/supplement files
  unchanged after supplement rebuild/finalization, including legacy berth files.
- Restored native sleeping capture inspected in output/crew-activity/marsh-bunk/.
- Full canonical rebuild reproduced 211 source frames. First parity comparison
  changed two manifests solely through carry-direction key order; reconstructing
  that order reproduced both pre-build hashes exactly. The writer now sorts the
  set before serialization. The first sorted run normalized the key order; a second independent run
  reproduced all 732 inventoried files exactly, including clearance. Evidence:
  marsh-bunk-canonical-repeat-parity.json.
These are controlled fixtures, not a full expedition or packaged release test.

## Next action
Run broader autonomous multi-crew use of the bought bunk, then return to remaining
furnishing, bug/performance work and current release packages. Apple Silicon
runtime acceptance remains pending.
