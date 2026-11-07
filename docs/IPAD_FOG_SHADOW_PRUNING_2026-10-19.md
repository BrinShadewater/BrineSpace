# iPad fog shadow pruning — October 19, 2026

Validation 2 **brinespace-f218152558a44c07** is installed and tested on the physical A14 iPad13,18 / 4 GB / iPadOS 27.2. The shader skips shadow checks for a lamp whose unoccluded brightness cannot exceed the illumination already found. Occlusion can only reduce that lamp's contribution, so skipping it preserves the maximum. No new texture, visual reduction, asset replacement, save rule or gameplay change was introduced.

Branch: `codex/ipad-memory-placement-2026-10-17`, base HEAD `81b2f9a4a36eb0e3162d86ccfb4e9ef735836122`, with earlier accepted uncommitted work preserved. Source fingerprint `f218152558a44c07d046dcd12bbb369cc74bad629a98f9ec458b8279d015a18c`; PCK SHA256 `a0ae2dae1f1aec47d5226381aa38d65a13393c7bd2044a2d03882367ca61128b`. Compared with the preceding validation manifest, the only changed selected asset is `scripts/underwater_fog.gdshader`; no additions/removals. Strict signature passes and the signed pack equals the audited export. Temporary project/export metadata was restored byte for byte. Frozen/public Mac and Windows builds and the protected integration checkout were untouched. No commit or push.

## Verification

- Instrumented brightest-first, 48-overlapping-lamp fixture fails on the original shader and passes on the candidate: only the first useful lamp needs its 23 shadow samples. This is a controlled worst-case work bound, not a whole-game percentage gain.
- Eight native image cases match exactly across **2,457,600 channels**, varying lamp counts, directions/radii, obstruction masks, time, zoom and Reduced Motion. The actual synthetic 40-room station's four fixed-clock captures also match across **15,481,600 bytes** each.
- Ten exact-pack fixtures pass, including the new shader fixture, crew/cache fixtures, Hull UI's 175 checks, Save and tablet controls. The strengthened final shader fixture also passes separately against the exact pack. Asset audit: 36,197 checked, no missing/changed/unexpected files; source audit: no missing/changed/unknown scripts. Independent scoped review found no actionable correctness issues. Test UID normalized to its canonical spelling.
- Completed native runs use scratch profiles and assert the real Mac profile fingerprint stayed unchanged.

Native Mac M4 end-to-end rendering remains inconclusive: reference medians **21.398 / 21.974 ms**, optimized **21.137 / 22.478 ms**. A generic zero-angle sprite probe was not adopted: both versions already batched to one draw call.

## Physical observations

Same copied synthetic 40-room/four multi-cell/52-cell station, cycle 65, **paused**, fixed camera, all 40 rooms visible, normal failure/build rules and fixture-only seeded reserves. The assembly is footprint-valid, not organic/full-port-connected/multi-crew acceptance. Each side sampled five approximately one-second performance buckets spaced 15 seconds apart. This is not a full-run FPS distribution or repeated A/B/A experiment; cache, thermal and timing differences remain uncontrolled. Another installed QA app was left untouched.

| Observation | Previous build | Updated build |
|---|---:|---:|
| Sampled FPS median | 28.53 | 29.44 |
| Sampled FPS range | 22.62–29.33 | 28.30–35.68 |
| Draw calls | 2965 | 2965 |
| Retained texture counter | 1092.854 MiB | 1092.854 MiB |
| Valid nominal 1 Hz memory samples | 215 | 216 |
| Process footprint peak | 2.155 GB | 2.166 GB |
| Process footprint at end | 2.155 GB | 2.164 GB |
| Station build | 5608 ms | 5587 ms |
| Interface/grid | 2883.602 ms | 2842.399 ms |
| Save restore | 1864.381 ms | 1881.017 ms |

Both observations recorded zero game errors and no crash. **No RAM saving or reliable overall loading/frame-rate improvement is established.** The previous active large-station performance gate remains unpassed. Multi-second loading callbacks still occur.

On the disposable station, the visible Rotate button was exercised, then a drag into the hand cleared blueprint placement controls. The inspector correctly retained its description. An initial OCR assertion wrongly expected “No Selection”; that was a harness assumption, not a game failure. No new paid placement, construction completion, pinch or two-finger gesture acceptance is claimed.

## Owner restoration and final state

All five core save/checkpoint files were backed up, restored hash-exact before installation, preserved hash-exact by installation, and restored hash-exact again after the disposable test. The owner station was then loaded, saved, returned to title, continued and saved again. **Full gameplay state and timer parity pass:** cycle 64, seven rooms, resources/cards/crew intact, timer `1.11834893097652`. Existing Continue speed reset to 1x was manually corrected to the original 4x before each save; that separate issue is unchanged. Final Save **62.029 ms**, result 0, errors 0.

Final differences outside gameplay state/timer are timestamps, event history, file path, scroll and workspace camera center. Do not claim whole-file parity after UI testing. Final app PID **11116**, paused at 4x, menu closed. The same two-hour touch helper PID **64358** stayed connected without another authorization and was left running.

Next work: measure room/environment texture residency and room-content submissions. Memory growth, initial loading stalls, active large-station performance and iPad release readiness remain open.

[Portable evidence](ipad-memory-placement-evidence-2026-10-19/fog-shadow-pruning/SUMMARY.json). Full local artifact: `/Users/Shared/BrineSpace-ipad-optimization-20261019/fog-shadow-pruning`.
