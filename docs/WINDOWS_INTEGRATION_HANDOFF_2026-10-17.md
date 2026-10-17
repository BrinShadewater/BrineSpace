# Windows integration handoff — October 17, 2026

Read this first on the Mac. The owner wants **Windows, Mac and iPad released together**. This branch publishes the tested Windows source for review alongside the Mac-specific fixes and iPad port. It does not merge the Mac work, rebuild an export or promote a release.

**Branch:** [`codex/windows-integration-20261017`](https://github.com/BrinShadewater/BrineSpace/tree/codex/windows-integration-20261017).

## Shared starting point and commits

The Mac kit was a dirty source snapshot, **brinespace-d3cfa1890bafefe7**, not just Git HEAD. This Windows workspace also had uncommitted work. A comparison against Git main alone would mix the shared kit with the later Windows changes.

| Commit | Scope |
|---|---|
| `632612a0bfb258660661f47041ba9d1409eacf49` | Records the selected shared d3 source/assets/tests relative to repository base67e7db9. Contains the already shared performance/save/crew/art integration, including140 needed LFS rasters. It is context, not a new post-kit art pass. |
| `9f7c0fae2becc477c31935a9d5449ff174f8c38c` | Focused post-kit Windows loading changes: **eight runtime files**, two existing test/index files and twelve new test/UID files. No post-kit artwork or save/gameplay change. |
| Branch tip | This handoff, existing reports, portable summaries/reference images and validation fixtures. Includes a standalone Python-test import bootstrap and two router regressions with paired UIDs/native routing. |

Existing tracked authoring/archive content is retained. Local import sidecars, SDK binaries, exports, logs, player profiles and unrelated later character/art/skill work are excluded. The newly published source is selected from the frozen snapshots, rather than copied indiscriminately from the mixed live checkout.

## Inspect safely from the Mac

Preserve the Mac/iPad working state on its own branch first. If it is a source-ZIP extraction without Git metadata, preserve that directory and use a separate clone for review.

In an existing clone, these commands inspect the published work without replacing working files:

```sh
git fetch origin codex/windows-integration-20261017
git show FETCH_HEAD:docs/WINDOWS_INTEGRATION_HANDOFF_2026-10-17.md
git diff --stat 632612a0bfb258660661f47041ba9d1409eacf49 9f7c0fae2becc477c31935a9d5449ff174f8c38c
git diff 632612a0bfb258660661f47041ba9d1409eacf49 9f7c0fae2becc477c31935a9d5449ff174f8c38c -- scripts rooms assets/environment/seabed-v1/seabed_background.gd
```

The focused Windows runtime commit is the useful post-kit comparison. Reconcile overlapping changes on a separate integration branch after reviewing the Mac/iPad delta. Preserve the Mac/iPad export presets, signing configuration, touch/interface work and native fixes; the Windows branch's full `export_presets.cfg` is shared-baseline context, not an instruction to overwrite Apple presets.

## Post-kit runtime changes

| File | Change and merge concern |
|---|---|
| `scripts/crew_sprite_player.gd` | Reuses immutable clip metadata during loading; source/clip/timing/filter identity remains equivalent. |
| `scripts/crew_storage/worker_batch.gd` | Primes first-profile paths and prioritizes immediately consumed compression tasks; inspect native worker-pool policy. |
| `scripts/image_prefetch.gd` | Services the existing bounded startup decoder/progress lifecycle during preparation. |
| `scripts/main.gd` | Adds the initially visible-art preparation stage before startup completion; retain title/loading begin/end and failure cleanup ordering. |
| `scripts/grid_canvas.gd` | Defers an unused nursery fallback during selection; prepares opening environment/companion views; predicts the initial clamped view with a zero-size fallback; prepares initial floor/wall images only for multiroom groups. Retains the existing three-cell join cover, owner finish/rotation, disabled-wall and offscreen rules. |
| `rooms/whole-room/room_dressing.gd` | Announces known artwork to the existing decoder before consuming it. |
| `assets/environment/seabed-v1/seabed_background.gd` | Prepares the generated site's existing art during loading. |
| `rooms/whole-room/painted_shell.gd` | Keeps hand-prepared images first, then consumes `SafeImage.raw_image`; same original PNG pixels and existing texture cache. |

No new image cache, room geometry/draw order, camera behavior, crew/navigation behavior, save schema/admission, gameplay flags, room costs, unlock rules or survivor additions. Single-room New keeps floor/wall images lazy. Earlier batching/navigation/save improvements are already in the shared d3 source; do not implement them a second time.

## Platform-sensitive review

- Keep preparation inside the decoder's startup begin/end window and preserve cleanup on failure/cancellation.
- Reconcile predicted initial view with the actual Mac/iPad scroll area, Retina scaling, safe areas, orientation and zoom. A prediction miss changes where loading work happens; existing lazy drawing remains.
- Review decoder/compression concurrency and main-thread texture acquisition on native hardware. Max pending96/compression8 are counts, **not a decoded-byte cap**; the recent-image cache is16MiB.
- Windows repeat-New decoded peak is~237.48MiB; sampled private peaks include later QA and reach~2.2GiB. This establishes no iPad memory acceptance. Measure actual-device memory pressure, background/resume and longer play.
- Preserve raw PNG inclusion, exact path case, LFS bytes and the maintained export/import-role workflow. Avoid replacing raw runtime loading with editor-only imports.

## Measured Windows scope

The latest ordinary New outlier investigation made **no runtime fix**: the valid9.546s sample remains unexplained. Its old250ms process samples contain~1.505s near-idle activity, without stacks/exact old clock alignment; do not attribute it to a particular GPU/OS/decoder cause.

Sixteen new primary New visits compare existing3a/5dd builds. First-profile uncover medians6.465→6.475s (paired+19ms/+0.31%, B faster2/4); repeats5.960→5.765s (paired−158ms/−2.63%, B faster4/4). Four separate diagnostics do not reproduce the stall. Post-ready CPU drawing~580–590ms includes derelicts337–343ms; render-signal spans14–18ms are not GPU execution times. Four separate Continue controls give7.608→7.492s fresh and6.714→6.558s repeat. Historical samples/controls stay separate.

Earlier surface-preparation primary16: Continue7.580→7.363s first and6.628→6.192s repeat, all four pairs faster. Fresh New was mixed because of the retained outlier. See [surface report](INITIAL_SURFACE_LOADING_2026-10-17.md) and [outlier report](NEW_LOOP_OUTLIER_2026-10-17.md). The common d3 [Save report](SAVE_HITCH_2026-10-16.md) records the prior Save benefit; do not infer a general60FPS, memory, endurance or Mac/iPad acceptance.

Windows timing used a native visible secondary display,1600×900, Compatibility/OpenGL, Godot4.7.2, RTX4070Ti and Dummy/silent audio. Times begin at the title action, not executable bootstrap. Fresh profiles are not cold OS caches; other gameplay RNG and small samples limit generalization.

## Validation and provenance

- Working runtime closure: **36,430 dependencies**, exact bytes and source fingerprint equal frozen5dd; **34,051 committed LFS runtime objects** match their original source hashes. No dependency additions/removals or asset-byte differences.
- Git's configured line-ending normalization changes only CRLF/LF for **1978 committed runtime text files**. Paths are in [source audit](integration/windows-2026-10-17/source-audit.json). Git source content matches; a fresh platform checkout/export may obtain a different raw-byte build fingerprint. Regenerate build metadata for a future candidate; never relabel it as the frozen5dd artifact without equality checks.
- Fresh isolated-worktree checks: four Python suites (assert safety, manifest collection, Mac exporter selection, test-runner selection) and seven Godot fixtures (initial surfaces16 checks, visible art, room prefetch, view selection, image prefetch, router lifetime and native router pixels). All11 invocations pass. [Results](integration/windows-2026-10-17/fresh-validation.json). The standalone selector-test import issue was reproduced and its test bootstrap corrected; game runtime is unchanged. Router pixel test matches the overlay already shipped in the Mac source kit.
- Source tests use disposable APPDATA/user paths and ignored import metadata copied for validation; no player profile is used. Native router pixels are a scoped source fixture, not a fresh playable-export acceptance.
- Earlier frozen-package native room/floor/wall/crew/image tests and24 latest accepted visits/288 retained runtime checks remain scoped to the recorded builds. Full crew identities match within mode; actual New/Continue images and fresh evidence/code reviews found no material issues. These do not establish native Apple gameplay.
- Two inherited shared-baseline blank-at-EOF warnings in cold-store/galley render helpers are preserved to retain tested source. No other whitespace warnings are accepted.
- [Provenance](integration/windows-2026-10-17/provenance.json), JSON timing summaries and two1600×900 Windows reference stills are portable review evidence. Local full logs/fixtures/frozen binaries remain on Windows; no actual save/profile, SDK or exported EXE/PCK/ZIP is published here.

![Windows New Loop reference](integration/windows-2026-10-17/reference-new.png)
![Windows twelve-room Continue reference](integration/windows-2026-10-17/reference-continue.png)

Final publication guard: **136 protected delivery hashes and 2,948 owner files unchanged**, with no new exports. Independent read-only publication review found no material issue. See [integrity record](integration/windows-2026-10-17/publication-integrity.json) and [review scope](integration/windows-2026-10-17/publication-review.md).

## Frozen delivery identities

The existing matching **d3 Windows/Mac** kit remains unchanged. PCK `49a95db92f2382f52b56034a5af4515746a464d2695e2aa1e150ca83d0c09b12`; Mac ZIP `8afa0ada638939f8e263b3031752562d4c332c46a7857201e4579e374aeebcf1`; source ZIP `157b4ae797be415cce09b63cefeae02a4a798a7d9b04aa697b913cbde3f3de53`.

Latest frozen Windows **5dd** source fingerprint `5dd3aea89a5b1c1ff763cd1fd67994314cfc679cfed6455dca207240d3947185`; PCK `cc05a0b90e6628f2f357d339372f2577457b3e8e2f301a21072d0b713b60ee55`. No matching5dd Mac/iPad export or new release acceptance is claimed.

## Next Mac/iPad review

Record the Mac branch name, starting kit/commit, engine version, shared versus platform-specific changes, actual tested Mac/iPad models and outstanding problems. Check New/Continue/Save/Quit/relaunch restoration, crew/doors/lights/water/exterior/cards, touch/input/layout/orientation, focus/background/resume and memory on each target. Use a disposable macOS QA account or verify the engine's actual user-data path; Windows APPDATA isolation does not establish Mac/iPad isolation.

First review and preserve both source states, then agree the integration changes, run targeted tests and native gameplay, and freeze new cross-platform candidates together. The old frozen pair remains the comparison reference. Publish the Mac handoff so the automatic Windows-side checker can discover it. Direct Mac chat messaging has not been established.
