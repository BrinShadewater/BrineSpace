# Project handoff

Updated: September 27, 2026 · Task: Bill rear stance investigation

## Objective and acceptance
Remove exaggerated lateral swaying and crossed steps while preserving Bill's identity and dark uniform. Candidate requires owner motion and stance review.

## Accepted decisions and constraints
Owner continued after v3/v4 rejection. Use paid Hailuo and save free Genjutsu. Existing rear masters remain preserved; no runtime installation.

## Current state
Compared Bill, Branforth and Veld starting images. Bill's feet were wider and splayed; possible influence, not established cause. Built-in imagegen produced a narrower forward-facing stance in `character/bill-video-north-v5/master-source.png`; exact edit prompt saved in master-prompt.txt. This is authored artwork and not a pixel-identical edit. Deterministic preparation restores framing and dark-neutral colour.

One Hailuo2.3Fast trial used the same prompt/settings as v4 with this changed input. Late source frames110–128 show a complete alternating cycle with less apparent lateral lean; early motion is uneven. Original19-frame/24fps timing stays in manifest. A separate1.5-second playback proposal shows the same poses, not new in-betweens. Fixed scale/offset calibrated to this selected section; no per-frame warping.

## Verification
Source contact, every-third-frame legs, detailed late-cycle sheet and exported sprite inspected. Manifest validator and clipping/colour/seam measurements saved with candidate. Numerical checks are not visual acceptance. Review page provides master, source speed and slower timing plus original source video.

## Next action
Owner review at `character/bill-video-north-v5/index.html`, especially remaining sway, foot contact, arm movement and slower playback smoothness. Do not install or call the revised master locked without acceptance. Cost4; confirmed balance56; free Genjutsu remains1. No further trial submitted.

## Owner acceptance
Owner subsequently said "Okay looks good, whats next". Visual acceptance saved in acceptance.json with frame hashes. Playback choice remains unspecified; keep original manifest timing until cast cadence review. Next: refreshed four-direction cast comparison before runtime promotion.
