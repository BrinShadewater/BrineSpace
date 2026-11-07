# Project handoff

Updated: October 5, 2026 · BrineSpace · Complete selected Veld CPU bank

## Objective and acceptance

Test complete selected-character storage, existing source consumers and safe
overflow rendering before enabling private GPU presentation in gameplay. Preserve
PNG pixels, filtering, clip identity/metadata, playback and owner saves; measure
CPU/process costs alongside engine texture counters.

## Accepted decisions and constraints

Owner authorized continuing the isolated prototype. Normal runtime, selected art,
layouts, saves and frozen exports unchanged. Never mutate shared CPU pixels;
get_image returns copies. Private presentation textures are mutable, separate
from immutable source storage. Lower texture accounting alone is not an M1 RAM
win. Retained canvases keep their draw leases; extra visible poses must render.

## Current state

Artifacts/evidence: `output/private-full-veld-2026-10-05/`. Current grid loader
physically copied, actor loop restricted to Veld and optional CPU subclass selected;
manifest ordering and overrides otherwise unchanged. Source hash/changes recorded.
`cpu_player.gd` uses an isolated CPU batch: surviving sources decode before
presentation, PNG signatures share proven identical immutable pixels, weak lookup
entries do not retain superseded banks. Original CanvasTexture frame wrappers,
metadata, clocks and selected filtering remain; diffuse source provides native
Texture2D size/image/format APIs. Generated source conversion remains independent;
this current selected bank needs zero generated-image GPU readbacks.

`slots.gd` keeps four reusable private textures and canvas leases. When all four
are leased, extra visible poses get temporary immutable GPU images. These belong
only to current draw leases, release on replacement/owner exit, and never evict
other poses. Thus reusable capacity is fixed, total allocation follows concurrently
retained poses; many retained viewers can still exceed the nominal pool budget.
This is not automatic quality reduction or a permanent spill cache.

## Verification

Godot 4.7.2 native Compatibility / RTX 4070 Ti; every launch checks isolated user
directory and fingerprints all 2,936 owner non-log files before/after. All unchanged.

- 14,450 final storage/render checks pass. Every source frame's bytes and size
  match reference. Raster samples every eighth frame: 4,788 exact comparisons of
  overlapping poses, actual filtering, tint/clipping, scales and half-pixel origin.
  33 additional whole-scene overflow comparisons pass; repeated spills retain only
  one extra image in this fixture, peak decoded spill payload 256 KiB. Held canvas,
  mixed dimensions, lease exit and weak release checks pass.
- 48,847 existing-consumer checks pass across 390 clips / 3,186 frame references:
  native get_image/get_size, metadata/filter/timing, three samples per held-frame
  interval, 24 real Veld reading interruptions, and 1,080 original Player replay
  comparisons at 30/60/120 samples and 1×/2×/4× with pause, gear switching and
  snapshot restoration. Context fixture, not real gameplay navigation/focus/save.
- Three final alternating matched reference/candidate pairs: 600 uncapped draws,
  one retained pose and three changing poses, first 60 frames excluded. Incremental
  texture accounting 487.06→0.560 MiB; static CPU allocations 10.29→379.27 MiB.
  Immutable decoded CPU payload 365.35 MiB. All pairs agree on steady allocations.
  Final texture counter returns exactly to baseline and bank/presenters release.

Final Windows whole-process memory samples, externally polled every 25 ms:

| Peak metric, MiB | Reference samples | Candidate samples |
|---|---|---|
| OS peak working set | 622.51 / 627.26 / 611.34 | 615.90 / 612.67 / 612.15 |
| Sampled private commit | 815.20 / 804.11 / 698.67 | 639.62 / 635.42 / 633.76 |

Median differences ~9.84 MiB working set / 168.69 MiB commit. Working-set direction
is slightly worse in the third pair; commit varies substantially in reference.
These Windows process counters are neither physical GPU residency nor M1 unified
memory. Do not sum them with engine counters. Validation runs hold both versions
at once and are excluded from matched memory savings.

Final fixture frame p99 reference 0.884/0.711/0.819 ms versus candidate
2.670/1.093/1.321 ms; medians 0.298/0.292/0.304 versus 0.527/0.494/0.488 ms.
Added median work ~0.2 ms, all candidate maxima <6.2 ms, no >50 ms frames.
Upload-call p99 96/78/60 µs; max 944/630/2,970 µs. API submission is not isolated
GPU execution. Each candidate makes 1,801 uploads and 33 dimension replacements;
ordinary benchmark stays within four slots, overflow is tested separately.
Preparation median 2.626→2.677 s. No loading/FPS improvement or packaged acceptance.
Earlier pre-spill comparison is superseded by final rerun. Final logs no errors or
warnings; loader/runtime hashes retained and checked.

## Next action

Proceed to a controlled Veld-only station integration with explicit presentation
routing at actual canvas draws. CPU source textures have no renderable GPU RID:
never let direct draws, shader uniforms or controls silently use one. Exercise
layered rooms, water/cryo effects, bunk composites, retained/offscreen canvases,
Studio/menus, gear and Continue. Measure full-station FPS, uploads, peak/process
RAM and transitions before default enablement; verify no art placeholders/errors.
Bill historical bindings and other character banks are not covered. Mac native
total-memory/Retina/signing and original release gates remain open. No maintained
runtime feature flag, production integration, export or upload this milestone.
