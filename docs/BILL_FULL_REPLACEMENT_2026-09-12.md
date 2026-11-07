# Project handoff

Updated: September 12, 2026 · Project: BrineSpace · Task: Bill complete local replacement

## Objective and acceptance

Replace every active Bill animation/state from preserved sources, retaining detail
and identity, improve appearance and motion, and update the asset pipeline skills,
workflow and visual bible. The selected revision and its side-view motion repair
are integrated and verified. Original source packs remain intact.

## Accepted decisions

The owner chose local repair, rejected the muddy/reduced-detail material trial,
and authorized the complete replacement. Bill retains warm skin, red insignia and
the original base palette. A 148-source-pixel standing calibration renders at the
same 65.28 world units (2.27 source pixels per world unit). Canvas sizes and pivots
vary with pose/props. No generation service, other-crew redesign or EXE export.

## Selected implementation

`character/major-bill-v3/catalog.json`: 175 bare states / 1,134 frame references,
168 helmet states / 1,080 references, grouped into 19 canvas/pivot profiles.
All existing runtime coverage is replaced, including composed turns and endpoints.
Four weld directions, diagonal walk, equip and remove retain their pre-existing
bare-only coverage; equip/remove contain their own authored gear interaction.

Bill's grid loader, locker timing readers and clearance readers select this revision.
Six draw sites use standing-height metadata with the legacy 74 default. The player
preserves per-frame water kind/facing/pose/depth through joins and avoids applying
legacy helmet fitting to already-composed equipment. Headless action composition
duplicates images before mutation so bare frames cannot acquire helmet pixels.

Four idle loops retain the V4 breathing treatment; walking head identity and the
east interaction's planted lower body are stabilized. East/west walk legs now
exchange stance/swing roles using separately registered source regions. Detailed
upper-body pixels are retained with a one-source-pixel rise. Both helmet variants
follow the same torso phase. The first articulated trial was rejected in native
review as a short shuffle; the selected wider step travels 46 source pixels during
each half-cycle. Its full-key stride override is 0.1056756757 cells per cycle.
North/south/diagonal retain 0.12; run retains 0.168. Both the generic player and
legacy human clock honor full-key overrides with state-wide fallback. Simulated
movement speed, action durations, loop modes and locker event timings are unchanged.

## Reproducible workflow

1. `tools/bill-art-source-contract.json` records the original native consumer:
   1,134 references matched to 780 preserved frames from 113 manifests. Preserve
   this migration baseline; do not replace it with a dump of the new consumer.
2. `python tools/rebuild_bill_art.py` rebuilds the whole selected revision from
   authored sources. It exactly reproduces source crop selection for 504 action/life
   crops before increasing density. Helmet cutouts are re-extracted at density.
3. `tools/repair_bill_walk.py` supplies the local side-view limb repair. Its direct
   command reconstructs pre-repair source pixels independently, writes review data,
   and never feeds installed repaired frames back into themselves. No recolouring,
   flipped body art, generated replacement drawing or enlarged low-res final frames.
4. `python tools/validate_bill_art.py` checks source preservation, exact state/frame
   coverage, durations, loop modes, metadata lengths, equipment profile/playback
   pairing, binary alpha and border touches. Border touches fail the check.
5. `python tools/review_bill_art.py` refreshes all-state contact sheets and timed
   browser review. Native fixtures verify actual selection and room rendering.

The maintained and installed character skills now cover source density, actual
consumer inventory, local pose repair, stride calibration, immutable source inputs,
headless image aliasing, fixture isolation and limits of still-image evidence.
The visual bible and ACTIVE_ASSETS registry identify the selected revision.

## Final verification and completion audit

| Requirement | Current authoritative evidence |
|---|---|
| Every existing state and helmet variant replaced | `test_bill_complete_pack`: 11,773 checks, zero failures; 20260912-025630-headless |
| Preserved original art, density and frame contracts | `output/bill-full-replacement-2026-09-12/validation.json`: zero errors; 780 source frames and 113 manifests unchanged; 2,214 output references; zero border touches |
| Side-view motion repair selected with calibrated stride | `candidate-checks.json`: no new colours, preserved upper pixels, zero stance-sole error and zero calculated planting drift; generic/legacy directional cadence and pause checks pass |
| Bare/equipped runtime motion matches rebuilt reference | 240 native distance-driven comparisons, zero failures; 20260912-025637-native |
| Native room use and animation behavior | `playtest_major_bill`: storage/corridor/nursery, four-facing idle/walk/run, repair chain, reset/pause; zero failures in 20260912-025637-native |
| All-state native coverage after final walk change | 96 rendered sheets covering all 175/168 states; 20260912-025739-native |
| Active asset selection and packing | Bindings audit: zero errors, 28 registered packs / 698 clips / 3,702 references across the character library; PNG LFS attributes retained |
| Pipeline skills, workflow and bible updated | Maintained/installed skill sync: 15 files, zero differences; current animation-contract and direction references identify v3; this workflow and visual bible updated |

Earlier relevant integration checks also pass: airlock (1,039 travel samples with
equipment/pause/save), death/save, crew medium, crew polish and character mirrors.
The final motion change does not alter geometry, action clocks or save format.
The direct walk-reference rebuild was exercised after integration: all 24 bare/
helmet reference PNGs were reproduced byte-for-byte (`rebuild-reference.log`).

Review: `output/bill-full-replacement-2026-09-12/review.html`, updated contact sheets,
native sheets and room captures. Walk sources, pose sheets, GIFs, joint provenance
and native-selected comparisons are in `output/bill-walk-repair-2026-09-12/`.
Agent visually inspected the source layers, phase sheets, native comparison and
room-scale result. This is agent review, not a new claim of owner visual approval.

## Limits and unrelated findings

Other authored action families retain their existing choreography and some style/
helmet-size variation. This is a complete detailed replacement with the identified
motion repairs, not a claim that every pose was newly drawn or every animation is
perfect. Original and rejected evidence is preserved; no executable was rebuilt.

The broader room-activity test reported six blocked Cold Store approaches, rotations
0 and 2 for all three crew, before furniture activity begins; the other 66 cases
completed. Those failures overlap concurrent Cold Store layout work and do not
depend on the Bill art/stride changes. They remain a separate room-layout finding;
the full room-activity suite is not reported as passing.

## Next action

The requested Bill replacement and pipeline update are complete in source. Use the
review artifacts for owner feedback. Any export follows RELEASE_WORKFLOW separately.
Further art polish can build on this reproducible revision without reopening the
rejected palette simplification or reusing repaired frames as source inputs.
