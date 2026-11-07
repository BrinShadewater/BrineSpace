# Opt-in CPU frame backing candidate — November 3, 2026

## Preservation and identity

Active source: `/Users/Shared/BrineSpace-native-validation-20261017`, branch
`codex/ipad-memory-placement-2026-10-17`, HEAD `81b2f9a4a36eb0e3162d86ccfb4e9ef735836122`
plus preserved prior dirty work and this candidate. No commit, reset, merge or push.
Before edits, all 598 modified/untracked files (19,421,749 bytes) were archived
and SHA256-verified at `/Users/Shared/BrineSpace-resume-preservation-20261103`.
The directory includes the full per-file manifest, binary staged/unstaged patches,
original Git index and NUL-delimited status. Clean tracked files remain reconstructible
from HEAD. Ignored packages/evidence were left in place, not removed or rewritten.

Installed playable19db and all frozen releases/rollback donors remain untouched.

## Candidate and limits

Explicit `--bounded-crew-cpu-store` AND tablet policy are required. Default/desktop
policy remains in-memory. Bank adoption writes immutable compressed frame bytes to
one uniquely named, open session file, verifies the write with SHA256 before releasing
the original payload, and retains no frame references in the store. Frames keep
strong ownership of that file. Hot compressed bytes use a16MiB LRU; oversize records
are served transiently. Returned Images are independent. Last-owner cleanup removes
the file. Abnormal process termination can leave an expendable cache file; no
unattended cleanup or deletion of other sessions was added.

Cold reads validate each record. Corruption may recover only by reproducing the
exact compressed bytes from the original PNG; changed source data is not accepted
as the old image. File-creation/append failure leaves the original payload in RAM.
Checkpoint hashes, full-frame metadata, sampling, GPU leases and gameplay are retained.

Writes/flush/readback and cold reads are synchronous. This is a retained-CPU-storage
experiment, not a solution to startup peak or a demonstrated performance win.
File metadata, transient reads and OS page cache are outside the16MiB payload limit.
Do not add the virtual decoded inventory to process footprint.

## Fresh evidence

- Red test reproduced missing offload support; bank integration separately reproduced
  missing opt-in offload before implementation.
-108 storage checks pass, including bounded eviction/reentry, original pixel/checkpoint
  hashes, independent Images, creation failure, corrupt-record recovery and final-owner cleanup.
- Eight scoped native suites pass: CPU store, source sharing, source-sharing pixels,
  pose cache, routed pixels, hidden leases, tablet decode, tablet loading.
- Updated native pixel matrix:79checks pass. Original in-memory viewport captures
  precede offload; test uses a1-byte hot budget to force cold reads. Fractional scales,
  regions, transpose, materials, retained peers, reveal and spills remain exact.
- New fixture also passes without the opt-in flag. Registered native lane verified
  using bundled Python3.12. No full-repository suite claim.
- Actual native crew-loading inventory:140,535,542 compressed bytes offloaded
  (all source payload in this fixture),512,688 hot bytes,16,432 source references;
 25cold reads /1,316usec at the sampled point. This is a startup snapshot, not active
  gameplay timing or a measured iPad/whole-process saving.
- Owner Mac save-folder fingerprints unchanged around every native batch.
- Independent read-only review found no actionable correctness/lifetime blocker.

Original red logs and failed harness attempts are retained: first baseline used the
pack profile name against source and correctly hit its scratch-profile guard;
corrected source profile passed. A packaged decode invocation named a fixture omitted
from the pack and failed before running; corrected external-fixture invocation against
the same mounted pack passed. The system Python3.9 cannot classify this project's
Python3.10+ annotations; bundled3.12 classification passed. No production fixes were
made for these harness/environment errors.

## Separate physical probe

`/Users/Shared/BrineSpace-cpu-store-probe-20261103` contains a separate signed app:
`com.shadewater.brinespace.cpustore20261103` / BRINE CPU Probe. It does not replace
Validation2 or share its container. Based on preserved SourceSharing.pck with exact
candidate overlays; signed-build.json records executable/PCK hashes. Mounted-pack
storage108/pixel79checks and external tablet-decode fixture pass. Overlay hash audit
matches all9replacement resources. Strict signature verifies and signed PCK matches.

## Physical iPad result

Owner unlocked the paired iPad10; fresh process query then succeeded. All five
owner files were copied and hashed before the separate installation. Probe installed
under its unique bundle, leaving Validation2 unchanged. PID1373 passed all79native
pixel checks, including original in-memory oracle versus cold records. Five owner
files were SHA256-identical afterward.

Same signed package /56rooms/four crew / normal rules, ABBA order;120actual active
seconds per run, comms advanced by the fixture and paused intervals counted separately:

| Run | Middle process median MiB | Median frame ms | P99 ms | Station setup ms | First redraw ms |
|---|---:|---:|---:|---:|---:|
| Reference A, first/cold |2129.300|48.999|81.029|10705|1154.479|
| Bounded B, warm |1882.339|50.682|88.457|9005|563.975|
| Bounded C, warm |1913.347|50.942|88.005|8718|576.827|
| Reference D, warm |2019.316|50.792|89.095|7868|502.586|

Candidate middle-memory median of the two run summaries is1897.843MiB,
121.473MiB (~6%) below the warm reference. These are approximate same-PID native1Hz
windows (first30/last10valid samples excluded), not allocations or exact matched
per-frame residency. Both candidate runs offloaded140,535,542bytes; hot payload
stayed below16MiB. Cold reads during gameplay totaled approximately0.35CPU-wall
seconds over120active seconds in each run. No reliable FPS gain: candidate median
50.812ms versus warm reference50.792ms. The cold first reference is explicitly
excluded from loading-win claims.

Verified-record adoption costs1141–1153ms, versus24ms in warm reference. Full warm
station setup is850–1137ms slower. First redraw remains about0.56–0.58s, versus
0.50s in warm reference. The tradeoff is reduced retained CPU storage at extra
startup I/O cost; no claim of improved first redraw or faster loading.

All four runs: all four crew survive,120active seconds reached, fixture save/readback
full serialized state and exact timer match. Startup reveal differences remain only
`discovery_bursts` aging; this is not complete-startup-state equivalence. These are
fixture/direct-method checks, not touch-driven Save/Continue UI or long-soak/leak
acceptance. Sparse console output is not evidence of an error-free full gameplay log.
After each result/native sample collection, the exact fresh launch/result PID was
intentionally stopped; stop receipts are retained. No owner app was terminated.

Physical evidence: `/Users/Shared/BrineSpace-cpu-store-probe-20261103/physical`,
including RESULTS.json (pixel result), benchmark-summaries.json,
each run's result/memory/launch/stop receipts, owner backups and final preservation
receipt. Mac source remains the opt-in candidate; installed Validation2/frozen
releases are not promoted or replaced.

Next: reduce measured per-record adoption/write-verification overhead while keeping
verification-before-release and exact fallback/lifetime gates. Then repeat the same
physical comparison. Full touch-driven Save/Continue, placement/reentry, longer growth
and broader physical visual acceptance remain required before promotion/release.
