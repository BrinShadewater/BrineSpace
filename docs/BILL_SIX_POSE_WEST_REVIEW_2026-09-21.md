# Bill six-pose west candidate

Updated September 21, 2026. Project: BrineSpace. Broad goal remains unfinished.

## Objective and acceptance

Replace the repeated west half-cycle with a connected alternating stride, without
losing Bill's appearance or introducing detached feet. This is a staged candidate,
not a selected runtime change. Earlier four-key study is preserved separately.

## Decisions and current state

Sources and exact prompts remain in
`character/major-bill-v3/sources/west-walk-alternation-2026-09-21/`.
Three new built-in image_gen edits produced `passing-b-low.png`, `down-a.png` and
`down-b.png`. Nine generation calls belong to the full alternation study so far;
rejected sheets/reach art remain explicitly rejected. No Higgsfield or API fallback.

Candidate order: near-forward contact, near-leg weight transfer, near support/far
swing, far-forward contact, far-leg weight transfer, far support/near swing.
The lower passing revision keeps the foreground leg and reduces its knee lift.

`output/bill-six-pose-west-2026-09-21/` contains reproducible staging scripts,
manifests, twelve bare/helmet frames, registration, native fixtures and review
media. Existing six-frame timing170/130/150/170/130/150ms and stride are retained.
Each large source uses the common146/919 scale; the lower-resolution row contact
uses146/467. Whole bodies are aligned by head-band center and sole baseline.
No independently moved boots/shins or pose-height normalization. Derived alpha
cleanup removes values1..16; raw sources stay intact. Normal48x56 helmets follow
per-pose head anchors, preserving all lower-body pixels exactly.

## Verification

- Six opaque-body bounds fit184x184; pivot92,172 and standingHeight148 retained.
- Native selected/candidate comparisons:27frames each bare and helmet, no missing
  textures, identical900ms phase progression. Full-size and384-unit room-scale
  views inspected. Two GIFs preserve900ms using30/30/40ms encoding.
- Initial paid opening captured240samples but only24west walks before a north
  turn; coverage gate failed (exit1). This is retained, not called a passing test.
- Extended paid opening exited0:480samples,80unpaused west walks,182west idle
  samples plus east/south travel. One additional west sample has pause=true.
  Costs/failures remain enabled. Candidate is bound after room setup and the
  actual frame getter is checked on every west walking frame. Setup, manual30Hz
  stepping and actor-follow camera remain fixture limitations.
- All actor crops fit the viewport. Station context inspected. Consecutive first
  120samples are packaged at15fps into `station-walk-stop.gif`, preserving the
  brief dialogue pause and subsequent stop; it is not a stitched idealized loop.
- Registered bare/helmet walk/idle/kneel comparison inspected. Candidate walking
  has simpler/smoother lower-body detail than current idle/work. That mismatch
  remains visible and prevents declaring final art consistency.
- Twelve selected bare side-walk hashes remain unchanged. No production art,
  controller, rooms, timings or release files were changed. No tests of a newly
  installed pack are claimed. `six-pose-review.json` records source hashes/results.

## Next action

Use the owner motion feedback requested alongside the comparison to guide the
next refinement. Resolve the walk-to-idle/work detail difference and inspect
anatomical contact through the cycle before selecting this art. Then make the
canonical rebuild reproduce the reviewed bare/helmet frames, verify affected and
unaffected outputs, and run installed consumer/station checks. East still uses
current source poses; no full-direction or expedition acceptance is implied.

## One-pose surface detail follow-up

The tenth built-in generation in this study is `detail-down-b-source.png`, with
exact `detail-down-b-prompt.txt` beside it. It adds finer suit seams and structured
kneepad edges to the same down-B pose. Its raw upper body is not selected.

`output/bill-walk-detail-2026-09-21/review.py` makes a deterministic RGB-only
transfer inside a recorded lower-body polygon, only where both original and edited
alpha are at least128. The original alpha is retained everywhere; pixels outside
the mask and the entire source above y710 are exact. No limb geometry is moved.
After the same registration/resampling, the complete alpha and upper100rows are
also byte-exact to staged candidate04. The delta is83,766source pixels and
2,274registered pixels, all from the intended surface edit.

`detail-comparison.png` was visually inspected beside current idle and the prior
candidate at the same scale. Seams/panel definition are closer, without broken
ankle contours. This remains a single-pose candidate; it is not included in the
six-pose manifests or their earlier native acceptance. No production change.
Raw art, mask, hashes and registration are recorded in `detail-review.json`.
Continue only with comparable pose-preserving corrections across the cycle;
review whether the resulting full sequence is more consistent before selection.

## Full surface pass and production-compatible candidate

The eleventh built-in generation is `six-pose-detail-source.png`, edited from the
recorded transparent2x3 pose atlas. Exact prompt/reference are beside it. The
generated source includes soft background/edge alpha and is never selected raw.
`output/bill-six-pose-detail-2026-09-21/build.py` transfers RGB only below y122,
inside the original alpha eroded by a3x3 minimum filter. Original upper122rows,
one-pixel contour and all alpha remain exact at this intermediate stage. Six
same-scale before/after poses were inspected; shin/boot detail is closer and
foreground/far-leg ownership remains distinct.

Pre-integration inspection of `validate_bill_art.py` exposed the production hard-
alpha contract: the staged Lanczos images still carried partial alpha. The checks
were not weakened. `output/bill-six-pose-finalize-2026-09-21/build.py` thresholds
alpha at128, clears transparent RGB and checks canvas borders. This finalization
changes the earlier soft-alpha invariant deliberately; retained opaque RGB stays
exact. Earlier source/raw studies and their evidence remain untouched.

Final candidate: six bare plus six helmet frames,184x184,pivot92,172, standing148,
normal48x56 helmet, existing900ms timing/stride. Finalized native comparison
captures27frames per equipment variant with matching phase and no missing textures.
Bare/helmet renders inspected; GIFs retain900ms each. The earlier paid opening
belongs to the preceding surface version, not a new installed-art acceptance.

New maintained `tools/build_bill_alternating_west_walk.py` reproduces all12final
decoded frames exactly. It reads frozen `walk-registration.json`, checks source
hashes, replays whole-body registration, surface masking, alpha finalization and
helmet fits, then checks decoded output hashes. It has NOT yet been selected by
`tools/rebuild_bill_art.py`; no production frames or releases changed.

Next concrete integration: select the helper for walk-west only, keep east's
connected-source recipe, update the review exporter and source-preservation tests
to distinguish these two recipes, compare all changed/unchanged outputs, and run
full library/consumer plus installed native checks. Do not claim owner approval,
complete foot locking, east repair or a new release from these staged results.
