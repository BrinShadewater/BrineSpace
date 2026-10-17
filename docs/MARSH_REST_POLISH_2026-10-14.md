# Marsh seated and resting polish

Updated: October14,2026 · BrineSpace · animation polish

## Objective and acceptance

Owner accepted the gesture pass and requested seated/resting animations next.
Review sitting, reading, lying, sleeping and rising against current identity and
actual furniture. New result is installed for owner review at
`character/marsh-rest-review-2026-10-14/review/index.html`.

## Accepted decisions and constraints

Retain accepted swim, locomotion, work and conversation changes. Existing normal
station-prop bunk and its support choreography remain authoritative; old bought
berth furniture is compatibility evidence, not a current-room replacement.
Preserve owner layouts, gameplay, clocks, movement and furniture registration.
Whole generated bodies only; no arm grafts or procedural pose invention.

## Current state

Reviewed34selected rest states/120holds. South sitting/reading still used the old
dark-boot body. Seven complete matching drawings now cover lowering, seated
neutral/breath and three tablet-reading poses. The same lowered bodies play in
reverse for rising. Exact current idle joins standing entry/exit. Generic south
lie-down/get-up also use current idle at their standing endpoints; interiors
remain exact. Six states/15holds change; other directions and all current bunk/
compatibility berth bodies are retained.

Selected override: `character/marsh-rest-polish-v1/manifest.json`.
Original state durations, loop flags,184canvas,pivot92/172,height148, depth/water
metadata and all physical offsets remain exact. No game-controller change.
`tools/build_marsh_rest_polish.py` is called by the maintained rebuilder.
Raw generation, exact prompts, reference guide and extraction provenance are
preserved. Neutral establishes a single147px measured-density scale; it is not
selected. Boot registration is checked after sampling. Generated source has
transparent alpha with hidden RGB haze; packaging clears invisible RGB and
retains the body/antialias fringe. A second unnecessary cutout redraw is retained
unselected. No furniture pixels or owner layouts changed.

`tools/review_marsh_rest_2026_10_14.gd` records actual reachable furniture arrival,
actor updates, held stage and rise. Nine cases: lounge/observation four rotations
each plus current bunk. Real contacts resolve north for lounge, south for reading
and east for bunk; these rotations do not imply four character facings. Long held
intervals are shortened after1.2s, so the gallery emphasizes transitions.
Publisher: `tools/publish_marsh_rest_review.py`. Gallery has34source clips,
four paired source comparisons and nine25fps native room movies.

## Verification

- Python source/contract checks pass: all120original references unchanged;
  exactly six states/15selected holds differ. Whole generated bodies fit original
  canvases and keep sampled planted soles. All metadata except revision retained.
- Engine rest joins/reversals:64checks/zero. Current crew baseline differs only
  those15Marsh holds/derived alpha extents. All other actors, states, equipment,
  timing and metadata remain exact, including accepted prior passes.
- Before and after native:7,211checks/zero each,739samples each. All739 foot,
  offsets, head alignment, canvas position, keys, slots, timers and action/player
  clocks match. Publisher independently checks every before source against the
  frozen selection. Only256south-reading native source samples differ; lounge
  and bunk source samples remain exact. Current rendered markers and transformed
  selected-alpha bounds guard each native crop.
- All nine final native chronological boards inspected, plus source family boards
  and generated comparison. Reading body/tablet remains visible on the chairs;
  bunk support and exit remain intact. Native lifecycles are actual controller
  playback with prescribed reachable arrivals and shortened held intervals, not
  autonomous approach, continuous real-time viewing or all-furniture acceptance.
- Current bunk native regression:117checks/zero, normal chooser and ordinary
  arrival, seven actual disk restores, pause, reverse interruption, completion and
  invalid-save rejection. Log: `output/marsh-rest-2026-10-14/bunk-native-restores.log`.
  Retired berth test was not run; generic/compatibility source review is distinct
  from current station-prop bunk integration.
- Crew complete packs, crew life72room/rotation/actor cases, accepted gesture
  joins and new rest joins pass:
  `output/test-runs/20261014-221421-headless`. Builder reproduces exact bytes;
  all38animated WebPs and nine native movies fully decode.
- Every Godot run used scratch APPDATA; all2,948owner non-log fingerprints remain
  exact. Owner's pre-existing game and other chats' processes left untouched.

Evidence: `output/marsh-rest-2026-10-14/`. Initial incorrect crop transform and
overly large fixed-margin checks are retained separately. Final capture guard
uses transformed actual alpha bounds with2px padding. A native-only bunk fixture
was initially invoked headless and timed out waiting for frame_post_draw; its log
is retained, and the successful native run above supersedes that invocation.
No runtime/test contract was relaxed. Earlier disclosed historical shutdown-source
rebaker failure is unchanged and was not rerun for this seated-source repair.

## Next action

Owner rejected the corner lounge armchairs' facing after this review. Their
omission supersedes the earlier lounge presentation; see correction below.
Further everyday meal polish remains a
separate family if requested. No game export, commit, upload or automatic follow-up.

## Corner-chair correction — October 14, 2026

Objective/acceptance: avoid Marsh sitting the wrong way in angled corner lounge
armchairs. Owner explicitly permits omitting those seats.

Accepted decision: omit `library/sp-crew_lounge-4` contacts for Marsh, including
copied/variant props. Preserve other actors and furniture. No new seated art.

Current state: `scripts/crew_room_activity.gd` filters the corner armchair from
Marsh's station list, shared by choosing goals and beginning activities. His
existing geometry actor marker identifies the profile. Default lounge rotations
have no reachable alternative seat; do not claim a bench replacement. Historical
`seated_contact` fallback remains for saved seated actors to finish their rise.
`tools/publish_marsh_lounge_contacts.py`, also called by the main rest publisher,
removes the four rejected clips from the current gallery. Historical evidence
and movies remain on disk. Source art, furniture and owner layouts unchanged.

Verification: rest joins/contact regression adds Marsh/copy exclusion, unchanged
Bill armchair contacts and retained straight-bench station support. Native
fixture checks former corner contacts cannot begin sitting in all four lounge
rotations, then captures the four reading layouts and bunk. Final receipts and
owner profile guard are recorded in `output/marsh-rest-2026-10-14/corner-*`.
Final results: 69 source/contact checks and 4,139 native checks, zero failures;
423 reading/bunk samples retain exact prior clocks, poses and physical/visual
positions. Gallery omits all four chair cards. All 2,948 owner non-log files
retain exact fingerprints.
An initial run correctly found no reachable lounge seat; its old fixture still
required one and failed four assertions. The revised fixture checks authorized
omission explicitly rather than forcing a replacement seat.

Next action: owner can review the remaining seated/resting clips. No additional
corner-chair animation work is required by this decision.
