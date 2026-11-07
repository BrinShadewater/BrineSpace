# Project handoff — repeated drone texture uploads confirmed

Updated: October 10, 2026 · BrineSpace · PC/Mac performance readiness

## Objective and acceptance
Continue optimizing the larger rendering costs after the accepted Solar working-copy
change. Previous goal turn was progress: installed a measured local improvement with
real-map and native visual checks. This turn changes the next priority using fresh
callback/cache evidence and tests a private smaller-upload prototype. Release remains open.

## Accepted decisions and constraints
Current source; actual debug=false Windows RTX4070Ti/1080p instrumented station runs,
muted secondary display, isolated resolved APPDATA, physical input disabled, owner
fingerprints and20GiB storage floor. Small overlays/reused runtime. No production code,
art, quality, simulation or cache-budget change this turn. Prototypes stay private.

## Current state and evidence
Three corrected40-room traces,1080 measured frames each, idle/pan/zoom/lighting1×/2×/4×:
- Callback grouping: live room surface~4ms, main grid~3ms, foreground~1.4–1.5ms;
  lighting also repaints floor halves~2.47+1.93ms. Prop callbacks are separate from these
  grid groups. Nested timings are not additive; instrumentation is not FPS certification.
- Foreground breakdown: synergy drawing~0.7ms, but active-link lookup only~0.026ms,
  nine calls/frame. Do not pursue the hypothesized lookup optimization yet.
- Drone drawing is the larger variable cost:946 frames without sampled uploads average
  ~0.399ms there;134 frames with uploads average~9.272ms, including~7.549ms in texture
  creation. Whole-frame means27.639 versus39.563ms are correlation, not a causal A/B gain.
- One zoom sample submits two atlases totaling240,844,800decoded bytes (~229.69MiB),
  taking42.652ms in measured ImageTexture creation. This measures CPU wall time of the
  submission call, not a hardware GPU timer or physical bus traffic.
- First upload trace:193 complete events,53 unique paths,140 repeated uploads, about
  7,416MiB decoded texture data submitted over1080 frames. A45.94MiB wheel atlas is
  uploaded10 times;137.81MiB mining body/effect atlases recur too.21 of43 >50ms frames
  have sampled uploads; other expensive work remains and is not attributed to uploads.
- Separate cache-pressure trace:160 uploads,123 repeats;118 repeats have an earlier
  measured eviction of the same path.112 upload-time evictions,133 post-render evictions,
  55 weak-reference restores. Bookkeeping records~1149.75MiB resident before a logged
  event despite the nominal256MiB budget. Recent-use protection makes that a soft budget;
  this is neither a complete GPU peak nor evidence that live images may be dropped safely.

These are separate runs; do not merge event counts as if they describe one replay.
The installed Solar change is included in all current overlays.

## Private upload-page feasibility
Test existing RGBA PNG pixels in two-row GPU pages, with no on-disk art conversion,
frame removal, palette shader or quality change. The normal runtime still uses full atlases.
Godot documents exact-area image copying through
[Image.get_region](https://docs.godotengine.org/en/stable/classes/class_image.html#class-image-method-get-region)
and region drawing through
[CanvasItem.draw_texture_rect_region](https://docs.godotengine.org/en/stable/classes/class_canvasitem.html#class-canvasitem-method-draw-texture-rect-region).
These API references do not establish native raster equality; the probes test that separately.

Native one-atlas probe uses mine-north.png:2688×13440, manifest448×448 frames/six columns.
Seven frames include row/page boundaries and the final frame; three scales, two mirrors,
nearest and linear filtering give84 comparisons. Full image137.81MiB versus page9.19MiB.
Single-probe texture creation~37.966ms full versus1.076–2.874ms pages; CPU copying
2.661–3.975ms/page. This is one native feasibility probe, not repeated release gameplay.
No integrated decoder/page cache, loading path, prefetch, fallback or lifetime remedy exists yet.

Nearest9/42 pairs exact,33 fail; linear0/42 exact. Representative nearest0.42 capture
differs in81 pixels with equal nonempty bounds. The renderer differences block admission.
Separate isolated headless raw-byte comparisons prove four extracted pages exactly equal
the corresponding original RGBA rows. Texture-coordinate normalization/precision is a
candidate explanation, not yet an established mechanism. Next isolate that difference.

Initial fixture had incorrect frame dimensions/division; corrected to the actual manifest,
retaining failed evidence. The corrected probe still fails raster equality. Do not call the
approach visually accepted or relax the pixel gate to obtain a passing optimization.

## Verification and retained artifacts
Station trace/runtime/missing-image/mute/input/coverage guards pass. All jobs terminal;
runtime override restored; source identities unchanged. Every owner guard2938 files
before/after, no changes. Native page failures are expected recorded trial failures;
raw CPU-page proof passes4 checks. No production fix or FPS gain claimed this turn.

Evidence under D:/bs-release-crew-cache-20261009/benchmark-input-isolation:
large-callback-groups-trace, large-foreground-groups-trace, large-cache-pressure-trace,
rgba-page-feasibility. Trace reports, upload repetition/cache analyses, logs, prototype,
native PNG comparisons, CPU proof and owner/storage records retained. Focused runners
under output/renderdoc-tools-2026-10-08/run-large-*-groups-trace.py,
run-large-cache-pressure-trace.py and run-rgba-page-*.py.
28.60MiB evidence+isolated profiles; C125.01/D74.02GiB free. No full copies/deletions.

## Next action
Prototype a smaller upload unit that preserves original atlas sampling, then prove
nearest/linear pixels before integrating anything. Keep immutable source images and
frame metadata; bound CPU decoded data as well as GPU pages. Preserve required loading,
animation timing, canvas pins, PNG runtime loading and explicit filtering choices.
Compare against the existing private indexed provider as a measured alternative, rather
than assuming paging will win. Any integrated candidate needs all three matched map
replays, motion/fallback/lifetime checks and whole-station visual acceptance. Continue
CPU room/floor work for the remaining non-upload hitches. All broader release/Mac
and performance gates remain open; do not increase the cache or lower art quality blindly.
