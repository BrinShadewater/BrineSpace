# Branforth south walk pilot

## Objective and acceptance
Continue crew animation improvements with a south-facing walk matching current Branforth design. New front reference and walk remain review candidates; not installed.

## Accepted decisions and constraints
Dark graphite suit, silver fittings, muted yellow engineering accents, grey moustache/hair, forehead goggles and correct anatomical tool sides. Preserve complete gait cycles and source cadence; no per-frame size normalization.

## Current state
`character/branforth-video-south-v1/` contains reference-derived transparent front artwork, prepared input, source video, metadata, extraction scripts, manifest, 76 frames and review gallery. Front source was isolated with built-in image generation from crew-reference-v5; this does not overwrite the accepted side masters. One Hailuo 2.3 Fast 6s/768p trial with optimizer off, 4 credits, confirmed balance 96. No retry.

## Verification
Inspected source contact sheet and leg phases every three frames. Source frames 20–95 retain three full alternating cycles at 24fps, 3167ms. Fixed scale calibration counters source body expansion. Constant feathered neutral gain [69/85.5,67/80.5,65/82] targets accepted side midtones; corrected diagnostic medians range [69,67,65] to [72,70,69]. No clipping, height 145–151px, sole 167–173px. Seam difference 0.00810 versus internal median 0.00842. Manifest: zero errors/warnings. Original MP4 and front reference retained unchanged; the front reference is lighter than corrected animation. Numerical diagnostics do not establish owner motion acceptance.

## Next action
Review south gait and front/side identity before installation or another paid generation. Current idle/walk and cardinal palette candidates remain staged. Budget is 96; prioritize Bill's next useful replacement after this review rather than exhausting one character.
