# iPad crew cache writes — October 19, 2026

Validation 2 `brinespace-e8afae3a95947e78` is installed on physical iPad13,18
(A14, 4GB, iPadOS27.2), bundle
`com.shadewater.brinespace.nativeoptimization20261017`.
Branch `codex/ipad-memory-placement-2026-10-17`, HEAD
`81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus existing accepted dirty work.
Evidence and complete signed build:
`/Users/Shared/BrineSpace-ipad-optimization-20261019/grid-loading-pass`.
Prior installed `efdb7ff32be59034` remains complete in `title-load-pass`;
`f9155b4334164440` in `card-png-staging` is also retained. Frozen/public Mac and
Windows deliveries and the integration-monitor checkout were not changed.

## Change and attribution

Cold native profiling attributed 433.632+301.009ms to synchronous crew prepared-cache
stores. These disposable serialized files now use one bounded CPU writer. Main
thread serialization, index/LRU ownership and admission remain explicit; the worker
only hashes/writes immutable bytes. A second write joins the previous ticket, and
batch completion/index flush drains the last writer. Successful tickets can be
finished repeatedly without double-counting, including overlapping batches. Existing
direct store callers still observe synchronous completion. No textures, Images or
SceneTree operations move into the writer. Cache format and source pixels remain
unchanged; saves never depend on these files. One pending payload is bounded below
4MiB, in addition to the existing four preparation workers. This is not a demonstrated
retained-memory reduction.

Demand-deferred James loading was rejected because normal checkpoint capture and
validation still require his cargo bindings. Cross-bank deduplication would remove
only 181,299 of 102,953,537 compressed source bytes and was not implemented.
Temporary main/grid and store-timing instrumentation was restored byte-exact.
Alternating fresh native processes measured interface/grid new2719/2079ms versus
old2183/2158ms; variability prevents claiming a consistent native speedup.

## Verification and exact package

Eight scoped native tests passed, including the new red/green cache-write fixture,
corruption fallback, cache workers/session/index, source keys, crew and title loading.
The new fixture covers joined bounded writes, exact reused pixels, failed-write
metadata preservation and idempotent ticket accounting. Independent scoped static
review found no actionable issue. Twelve actual-PCK fixtures passed: cache writes,
workers/session/source keys, title, cards/regions, raw texture regions339checks,
shared floors, hull UI175checks, RunSave and tablet controls. Asset/source audits,
Release compilation, strict codesign and signed/export pack equality passed.
Native tests used isolated profiles and guarded the real Mac profile fingerprint.

Source SHA-256:
`e8afae3a95947e7863d08f4c8ae1b0f222615a1eb10da05f5aa489f0aab8e3c8`.
PCK SHA-256:
`d29dbc565c54f8e7eef1ac6d052823458bb559595d65ee2bc2d15f84b75caa09`.
Executable SHA-256:
`df6e3acebc8150a574fa5b4937362188b1a40f238ffe7bb105199595520e6e47`.
Export config restored exactly, temporary QA source files removed; CR-at-EOL-aware
diff whitespace check passed. No commit, push or public release.

## Physical observations and limits

Normal paused cycle64/seven-room checkpoint, water0; no free-building/stress marker.
Old and new builds each had one fresh-process empty-crew-cache load. Cache directories
were renamed and verified, not deleted, preserving the original warmed directory and
baseline-generated files. Installation preserved all five saved-progress files by
SHA-256. Actual Continue reached the station on both builds. Candidate Save & Return
to Title and a second Continue reached the station without logged game errors.

| Measurement | Old efdb7ff32be59034 | New e8afae3a95947e78 |
|---|---:|---:|
| Empty-crew-cache station setup | 6701ms | 6506ms |
| Interface/grid part | 5271.649ms | 5119.979ms |
| First title-return frame | 218.142ms | 243.476ms |
| Sampled whole-process peak footprint | 1,917,226,360B | 1,926,499,704B |

New cached station setup3157ms, interface/grid2305.204ms. These are single ordered
runs with different durations and uncontrolled device/OS caches, not proof of a
causal loading or RAM improvement. Candidate manual report still shows a6129.784ms
setup frame and2644.289ms after-render interval. Title-return and initial loading
pauses remain open. Automatic reporting skips paused stalls; zero automatic stall
reports does not certify pause-free loading. Compressed crew source payload remains
102,953,537B; do not substitute that for whole-process memory.

Actual card return cleared selection; pinch changed saved zoom0.07086→0.21911;
rotation button saved rotation1; Codex touch scrolling and Home/activate returned
paused. Gameplay fields and exact timer matched through these checks. Two-finger
pan/tap were not automated. The initial two-hour helper ended normally, and a
replacement timed out before authorization. Owner approved the next replacement
(helper8545); it remains active with the two-hour limit.

After restoring the originals, an actual UI Cancel established a no-selection
baseline. Save/title/Continue/Save then matched the complete state dictionary,
workspace and exact timer; only save-path/timestamp/event-history metadata changed.
The manual report had errors0, Save68.823ms, title-return223.720ms and still a
2612.841ms after-render interval. Initial setup in that new process3984ms.
This does not establish stall clearance or a RAM improvement.

Finally all five originals from before the cold baseline were restored again and
verified SHA-exact after the normal app reached the station. Left paused4x,
cycle64/seven rooms, menu closed. Fresh launch and hashes are in
`final-owner-restoration.json`; screenshot `final-original-station.png`.
Intentional process stops during restoration generated normal recovery notices;
no spontaneous crash was observed in these checks. Follow fresh launch metadata,
not an old PID/container. No new build was needed for this authorization continuation.

The earlier first-title full-state probe failed on selection/hover and a tiny
camera recenter difference relative to the pre-baseline view. Its evidence is
retained; it is not full-state acceptance. The controlled no-selection pair above
passed. The harness also initially missed OCR of4x; targeting now uses the visibly
confirmed4x column on the current RESUME row, since inspector layout shifts it.
Not release-cleared. Continue attribution of first-use grid/render work and title
return, with whole-process measurements and preserved owner state.
