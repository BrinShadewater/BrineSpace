# Review, failures and boundaries

Read AGENTS, current status, integration and Mac-parent handoffs, release workflow and relevant Apple tooling. Static review used the7e3029a4→585111ca3 delta with whitespace-at-EOL ignored. A separate read-only reviewer found no introduced critical/important defects: startup completion ordering, tablet guards on desktop eager art/profile work, worker CPU image preparation without SceneTree/GPU access, drone budgets/live leases, save policy, shared intro Skip and Apple preset options remain consistent. This is scoped evidence, not proof of absence of bugs.

No runtime/source fixes were made. Generated export presets and nine translation files were restored; tracked runtime tree matches the integration. QA-only guards, adapters and identities are external to the PCK.

## Failures retained locally

- Initial Mac export was rejected for two unhydrated older scene textures. Fetched only those exact LFS paths and reran the maintained export in a new directory. Clean export and audits passed. Failed ZIP/log retained.
- Initial release adapter skipped the intro before `_ready`/player initialization: two SIGSEGV exits139. Corrected the external fixture to wait for initialization and defer UI actions. Subsequent final New/Continue journeys passed. This bypassed normal input registration and does not establish a production Skip defect. Crash IPS retained locally.
- A subsequent startup was blocked by AppKit's reopen-windows modal after those crashes, confirmed by a process sample. QA identity was made unique; final launches passed. Not classified as a game freeze.
- Two parent-comparison setup attempts had missing ignored imports/four tiny unhydrated PNGs, with a competing import in one attempt. Explicitly invalidated as setup failures. Completed import and exact runtime verification before all six accepted visits. Accepted-run outliers were retained.
- An initial release measurement configuration enabled script call-stack tracking; one valid visit and a deliberately interrupted visit are separately retained in `release-benchmark-instrumented*`. Primary three-visit cohort reran consistently with tracking off; never pooled configurations.
- Native fixtures retained known ObjectDB/RefCounted shutdown warnings from intro preload (34 in the affected log). They are not silently removed from evidence.
- Production automatic reports captured title-screen frames of roughly556–643ms in final journeys (earlier runs also captured561/640ms). Reports are retained locally and available summaries are portable. These occurred at startup/title, not the measured placement phases. Cause and reproducibility remain open.
- Accidental binding by generic app display name launched the old Escape-fix Mac app. It was immediately killed. Original logs were restored from exact hash-matching rotated copies; incidental lock/log files moved out. Accessible saves/progression/settings and frozen bytes match before; `last_session.json` does not. See preservation.json. The QA app was thereafter bound by exact absolute path and unique bundle identity.

## Not established

Audible playback (QA muted), physical F-key media-mode variants, complete manual visual coverage of every door/lighting/warning/animated-room state, long endurance/leak bounds, physical iPad touch/lifecycle/compact rendering/memory acceptance, notarization or public release. Existing iPad app/container was not replaced or written by this task. A connected device/preflight PASS is not physical game acceptance. Do not infer iPad safety from Mac footprint or forced-tablet fixtures.
