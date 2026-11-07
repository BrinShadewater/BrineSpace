# Windows integration performance — October 17, 2026

Six valid packaged runs, balanced ABBAAB, 40-room large fixture, three visits per build. Baseline5dd vs candidate808. Windows/Godot4.7.2/RTX4070Ti/Compatibility OpenGL3.3/1600×900/Dummy audio. Visible secondary display and foreign-process guards passed. Upload/repacking stopped. Identical frozen layout/checkpoint and common QA adapter; isolated profiles. Each cell pools540frames; all slow frames retained. These are short fixture measurements, not a soak, cold-boot certification or physical Apple acceptance.

| Phase | Avg FPS A → B | p99 ms A → B | Max ms A → B | >100ms frames A / B |
|---|---:|---:|---:|---:|
| 1× idle | 56.5 → 56.9 | 34.7 → 34.1 | 51.3 → 40.3 | 0 / 0 |
| 1× zoom | 47.6 → 47.2 | 45.9 → 40.9 | 54.7 → 50.1 | 0 / 0 |
| 1× placement | 55.5 → 54.7 | 34.2 → 36.8 | 59.8 → 61.1 | 0 / 0 |
| 2× idle | 53.7 → 53.0 | 31.9 → 33.4 | 34.0 → 38.4 | 0 / 0 |
| 2× zoom | 43.2 → 44.4 | 46.8 → 41.6 | 58.9 → 68.6 | 0 / 0 |
| 2× placement | 50.4 → 50.5 | 50.3 → 51.6 | 82.2 → 241.0 | 0 / 1 |
| 4× idle | 50.0 → 49.4 | 39.5 → 40.4 | 54.7 → 55.6 | 0 / 0 |
| 4× zoom | 39.9 → 40.0 | 56.5 → 50.2 | 67.9 → 79.3 | 0 / 0 |
| 4× placement | 48.4 → 44.7 | 44.8 → 46.5 | 76.5 → 863.1 | 0 / 1 |

Candidate has a valid 863.143 ms frame during 4× placement (action 2 µs, step 1,479 µs, engine wait 861,649 µs). Excess phase-aggregate child content drawing (~831 ms) matches most of it; engine wait includes those drawing callbacks. Tiny texture upload calls totaled 309 µs, which excludes preceding synchronous PCK reads/PNG decoding/worker wait/eviction. Exact responsible operation and OS/GPU causation remain unproven. Another candidate visit had 241 ms in a different placement phase and 27.3 s ready time. Desktop tablet serialization/compact cache guards remain off and budget remains 256 MiB; no new blocking desktop source path was found. Ordinary timing is similar; this does not establish completed performance acceptance, 60 FPS or eliminated rare stalls.

The 863ms run ended about 183.7 MiB below the usual texture endpoint; scheduling/residency parity remains unproven. No new physical Mac/iPad, scheduler-stack trace or long soak was run. Follow-up: bound and time first-use texture PCK read/decode, own-worker waits and eviction inside child content drawing before further mitigation.
