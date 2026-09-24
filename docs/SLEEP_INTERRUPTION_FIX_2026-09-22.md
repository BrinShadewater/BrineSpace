# Partial sleep interruption repair

Updated September 22, 2026. Project: BrineSpace.

## Objective and acceptance
Prevent existing human crew from jumping to fully reclined poses when a room loses
service partway through lie-down. Keep the current contact and reverse only the
motion already performed. This is an installed runtime fix, separate from the
unfinished bought-bunk controller.

## Accepted decisions and constraints
Preserve art, owner layouts, normal service/resource rules and full-sleep behavior.
Furniture-specific overrides retain their own duration. No generation, publishing
or commits for this fix.

## Current state
scripts/bill_npc.gd supplies interrupted_life_rise_seconds, inherited by Veld and
Branforth. Partial entry returns elapsed lie-down time; fully sleeping actors keep
the full rise duration. The existing service-loss branch already calls this hook.
A 0.0000001s bias resolves half-open reverse-frame boundary selection, capped at
full rise length and omitted at zero elapsed. No source or manifest pixels changed.
Marsh's existing furniture-specific override remains unchanged.

## Verification
A source probe first established matching human forward/reverse poses at 72 sampled
points. A separate exact-boundary probe exposed adjacent-pose selection at all 60
boundaries; the timing bias fixes those cases.

tests/test_sleep_interruption.gd passes 507 checks headlessly: three human actors,
four directions, six partial elapsed samples through actual service-loss update;
expected reverse pose pixels, contact offsets, no completion event and valid
snapshot checks; all 60 exact source-frame boundaries and full-sleep duration
controls. Indexed in crew tests and paired with a Godot-generated UID.

The native Marsh berth regression also passed after adding the inherited hook:
arrival, five disk restores, pause, partial reversal, completion, low battery and
invalid-save cases. Its override was not modified by the later boundary bias.
Logs in output/layout-default-audit-2026-09-21/: sleep-interruption-final.log and
marsh-berth-after-human-interruption.log. This is not a new packaged-build test or
an autonomous expedition/owner visual acceptance claim.

## Next action
Continue the bought-bunk furniture-specific profile, equipped art and complete
cast motion. Reuse partial-reversal semantics and test its own frame boundaries,
contact anchors, save/restore and ordinary travel before live acceptance.
