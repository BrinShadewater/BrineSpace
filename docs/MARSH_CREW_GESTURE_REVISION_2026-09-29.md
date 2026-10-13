# Project handoff

Updated: 2026-09-29 · Project: BrineSpace · Task: repair Marsh crew gesture anatomy

## Objective and acceptance

Owner rejected v1: his body did weird things. Correct the paired conversation gesture, especially doubled/disconnected side-view arms. Revision 2 is installed and owner visually accepted it ("Okay looks good"). Technical verification and owner visual acceptance are recorded separately.

## Accepted decisions and constraints

Keep approved android identity, fixed head/neck/stance, 148px calibration, 184px canvas, foot pivot (92,172), exact idle joins, and existing 1.1s speaking gesture. Preserve the six-second paired conversation and three-second turns, injury/charging priority and checkpoint format. No gameplay change in this revision.

## Current state

- `character/marsh-crew-chat-v2/`: four independent built-in image_gen strips and exact prompts, complete-arm masks, 32 registered exports, manifest, frozen installation hashes, contact sheet and four native/source previews.
- Complete moving arm replaces the old hanging glove in side views. Head translation removed. Every pixel outside the documented arm polygons is canonical idle. Centre torso remains original except where the foreground hand/arm occludes it.
- First v2 sheet remake retained duplicate arms and was rejected; preserved with status. v1 remains preserved, overridden by v2 in the catalog. Earlier v1 visual-review claims do not establish acceptance.
- New preparation and publishing tools; canonical rebaker selects v2; colour guard freezes its new paths. Current consistency source review resolves 204 states / 1,058 slots / 27 chains and links the revision.
- Updated source test protects all pixels outside each arm polygon. Native fixture additionally checks exact v2 loaded pixels for every slot.

## Verification

Native paired conversation: 220 checks, 36 room captures, zero failures, all four facings, all 32 loaded v2 slots, four disk restores and pause. Two source/provenance tests pass. Colour guard: 8,691 PNG paths, 1,031 prior approved corrections, zero errors. Five changed Python files compile and revision review links resolve. All four complete pose rows and native peak-gesture room captures inspected; small compact motion retains four authored interior poses rather than interpolated video. Prior full-set native report remains evidence of its prior revision, not fresh v2 proof.

All 2,730 pre-existing real-profile fingerprints unchanged; four test files appeared during this shared session (`test_large_room_studio.json`, its recovery file, `large_revision.meta` and its backup). This task ran Godot with scratch APPDATA. Their origin is not established here; no owner-profile files were changed or removed by this task.

## Next action

No remaining work for this gesture. Preserve accepted revision 2 and existing Marsh actions. No commit or executable export requested.
