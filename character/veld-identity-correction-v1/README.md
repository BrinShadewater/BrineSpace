# Veld identity correction

Dr. Veld is a woman, with medium-brown skin, a silver-streaked dark bun,
cobalt Science markings and ivory chest panels. No glasses under her helmet
or in bare-headed poses. Canonical reference: ../dr-veld-v1/concept-01.png.

## Current state

All four directions of idle, walk, scanner and kneel/sample/stand are selected:
26 body clips and 24 equipment variants, 312 frames, including east helmet
donning/removal. Original timings and exact
corrected idle/action endpoints remain authoritative. The broader identity and
full three-character replacement goal remains open.

Built-in image generation authored sources/turnaround-01.png and
sources/east-sample-heads-01.png; exact prompts are saved beside them.
The turnaround is a face reference only: generated body equipment differs
between rows, including rear vial side. The original concept controls identity.
Independent pre-correction body/equipment frames are retained under sources.

## Reproducible pipeline

- tools/prepare_veld_directional_identity.py fits south/west/north idle and walk
  heads directly from raw art, preserving original equipment/body placement.


- tools/prepare_veld_identity_reference.py extracts eight identity views.
- tools/prepare_veld_east_identity_chain.py fits pose-matched authored heads to
  each corresponding original body, using a shared ruler and exact endpoint copies.
- tools/veld_scanner_revision.py selects explicit states and translates the
  study pivot128,224 to the frozen east source pivot92,172.
- tests/playtest_human_crew_candidate.gd supports identity-chain-study,
  identity-chain-selected and current scanner-selected/sample-selected modes.

The larger isolated sample-head study is superseded by the connected sequence.
Preparation metadata points to the ledger for current selection status.

## Verification

Agent reviewed original concept, raw identity sources, reduced paired contacts
and native phase captures. Native selected-source, timing and join checks pass
for the five action clips, with170body/164equipment states and zero failures. Validator:
zero errors/border touches,670original frames and108manifests unchanged.
Evidence under output/crew-replacement-2026-09-12/veld/:
identity-scanner-selected-native.log and identity-scanner-validation.log.
Legacy review modes also pass in identity-current-scanner-selected.log and
identity-current-sample-selected.log. Native fixture source-image warnings are
not packaged-game verification; no export was requested or produced.

Earlier isolated fitting changed40collar pixels by using bare bodies for equipped
endpoints. Preserving the corresponding equipped body fixed this. Failed
sample-identity-study-native.log and corrected sample-identity-collar-native.log
remain as historical evidence, not current sequence acceptance.

East walking now passes60distance-driven samples for both body and fitted helmet
in tests/playtest_crew_walk.gd. Each corrected frame preserves the original gait
pixels below the collar and unchanged stride. Evidence: identity-walk-native.log
and identity-walk-validation.log under the same Veld output directory. Native
preview: walk-native/east/identity-walk-preview.gif. The current Veld contract
has no separate run state. This is gait-fixture evidence, not continuous live
activity/occlusion acceptance.

South/west/north selected native checks pass72frames, original timing and exact
outside-head preservation, plus360distance cadence samples across body/helmet.
Evidence: identity-direction-cadence-native.log, identity-direction-validation.log
and independent identity-walk-west-native.log (60samples). Four initial cadence
failures at sample50 were a test precision mismatch: expectations now use the
supplied Vector2 position instead of unrounded scalar distance. No runtime change.
Failed identity-direction-selected-native.log and cadence-probe log are retained.

## Current scanner source selection

All four scanner directions have corrected identity. South, west and north use
full-body replacement interiors fitted to corrected idle proportions. Helpers:
tools/prepare_veld_{south,west,north}_scanner_{body,equipment}.py. East uses the
connected east-chain study. Opening and closing frames are exact corrected idle.

Raw full-body sources: scanner-south-body-02.png, scanner-west-body-01.png and
scanner-north-body-01.png. Fitted helmet sources: scanner-south-west-heads-01.png
and scanner-north-helmet-heads-01.png. Exact prompts are beside each raw source.
All paths are under sources/. Rear scanner occlusion is intentional; the body
faces away while the elbows and bowed head indicate operation in front.

Native selected-source/timing/join checks and preservation validation pass in
output/crew-replacement-2026-09-12/veld/identity-{south,west,north}-scanner-body-
{selected,validation}.log. West/north native phase contacts and timed previews:
scanner-study-native-{west,north}/identity-body01-{contact.png,preview.gif}.
Source review uses west-scanner-body-01 and north-scanner-body-01 under review/.

The head-only directional scanner study remains rejected for old body-proportion
changes and collar artifacts. A first west helmet fit was too small; the selected
scale is .12 for that sheet. North uses .09 and anchors the final opaque head
bottom at y108, fixing a rounding-induced collar gap. Body pixels below y111
(west) and y109 (north) are protected exactly. These scale factors belong to the
specific source crops, not a universal helmet size.

## Selected south sample chain

South kneel/sample/stand is selected with 18 body and 18 fitted helmet frames.
Sources: kneel-south-body-01.png, sample-south-body-01.png and
south-sample-chain-helmet-heads-01.png under sources/, with exact prompts.
Helpers: tools/prepare_veld_south_kneel_body.py,
prepare_veld_south_sample_body.py and prepare_veld_south_chain_equipment.py.
Review: review/south-kneel-body-01/paired-chain-contact.png.

One standing-derived ruler preserves anatomy through descent; sample interiors
match the 110-pixel settled kneel. The planted right-side boot anchors at x148.
Helmet heads use a shared source scale .09, collar anchors and a preserved
foreground vial/glove region. Exact idle and kneel/sample/stand joins remain.
Stand reverses kneel poses with original timing retained.

Native study and selected-source checks pass with zero failures. Evidence:
output/crew-replacement-2026-09-12/veld/identity-south-sample-chain-{study,selected,validation}.log.
Paired native phases and original-timing preview are in
south-sample-chain-study-native/{paired-phases.png,connected-study.gif}.
Preservation confirms 670 original frames / 108 manifests unchanged. Continuous
live motion, workplace occlusion and owner acceptance remain pending.

## Selected west sample chain

West kneel/sample/stand is selected: 18 body and 18 fitted helmet frames.
Sources: kneel-west-body-01.png, sample-west-body-01.png and existing authored
scanner-south-west-heads-01.png under sources/. Exact prompts are preserved.
Helpers: tools/prepare_veld_west_{kneel_body,sample_body,chain_equipment}.py.
Review: review/west-kneel-body-01/paired-chain-contact.png.

Kneel uses actual transparent-gap crops and one standing-derived ruler; sample
interiors match the settled kneel. A planted front boot anchors at x128. Helmet
heads use source scale .12 and crown-only horizontal anchoring. A narrow collar
mask avoids erasing the shoulder; the foreground vial hand is preserved.
Exact idle and kneel/sample/stand joins and original per-slot timings remain.

Native selected-source/timing/join checks pass with zero failures. Evidence:
output/crew-replacement-2026-09-12/veld/identity-west-sample-chain-{study,selected,validation}.log.
Paired phases and original-timing preview are in
west-sample-chain-study-native/{paired-phases.png,connected-study.gif}.
Preservation confirms 670 original frames / 108 manifests unchanged. Continuous
live motion, workplace occlusion and owner acceptance remain pending.

## Selected north sample chain

North kneel/sample/stand is selected: 18 body and 18 fitted helmet frames.
Sources: kneel-north-body-01.png, sample-north-body-01.png and authored
scanner-north-helmet-heads-01.png under sources/, with prompts preserved.
Helpers: tools/prepare_veld_north_{kneel_body,sample_body,chain_equipment}.py.
Review: review/north-kneel-body-01/paired-chain-contact.png.

The planted left boot anchors at x112. The rear boot's lower image-space sole
is excluded from registration. Sample interiors match the settled kneeling
anatomy. Neutral/bowed helmets use source scale .09 and preserve pixels below
the collar and throughout the raised vial-arm region (x144 and beyond).
Exact idle/action joins and original per-slot timings remain intact.

Native selected-source/timing/join checks pass with zero failures. Evidence:
output/crew-replacement-2026-09-12/veld/identity-north-sample-chain-{study,selected,validation}.log.
Paired native phases and original-timing preview:
north-sample-chain-study-native/{paired-phases.png,connected-study.gif}.
Preservation confirms 670 original frames / 108 manifests unchanged.

## Bounded live workplace review

A bounded autonomous native review now passes in tests/playtest_dr_veld.gd.
The fixture waits for startup, records recovered crew and uses clear navigation
nodes. A continuous north-facing bare-body work sequence contains 63 captures
across 6.2 simulation seconds (kneel, sample, stand, then walk), with a fixed work
position. Native room phases were inspected; source frames remain unchanged.
Evidence: output/crew-replacement-2026-09-12/veld/live-core-review-sequence.log and
live-core-review/{sequence.json,review-summary.json,continuous-work.gif}.
The run also observed east/south work states and walking in all four directions,
but only the north bare sequence received continuous capture. Equipped workplace
motion, other work directions and broader animation families remain open.

The north-facing helmet-equipped autonomous work review also passes: 63
captures across 6.2 simulation seconds cover kneel/sample/stand/walk with helmet
retained and fixed work position. Native room phases were inspected. Evidence:
output/crew-replacement-2026-09-12/veld/live-core-review-helmet.log and
live-core-review-helmet/{sequence.json,review-summary.json,continuous-work.gif}.
The fixture supports helmet-review and reports PASS only after all assertions.
It starts equipped; helmet donning/removal and other work directions are not
covered by this bounded run. Selected animation totals remain unchanged.

East- and south-facing bare-body autonomous work captures now also pass.
Each contains 63 frames over 6.2 simulation seconds with kneel/sample/stand/walk,
requested facing and fixed work position. Native phases show clear east-side
separation and south-side lower-body occlusion behind the lab apparatus.
Evidence: output/crew-replacement-2026-09-12/veld/live-core-review-{east,south}.log
and live-core-review-{east,south}/{sequence.json,review-summary.json,continuous-work.gif}.
The native fixture accepts review-direction= and asserts captured facing.
These add bounded bare-body review to north; east/south equipped and west live
workplace review remain pending. Selected animation totals are unchanged.

East- and south-facing equipped live work reviews now pass alongside their
bare-body runs: each captures 63 frames over 6.2 seconds with helmet retained,
fixed work position and full kneel/sample/stand/walk sequence. Native room phases
were inspected, including the apparatus overlap. Evidence:
output/crew-replacement-2026-09-12/veld/live-core-review-helmet-{east,south}.log
and live-core-review-helmet-{east,south}/{review-summary.json,continuous-work.gif}.
Thus north/east/south have bounded bare and equipped live work evidence. West
live work and broader transition/occlusion cases remain open.

A current-source audit of the separate 12-frame equip-helmet-east and 12-frame
remove-helmet-east clips is saved under the identity review folder's
helmet-transition-audit/. The donning contact shows suit/body and endpoint
identity differences from the corrected set; these transitions remain reopened
and require correction against current bare/equipped idle references. No new
animation rows were selected by this live-review milestone.

## Selected helmet transitions

East helmet donning/removal now selects 24 slots from six authored poses,
explicit holds and exact corrected bare/equipped idle endpoints. Native selected
pixel, original timing and endpoint checks pass. The study phase contact and
selected overhead pose were inspected. Continuous equipment-locker interaction
and occlusion remain pending. Source 01 was rejected for a face inside the held
helmet; corrected source 02 and both exact prompts are retained. The builder
now preserves explicit transition endpoints instead of overwriting them with
legacy identity art. Evidence: helmet-transition-{selected,validation}.log under
output/crew-replacement-2026-09-12/veld/.

## Remaining work

Fifty ledger rows record selected corrections; 284 other Veld variants
remain under identity review. Next: continuous live workplace scanner/sample
motion, direction/activity transitions and occlusion for the connected set.
Remaining life/water/death and other actions across Veld, Branforth and Marsh
remain in the full active goal. Native source/phase checks do not establish
continuous live motion or owner acceptance.

Native live locker follow-up: the focused Veld airlock test passes 224 travel
samples, equipment pickup/return, pause, power interruption and disk save/restore.
Captured phase traces compare the actual runtime texture bytes with the selected
source. Pickup at 0.321 seconds uses frame 2 with the helmet in her hands and
shelf hidden. This resolves the apparent empty-hand ambiguity in the small room
capture; no runtime animation mapping repair was needed. Evidence:
output/crew-replacement-2026-09-12/veld/helmet-locker-source-trace.log and
helmet-locker-source-trace-native/*-pose.json / *-actor.png / room captures.
These are discrete checkpoint captures; continuous locker motion remains open.


Continuous Veld locker review now captures both actions at 0.05-second steps:
44 pickup captures through 2.15 seconds and 46 removal captures through 2.25
seconds, including all twelve authored slots in each. Fixed-foot and equipment
completion checks pass, and runtime texture bytes match selected sources.
Native phase review found a remaining visual mismatch: the staged shelf helmet
is larger than the fitted held helmet, causing a size jump at pickup/return.
Keep live visual acceptance open until the shelf/held size relationship is fixed.
Evidence: output/crew-replacement-2026-09-12/veld/helmet-locker-continuous.log and
helmet-locker-continuous-native/{continuous-equip.json,continuous-remove.json,
handoff-phases.png,continuous-equip.gif,continuous-remove.gif}. That first run's
summary reused the broad test label; its actual scope is continuous locker motion,
travel and UI. The fixture now reports mode-specific coverage accurately.
Next: reconcile the staged shelf helmet with Veld's fitted held source while
preserving other actors and the shared interaction anchor.


Veld shelf scale correction: AirlockService now derives a 0.6 staged-helmet
scale from the active/reserved Veld locker request, retaining it while she stands
at the interaction point after return. Other servicing actors and Studio retain
the existing default. The shelf base and shared interaction point are unchanged;
no new save field or gameplay timing was introduced. The held shell is roughly
12 room units wide at Veld's existing body scale, matching the 12-by-15 shelf draw.
Changed: scripts/airlock_service.gd, scripts/grid_canvas.gd and
rooms/underwater/airlock-v1/airlock_view.gd.

The repeated native continuous Veld review passes 223 travel samples, both full
helmet actions, fixed-foot registration and UI. Native shelf-handoff-contact.png
was inspected: the previous conspicuous shelf/hand size jump is corrected.
Evidence: output/crew-replacement-2026-09-12/veld/helmet-locker-fitted-shelf.log and
helmet-locker-fitted-shelf-native/ captures. This establishes bounded q0 Veld
locker continuity, not every room rotation or broader animation acceptance.
Next: resume remaining Veld action-family identity corrections and the broader
Branforth/Marsh review/replacement queue. Counts remain 50 corrected Veld variants.


East seating identity study: generated canonical female Veld sit-down, seated
idle and rise sources, registered with one standing-derived anatomical ruler and
exact corrected standing endpoints. Eighteen bare study frames are prepared by
tools/prepare_veld_seated_identity.py under the identity folder's
review/seated-east-body-01/. Registered body contact was inspected. Source 01
had a baked checkerboard and is rejected for extraction; source 02 uses keyed
magenta. Both raws and exact prompts are retained. The source idle has two
authored settling poses with explicit holds, not six independent drawings.
Fitted equipment, furniture contact and native playback remain to be reviewed;
these frames are unselected and the 50-variant correction count is unchanged.


East seated fitted study now contains 18 bare and 18 helmet poses with bounded
collar edits and exact standing/seated/rise joins. Native study checks pass
original timing and all paired source slots; middle-descent native capture was
inspected. Evidence: output/crew-replacement-2026-09-12/veld/seated-identity-study.log
and seated-identity-study-native/page-00-frame-03.png. Added
prepare_veld_seated_helmet.py and seated-identity fixture modes. The fixture now
creates the final mode-specific output directory and checks every screenshot
write; an initial missing-directory run was corrected and rerun successfully.
The study remains unselected pending furniture contact and selected-pack checks.
Current correction count stays 50 variants.


East seated sequence selected: sit-down, seated idle and rise now use corrected
female Veld body art and pose-fitted helmets, adding six variants / 36 frames.
Totals are 29 body clips + 27 equipment variants = 56 corrected variants,
348 frames; 278 other Veld variants remain under identity review. All selected
pixels, original timing and corrected standing/seated joins pass the native
fixture; the selected endpoint phase was inspected. Preservation validation:
670 original frames / 108 manifests unchanged, zero errors or border touches.
Evidence: output/crew-replacement-2026-09-12/veld/seated-identity-{selected,validation}.log
and seated-identity-selected-native/page-00-frame-05.png. Explicit overrides
respect per-slot source offsets: only the embedded standing endpoints need the
smaller crop. Sources, prompts and registration remain preserved.

Current lounge and observation stations request north-facing seated actions;
this east selection does not claim live chair contact. Next: north-facing seated
and reading identity replacements, then continuous furniture review. The full
Veld/Branforth/Marsh goal remains active. Bill unchanged; Marsh helmet-free.

