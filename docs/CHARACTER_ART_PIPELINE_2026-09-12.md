# Character art pipeline: the hybrid that works — September 12, 2026

Tested end to end on Major Bill, September 12. **Nothing is installed; no character
art in the source tree has changed.** Evidence in
`output/higgsfield-pilot-2026-09-12/`. This supersedes the character sections of the
[Higgsfield pilot](HIGGSFIELD_PILOT_2026-09-12.md) and the withdrawn
[canvas-size proposal](CHARACTER_CANVAS_SIZE_PROPOSAL_2026-09-12.md); the
[art-direction proposal](CHARACTER_ART_DIRECTION_PROPOSAL_2026-09-12.md) still stands
for the question of whether to convert the cast.

## The pipeline

| step | tool | why that tool |
|---|---|---|
| 1. Look | GPT Image 2.5 (Higgsfield) | Only model tested that draws in the rooms' language and keeps identity from a reference |
| 2. Other directions | GPT Image 2.5, all four poses in **one** turnaround sheet | Owner review, September 12: only the GPT Image poses were judged good. Both PixelLab rotation routes degraded the character |
| 3. Motion | PixelLab `animate-with-text-v3` | Produces real limb movement in one call; GPT Image cannot. Skeleton control tested and rejected for locomotion — see below |
| 4. Bake | existing local tooling | Binary alpha, palette, pivot, canvas — unchanged |

### Step 1 — look
Reference an accepted room asset as the style anchor and the character's own art as the
identity anchor. Name the drawing language explicitly: flat colour blocks, two or three
tones per material, hard edges, deliberate chunky detail, legible at ~65px tall.
A four-pose turnaround in **one** generation holds identity; four separate
per-direction generations do not (patches and proportions drift).

### Step 2 — directions
**Use the GPT Image turnaround; do not use PixelLab for rotations.** A single sheet
containing all four poses holds identity, and in owner review on September 12 only
those poses were judged good.

Two PixelLab routes were tested against them and both lost quality:

- `create-character-with-4-directions` **drifts from the approved design** — different
  face, different patch design, a thinner body and boots that were never in the brief.
  It is a generator that treats references as hints, which is the wrong job. It is also
  slow: still pending after 25 minutes, against roughly two for a single-reference run.
- `/rotate` is the technically correct endpoint — synchronous, one call per direction,
  and it genuinely transforms the supplied sprite rather than inventing one (face,
  beard, patches, chest light and belt all carried over). Even so, its north view lost
  the shoulder patches into an invented pale belt band, and the result still reads as a
  step down from the source art.

Note on the narrow profiles: `/rotate` returned 20px east and 19px west from a source
whose own west pose was 19px, so it reproduced the reference faithfully. The thin sides
came from the step-1 turnaround, not from PixelLab — fix them in step 1.

### Mirror one profile; never generate both

**Rule, learned twice on September 12.** Generate one side view and flip it for the
other. Do not ask a model for both, and do not ask it to make them match.

- Characters: GPT Image drew the left-facing pose as a three-quarter-from-behind view,
  19–22px wide against 32–40px for the right-facing one, and an explicit instruction to
  make the two exact mirror images did not fix it. Flipping the east pose produced
  identical 32px profiles at no cost.
- Room side walls: the same failure. Separately generated east and west banks came out
  as different installations, and the accepted hand-authored pair already differed
  (`303x974` against `279x979`). See the
  [mirrored side walls proposal](MIRRORED_SIDE_WALLS_PROPOSAL_2026-09-12.md).

Safe here because the art carries no text and no handedness, and lighting is even from
above. North and south are never mirrored — a vertical flip is wrong in both cases.

### Step 3 — motion
`animate-with-text-v3` took the approved Bill and produced seven 64×64 frames with real
stride, foot lift and arm swing, preserving face, patches, belt and boots, at one
subscription generation (~$0.037 equivalent). It writes its own motion brief, which
spaced the frames better than a hand-written six-pose prompt.

Known defects from that run: one frame had a stray black cluster at the foot (repair
with `inpaint-v3`), and the loop did not close cleanly — the last frame does not return
to the first.

**Skeleton control was tested and is not the answer for locomotion.**
`estimate-skeleton` returns 18 labelled joints in normalised coordinates (0.1 of a
generation), and `animate-with-skeleton` draws from posed joints — but it accepts
**exactly three frames per call**, a 3-frame window. Driving a six-frame walk therefore
took two calls (2 generations, against 1 for seven frames by text) and the two halves
did not share limb logic or lighting, so the join is visible. Frames also came back with
white outline halos where posed joints pulled the silhouette outside the reference
shape, and loop closure did not improve (mean first-to-last difference 13.2 versus the
text run's). My joint deltas — ±0.045 vertical, ±0.03 horizontal — were probably too
timid for a front-facing walk, so a stronger pose set might do better; that was not
pursued because the text path already works.

Use `animate-with-skeleton` where an **exact single pose** is needed (a specific repair
or interact stance), not for cyclic locomotion.

### Step 4 — bake
Unchanged and already correct: threshold alpha to binary, scale so the figure is ~65px,
seat the feet on the pivot row, quantize to the pack palette.

**Quantize the whole direction set together, not frame by frame**, so all four share one
palette as a real pack does. Done that way on September 12, the four Bill poses came out
at 44–59 colours inside a shared 64-colour palette, 0 soft-alpha pixels, figures exactly
65px tall on the 92x92 canvas with feet on the pivot row — technically registerable
(`output/higgsfield-pilot-2026-09-12/bill-reimagined/final-poses/`).

## What was ruled out along the way

1. **Blur is not a cleanup fault** — re-cutting from source reproduces what ships.
2. **Not canvas size** — Bill is ~73px inside both the 92px and 128px canvases, and
   `grid_canvas.gd` calibrates on a ~74px figure regardless.
3. **Not resolution** — at the owner's saved fit zoom (0.4446) the character is ~29px
   tall and every version looks the same. The gain is close-zoom only.
4. **Per-direction generation** is less consistent than the art it would replace.

## Cost signals

- Higgsfield: 3 credits per 2K image at `high`; the character work here used ~30 of
  1,000 credits.
- PixelLab: Tier 1 subscription, 2,000 generations, unused before today; a 7-frame
  animation is one generation.
- The expensive input is not the tools. It is review and per-pose correction.

## Open questions

1. ~~Does `animate-with-skeleton` close the loop cleanly?~~ Tested September 12: no.
   It is a 3-frame window, costs more, and produced outline artefacts. Rejected for
   locomotion; retained for exact single poses.
2. ~~Do PixelLab rotations hold up if given all four step-1 poses as references?~~
   Moot: rotations are no longer part of the pipeline. The four-reference and
   mirrored-west experiments were left running and their results are not needed.
3. Conversion scope for the cast remains the owner decision in the art-direction
   proposal: 501 manifests, 1,495 states, 7,272 frames.
