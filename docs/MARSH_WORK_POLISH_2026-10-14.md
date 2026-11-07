# Marsh cargo and work polish

Updated: October 14, 2026 · BrineSpace · continued animation polish

## Objective and acceptance

Owner accepted the east-run correction (“That looks better, keep going”). Keep
that selection and inspect pickup, carrying, unloading, tablet work and welding.
Current cargo/work changes are installed for owner review in
`character/marsh-work-review-2026-10-14/review/index.html`.

## Accepted decisions and constraints

Preserve accepted swimming, locomotion, timings, stride, registration, android
identity and gameplay rules. Use complete selected drawings for anatomical joins;
no generated replacement art was needed. Construction sparks still land at the
doorway as the owner previously requested. Other crew and owner layouts stay exact.

## Current state

- Reviewed 44 selected dry cargo/work clips, 232 holds, against directional idle.
  Four pickup/carry/unload source chains and all individual clips are in the gallery.
  Cargo grips and endpoints retained; tablet actions retained.
- South `torch-draw` slot0 and `torch-stow` slot5 used an older standing body.
  `character/marsh-work-joins-v1/manifest.json` now supplies the exact selected
  south idle with transparent padding. All ten interiors, the welding loop and
  original 184×237 canvas / pivot92,172 / height148 / timing remain unchanged.
- Native inspection exposed sparks floating above the torch. The shared old
  world-unit offsets did not fit Marsh's current source density or moving reach.
  `scripts/station_effects.gd` now selects his measured flame attachment by the
  actually submitted welding texture. Twenty-four measured anchors convert source
  pixels through the renderer's 65.28/148 physical ruler. Construction's existing
  doorway override is unchanged; no per-frame image readback or hashing is added.
- Deterministic builders: `tools/polish_marsh_work_joins.py` and
  `tools/build_marsh_torch_tips.py`, called by `tools/rebuild_marsh_art.py`.
  Source PNGs and measured coordinates/hashes are retained. Crew baseline changes
  only the two endpoint slots and their derived alpha extent; all other actors,
  states, timing, strides and equipment remain exact.
- `tools/review_marsh_work_2026_10_14.gd` supplies current native room/source
  captures. Publisher `tools/publish_marsh_work_review.py` makes four 60fps videos,
  including paired south, plus full-height source WebPs that retain the low torch.

## Verification

- Python source/contract checks pass: all original 232 PNG references unchanged;
  only the two selected endpoints differ; authored metadata preserved. Original
  selection fails the two south idle joins; corrected selection passes.
- Selected engine handoffs:52 checks pass. Torch attachment:26 checks pass,
  including out-of-order pose submission and unchanged construction-door policy.
- Native before:1,457 checks/zero,204 samples. Final after:6,242 checks/zero,
  816 samples across four directions, all18 torch holds/direction. Each rendered
  sample has a current viewport marker and whole actor crop. Actual flame-pixel
  attachment checked through432 working samples. The south204 physical-foot,
  canvas-position, key, slot and player-phase samples match exactly.
- Four final native chronological boards inspected, alongside all11 family source
  boards and the standing comparison. Four MP4s and48 full-height animated WebPs
  decode; both builders reproduce exact bytes. This is chronological inspection
  and prescribed advancing construction timers, not continuously watched real-time
  playback, autonomous dispatch or proof of every furniture contact.
- Crew complete packs, walking, east-run registration and prior locomotion joins
  pass: `output/test-runs/20261014-213146-headless`. New attachment, joins and crew
  loader pass after the effects change:
  `output/test-runs/20261014-214001-headless`.
- Paid construction originally failed88 times on an old walking-only 4.61-unit
  bound. Historical-art control reproduced the same88 failures; movement probe
  showed normal 6.9-unit run steps. The assertion now allows6.91 only on steps
  entering/continuing/leaving Marsh's existing run; other steps retain4.61.
  Paid construction then completes all four directions with zero failures,
  including pause and disk checkpoint restoration. No movement code changed.
- Every Godot run used scratch APPDATA. All2,948 owner non-log fingerprints remain
  exact. Owner's pre-existing app and concurrent unrelated work remain untouched.

Evidence: `output/marsh-work-2026-10-14/`. Initial bad crop and technically passing
but unpaired cosmetic-clock captures are retained separately. Final fixed-clock
before/after reports and final gallery supersede those attempts. Before comparison
can be rebuilt with the pre-repair catalog and old shared spark offsets in the
fixture; the normal catalog remains current throughout.

## Next action

Owner accepted cargo/work: “Those look better, keep going with the other
animations.” Changes remain selected. Social gestures/reactions follow in
`MARSH_GESTURE_POLISH_2026-10-14.md`. No release rebuild, commit or upload.
