# iPad card PNG staging — October 19, 2026

Candidate `brinespace-f9155b4334164440`, source SHA-256
`f9155b433416444054575e14330ecf204fbd227b889dc9a7ba71a4f74a231c04`.
Branch `codex/ipad-memory-placement-2026-10-17`, HEAD
`81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus accepted dirty work.
Exact pre-pass snapshots and complete logs/build:
`/Users/Shared/BrineSpace-ipad-optimization-20261019/card-png-staging`.
Prior installed/tested baseline `58324c425a8fc834` remains in sibling
`card-region-demand`. Frozen Mac/Windows deliveries were not edited.

## Change

Tablet thumbnails retain their immutable original PNG payload rather than
mipmapping and ZSTD-compressing every unused card during station setup. The PNG
is decoded initially to validate it and retain exact dimensions, format and alpha
metadata. Mipmaps are prepared only when CPU pixels or the first display are
actually requested. Displayed cards release staging and retain the same ordinary
ImageTexture as before. Desktop/reference and decode-failure fallback paths remain.
No raster source, gameplay, save format or normal rule changed.

## Native and exact-package evidence

The new payload-budget assertion failed on the prior loader (37,522,023 bytes),
then passed at 24,996,178 bytes: **12,525,845 bytes / 11.946 MiB less unused-card
CPU payload** across all79 cards. This is payload accounting, not whole-process
physical RAM. All79 full pixels/mipmaps, alpha/dimension/mip metadata and exact
pixel-byte accounting match; fractional/rotated native sampling also matches.
Unused grid crop preparation still makes zero CPU image reads.

Isolated native card-loader observations were518.709ms before and255.494ms after.
These single observations do not establish a controlled whole-load or physical
loading improvement. The40-room frozen native viewport matches the prior baseline
hash exactly: `2ab4af303d869b02671b72ea05b6285c3dda103bef2217cc9d2ca0cf1875d841`.

Seven actual-PCK tests passed: tablet card storage/regions, raw texture regions
(339checks), shared floors, hull UI(175checks), RunSave and tablet controls.
Asset audit36197selected:0missing/changed/remapped/unexpected. Source audit
437selected/433extras:0missing/changed/unknown. Export/app PCK hashes match:
`4e5633c0f6093a1c2bdf9c02b6a4e909c3fa96fea6000361c59121934b1d9c27`.
Native Release build and strict signature passed; executable SHA-256
`0c8bcd4641b1fdeb3f505034e007e83691f8ddd2bcb0a21b02ef660d72c365d2`.
Scoped independent review found no actionable issues; the reviewer did not rerun
parent tests. Real Mac profiles were isolated and guarded during native probes.

## Physical validation

Installed on iPad13,18/A14/4GB/iPadOS27.2 with all five save/checkpoint files
SHA-256 identical before/after installation. The packaged synthetic40single-cell
room/one-actor workload passed all9phases/5400frames: phase maxima50.291–66.315ms,
no artwork failures and zero automatic stall reports. This is method-driven
idle/zoom/placement requests at1×/2×/4× with deterministic stepping and fixture-only
free build/failure bypass; it does not certify actual paid placement or organic play.
252 valid1Hz exact-PID samples: peak1,856,654,664bytes, last1,815,629,104bytes.
Initial3-room setup4.996s, including3.770s interface/grid and.484s interface art.
No matched process-RAM or whole-load improvement is established.

The benchmark left the five owner files unchanged; they were restored hash-exact
again and the opt-in marker was removed/absence verified. Normal app relaunched.
Actual touch card return, pinch, rotation button, Codex scrolling and Home/activate
passed. Saved-state inspection confirms zoom.0708597375174268→.219108316577404,
rotation1, with resources/room list/hand/cycle/crew/speed and exact timer unchanged.
Normal7-room device card payload35,988,600→23,941,948bytes with the same3cards
uploaded:12,046,652fewer bytes retained for unused cards. This is card storage
accounting, not total app RAM. First owner setup4.133s; cache-sensitive, not a
controlled comparison. There were0logged game errors/automatic reports during
these paused UI checks; automatic capture skips paused stalls, so this does not
certify their absence. No two-finger rotation/pan gesture claim is made.

The five original files were restored byte-exact once more before final owner
Save/title/Continue/Save acceptance. Intentional app terminations produced recovery
notices/reports; these were retained and dismissed, not counted as spontaneous
crashes. Final Save/title/Continue/Save passed full gameplay-state equality and exact
1.11834893097652timer parity. Continue's existing1× speed reset was manually
returned to the original4× before saving. Only timestamp/event/path and
camera/scroll metadata differed. FinalSave92.913ms; original cycle64/seven-room
station visibly paused at4× with menu closed. The authorized2hour helper remains
running. Owner repeat setup3.180s; no controlled whole-load improvement claim.

The final session logged0game errors but **one automatic stall report**:
`brinespace-report-20261019-120615-29798-79132157.zip`. Save & Return to Title
produced425.574ms at the title screen with no active station;408.664ms was
before-render time. The preceding Save itself took60.769ms. The transition cost
is not yet attributed; do not call all stalls fixed. The full report and extracted
performance payload are retained in local evidence; see the portable finding.

[Portable evidence](ipad-memory-placement-evidence-2026-10-19/card-png-staging/ui-summary.json)
and [remaining title-transition stall](ipad-memory-placement-evidence-2026-10-19/card-png-staging/title-transition-finding.json).

Long-term growth, organic multi-crew play and initial loading pauses remain open.
**The iPad build is not release-cleared.**
