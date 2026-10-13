# Project handoff

Updated: September 28, 2026 · BrineSpace · Muted south and east v3

## Objective and acceptance
Owner likes south direct v2 motion but requests slightly muted colour; east must be regenerated and match that palette. Preserve south poses. New colour treatment and east motion remain candidates for review.

## Accepted decisions and constraints
Deterministic colour-only south edit, one paid east retry. Preserve graphite suit, muted burgundy, brown hair, warm skin, silver hardware and existing matte treatment. No per-frame resizing, no pose interpolation, no runtime replacements yet. Higgsfield credits/free run remain reserved.

## Current state
`tools/prepare_bill_muted_redo.py` creates `character/bill-south-muted-v1` from all 141 already-matte south direct v2 frames: chroma multiplied by 0.90 about encoded Rec.709 RGB luma, alpha/geometry identical. It does not apply matte twice. Source video/frame hashes and output hashes retained.

The same tool prepares `character/bill-east-direct-v3/master-input.png` using the previous east master. A fixed feathered fabric-only RGB gain (0.8451,0.7971,0.7917), calibrated to south's source neutral fabric median, darkens the body below the head; then foreground chroma is reduced 10%. Background and geometry unchanged. Exact treatment metadata is saved. New prompt requests an easy natural side walk with upright constant-size torso. Generation task 446794947752469 completed; original video and matte extraction saved.

Combined review: http://127.0.0.1:8791/character/bill-muted-east-south-v1/. East previous/new, south approved/muted, full source timing, game-scale rows and raw source videos (south raw video is explicitly before the colour pass). No cycle selected or runtime installed.

## Verification
South: 141 frames retain exact alpha/poses; maximum encoded luma change 0.4974 of 255 from quantization. East: 141 frames, 24fps, no clipping. Height first/last 148/142px, range 141-149; some residual size variation remains. Neutral material medians east range (51,47,48)-(54,51,52), muted south (50,45,46)-(55,51,53), much closer than prior east. Statistics support sampled visual comparison, not full material/temporal acceptance. Both 24-pose contact sheets inspected; motion review remains with owner. No Godot tests or owner-save writes needed.

## Budget and next action
One east generation estimated US$0.19 this turn, seven direct attempts total US$1.33; actual billing unverified. South processing costs no generation credits. Review colour subtlety and new east gait; retain accepted south motion even if further palette adjustments are needed. Cut a full alternating cycle only after source selection, then validate native installation separately.
