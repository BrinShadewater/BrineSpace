# Proposal: redraw the crew in the room art's language — September 12, 2026

Owner observation that started this: the characters look blurry, and they do not
match the environments. Both are true, and the second is the real problem.
**Nothing is implemented. No character art has been changed.**

## What was established first (and what it killed)

1. **Not a cleanup fault.** Re-cutting Bill from his own source at today's figure
   height reproduces what ships; the pipeline loses nothing.
2. **Not a canvas-size problem.** Bill is 73px tall inside his 92px canvas and 72px
   inside the 128px action canvas — the larger canvas is margin for carried objects.
   `pixel_scale = cell_size * 0.17 / 74.0` (`grid_canvas.gd`) calibrates on a ~74px
   figure regardless of canvas, so moving to 128x128 changes nothing visually. The
   earlier [canvas proposal](CHARACTER_CANVAS_SIZE_PROPOSAL_2026-09-12.md) is wrong
   on this point and is superseded by this document.
3. **Not fixable by resolution.** A 104px re-cut is sharper at close zoom, but at the
   owner's saved fit zoom (0.4446) the character is ~29px tall and every version looks
   the same.
4. **The actual mismatch is drawing language.** The rooms are drawn *for* the pixel
   grid: flat colour blocks, two or three tones per material, hard edges. The crew are
   painted illustrations with soft shading, shrunk to 65px. Beside each other, the
   crew read as pasted on — see `bill-vs-room-art.png`.

## What the test produced

Bill regenerated in the rooms' language (GPT Image 2.5, engineering bank as the style
reference, his own art as the identity reference):

- **Stills: convincing.** He sits in the scene as part of the same art set; the face,
  beard, shoulder patches and boots stay legible at 65px where the current sprite
  smudges (`bill-reimagined-4poses.png`).
- **Identity across views: solved.** A single four-pose turnaround sheet held build,
  suit markings, belt and boots across all four directions — the consistency that four
  separate per-direction generations failed to produce.
- **Animation: not solved.** A six-frame walk cycle kept identity perfectly but barely
  moved: legs shift slightly, arms hardly swing, two poses are near-duplicates. It
  reads as a shuffle. The current walk is worse-matched but better animated
  (`bill-styled-walk.gif`).

## The proposal

Adopt the rooms' drawing language for the crew, as a deliberate art-direction change,
and produce it with generation for poses plus explicit per-pose motion authoring.

**Scope reality:** the character library is **501 manifests, 1,495 states, 7,272
frames**. A full conversion is not a session's work. The largest roots are
`crew-life-v1` (174), `crew-underwater-v1` (152) and `crew-actions-v1` (111).

**Suggested sequencing:**

1. One character (Bill), one state (walk), four directions, finished to shippable
   quality including motion. This is the honest cost probe — if the in-between frames
   need hand authoring, that shows up immediately.
2. Owner review beside the rooms at both zooms before anything else is drawn.
3. Then Bill's remaining locomotion states, then Veld and Branforth, then a decision
   about the action/life/underwater packs, which are the bulk.
4. Companions (Josh, River, Margot) last, and possibly never — they are chunky
   high-contrast shapes that already survive the downsample and already match.

## Known risks

- **Mixed cast during conversion.** A converted Bill beside an unconverted Veld looks
  worse than either state alone, so conversion must land per character, not per state.
- **Motion is the unsolved part.** Generation gives identity, not animation. Budget for
  per-pose authoring or hand-editing the few pixels that carry the swing.
- **Equipment overlays** (`crew-underwater-v1/equipment/`) are registered against
  existing frames and would need regeneration in step.
- **Registrations are welded.** Every converted pack is a new revision linked to the
  previous one; nothing is overwritten, and the old packs stay until the owner retires
  them.

## Owner decisions

1. Is the new look right? `bill-vs-room-art.png` is the evidence; everything else
   depends on this answer.
2. If yes, fund step 1 only (one character, one state, four directions, real motion)
   before committing to the cast.
3. Do the companions convert at all, or stay as they are?
