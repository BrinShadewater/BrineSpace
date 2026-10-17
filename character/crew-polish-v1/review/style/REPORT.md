# Character density, colour and style pass

September 27, 2026. **Result: export density matches; full visual consistency does not yet pass.**

## Coverage and authority
Measured 5,301 body-frame references across 959 states: the four current crew
catalogs (724 states / 4,413 references), the Veld candidate (20 / 100), and current
Margot/Josh/River aggregate packs (215 / 788). Counts include repeated frames.
These are stored body exports, not every runtime-generated join, equipment variant,
lighting/flood composite or release binding. Every reference received density,
alpha and image-statistic inspection. Visual review sampled the contact boards;
it did not inspect every frame of every animation in motion.

Authority: `docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md`, its accepted prop board,
character-specific identity references, current selected idle/action art and recent
companion consistency evidence. Existing character identity is preserved; the prop
bible does not justify replacing everyone's anatomy or recolouring departments alike.

## Findings

| Area | Result | Evidence and consequence |
|---|---|---|
| Declared pixel density | Pass | All inspected manifests use standingHeight 148: 2.2672 source pixels per world unit. Different 184–276px canvas extents are padding/pose coverage, not different pixel scales. No blanket resizing is warranted. |
| Effective detail density | Needs work | Bill's side gait/work and Marsh's older work/swim use broader shapes and heavier outlines than their detailed standing references. Equal metadata cannot restore missing painted detail. |
| Veld current palette | Needs work | Walking becomes lighter/softer and slightly purple compared with idle/work. East neutral-mask RGB is 67/69/74 in walk versus 55/58/60 idle. Masks include several materials; these are diagnostics, not target paint colours. |
| Veld candidate palette | Needs work | The candidate is more coherent internally but lighter than existing charcoal. East idle neutral median is 68/70/75 versus 55/58/60 current; south is 75/79/87 versus 51/55/60. Preserve steel highlights and ivory fittings while correcting cloth locally. |
| Veld collar continuity | Fail in sampled current east poses | Light-background review exposes a separated head/collar in idle-east and repair-east frame 0. Connected-component sizes are 3360+397 and 3462+397 pixels. Visual position confirms the smaller component is the head, not a held tool. The new candidate avoids that visible gap in sampled views. |
| Branforth consistency | Needs work | Walk-south introduces purple into neutral cloth and softer construction detail. Neutral-mask RGB is 62/59/65 versus 55/54/52 idle. Keep burnt orange, goggles, grey moustache and handed tools. |
| Marsh consistency | Fail in sampled work/swim | Older work/swim shift to a larger cartoon head, heavy black contours and rounded simplified armour. A colour grade alone cannot fix anatomy and construction. Preserve blond human-looking android identity and ivory/sage. |
| Companions | No new mismatch found in sampled views | Shared density retained. Margot's small size is intentional. Josh retains muted lavender/charcoal and River ivory/sage. Recent robot colour repairs remain selected; no companion art changed here. This is sampled review, not renewed full acceptance. |
| Transparency/filtering | Technical pass in measured exports | No partial-alpha pixels across measured references. Source game already requests nearest texture filtering. Dark and light backgrounds still reveal anatomical gaps and contours that alpha tests cannot judge. |

## Colour correction experiment

A built-in image edit tested Veld's east walk with the current idle/work palette as
authority. Raw source and exact prompt: `sources/veld-east-colour-v3.*`.
**Rejected for selection:** the neutral median moved from 65/68/71 to 66/64/62,
overshooting into warm grey rather than the existing cool charcoal. Registered
silhouette overlap was 94.66–99.06%, so this was not an exact colour-only edit.
`colour-pilot/comparison.png` and `colour-pilot/review.json` retain the evidence.
No production or Veld-candidate pixels/manifests were overwritten.

## Correction order

1. Repair the existing Veld east collar join with intact original anatomy; check
   all affected bare/equipped endpoints together on light and dark backgrounds.
2. Establish a material-correct Veld idle/walk/work reference set: cool charcoal
   cloth, cobalt plates, restrained ivory/steel, preserved skin and hair. The warm
   colour pilot is not that reference. Match body thickness as well as colour.
3. Re-author Marsh work/swim against his accepted idle anatomy; retain pose/timing
   and functional actions. Do not solve heavy outlines with blur or posterization.
4. Bring Branforth walk materials and Bill side-action detail toward their own
   standing references. Preserve distinct build, tools and department colours.
5. Review complete action chains at source scale and gameplay scale, then native
   room contact/occlusion. Correct static palette does not certify smooth motion.

This pass does not approve installation. It establishes the mismatches to repair,
without changing gameplay, accepted companion packs or character source identities.

## Reproduce and inspect

- `python character/crew-polish-v1/audit_style.py`
- `python character/crew-polish-v1/audit_companion_style.py`
- For board layout only, `audit_style.py --boards-only` reuses recorded measurements.

`metrics.json` and `states.csv` contain per-state/per-frame crew diagnostics;
`companion-metrics.json` contains companion summaries. Interior contrast is not a
blur detector, silhouette height is not anatomical scale, and hue masks are not
semantic material segmentation. No threshold automatically accepts style.

No Godot process or save-writing probe was needed for this read-only source audit.
Previous native Veld checks remain valid only for their documented candidate scope.
