# Placement and navigation CPU — October 15, 2026

Two contained changes are installed in normal source: skip impossible synergy
recipe scans within one evaluation, and preserve already-proven canonical door
seams inside an unchanged navigation prefix. Normal placement frames improve
53–55→46–52 ms in the clean comparison. Idle remains about 50 FPS; 4× peaks are
mixed. No 60 FPS, renderer, art, clock, quality, export or gameplay change is claimed.

A test-isolation mistake occurred and was corrected during this task. Progression
was restored from its untouched protected backup; two legacy test-metadata files
remain changed. The whole player folder was not untouched. See the
[incident and recovery](TEST_PROFILE_INCIDENT_2026-10-15.md).

## Installed changes

`scripts/synergy_manager.gd` builds an evaluation-local set of IDs from occupied
cells. Recipes with an absent required type skip their expensive adjacency,
hallway and pattern scans. Existing recipe/cell/direction iteration and link
ordering stay intact for possible recipes. Passage links run first as before;
the separate tagged-medical Cryo tail still runs even without Life Support.
There is no persistent result cache or revision/invalidation shortcut.

`scripts/bill_npc.gd` already retained an unchanged leading graph prefix, but
disconnected and revalidated all door seams on every rebuild. It now remembers
which ordered ID pairs were proved through the canonical boundary path. A seam
can remain connected only if both IDs are in the proven unchanged prefix and
hardware/room-lock policy matches the actor's copied previous snapshot. Existing
reciprocal seam handling then reuses that proof. Noncanonical seams retain their
original validation. Staged builds, layout changes, changed locks, missing points
and disabled optimization flags retain the original paths. Disabled-node reset,
point IDs, weights, ordered connections and route selection stay unchanged.

Bookkeeping remains actor-local, replaced each rebuild and bounded by that graph's
current boundary records and locked cells. It introduces no new texture or image
cache. `--reference-prefix-boundaries` selects the reference seam behavior.
Main placement, paid completion, costs, RNG, cascades and comms code are untouched.

## Trace and attribution

Actual release diagnostics use the latest frozen one-spare private LOD cohort,
including the previously accepted water, Moonbay and Bill lookup improvements.
Twenty overlay files are frozen in `C:/bs-placement-nav-20261015/`. Native jobs
are serial, silent, on the secondary display with scratch APPDATA.

The benchmark action includes a synthetic valid-site search. That search costs
about 1.2–1.4 ms and is unchanged; it must not be described as room creation.
The actual placement call costs about 6.8–7.2 ms, almost entirely synergy evaluation.
Its diagnostic breakdown includes 100 adjacent-pair scans (~1.17 ms), 99 passage
scans (4.1–4.24 ms) and eleven pattern scans (1.27–1.35 ms).

The candidate evaluates twelve possible pair recipes in this station. Synergy
evaluation falls to 1.034/1.036 ms at 1×/4×; the actual placement call is about
1.08 ms. Two normal companion rebuilds fall from 8.108→7.000 ms in one diagnostic,
including boundary work 2.786→1.713 ms. The 4× navigation diagnostic remains mixed:
large point/link suffix rebuilds dominate. These scopes nest and must not be
added together or treated as GPU time. Instrumented frame timings are not the
average-FPS evidence below.

## Controlled navigation check in actual release mode

The loaded large station is frozen while two temporary actors rebuild identical
input geometry. Reference and candidate order alternate for twenty pairs per
case. The first pair also verifies every ordered point/connection/weight/disabled
record, point/room maps and ordered boundary bookkeeping. Initial variant creation
can differ in cache warmth, so both all-twenty results and warmed-nineteen summaries
are retained. The latter excludes only the first pair uniformly across cases.

| Rebuild case, warmed 19 pairs | Reference mean | Candidate mean | Saved |
| --- | ---: | ---: | ---: |
| Unchanged warm graph | 3.468 ms | 2.840 ms | 0.627 ms |
| Append room | 4.053 ms | 3.321 ms | 0.733 ms |
| Middle-room rotation | 14.490 ms | 13.921 ms | 0.570 ms |

Candidate means improve in both execution-order subsets for all three cases.
Warmed p95/max also improve in these samples. All-twenty means are
3.468→2.837, 4.051→3.319 and 15.017→14.163 ms. The middle case's first cold variant
contributes reference/candidate maxima 25.015/18.762 ms, which are not attributed
solely to seam retention. The station has 14,097 points; append has 14,382.
Warm/append retain 268 ordered seam records; middle rotation retains 5,587 points
and 28 seam records, with 268 current canonical records. This establishes a local
construction saving, not a frame-rate or universal hitch guarantee.

## Clean FPS and placement comparison

The first full `ab1` attempt had a noisy early reference stretch and its final
reference process was rejected for a minimized window. The three completed runs
and failed log are preserved but the series is excluded from acceptance. After
the owner confirmed visibility and paused other runs, `focused1` runs four fresh
processes: reference → candidate → candidate → reference.

Actual Godot 4.7.2 release mode, OpenGL Compatibility, RTX 4070 Ti, 1920×1080.
Mixed large station; 180 warm steps, 120 frames per idle/placement phase at 1×/4×:
**1,920 measured frames, eight exact paired gameplay/camera/path phases**.
Every process verifies actual loaded source/backend and immutable overlay identity,
including Main's actual synergy constant. The 255-sample process guard detects
no foreign Godot, duplicate game or monitor error; maximum sample gap 0.774 s.

| Actual placement frame | Reference | Candidate | Difference |
| --- | ---: | ---: | ---: |
| Normal, forward | 52.852 ms | 46.237 ms | −6.615 ms |
| Normal, reverse | 54.871 ms | 51.717 ms | −3.154 ms |
| 4×, forward | 79.374 ms | 71.810 ms | −7.564 ms |
| 4×, reverse | 76.126 ms | 78.696 ms | +2.570 ms |

The action call, including unchanged site search, improves in all four pairs:
7.884→2.336, 8.234→2.490, 8.097→2.463 and 8.151→2.593 ms. Normal crew CPU improves
9.570→8.009 ms forward but worsens 9.829→11.281 ms reverse. At 4× it is
27.608→27.659 and 26.683→30.611 ms. No sampled atlas upload coincides with these
four action frames. The combined construction reduction is real, but aggregate
crew work and full-frame peaks still vary, especially for large suffix rebuilds.

Pooled normal idle is **49.57→49.96 FPS**, 20.1725→20.0151 ms. Forward idle improves
20.4739→20.0742 ms; reverse worsens 19.8711→19.9559 ms. This is essentially flat,
not a dependable sustained-FPS improvement. Pooled p95 is 22.663→22.188 ms.
Across the whole idle+placement/1×+4× workload, 44.78→45.56 FPS. Whole-run means
improve forward 22.4982→21.8573 ms and reverse 22.1693→22.0380 ms; whole-run p95
improves forward and worsens reverse. Only three of eight phase p95 pairs improve.
Zero candidate phases pass both mean and p95 ≤16.667 ms.

In the following sixty frames, normal speed has no >50 ms frame in either lane;
its maxima improve 40.573→35.501 and 35.279→32.846 ms. At 4× following-window
maxima improve 60.991→59.291 and 56.847→53.982 ms, but still hitch. Counts over
50 ms fall 3→2 and 3→1. Including placement, the forward normal window loses its
single >50 ms frame; reverse retains one. Window means/p95 are mixed. This is not
hitch-free or 60 FPS acceptance.

Peak engine texture counters are 2,046.109 MiB in both references and the reverse
candidate; forward candidate is 2,044.109 MiB. Texture policy is unchanged and no
memory-saving claim is made. This focused sequence has no zoom phase and must not
be directly compared with the earlier ~2,778 MiB zoom cohort or treated as an
endurance/process/GPU-memory measurement.

## Verification and source admission

- Eleven installed-source regressions pass with zero skips in
  `output/test-runs/20261015-154239-headless/`: navigation prefix, boundary reuse,
  ownership, staggering, companion topology, topology signature, segment parity,
  synergy evaluation and paid/cascade/large-room/completion behavior.
- Expanded graph oracle: 1,488 checks, 259,265 exact ordered records, 2,328 routes
  and 126,528 sorted targets. Includes adjacent large rooms inserted globally
  row-major and column-major, partial-prefix edits, locks, revision changes and
  staged rebuilding for Bill and Marsh. Private Marsh testing binds its complete
  motion inheritance chain to the candidate base.
- Synergy oracle: 8,043 checks / 1,188 cases / 112 recipes. Full ordered output,
  ordinary/stabilized bonuses, alias ownership and input bytes match the legacy
  evaluator, including immediate ID/layout/rotation/tag mutations and tagged
  medical Cryo without Life Support.
- Twelve cross-process station RGBA pairs and twelve within-process repeat pairs
  are exact at three zooms with lighting on/off. Five additional first-placement
  frame pairs match state/camera/readiness and pixels. Both draw live first,
  activate one ready capture on the next frame and retain it thereafter. Fitted
  station appearance visually reviewed. Crew/doors/warnings remain on live paths.
- The controlled native release navigation check adds three exact full graph
  states and alternating-order CPU evidence. Independent review found no
  actionable implementation issue after connected-prefix coverage was added.
- Four fake-engine runner isolation checks pass. Darwin/Linux environment paths
  are simulated; this is not native Mac/Linux performance verification.

The timed candidate and installed code differ only in two clarified comments;
an executable-code comparison verifies equality. The admitted pack matches the
installed normalized source and is the pack used for final image checks and the
release navigation microbenchmark. Original script UIDs are preserved.

Installed SHA-256:

- Bill: `b7e0a3cc21b8d928a38e874f7ac493a73e9489eab73ca4150362cc79f663c53a`
- Synergy: `00f3c72e25e4b3a4d463b3f824c36bfb8659b74f7e9eb8aadc12d02937a03261`

Reference / timed candidate / admitted PCK SHA-256:

- `13b54175cfea87636310b12e0f975fa8aafc43ea0523e02c78e6ea30d8fd0750`
- `fe359d76c7bb3798cc8bdb5b9749c0f310629856d90df21447f0b9abfb3db9a4`
- `d29c5665aeba192d2912cac168a979032760354e5791aa56217109662521612b`

The task has 35 clean saved owner guards and one failed guard for the documented
incident. Final full fingerprints equal the 2,948-file post-recovery baseline.
This does not erase the two pre-existing test-file changes or establish that the
whole folder matches its pre-incident state. Early extractor stalls and explicit
external-script test adapter/parser failures are excluded; accepted runtime logs
have no engine errors. No task-owned game remains; the existing editor is left open.

Evidence: `C:/bs-placement-nav-20261015/`: `focused1-analysis.json`, four valid run
JSONs/identities/owner guards, three diagnostic traces, `nav-release-micro.json`
and analysis, `visual-parity.json`, `first-paint-parity.json`, `final-audit.json`,
normal regression logs and incident evidence. Helpers:
`output/placement-nav-20261015/`.

This accepts the contained normal-source CPU reductions. Private distant-room
LOD remains private, and frozen Windows QA remains separate from a current-roster
packaged Windows/Mac release. Next useful targets are large navigation suffix
point/link rebuilding at 4× and the steady rendering/exterior/upload costs; do
not repeat an unchanged timing series to seek a favourable FPS result.
