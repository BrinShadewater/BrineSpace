# Drone preparation: memory gate and exact duplicate inventory

Updated: October 10, 2026 · Project: BrineSpace · PC/Mac performance work

## Objective and acceptance

Prevent simultaneous first-use drone atlas uploads while keeping selected pixels,
animation timing, complete drones and the large-station 3 GiB texture budget.
Two private approaches were tested and rejected. No runtime source was changed
by this pass. The accepted transparent-layer fix remains installed.

## Accepted decisions and constraints

Do not accept earlier loading that exceeds the memory gate. Keep simulation and
animation records unchanged. Do not repeat larger-cache or cropped/row proposals
that already failed their respective gates. Tests use isolated profiles, muted
secondary-display windows, disabled physical input and shared PCKs.

## Current state

Private artifacts are under
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:

- `drone-collection-trial/`: one-second collection lookahead; no more than four
  additional decode jobs and one predicted GPU upload/frame, with an instantaneous
  3 GiB texture-memory admission check. Existing drawing and sampling unchanged.
- `drone-collection-preliminary/` and `drone-collection-repeated/`: actual native
  debug=false saved40 trials, including new per-measured-frame texture peak collection.
- `drone-grace-trial/` and `drone-grace-preliminary/`: one-frame rather than
  two-frame recently-used protection, tested independently with prediction disabled.
- `drone-collection-trial/encoded-duplicate-audit.json`: exact-byte source evidence.

Focused runners remain in `output/renderdoc-tools-2026-10-08/`. No release package,
art, UID, owner layout or gameplay rule changed. Full release goal stays active.

## Verification

Same shared release executable/PCK and current-source overlays, RTX 4070 Ti,
1080p, reported save expanded deterministically to 40 rooms. Idle/pan/lighting,
1×/2×/4×, 90 frames per phase. Fixture settings do not certify target hardware or
actual mouse/keyboard interaction.

Initial collection pair: worst frame 114.097→80.515 ms, but mean
27.572→27.606 ms and p99 50.374→52.346 ms; >50 ms frames 9→13. Phase-boundary
texture observations rise from 2,660.0 to 2,843.8 MiB. This was insufficient
evidence of either benefit or compliance, so per-frame memory collection followed.

Repeated trial first pair:

| Metric | Reference | Predicted collection |
|---|---:|---:|
| Mean frame | 27.370 ms | 27.591 ms |
| Worst frame | 110.383 ms | 79.678 ms |
| Measured-frame texture peak | 3,027.507 MiB | 3,272.507 MiB |

Candidate uploads eight predicted textures and skips five attempts under its
instantaneous memory check. A second candidate also peaks at 3,272.507 MiB and
has an 80.950 ms maximum. The guard cannot reserve space for subsequent required
uploads; warming textures adds approximately 245 MiB at peak. Reject: the candidate
exceeds the 3,072 MiB gate by about 200.5 MiB. The unchanged reference has only
approximately 44.5 MiB headroom in this workload. Phase-boundary measurements
previously obscured that peak.

The second candidate had completed when the failed-budget run was stopped. The
owned next reference process was stopped before completing its workload; the
remaining repetitions were not run. Finally guards restored runtime configuration
and verified the owner folder. Do not interpret the aborted repetition as a crash.

Independent grace-window pair:

| Metric | Two-frame protection | One-frame protection |
|---|---:|---:|
| Mean frame | 27.726 ms | 27.640 ms |
| p99 | 53.206 ms | 51.448 ms |
| Worst frame | 90.344 ms | 95.723 ms |
| Measured-frame texture peak | 3,027.507 MiB | 3,026.487 MiB |

Only about 1.02 MiB freed: insufficient for the prewarming proposal. Reject as the
memory remedy; no source installation or claim of broad quality acceptance.

Exact duplicate audit: only the 70 texture paths uploaded in the preceding saved40
request trace were read. Zero missing files and zero LFS pointers. Seven equal
encoded-PNG groups, including six visible groups, prove identical source bytes:

- idle-south / charging-south: 48,168,960 decoded bytes.
- drive-south / carry-south: 48,168,960 bytes.
- drive-north / carry-north: 48,168,960 bytes.
- drive-east / carry-east: 48,168,960 bytes.
- drive-west / carry-west: 48,168,960 bytes.
- collect-south / unload-south: 96,337,920 bytes.

Duplicate visible storage across this traced asset set totals 337,182,720 bytes
(321.5625 MiB). This is potential sharing across the session, **not** measured
simultaneous residency or an achieved reduction. Different encoded hashes do not
prove different decoded pixels. A separate equal-byte group contains transparent
effects; the prior bounded transparent-layer retention remains responsible for
avoiding their repeated decoding.

All jobs terminal/configuration restored; all 2,938 owner files unchanged. This
pass added approximately 25.9 MiB evidence and 22.7 MiB scratch, no full PCK copies.
At completion C:126.92 GiB/D:78.71 GiB free. No recursive cleanup retry.

## Next action

Test session-scoped immutable GPU storage sharing for the verified identical
visible sheets. Preserve original manifest/frame objects, metadata and filtering;
never mutate shared image storage. Validate equivalence against actual current
source bytes so changing one PNG cannot silently redirect it to stale artwork.
Keep the lookup bounded and release it at final scene exit. Measure unique GPU
storage and actual per-frame memory, then test whether any achieved headroom makes
earlier preparation viable. Do not assume all 321.6 MiB can be freed concurrently.

Full performance, loading, endurance, original bug, packaged Windows and native
M1/Mac signing/notarization/gameplay gates remain open. No itch.io action.
