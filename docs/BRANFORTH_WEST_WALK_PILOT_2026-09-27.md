# Branforth west walk pilot

## Objective and acceptance
Continue the accepted crew animation work with Branforth's independent west walk. Owner review pending; accepted east reference remains the 92-frame v2 recut.

## Accepted decisions and constraints
Preserve the muted yellow engineering markings, graphite suit, silver fittings and anatomical equipment sides. One Hailuo 2.3 Fast 6s/768p generation, optimizer off, 4 credits; confirmed balance 100. No retry or mirrored tools.

## Current state
`character/branforth-video-west-v1/` contains the master input, original source, generation metadata, extraction scripts, 72 PNG frames, manifest and comparison gallery. Selected source frames 16–87 inclusive cover two full cycles over 3000ms at original 24fps. Comparison uses accepted `branforth-video-east-v2`. West stride is shorter than east; retained for review. Candidate not installed.

## Verification
Reviewed source leg phases and corrected master comparison. Fixed scale and pivot; no per-frame resizing or synthetic poses. A constant feathered neutral gain [69/75,67/69,65/70] reduces warm-purple brightness drift without per-frame pumping. No source/export clipping; height 144–149px, soles 169–173px. Seam difference 0.00393 versus internal median 0.00542. Manifest validator: zero errors or warnings. These diagnostics do not replace owner motion acceptance.

## Next action
Review west against the master and accepted east. On acceptance, record it before prioritizing the next missing high-value crew direction. Preserve credits by reusing sources for simpler actions.
