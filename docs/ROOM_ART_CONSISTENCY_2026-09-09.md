# Room art consistency handoff

Updated: 2026-09-09 · Project: BrineSpace · Task: room materials and radio headphone scale

## Objective and acceptance

Apply the room/art consistency findings to the game. The owner said the art looked good except for oversized radio headphones. Those headphones have now been reduced on both directional wall banks and the shared floor console, and checked beside Bill at native crew scale. Final headphone correction has agent visual review; owner acceptance of that correction is still pending feedback.

## Accepted decisions and constraints

Keep each department’s palette, quieter matte machinery, owner-authored large prop layouts and explicit prop removals. Preserve the restored BRINE room. Original source assets remain available. No gameplay balance, room layout, portrait selection or release publishing is part of this pass.

## Current state

- `assets/room-consistency-v1/`: 17 source identities, 16 selected repainted sources, 39 total recorded original/candidate versions, exact prompts, previous registrations and six final native card bakes.
- 17 JSON registrations in `rooms/full-wall-v1/registrations/` bind the selected directional art. `final-registration-report.json` records final source and registration hashes, including the headphone revisions.
- Radio, shield and salvage room view scripts bind repainted equipment separately from original structural hull textures. Pressure control uses its refreshed fitted source. Listening Post inherits the radio equipment change. These are six affected room families.
- `scripts/room_card_art.gd` and `scripts/grid_canvas.gd` select the six refreshed `cards-final` images. Existing unrelated work is preserved.
- `tools/audit_room_dressing_hosts.gd` now recognizes explicitly deleted layout hosts and the renderer’s existing baked quarter-zero branch. Unknown missing hosts remain errors.
- [Native review gallery](room-art-consistency-2026-09-09/review.html) includes headset scale, six detailed before/after room comparisons, all 188 native views and dispositions for all 47 rooms. The other 41 rooms retain existing art after this review.

Some source canvas dimensions shifted slightly during generation. Registration accommodates this without changing world layout rectangles; source geometry is not asserted to be pixel-identical. No broad desaturation filter or per-frame image processing was added.

## Verification

- Complete 47-room × four-rotation native capture, followed by 16 refreshed views after equipment/headphone fixes. Merged `output/room-material-consistency/final-report.json`: 188 views, zero editor/runtime layout differences. All final overview contact sheets and six detailed room comparisons visually inspected.
- Source audit: 17 identities and 39 recorded versions verified. Final 17 registration/source hashes independently checked.
- Dressing audit: 39 profiles, 448 references, 47 catalog rooms, zero errors. Explicit owner deletions are classified rather than restored. Negative control fails with exactly the injected missing host.
- Card catalog check: all 47 identities pass; six cards rebaked natively and primary/grid/variant bindings agree.
- Native headphone capture at a 344-unit bank beside 65.28-unit Bill: exit zero, no errors. Log: `output/room-material-consistency/headphone_scale-1788991888621534800.log`.

Evidence is native editor/source-checkout validation, not an exported executable test. Historical failed/intermediate captures remain in ignored output; final evidence is identified above. Later concurrent source changes are outside the captured revision.

## Next action

Review the corrected headset and six room comparisons in game or the linked gallery. Further art edits should follow concrete feedback. No executable rebuild, export, commit or push was performed for this pass.
