# Marsh gestures and reactions

Updated: October14,2026 · BrineSpace · continued animation polish

## Objective and acceptance

Owner accepted cargo/work (“Those look better, keep going with the other
animations”). Preserve that selection and inspect social gestures, everyday
actions and reactions. Current gesture revision is installed for owner review:
`character/marsh-gestures-review-2026-10-14/review/index.html`.

## Accepted decisions and constraints

Accepted swimming, locomotion and welding stay selected. Marsh remains the same
sealed android with white synthetic fluid. Keep original social rules, state
timing, physical movement, save semantics and asymmetrical identity. Whole-body
authorship and deterministic extraction only; no grafted limbs or procedural art.

## Current state

Reviewed40 current clips/208holds: idle, conversation, kneel/tablet raise and
return, eating, drinking, ground/water shutdown and nonfatal fall/recovery.
South conversation used the older all-dark boots/body throughout its gestures,
causing a visible suit change when entering from current idle.

`character/marsh-gestures-polish-v1/manifest.json` now overrides only
`crew-chat-south`. Four generated complete gesture drawings match current ivory
boot panels, suit, face and planted stance. Four neutral holds use the exact
current south idle. The generated neutral calibrates the147px measured source
height and is unselected. One shared scale, boot registration and final sampled
sole correction preserve natural source geometry. Real alpha preserved; no local
body-part repaint, grade, morph or interpolation. Original eight durations
120/100/140/200/160/140/100/140ms, finite1.1s clip, pivot92/172,184canvas and148ruler
remain exact. Other39 reviewed states retain their selected source hashes.

Generated sheet, exact prompt and pose guide are in `sources/`; explicit crop,
scale, registration and hashes are in `provenance.json`. Deterministic builder:
`tools/build_marsh_south_chat_polish.py`, called last by the maintained rebuilder.
The new gallery has41 source/comparison WebPs and eight native videos. South
conversation is paired before/after; four-direction injury/recovery is retained.
Meal clips remain unchanged in this pass; broader seated/rest/meal body matching
remains possible future polish, not a newly accepted body revision.

## Verification

- New Python source contract passes:208 original source references unchanged,
  only south conversation's eight selected slots differ, state metadata/timing
  exact, generated whole bodies retain planted sole registration. Original
  selection fails four current-idle neutral holds; new selection passes.
- Engine gesture and current fall/rise joins:28checks/zero. Only Marsh south-chat
  changes in the full crew baseline; other actors/states/equipment and all other
  metadata exact, apart from derived alpha extent for revised drawings.
- Before and after actual main-scene fixtures each4,376checks/zero,496 native
  samples. Both runs exercise reciprocal conversations in all four directions,
  four full disk checkpoint restorations, pause and normal partner release, then
  physical-impact fall/recovery triggers in all four directions. All32 gesture
  and48 reaction source holds observed.496 paired foot/canvas/key/slot/phase/
  action-time records exact. Only40south-chat source samples differ; other456
  source images remain exact.
- Native rendered markers guard every frame. Eight final chronological boards,
  the source comparison and ten original family boards inspected. Native30Hz
  simulation movies skip the three-second listening interval. Chronological
  inspection and owner playback remain distinct; no claim of continuous real-time
  viewing, every death transition, furniture contact or fresh title-screen Continue.
- Engine crew complete packs, social, gesture joins, accepted work joins and
  torch attachments pass: `output/test-runs/20261014-215702-headless`.
  Expanded28join checks: `output/test-runs/20261014-215935-headless`.
  Original chat provenance/source tests pass. Builder reproduces exact bytes;
  all41 animated WebPs and eight native MP4s decode fully.
- One historical check remains failing:
  `tests/test_marsh_shutdown_injury_match.py` compares old material-remapped
  shutdown PNGs with the old rebaker's ungraded override and differs at an
  interior drawing. Its registration/provenance test passes. None of those
  source files, material mappings or rebaker override inputs changed in this
  pass; current selected injury/native and whole-crew baseline checks pass.
  Kept the failure visible rather than broadening this gesture repair into an
  unrelated historical rebuild change. Log: `output/marsh-gestures-2026-10-14/injury-sources.log`.
- All Godot runs use scratch APPDATA. All2,948 owner non-log files unchanged.
  Owner's existing app and concurrent unrelated work are untouched.

Fixtures/publisher: `tools/review_marsh_gestures_2026_10_14.gd` and
`tools/publish_marsh_gesture_review.py`. The existing conversation playtest now
resolves current selected manifest sources instead of asserting the historicalv2
PNG filenames. Before comparison can reconstruct the pre-repair chat selection;
the normal catalog stays current. Evidence: `output/marsh-gestures-2026-10-14/`.
An initial Python-only legacy test invocation inherited scratch APPDATA and could
not see user-site libraries; corrected invocation retained separately and did not
change dependencies or use the owner's save folder for Godot.

## Next action

Owner accepted the gestures: “Those look better, keep going with the seated and
resting animations next.” Changes remain selected. Continue with
`MARSH_REST_POLISH_2026-10-14.md`. No release rebuild, commit or upload.
