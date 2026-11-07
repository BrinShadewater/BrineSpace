# Handoff to Astra: Bill's art conversion — September 12, 2026

Everything an image-generation agent needs to continue the crew art conversion.
**No character art in the source tree has been changed.** All output lives in
`output/higgsfield-pilot-2026-09-12/`. Owner acceptance is recorded nowhere yet;
treat every asset here as a preview.

## 1. The decision that was made

The crew do not match the rooms because of **drawing language**, not resolution.
The rooms are drawn *for* the pixel grid — flat colour blocks, two or three tones per
material, hard edges. The old crew are painted illustrations shrunk to fit.

Ruled out first, with evidence (see [pipeline doc](CHARACTER_ART_PIPELINE_2026-09-12.md)):

- **Not the cleanup path.** Re-cutting from the original sources reproduces what ships.
- **Not canvas size.** Bill is ~73px inside both the 92px and 128px canvases.
- **Not AI upscaling.** PixelLab's `image-to-pixelart` on the originals came out worse
  than the shipped frames — it invented a dark eye mask and muddied the belt.

The owner approved **option C**: redrawn in the rooms' language, in a muted grey-green
suit. Measured against the shipped suit: hue 160° vs 169°, saturation 0.13 vs 0.12.

Reference art to match, in priority order:
1. `output/higgsfield-pilot-2026-09-12/bill-reimagined/turnaround-greygreen.png`
   — the approved four-pose turnaround. **This is the identity anchor.**
2. `output/higgsfield-pilot-2026-09-12/preview-pack-full/` — the finished 17-state pack.
3. `output/higgsfield-pilot-2026-09-12/brief3-gpt-07-engineering-sculptural.png`
   — the room bank whose drawing language the character must match.

## 2. Engine changes (committed, tests green)

| change | commit | effect |
|---|---|---|
| Character mirroring at load | `7fafaa9e` | A pack declares `{"mirrorDirections": {"west": "east"}}`; the loader flips the raster, reflects the pivot about the frame centre, copies timing, tags `crew_mirrored_from`. Authored art always wins. Only east/west may mirror. |
| Per-pack standing height | *pending commit* | Frames carry `crew_standing_height` from the manifest's `standingHeight` (default 74). Six draw sites divide by it instead of a literal 74. A 148px pack lands at the same 65.28 world units as a 74px one. |

Tests: `tests/test_character_mirror.gd`, `tests/test_crew_standing_height.gd`, both in
the `crew` subsystem of `tests/index.json`.

**Why this matters to you:** art can now be authored at any density. Bill's preview
pack is 2× — a 148px figure on a 184×184 canvas, pivot (92, 172) — which brings him to
2.27 source pixels per world unit against the room banks' median of 2.1. At the old
74px he was 1.13, which is why he looked coarse beside the props.

## 3. The generation recipe (what works, proven by A/B)

**Use the right tool per state kind. This was tested, not assumed.**

| state kind | tool | why |
|---|---|---|
| Idles, turnarounds, any static pose | GPT Image 2.5 via Higgsfield | Only model that draws in the rooms' language and holds identity from a reference |
| **Cyclic locomotion** (walk, run, carry-walk) | PixelLab `animate-with-text-v3` | Real stride, foot lift, arm swing. GPT Image produces near-identical frames — it cannot animate a loop |
| **One-way pose changes** (kneel, stand, sit-down, lie-down, get-up) | GPT Image 2.5 six-frame sheet | A/B on `kneel-east`: GPT 47px of descent vs PixelLab 32px, and PixelLab's first four frames barely differed |
| Opposite profile (west) | **Mirror the east frames locally** | Never generate both. GPT Image draws left-facing as a three-quarter view, 19–22px wide vs 32–40px; explicit "make them mirror images" did not fix it |

Rule of thumb that matched the data: **the shipped manifest's own `loop` flag is the
switch.** `loop: true` → PixelLab. `loop: false` → GPT Image sheet.

### Settings that work
- Higgsfield: `gpt_image_2_5`, `--resolution 2k --quality high --background transparent`,
  `--aspect_ratio 21:9` for six-frame strips, `1:1` or `16:9` for single poses.
  3 credits per image at `high`.
- PixelLab: `animate-with-text-v3`, `frame_count 6`, `no_background: true`,
  **`enhance_prompt: true`** (it writes a better motion brief than hand-written pose
  text). First frame at 160×160 with a 148px figure. 1 generation per state.
- `animate-with-skeleton` was tested and **rejected for locomotion**: it takes exactly
  3 frames per call, cost double, produced white outline halos, and did not close the
  loop. Keep it for an exact single pose only.
- `create-character-with-4-directions` and `/rotate` were tested and **rejected**: both
  reinterpret the character rather than preserving the approved design.

### Local bake (do not skip)
1. Threshold alpha to binary — packs never carry partial alpha.
2. Despeckle: drop detached components under ~40px (GPT sheets leave fragments).
3. Scale **per source family**, not globally: the 2K turnaround, PixelLab's 160px
   frames and GPT's sheets have wildly different native sizes. Use each family's
   tallest standing frame as the reference for its own scale.
4. Seat feet on the pivot row; centre horizontally.
5. Quantize the **whole pack together** to 64 colours (`Image.FASTOCTREE`, no dither)
   so every state shares one palette, as `character/major-bill-v2/build_pack.py` does.
6. Preserve the shipped manifest's `frameDurationsMs` and `loop` per state; do not
   invent timings.

## 4. Where the work stands

**Done — Bill's full base pack**, `output/higgsfield-pilot-2026-09-12/preview-pack-full/`:
17 states, 82 frames, one 64-colour palette, 184×184, `standingHeight: 148`.
idle ×4, walk ×4, run ×4, walk-south-east, interact-east, kneel-east, stand-east,
repair-east. West states mirrored from east and tagged `mirroredFrom`.

**In progress — pass 1 of the extended library.** 80 states (480 frames) of dry-land
actions: 59 to generate, 21 mirror for free. Plan file:
`output/higgsfield-pilot-2026-09-12/pass1-plan.json`. Batch 1 (10 states) is generated
into `output/higgsfield-pilot-2026-09-12/pass1/`; **49 states remain**.

### Batch 1 results — read this before continuing
- **Worked**: `kneel-north/south`, `stand-north/south` (36–55px of real movement),
  `carry-east` (crate held convincingly at chest height).
- **Failed — object disappeared**: `carry-north`, `carry-south`. Same prompt as
  `carry-east`, but the model walked him without the crate. Name the carried object
  explicitly and repeat it per frame.
- **Failed — motion too small**: `interact-north/south` (3–4px). The arm barely
  leaves the body. Needs the movement described as large and per-frame.
- **Weak**: `repair-north`. From behind, the crouch and hands do not read as work.
  Consider whether rear views of hand-work states are worth generating at all.

Roughly 60% of states land first time. Budget rework accordingly.

## 5. Still blocked, needs an owner decision

- **Equipment overlays** — 156 frames in `character/crew-underwater-v1/equipment/`.
  A helmet overlay must align frame-for-frame with the body underneath. Our bodies are
  new, so overlays cannot be generated independently. Either regenerate as full
  body-plus-helmet states, or Bill stays unhelmeted.
- **Water poses** — ~336 frames (swim, tread, dive). No art direction established for
  the new style: buoyant posture, no ground contact, pivot meaning changes. Get one
  swim pose approved before generating the rest.
- **Cast scope** — Veld and Branforth would follow the same recipe. Companions
  (Josh, River, Margot) are chunky high-contrast shapes that already match; converting
  them may be unnecessary. Full cast is 501 manifests, 1,495 states, 7,272 frames.

## 6. Hard constraints

- **Never overwrite art, registrations or manifests.** Registrations are SHA-256
  welded; a change means a new file and a new revision linked to the previous one.
- **Nothing enters the source tree without owner acceptance**, recorded separately.
- **North and south are never mirrored** — a vertical flip puts feet above the head.
- **No text in artwork**, and no invented iconography: a biohazard symbol and a
  crosshair glyph both appeared unprompted and had to be rejected.
- Read `skills/brinespace-character-pipeline/SKILL.md` for the pack contract, and
  `docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md` for material and palette rules.

## 7. Cost so far

Higgsfield ~50 credits of 1,000 (about 950 left). PixelLab ~25 generations of 2,000
(subscription, not cash). The expensive input is review, not generation.
