# Bill matched walk installation

## Objective and accepted direction
Owner preferred narrower south source, reviewed refined loop and asked to continue. Install reviewed refined south plus west and darker-hair revisions without further credit spend.

## Changes
Shared `character/crew-runtime-matte-v1/bill/manifest.json` now uses copied reviewed exports under `frames/matched-v1`. South is 41 frames from bill-south-loop-v2; remaining directions and idle use bill-hair-match-v1. All copied pixels byte-identical. 208 Bill frames, 647 total crew idle/walk frames. Updated active hashes and acceptance record. Previous manifest saved at character/bill-matched-install-v1/previous-manifest.json; previous art retained. Existing game and Studio loaders use the same manifest.

## Verification
See character/bill-matched-install-v1/validation.json for actual runtime/native test results and owner profile fingerprint check. Native capture is saved beside it when complete.

## Remaining work
North still has old smaller-head motion; larger-head reference awaits animation. South retains source height variation (140–152px), no geometry correction applied. Side idles still retain previous proportions. South uses reviewed source hair, other states use darker crown pass; exact semantic hair matching is not certified. Avoid rerunning the old hair-match builder against its now-modified runtime input; its existing exports are the reviewed source snapshot. No credits spent this turn; last confirmed 36, free Genjutsu preserved.
