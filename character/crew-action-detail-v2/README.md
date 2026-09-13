# Crew action detail sources

Veld east sleeping candidates 01/02 are unselected studies. Candidate 01 is too
long when supine; candidate 02 loses detailed identity. The extractor now thresholds
alpha before bounds/anchor measurement, fixing invisible-speckle registration.
All previously selected rest extractions remain byte-identical. See action handoff.

Both humans' north sleeping revisions now pass source/filmstrip, native timing
and live pillow-contact review. Branforth source 01 uses his own head registration;
all 160 selected rest joins and complete-pack checks pass. Other sleep views remain.

Veld north sleeping now passes live pillow alignment through exported head metadata
and the authored berth target. Transition easing, all 144 rest joins, asset and
room activity checks pass. Other sleeping families remain open.

Veld north sleeping source 01 is selected with a coherent prone transition and
fitted equipment. Source, filmstrip, native timing and all 144 rest join checks
pass. Live berth head/pillow alignment remains open; source selection does not
mean this family has final furniture acceptance. See the action handoff.

Both humans now have all four seating directions selected with fitted equipment.
The west source 01 additions pass source/filmstrip, native timing and asset checks;
all 128 selected seating join comparisons pass. North has live lounge evidence.
Sleeping and other action families remain under review. Notes below are historical.

Both humans' east/north/south seating is selected with fitted equipment. South
source 01 for each actor passes source/filmstrip and native timing review; all 96
selected seating join checks and the complete-pack check pass. West remains open.

Both humans' east/north seating is selected with fitted equipment. Branforth east
source 01 passes source/filmstrip, native timing and pack checks. The shared seating
join validator passes 64 full-channel comparisons across all selected families.
South/west and the broader action review remain open; older notes follow.

Branforth north seating source 01 is selected with fitted equipment and live
lounge review. Source/contact, selected filmstrip, native timing and pack checks
pass; seated joins/reverse rise are exact. Seating selection now covers Veld
east/north and Branforth north. Remaining directions and other families stay open.

Veld north seating source 01 is selected with fitted equipment and live lounge
review. Its source, frozen inputs and prompt are retained here. Both east and
north seating are selected; remaining directions and Branforth seating are open.
The live review corrected a shared furniture-anchor offset; see the action handoff.

Veld east seating source 01 is selected for sit-down/idle/rise with fitted gear.
The original inputs, exact prompt, uniform extraction and contact review are kept
here. Native timing/coverage and pack checks pass; seated joins and reverse rise
are exact. In-room furniture contact remains pending. Other seating directions
and sleep/role/water families remain under review.

Both humans now have all four cargo directions selected with fitted equipment.
Branforth north source 01 has matching 146px standing endpoints; carry retains its
held endpoint. Native timing/distance playback, rendered-pose review, exact reverse
unloading and complete-pack checks pass. Detailed seated/rest and other action
families remain under review. Entries below are historical source-study evidence.

Veld north cargo is now selected with fitted rear equipment, completing her four
cargo directions. Source 01 has 148/149px standing endpoints; carry retains the
held pickup endpoint and uses rear axial phase ordering. Native timing/distance
playback, focused render and complete-pack checks pass. Branforth north remains
open. Earlier entries below retain the sequence of source and rig decisions.

Both humans now have east/west/south cargo selected. Branforth south source 01 has
matched 146px standing endpoints. It uses the shared projected front-carry builder
and fitted front helmet; native playback, exact reverse unload and pack checks pass.
North cargo remains open, alongside the broader action review.

Veld south cargo is now selected with fitted front equipment. Native vertical
distance playback, focused rendered poses and complete-pack checks pass. The
earlier candidate notes below preserve extraction and mask decisions.

Veld south is a candidate: pickup source 01 plus a front carry study built directly
from its endpoint (`tools/repair_front_cargo.py`). Reference, prompt, extraction,
recipe and portable motion review are preserved. Front boot registration excludes
the crate lip; full-width sole masks prevent stationary foot fragments. The source
strip and corrected carry filmstrip were inspected. Equipment and runtime review
remain pending.

Current side-cargo selection is complete for Veld and Branforth: east/west pickup,
carry and reverse unload with fitted equipment. Branforth west source 01 has
151/152px standing endpoints and its own preserved carry donor/masks. Native
distance playback, focused render review and full pack checks pass. North/south
cargo is the next source work; older candidate notes below are retained as history.

Veld west is now selected with fitted equipment and a 64px carry stride. The near
knee pivot was corrected onto the donor's actual kneepad before promotion.
Native distance playback (60 samples), focused renders and complete-pack checks
passed; the preserved candidate notes below record the earlier joint concerns.

Veld west cargo work is a candidate. Pickup source 01 uses the west idle reference
without mirroring; extracted standing endpoints are 150/149px. The extractor now
accepts `--direction west` and locates boots on the side opposite grounded cargo.
The dedicated west carry donor has a local rig and six-pose review. A 64px stride
with hips restored to y=118 avoids the earlier lowered attachment; stance checks
pass, but knee/hip seams still need closer review before promotion. West equipment
and runtime binding remain pending. Original prompts and sources are preserved.

Current selection: both Veld and Branforth east pickup/carry/unload, with fitted
equipment. Branforth's carry donor now has its own deterministic rig in
repair_veld_carry.py (`--actor branforth`), preserved recipe and contact sheet.
Both legs measure zero stance drift/sole error. Native cargo and complete-pack
checks passed for this selection; remaining direction/action work stays open.

Branforth east pickup candidate 01 is preserved with its six poses and exact prompt.
The generalized extractor uses his frozen idle reference, yielding matched 147px
standing endpoints; its contact sheet was inspected. A single carry contact-pose
donor is preserved separately with its prompt. It retains his heavier anatomy and
crate grip, with separated near-forward/far-back legs for a local rig. These
Branforth sources are not yet selected. Next: extract the donor, author its own
limb masks, review the cycle and fit equipment before coherent cargo binding.

Veld east cargo revision, September 12, 2026. Pickup 03 and locally rigged carry 02
are now selected together, with reverse unloading and per-pose fitted equipment.
The studies below preserve the decisions that led to this selection.

The frozen pickup input records the six currently selected bare poses; the idle
reference records her accepted detailed standing identity. Candidate 01 preserves
the lifting progression with finer material detail, but generated an opaque RGB
checkerboard instead of transparency. Candidate 02 replaces that background with
magenta. Both raw results and exact prompts are retained.

`tools/extract_veld_cargo_study.py` removes chroma, applies one scale calibrated to
the first standing body, and registers each boot sole independently of the crate.
It retains source hash, bounds, scale and anchors in review/veld-pickup-east-02.
The comparison shows improved interior rendering, but the final standing pose is
156px tall versus 145px at the start. Correct this source-scale drift before
promotion; do not hide it by scaling every crouched pose to standing height.
Carry, unloading and fitted equipment integration remain pending.

Candidate 03 corrects the last pose's excess height. The preserved source and exact
prompt reproduce standing endpoints of 145px each at one uniform scale, and the
six-pose contact sheet was inspected. The extraction CLI defaults to 03; use
`--revision 02` to reproduce the rejected height-drift study. Candidate 03 remains
unselected until carry/unload and fitted equipment are prepared together.

Carry experiment `review/veld-carry-east-rig-01` combines the last pickup's upper
body with the accepted independently reconstructed Veld east walk legs. It is
rejected: the hip seam is visible. Recipe: crop pickup-03 frame 005 to
(36,52,220,171), paste at (0,0) onto each `repair_crew_walk.build` frame from original
Veld walk-east frame 002 and the selected east rig, without mask blending. This
records the failed experiment, not an integration recipe. The frozen carry input
also repeats its leading leg; a consistent detailed carry source is still needed.

Carry candidate 01 improves the hip connection but still repeats near-leg ordering
as a raw six-frame loop. Its first pose is the donor for
`tools/repair_veld_carry.py`: independent masks now use the cargo source's own hip,
thigh, lower-leg and boot anatomy. The six-frame local-02 contact sheet was
inspected and has alternating contacts without the earlier torso splice gap.
Measured stance drift and sole error are zero for both legs. These measurements
do not establish full visual or native acceptance. The portable motion.html pairs
the pickup endpoint with the carry cycle at source and station scales.
The entire cargo revision remains unselected pending motion review and fitted
helmet integration; source prompts, hashes and the full rig recipe are retained.
