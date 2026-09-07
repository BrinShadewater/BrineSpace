# Data Archive service mat repair

Current status: mat and cutout contacts repaired; native state regression passes.
The earlier failures below are retained as revision history. Packaging and crew
access/depth acceptance remain pending.

The service-cart mat now uses offset (-4, -3) and size (68, 34), replacing
(-28, -3) and (94, 34). It follows the 60-unit cart instead of extending toward
the separate lamp. No prop placement, hull, doorway, collision or source art changed.

## Evidence

- `output/archive-mat-contained-v1.log`: all four final mat rectangles fit the
  360-unit interior. This gate does not certify furniture separation.
- `output/archive-mat-after-v1`: four native rotation captures; q1 inspected
  against the earlier west-wall overflow.
- New 512-square `rooms/underwater/batch-two/data_archive-card-mat-v2.png`
  visually inspected and selected by station fallback, card and export manifest.
  Git attributes confirm LFS. Old card retained.
- Profile SHA256: `9F0E23A3C48ECE3E8C5F482F8CE570471A9AFF083AEACFAD9E2BBD181DD184C6`.
- Card SHA256: `A0C7CA45E3F0DE5A20FA03A01DD7E80289B524025C176AC8B9EBB53BEC5FB905`.

## Open regression findings

`output/archive-mat-state-native-v1.log` ends with four assertion failures,
not a passing room acceptance. Its error log names visible assembly overlap.
The composition audit identifies terminal/cart at q0 and cart/task-lamp at
q1, q2 and q3. An articulated lamp may intentionally reach over its work surface;
inspect actual overlap pixels before changing placement or narrowing assertions.
Do not remove the all-pairs test merely to obtain a pass.

The mat repair does not move these assemblies. Broader room-state acceptance,
crew access/depth review and fresh batch packaging remain pending.

## Polygon diagnostic follow-up

All four `archive-mat-after-v1` room captures have now been visually inspected.
The q1 lamp/cart bounding boxes overlap despite separated cutout geometry.
At q2 the lamp head crosses the cart's raised arm; at q3 the lamp head meets
the cart's lower-left wheel area. These are different relationships from a
deliberate light reaching above a usable work surface; review their placement.

`tools/audit_room_composition.gd --polygon-overlaps` now reports registered
cutout intersection area for each bounding-box candidate. The existing mat
gate and whole-room assertion are unchanged. Run
`output/archive-polygon-overlaps-v1.log` exited 0 without engine errors
(existing raw-image export warnings remain):

| Rotation | Pair | Cutout intersection, square world units |
| --- | --- | ---: |
| 0 | Terminal / cart | 0.478515625 |
| 90 | Cart / task lamp | 0 |
| 180 | Cart / task lamp | 19.3984375 |
| 270 | Cart / task lamp | 27.857421875 |

This is a geometric diagnostic, not a decoded-alpha, effect, shadow, collision
or crew-access test. Piece intersections are summed; overlapping pieces within
a host could double-count. Do not treat the areas as final visible-pixel counts.
The next repair should address the three actual cutout contacts while retaining
the q1 composition unless crew-access evidence requires otherwise.

## Clearance repair integrated

Renderer-local offsets now move the q0 cart 4 units south, q2 lamp 24 units
east and q3 lamp 12 units south. Q1 is unchanged. Prop sizes, source textures,
doorways and low walls are unchanged; the mat follows its cart.

`output/archive-clearance-v1.log` passes all four mat bounds. The sole remaining
bounding-box candidate is q1 lamp/cart, with zero registered polygon intersection.
`output/archive-clearance-review-v1` contains four native frames; q2 and q3 were
visually inspected, and the canonical composition was inspected in the new card.

The native fixture now compares actual registered pieces after a bounding-box
prefilter, instead of treating their transparent rectangular envelope as solid.
`output/archive-clearance-state-v1.log` exits 0 with zero assertions across four
rotations, six assemblies, input isolation and economy-driven powered, starved
and suspended states. The existing injected-clock repeatability checks do not
independently prove owning-clock pause gating or NPC access.

`--negative-archive-lamp-contact` moves the q1 lamp 20 units into the cart;
`output/archive-clearance-negative-v1.log` exits 1 with exactly one cutout
overlap failure. This proves the refined check still rejects a real contact.
It does not certify decoded-alpha boundaries or all possible regressions.

Card `data_archive-card-clearance-v3.png` is selected in the current card,
station fallback and batch manifest consumers. Its 512-square native bake exits
0; it was visually inspected and its LFS attribute verified. Older cards retained.

- Renderer SHA256: `EC8A6B26CAF6F3560271910AD10B577E1C4BBD46F30EA7A40F23DB94C3981A89`.
- Card SHA256: `BC92FD5609402C6E6E0FB0B1C98335297A5227BF9CD7DBED853344FBD749CE9C`.

Fresh package verification and actual crew working-space/depth review remain open.

## Static crew clearance and depth follow-up

`output/archive-clearance-crew-d643706c` freshly reviews the service cart,
terminal and task lamp in four rotations with Bill's existing south-facing
sprite. The native process exits 0, with 36 poses and zero ordering/sensitivity
failures. All 24 front/rear positions pass the room's `can_stand` check; the
other 12 are deliberately forced overlap probes, not reachable-pose claims.
All 36 comparisons match the explicit expected order and differ from reversed
order. Renderer SHA remains `EC8A6B26CAF6F3560271910AD10B577E1C4BBD46F30EA7A40F23DB94C3981A89`.

The q3 cart-front full-room diagnostic was visually inspected: Bill remains
in front of the cart with the lamp and mat visible. Captures are prop-centered
at 2x, so outer room edges can be off-canvas. This is static local clearance
and ordering evidence, not an arrival route, continuous NPC movement, multi-crew
traffic or normal station-zoom acceptance. Packaged verification remains pending.

An initial attempt used the already-existing `archive-crew-depth-v1` directory
and stopped at an assertion. Its older review JSON was explicitly excluded;
the precisely identified failed child was stopped after the timeout. The capture
tool now exits 1 cleanly for existing or invalid output directories. The fresh
negative guard run `output/archive-depth-guard-v1` confirms that behavior without
overwriting the successful review. Use new unique output directories.

## Production-controller route follow-up

`output/archive-clearance-route-26dd6438` runs the existing `--archive-tour`
with input isolation and visit captures. It exits 0 with no engine errors and
zero assertions. Each of four rotated layouts contains Archive plus four
connected battery rooms. Bill completes six scheduled arrivals including return
to the starting room: 24 arrivals, 32 reciprocal transitions and 2613 checked
movement samples total (636, 656, 660, 661 by rotation).

The fixture uses production core recovery to activate Bill; Veld and Branforth
remain inactive. Production navigation and movement handle the scheduled legs.
This is not autonomous destination selection, paid construction or multi-crew
traffic evidence. Per-rotation traces and summaries are retained.

The q3 `visit-03-data_archive.png` was inspected at its recorded 0.52 zoom.
The repaired service group and connected room remain legible. Seven of eight
Archive visit captures are arrival fallbacks; only the q1 return capture reaches
the fixture's near-terminal threshold. Do not claim these captures demonstrate
walking to every repaired work surface. The earlier static probes cover local
standing/order separately. The image also includes the checkout's existing
raised exterior bands on neighbouring rooms; this route pass does not approve
that separate wall treatment against the owner's low-wall decision.

Fresh packaged verification remains open.

## Reusable pipeline lesson

The project and installed room-pipeline repair-loop references now distinguish
empty bounding-box overlap from actual registered cutout contact. They route
compatible views to `audit_room_composition.gd --polygon-overlaps`, retain all
prop pairs and require an introduced-contact negative control when refining a
regression. Alpha, overlays, shadows, collision and crew access remain separate.
Both skill folders pass quick validation and both edited references have SHA256
`2DB1C12C3C45AD2BFE663A2C85BDE15DBF704CA003E4CFEEC05D4EBC17D78AAC`.
Behavioral support is the retained passing Archive state run and one-failure
lamp-contact negative run, not the skill syntax validator alone. No new art
direction was introduced, so the bible's existing composition intent is unchanged.
