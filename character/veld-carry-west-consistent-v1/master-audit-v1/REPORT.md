# Veld west carry: master detail audit

Reviewed September 29, 2026. Review only; animation frames and bindings unchanged.

Authority: the owner-approved September 27 west side foundation's
`side-master-01.png` and ungraded `west-standing.png`. Installed west idle is a
secondary runtime check. Unaccepted west walk master-v3 is not the authority.

`same-scale.png` compares master, installed idle, carry v4 and carry v6 at
148px visible standing height, with fixed head crops and gameplay sizes.
`raw-heads.png` matches body height before cropping either raw head.
`measurements.json` records paths, hashes and coarse silhouette measurements.

| Area | Master | Carry | Cause |
|---|---|---|---|
| Face | Defined brow, nose, ear and jaw | Broader, rounder, softer features | Source drift plus reduced contrast |
| Hair | Fine strands, integrated silver streak | Chunkier forms; silver reads as a headband | Source drift plus reduced strand contrast |
| Collar/suit | Distinct seams, rivets, fasteners | Simplified hardware and altered patch motif | Source drift |
| Finish | Matte with feature separation | Flatter face and hair | V6 contrast compression |

First-frame top-20px head/collar width is 27px for master, 29px for installed idle,
36px for both carry v4 and v6 at equal body height. This includes bun/collar and
is a coarse proxy, not a skull measurement. Raw figure heights are 911px versus
526px. Carry generation used reduced runtime idle and an east carry sheet,
rather than the high-resolution west master, contributing to detail drift.

V6 face contrast 0.72 and hair contrast 0.56 reduce tonal separation without
changing geometry. Cargo/arms obscure some suit detail; occluded features are
not evidence of missing detail. Exposed head, collar and patch are clearer evidence.

Next: restore proportions, facial landmarks, integrated hair streak, collar and
visible suit hardware from the high-resolution master while preserving the
owner-liked motion, continuous body and helmet alignment. Keep matte shading
with local feature contrast. Further broad flattening cannot fix source drift.

West carry remains staged/uninstalled. No other accepted animation changed.
Visual audit only; no Godot rerun necessary.
