# Project handoff

**Superseded direction:** the owner rejected the V2 material treatment as less
detailed and muddy. Do not adopt or extend it. The current experiment is the
[original-source 2x density rebake](BILL_DENSITY_REBAKE_2026-09-12.md), preserving
the original palette and motion. V1/V2 remain historical previews only.

Updated: September 12, 2026 · Project: BrineSpace · Task: Existing sprite repair trial

## Objective and acceptance

Owner wants to try repairing the existing spritesheets locally, addressing both
appearance and animation. Start with Bill's existing identity and representative
clips. This direction supersedes treating the hybrid generation proposal as the
next action; it does not approve a replacement pack or a cast-wide conversion.

## Accepted decisions and constraints

Use existing artwork for the trial. Preserve production art, registrations,
manifest timing and pivots. No generation service is used. All new raster work is
an isolated preview, with source hashes and reproducible local processing.

## Current state

Latest preview: `output/local-sprite-repair-2026-09-12/material-v2/`, built by
`build_material_trial.py` in the parent folder. This addresses the owner's follow-up
about matching room-art detail: five suit shade bands, separate red-patch and neutral
hardware ramps, and isolated bright suit-texel cleanup. V1 head and skin pixels are
preserved. All 18 trial frames receive the same material rules; the combined palette
contains 44 opaque colours. This is still source-pixel processing, not newly drawn art.

`material-v2/room-comparison.png` compares shipped / V1 / V2 against the active
Research Lab bank (`assets/material-polish-v2/research-north.png`), using its current
registration silhouette and default 344-world-unit width. Bill uses the existing
65.28/74 scale. Includes normal scale, 4x sprite detail, and 0.4446 fit zoom. Static
composites omit in-game lighting and occlusion. Three new comparison GIFs show all
versions against that reference; PNG strips, individual frames, a manifest, contact
sheet, and hash/check record are alongside them. Earlier V1 outputs remain intact.

Agent assessment: broader suit shading is closer to the room's quiet material
surfaces; face and silhouette remain recognizable. This is not a complete detail
match: the room has finer contours, and the difference is small at fit zoom. The
same 74px source profile remains. The underlying walk stride is unchanged.

`output/local-sprite-repair-2026-09-12/` contains `build_trial.py`, a standalone
manifest, provenance, 18 PNG frames in three clips, strips, `comparison.png`, and
`idle-east-comparison.gif`, `walk-east-comparison.gif`,
`interact-east-comparison.gif`. GIFs show original left, repair right, with enlarged
pixels and approximately 65px/29px standing-height samples on a neutral background.
They are composites, not in-game captures.

- Idle: reuse the first shipped drawing with a one-pixel upper-body breathing
  cycle; lower body remains fixed. Height range 70–75px becomes 72–73px.
- Walk: reuse the first walk head, following each original frame's vertical bob.
  All six original arm/leg poses, their order, and timing remain. This stabilizes
  facial identity; it does not fix the underlying stride or foot sliding.
- Interaction: reuse idle head and lower body; retain the authored reaching arm
  and torso. Shared idle endpoints remain identical.
- Appearance: mild shared contrast adjustment and one 40-colour palette across
  the trial. No new features, spatial blur, upscaling, or per-frame palettes.

Changed documentation: this handoff and `docs/CURRENT_STATUS.md`. Prior uncommitted
standing-height code, its test, and the Astra handoff were left untouched. Nothing
is installed into the game, committed, exported, or published.

## Verification

Builder checks pass: original source hashes unchanged, all 18 frames 92×92, binary
alpha, timing/loop preservation, identical interaction/idle endpoints, stable
interaction lower body, and no border clipping. Generic sprite manifest validator
passes with no errors or warnings. Agent inspected the complete before/after
contact sheet: existing identity retained, calmer idle poses, modest palette change.
Continuous motion and in-game visual acceptance remain with review; no native
gameplay tests were run for this isolated art trial.

V2 checks also pass: all V1 source hashes unchanged, exact alpha/silhouette
preservation, 92x92 dimensions, binary alpha, unchanged timings/loops, and identical
interaction/idle endpoints. Generic manifest validator returns no errors/warnings.
Agent visually inspected the full contact sheet and final room comparison. The
first colour-map attempt tinted warm boot highlights red and over-simplified the
face; corrected by restricting patch classification and preserving face/skin pixels.
No runtime integration or continuous-motion acceptance is claimed.

## Next action

Review the V2 room board and comparison GIFs. Decide whether its broader material
shading is useful before expanding beyond the three-clip trial. Finer contour work
and Bill's walk stride remain unresolved. Do not call head stabilization a complete
gait repair. Review seams at the composited neck/waist and the material mapping in
motion before adoption.
