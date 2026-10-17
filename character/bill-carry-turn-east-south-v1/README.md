# Bill east/south cargo turn candidate

Updated September 30, 2026. Bare candidate, staged and uninstalled; owner review pending.

Build-v3 supersedes pivot-v2's wider intermediate anatomy. New source plus one
frozen shoulder-width calibration from both cardinal endpoints narrows the
intermediate torso/head while preserving height and planted feet. Projection
may widen as Bill rotates; no per-pose rescaling is applied. Pivot-v2 superseded the first walking-stride turn: the owner specified that a
stationary turn must not leave a foot extended. Six poses now connect exact
loaded neutral `pickup-east/010.png` and `pickup-south/011.png` endpoints.
Four intermediate whole figures come from revised source cells1–4. Generated
endpoints are discarded. South-to-east reverses the same frames without mirroring.
Original quarter-turn duration is 800ms in each direction. Canvas256, foot
pivot(128,224), standing reference148. One frozen source scale and material
calibration apply across intermediate poses; no per-pose size normalization.

Source: `sources/turn-build-v3.png`, preserved original generation
`exec-eb103cf4-0a16-4d1d-8b05-4cc740ad65a4.png`. Exact prompt in
`sources/prompt-build-v3.txt`. Earlier walking/pivot sources and prompts retained;
packaged pivot-v2 in `review-before-build-v3/`; packaged
v1 review in `review-before-pivot-v2/`. Authorities: new loaded neutral cargo endpoints and
`crew-side-masters-v1/bill-side-master-01.png`. Matte calibration uses selected
east idle through the maintained east cargo grade helper. Registration and
source hash are recorded in `registration.json`.

Rebuild with `python character/bill-carry-turn-east-south-v1/build.py`, then
`verify.py` and `build_review.py` from the same folder. 95 packaging checks
pass: profile, alpha, clipping, foot contact, frozen scale, frame hashes,
exact neutral endpoints, compact boot spread, frozen width calibration, shoulder
width ceiling and reverse equality. Browser previews loaded both
the isolated turn and pickup→pivot→set-down cycle; contact-sheet and
82/54px dark/light samples visually inspected. This is not native acceptance.

Remaining: owner motion/material review, other three quarter turns, helmet
turns using matching canonical view art, opposite turns, then install and
verify the complete cargo family in scratch-profile Godot. Installation must
preserve neutral turn endpoints rather than replace them with gait frame zero;
review settling from movement into the turn separately. Runtime still uses
old cargo. South bare/equipped independent owner acceptance remains unrecorded;
north equipped was accepted by the owner's continuation from its preview.
