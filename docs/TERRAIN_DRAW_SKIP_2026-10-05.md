# Zero-alpha mineral draw skip enabled

Updated: October 5, 2026 · BrineSpace · R2 source acceptance

## Objective and acceptance

Remove invisible mineral-overlay submissions while preserving terrain pixels,
excavation, connectivity, buried-site exposure and all simulation decisions.
Compare the change with contact-shadow batching enabled in both paths.

## Accepted decisions and constraints

Keep loading the same mineral texture and calculating the same vertex grades.
Skip only its polygon submission when every resulting vertex alpha is zero.
Do not skip subsequent cliff edges, excavation cracks, work effects or selection.
`--reference-empty-minerals` retains the original submission for comparison.
No art, UV, filtering, resource cost, clearance or texture-residency changes.

## Current state

- `assets/environment/rock-blockers-v1/rock_view.gd`: enabled zero-alpha check;
  existing UID preserved.
- `tests/test_terrain_draw_skip.gd` and paired UID: native reference/candidate
  comparison. `tests/index.json` registers the native lane. Set
  `BRINESPACE_TEST_USER_DIR` to the resolved isolated profile, or supply
  `--profile=...`, after setting scratch APPDATA.
- `output/terrain-draw-skip-2026-10-05/`: fixture generator, guarded validation,
  benchmark runner, exact input hashes, logs/results, images, comparison and
  owner-file audits. No package build, commit or public upload.

## Verification

**40/40 byte-exact native images**, before and after enabling the default:
two cell sizes, integer/half-pixel offsets, nearest/linear filtering, idle rock,
active excavation, a mineral-boundary cell, cleared rock and exposed buried site.
The input field remains exactly unchanged by both draw paths. Reference/candidate
draw counts differ by 36 in idle/working cases, 35 after clearance and 34 after
buried-site exposure. Representative output visually inspected. This checks the
render consequences of supplied field states, not a complete paid excavation loop.

Six sequential native editor runs of the maintained 40-room workload: three
reference and three candidate, 1080p, 60 samples per phase, idle/zoom/lighting
at 1x/2x/4x. Shadow batching remains enabled throughout. No other native test ran
concurrently. The reference still computes the visibility predicate; the switch
isolates whether the invisible polygon is submitted. Existing fixed-step fixture,
free-build/failure flags and startup profile isolation remain unchanged.

| Aggregate across phase medians from three runs | Reference | Skip enabled |
|---|---:|---:|
| Mean of phase mean-frame-time medians | 41.704 ms | 40.063 ms |
| Mean of phase draw-call medians | 5,005.5 | 4,958.3 |
| Largest sampled frame | 928.224 ms | 1,001.461 ms |

The draw reduction is useful, but **p95 results are mixed**; do not advertise a
consistent FPS improvement or add this aggregate percentage to R1's separate
measurements. The approximately 47-call station difference is workload-specific;
the controlled pixel fixture proves 34–36 removed calls in its own field states.
Texture memory stays around 4,097 MiB on the engine counter, with small scene-state
variation, not a memory-remedy result. All release performance gates remain open.

Both validation runs and all six benchmarks complete without engine errors;
benchmark missing-image reports are empty. All owner checks show **2,936 unchanged
non-log files**. No native Mac, minimum-PC, 1440p, packaged release, endurance or
original-bug-report certification is implied by these tests.

## Next action

Reproduce R3's redundant redraws from freshly wrapped split-prop entries using an
actual affected room renderer and a library-prop control. Count static redraws
before changing identity comparisons; verify movement, copies, pass changes,
rotation and layout replacement. Keep texture-memory and long-stall blockers
separate from these measured reductions in rendering work.
