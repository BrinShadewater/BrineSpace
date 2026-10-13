# Performance coverage research

Updated: October 5, 2026 · BrineSpace · First-use, loading and presentation risks

## Objective and acceptance

Find contributors missed by the existing steady-state investigations. Distinguish
source-confirmed behavior from measured causes. This is research, not a new
performance acceptance or a claim that frame times improved.

## Accepted decisions and constraints

Preserve selected art, default effects, animation timing and user settings. Keep
the deterministic benchmark for matched optimization comparisons; supplement it
with actual packaged gameplay. No engine upgrade, quality reduction, driver-cache
deletion or system setting change is proposed here.

## Current state

### First-use stalls can fall outside our measured interval

`tools/release_benchmark.gd` preloads station room views, then waits for at least
180 warm-up frames and observable settled state before measuring. The room-view
prewarm loads art; it does not by itself prove every shader variant was rendered.
Warm-up rendering can nevertheless absorb first-use work for visible effects.
An effect first encountered later may still hitch.

The project uses Compatibility. Godot's shader-compilation guidance explicitly
excludes Compatibility from the Forward+/Mobile ubershader remedy. Its suggested
Compatibility approach is to render required effects during loading. This makes
first encounter versus repeat encounter a useful discriminator, not proof that
compilation caused the existing long stalls.
[Godot jitter/stutter guidance](https://docs.godotengine.org/en/stable/tutorials/rendering/jitter_stutter.html),
[pipeline compilation scope](https://docs.godotengine.org/en/stable/tutorials/performance/pipeline_compilations.html).

Next check: capture first placement, lighting change, water/effect activation and
UI opening from an actual release launch, then repeat each action. Separate
resource preparation, upload, draw and presentation timings where available.
Record driver/cache history; a new save profile does not guarantee a cold driver
shader cache. Do not indiscriminately preload every asset into already tight RAM.

### The comparison benchmark uses a different clock and presentation policy

The benchmark calls `game._process(1.0 / 60.0)` once per driver frame, manually
advances the cycle timer, disables VSync and frame caps, and disables unfocused
pause. This controls simulation work per frame for comparisons. When rendering
runs above or below 60 FPS, simulated time per wall-clock second differs from
ordinary gameplay. Other independently processing nodes can still use real delta.

Retain these results with their recorded `simulation_driver`; do not reinterpret
them as normal-clock timing, focus or VSync certification. Add a separate release
lane using normal clocks and saved presentation preferences, including 1x/2x/4x,
pause/resume and focus changes. Keep uncapped gate measurements separate from
the perceived pacing check. A frame cap cannot repair an expensive frame.

### Startup prefetch has a count window, not a decoded-byte ceiling

`scripts/image_prefetch.gd` uses WINDOW=96 and a separate 16 MiB recent-image reuse
cache. That cache limit does not cap pending decoded results. Image dimensions
therefore affect memory even with the same request window. `take()` can wait for
old skipped tasks; `end()` waits for all outstanding tasks, including unused work.
The prior launch's manifest determines speculative request order, so fresh-profile
and learned-manifest startup exercise different paths. Direct game fixtures do
not enable this title-transition prefetch.

Existing metrics already include peak decoded bytes, peak pending tasks, unused
results and worker decode time. Collect them through the real title transition
and time the final drain before tuning scheduling. Worker decode time is aggregate
work, not elapsed loading time. Compare missing/current/stale manifests in scratch
profiles. Consider a decoded-byte-aware scheduling budget only if measured peaks
or wasted work justify it; preserve independent mutable image copies.

### Output resolution and audio need valid isolation experiments

`scripts/screen_atmosphere.gd` uses a shared screen-reading shader at High quality.
Godot makes a back-buffer copy for the first 2D screen reader; this is not evidence
of a separate full-screen copy for each atmosphere effect. Its sampler uses
`filter_linear`, not a mipmap filter. Cost remains unmeasured here.
[Screen-reading behavior](https://docs.godotengine.org/en/stable/tutorials/shaders/screen-reading_shaders.html).

Measure actual drawable dimensions, not only logical window size, especially on
Retina. 1440p has 1.78 times the pixels of 1080p; doubling both dimensions gives
four times the pixels, not necessarily four times the frame time. Compare GPU and
CPU timings at matched views and unchanged High quality. A resolution slope helps
distinguish pixel work from submission cost; it does not identify one shader alone.

Audio is a lower-priority hypothesis. Music uses two decks with cleanup; station
events have per-kind guards and free completed voices. Source review did not find
unbounded player accumulation in those paths. However, zero volume generally
changes gain rather than stopping playback. Only selected ambient layers have
explicit silence-stop behavior. A muted run therefore does not isolate decoding.
Ogg playback has CPU cost, but that fact alone does not establish a bottleneck.
[Godot audio formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html).

If traces implicate audio, compare controlled playback-enabled and playback-stopped
fixtures with the same game workload and active voice counts. Do not ship that
diagnostic toggle or change formats without evidence and an audio regression check.

## Verification

Read current benchmark, room prewarm, image prefetch, atmosphere, music, audio bank,
station audio and shutdown code; checked primary Godot documentation. No game
process, benchmark or probe was launched. No owner-profile writes or runtime edits.
Changed this report and the release-readiness entry in CURRENT_STATUS.md.
Native Mac/Retina behavior and each proposed contributor's frame cost remain unknown.

## Next action

The existing pixel-tested shadow/mineral prototypes and blocked-route reproduction
remain stronger implementation evidence than these new hypotheses. Integrate and
measure those focused candidates, while adding first-encounter/normal-clock release
coverage. For startup, collect existing prefetch metrics plus drain duration before
changing worker scheduling. Avoid extending general research indefinitely without
a matched implementation result.
