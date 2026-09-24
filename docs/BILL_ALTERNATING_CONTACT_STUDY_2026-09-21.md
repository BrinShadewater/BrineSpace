# Bill alternating contact study

Updated September 21, 2026. Authoring study, not an installed gait repair.

## Objective and acceptance

Finish the owner's disjointed-feet repair by reviewing the actual alternating
stride after restoring connected source limbs. A complete cycle must preserve
each leg's identity through contact, support, passing and the opposite contact;
intact boots and a distance-driven phase alone do not establish natural walking.

## Decisions and current state

Current selected east/west poses were loaded from the live bare manifest, hashed
and displayed at common canvas/pivot in
`output/bill-contact-map-2026-09-21/registered-poses.png`.
Agent visual inspection finds several very similar support-leg poses in the west
row and repeated near-contact shapes in east. This is a static anatomical finding,
not a measured world-space foot-lock result or owner motion acceptance.

New sources and exact prompts are retained in
`character/major-bill-v3/sources/west-walk-alternation-2026-09-21/`:

- `rejected-repeated-stance.png`: eight-pose request again repeats similar
  near-leg-forward contact across both halves; rejected as a complete cycle.
- `opposite-contact.png`: isolated pose successfully makes the foreground leg
  extend behind the body. Useful anatomical reference only; no native approval.
- `rejected-anchored-cycle.png`: even with the two contact references, the new
  row repeats similar contact/passing shapes and forward arm positions. Rejected.
- `idle-reference.png`: frozen canonical identity; `near-forward-contact.png`
  is an unmodified crop of the first rejected sheet, retained only as a pose guide.
- `review.json`: hashes, alpha, crop provenance, review decisions and scope.

Built-in image_gen used for three generations, without Higgsfield or API fallback.
No generated frame was installed; no controller, timing, stride, helmet, room or
release package changed. The current polish checkpoint remains the selected build.

## Verification and limitations

All three generated PNGs have real RGBA alpha spanning 0..255. The twelve selected
bare side-walk PNG hashes remain unchanged after the study. Full sheets and the
isolated pose were visually inspected by the agent. No new native capture or
animation acceptance is claimed; rejected rows should not be animated and promoted
merely because eight frames can be sliced from them.

## Next action

Develop the missing support/passing poses individually from explicit whole-body
contact references. Compare foreground knee and boot positions across a complete
cycle before registration, helmet fitting or native station integration. Do not
repeat a full-row request that keeps producing the same half-cycle. Preserve
canonical identity and connected whole limbs; keep current runtime selected until
a better complete cycle survives actual-size and motion review.

## Individual passing-pose and native follow-up

Three more built-in generations are preserved with exact prompts:
`passing-a.png`, `passing-b.png`, and `rejected-reach-a.png`. The first two show
different support/swing legs; the reach attempt flips the near thigh forward
instead of retaining its backward position and is rejected. Six total generations
belong to this study so far, not six accepted frames.

`output/bill-alternation-native-2026-09-21/build.py` stages four whole-body key
poses (contact A, passing A, contact B, passing B), keeping pivot92,172,
standingHeight148 and the existing stride. Individual large sources share one
146/919 scale, while the contact cropped from the lower-resolution row uses
146/467. No per-pose height normalization or separate leg/boot compositing.
Faint source alpha1..16 is removed on derived copies; raw sources remain intact.
Registration records the threshold/count and verifies no opaque-body clipping.

Native CrewSpritePlayer comparison captured27frames at30Hz, with selected art
above and the candidate below, at source and384-unit room scale. Both clocks
match the same900ms cycle/root travel. Candidate uses four225ms holds only to
inspect alternation, not as an accepted final timing change. No missing textures
or engine errors. `west-four-key-study.gif` encodes30/30/40ms for900ms total.
The two passing renders and registered contact sheet were visually inspected.

The candidate makes opposite support legs distinguishable, but its stronger
knee lift, coarse four-pose cadence and changed lower-body detail prevent final
acceptance. This is controlled renderer evidence, not gameplay or owner approval.
No candidate frames, timing or manifests are selected by production. All twelve
selected bare side-walk hashes remain unchanged. `passing-review.json` records
new source hashes, decisions and these limits.

Next: reduce the near passing knee lift, author intermediate whole-body poses
while retaining leg ownership, and reconcile source detail with current Bill.
Preserve connected anatomy; do not solve timing by restoring detached boot rigs.
