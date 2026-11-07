# Branforth bunk motion study

Updated: September 22, 2026. Project: BrineSpace.

## Objective and acceptance
Connect Branforth's standing pose to a compact lower-bunk rest without stretching
legs, changing character scale or concealing hanging boots behind the front rail.
This is a staged bare motion candidate, not a completed runtime interaction.

## Accepted decisions and constraints
Preserve owner furnishing. Use built-in image generation for missing poses and
local deterministic extraction; no Higgsfield or API generation. No publication.

## Current state
character/bunk-contact-study-2026-09-21/ contains branforth-entry-source.png,
branforth-entry-prompt.txt and build_branforth_entry.py. The source is a six-pose
sheet generated with canonical idle and the existing compact sleeping reference.
The builder uses uniform 0.30 scale, canonical palette, alpha threshold 128,
recorded foot/hip anchors and exact padded canonical idle. Output branforth-entry/
contains seven frames, manifest, recipe, choreography and validation. Entry lasts
1.84 seconds; exit reverses it. First four frames stay in front of the bunk rail;
fully boarded poses use its interior layer. No live catalog/controller is changed.

## Verification
output/layout-default-audit-2026-09-21/branforth-bunk-native.log records 47 actual
sprite-player native samples. Entry, leaning and resting captures were inspected:
hanging boot remains visible and compact rest fits between the posts. Build is
reproducible, alpha binary, no canvas-border touches; idle matches canonical pixels
and first/last native images match byte-for-byte. Review animation:
output/layout-default-audit-2026-09-21/bunk-fit/branforth-full-entry.gif.

## Next action
Fit existing equipment to the six authored poses, review tilted shell/hair contact,
then integrate and verify normal travel, sleep, interruption and disk restore.
The new sleeping endpoint should remain from this coherent sequence; the older
static compact endpoint remains a reference. Full expedition, owner visual and
packaged acceptance are still open.
