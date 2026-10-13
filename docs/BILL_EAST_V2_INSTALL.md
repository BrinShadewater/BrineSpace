# Bill east walk installation

## Objective and acceptance
Owner approved revised Bill east walk: “Okay, looks good.” Preserve brown hair and dark matte suit.

## Current state
`character/crew-runtime-matte-v1/bill/manifest.json` now uses 72 byte-identical approved frames under `frames/walk-east-v2`. Original east files retained; previous state metadata saved in `character/bill-video-east-v2/previous-runtime-east.json`. Updated acceptance and active frame hashes. Shared gameplay/Studio loaders already reference this pack; no code change needed. Idle and other directions unchanged. Refresh/restart running previews to reload assets.

## Verification
2355 runtime checks passed; 120 native transition captures completed. Inspected native cast capture saved as `character/bill-video-east-v2/installed-native.png`. Scratch APPDATA used, real owner profile hashes unchanged. No generation spend; last confirmed balance 52 credits.

## Next action
Match Bill west and side idle proportions, then resolve Branforth side gait/proportions and Bill south style. Do not mirror asymmetric equipment. Free Genjutsu run remains reserved.
