# Higgsfield pilot — September 12, 2026

First real test of Higgsfield as an art source. Eight generations, 28 credits
(1,002 left). **No source-tree writes, no registrations, no owner acceptance.**
Everything produced sits in `output/higgsfield-pilot-2026-09-12/`.

## Verdict

**GPT Image 2.5 is the model to use, not Nano Banana Pro.** The audited plan
picked Nano Banana Pro on reputation for localized edits; on this project's actual
art contract it failed the first gate and GPT Image 2.5 passed it.

| | Nano Banana Pro | GPT Image 2.5 |
|---|---|---|
| Perspective | Flat front elevation, twice, including with a reference | Shallow view from above, worktop as a surface, props standing on it |
| Reference obedience | Took content from the reference, not geometry | Took style, geometry and density |
| Background | Solid colour, needs edge-connected removal | Native transparent alpha |
| Invented symbols | Added biohazard labels unprompted | One invented screen icon |
| Cost per 2K image | 2 credits | 3 credits at `high`, 5 at `xhigh` |

## What works

1. **Reference-driven generation.** Passing an accepted asset
   (`assets/material-polish-v2/research-north.png`) as `--image-references` is what
   moved the output from "generic pixel art" to "our art". Prompt text alone did not.
2. **Naming the geometry explicitly.** The phrase that fixed perspective was telling
   the model the reference is *not* a flat elevation: worktop receding, equipment
   standing on it, cabinet fronts facing the viewer.
3. **Self-referencing for revisions.** Feeding a generation back as its own reference
   changed only what was asked — massing — while keeping subject, palette and style.
   The taller variant went from 101 to 120 units at 324 wide, against 123 for the
   accepted bench.
4. **Consistency across subjects.** Two medical banks and one engineering bank from the
   same style contract read as one art set, with department palette carrying the
   difference.
5. **Native-scale readability.** Tools, gauges, hose coils and drawer pulls survive the
   downsample to 324 units wide; the earlier fear of mush at gameplay zoom did not
   materialise.

## What does not work yet

1. **Alpha is soft, never binary.** Every output carries anti-aliased edges (1.69M
   partial-alpha pixels on the engineering bank). A threshold pass is mandatory before
   registration. Cheaper than background removal, but not free.
2. **Invented iconography.** Biohazard labels and a crosshair screen glyph appeared
   despite explicit instructions. Every asset needs an icon review against the
   station-wide sign frame.
3. **Interior depth is shallower than the accepted art.** The research bench has
   equipment inside a glass enclosure; generations approximate that with a recess.
4. **Aspect ratios do not match the authored regions.** Side strips are about 1:3.2;
   the closest available is 9:16. The registration region has to crop, or the asset is
   authored wider than it should be.

## Character sprite test — four directions, one character

Twelve credits, four walk strips of Major Bill generated from two of his own source
strips as references, each cut and put through the real 92x92 path (binary alpha,
feet on the pivot row, 64-colour quantization).

1. **Technically valid**: 42-55 colours, zero soft-alpha pixels. They would pass the
   pack audit unchanged.
2. **Sharper at close zoom** than the shipped frames — better head, shoulders and boots.
3. **Identity drifts between directions.** Shoulder patches moved from red caps
   (south, north) to upper-arm squares (east, west); east and west read taller and
   slimmer than south. The shipped set holds one silhouette across all four, so
   per-direction generation is *less* consistent than what already exists.
4. **The improvement mostly vanishes at gameplay size.** At the owner's saved fit zoom
   (0.4446) the character is about 29 pixels tall and the two sets are near
   indistinguishable (`bill-gameplay-size.png`).

Conclusion: do not re-art the cast. The blur is the fit view, not the source art. If
close-zoom quality matters, the lever is canvas size — see
[character canvas proposal](CHARACTER_CANVAS_SIZE_PROPOSAL_2026-09-12.md). A likely
better use of generation is a single turnaround sheet containing all four directions,
so the model sees its own other views while drawing them; untested.

## The side-wall finding

Generating east and west separately produced two different banks. Mirroring one
produced a consistent pair — and the accepted art shows the same drift (`303x974`
east versus `279x979` west). This became its own proposal:
[mirrored side walls](MIRRORED_SIDE_WALLS_PROPOSAL_2026-09-12.md).

## Recommended pipeline, if this is adopted

1. Generate at 2K, `quality high`, `background transparent`, with an accepted asset as
   an image reference and the geometry named explicitly in the prompt.
2. Threshold alpha to binary, crop to content, area-average downsample to the target
   world width, then palette quantization.
3. Review at native gameplay scale beside Bill and an accepted asset from the same
   family — `gate-comparison-board-v2.png` is the shape of that check.
4. Icon and text review against the sign system; repair shine per component if needed
   by self-referencing, never by global darkening.
5. Register on a copy only, as a new revision linked to the previous one.
6. Owner acceptance recorded separately; it stays null until Alex says otherwise.

## Tooling note

The Higgsfield CLI (`npm i -g @higgsfield/cli`) is the right interface for this
project, not the web UI: prompts become repeatable text, `--image-references` accepts
local paths and auto-uploads, and results download straight into the pilot directory.
Their companion skills are installed but only `higgsfield-generate` is relevant; the
rest are marketing workflows. Both are gitignored (`.agents/`, `.claude/`,
`skills-lock.json`).

## Owner decisions still open

1. Is the style close enough to adopt for new assets, or does the gap in interior depth
   need to close first?
2. New assets only, or also regenerate existing families?
3. Whether to spend credits on an `xhigh` comparison — untested at 5 credits per image.
