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
| 2. Other directions | PixelLab `create-character-with-4-directions` or `generate-8-rotations-v3` | One request, consistent rotations, native sprite resolution |
| 3. Motion | PixelLab `animate-with-text-v3`, or `animate-with-skeleton` for exact control | Produces real limb movement; GPT Image cannot |
| 4. Bake | existing local tooling | Binary alpha, palette, pivot, canvas — unchanged |

### Step 1 — look
Reference an accepted room asset as the style anchor and the character's own art as the
identity anchor. Name the drawing language explicitly: flat colour blocks, two or three
tones per material, hard edges, deliberate chunky detail, legible at ~65px tall.
A four-pose turnaround in **one** generation holds identity; four separate
per-direction generations do not (patches and proportions drift).

### Step 2 — directions
PixelLab generates at true sprite size (32–256px) instead of downsampling a large
painting. Feed the approved front pose as the `south` reference. Caveat observed: its
side views came out narrow (16px wide against 36px front) and it reinterpreted the
character rather than copying it, so review rotations against the step-1 art.

### Step 3 — motion
`animate-with-text-v3` took the approved Bill and produced seven 64×64 frames with real
stride, foot lift and arm swing, preserving face, patches, belt and boots, at one
subscription generation (~$0.037 equivalent). It writes its own motion brief, which
spaced the frames better than a hand-written six-pose prompt.

Known defects from that run: one frame had a stray black cluster at the foot (repair
with `inpaint-v3`), and the loop did not close cleanly — the last frame does not return
to the first. For states that must loop perfectly, prefer `animate-with-skeleton`,
which takes explicit keypoints.

### Step 4 — bake
Unchanged and already correct: threshold alpha to binary, scale so the figure is ~65px,
seat the feet on the pivot row, quantize to the pack palette. PixelLab output arrives
almost pack-ready — 0 soft-alpha pixels on 3 of 4 rotations and on all 7 animation
frames, 437–1,166 colours against your packs' 41–64.

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

1. Does `animate-with-skeleton` close the loop cleanly? Untested.
2. Do PixelLab rotations hold up if given all four step-1 poses as references rather
   than only `south`? Untested, and it may fix the narrow side views.
3. Conversion scope for the cast remains the owner decision in the art-direction
   proposal: 501 manifests, 1,495 states, 7,272 frames.
