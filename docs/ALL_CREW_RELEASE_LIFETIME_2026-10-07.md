# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: release-runtime memory boundaries and checkpoint lifetime

## Objective and acceptance
Continue full PC/Mac readiness. Measure combined prototype resource lifetime before proposing larger drone residency. All original release gates remain open; no final package admission or certification.

## Accepted decisions and constraints
Reuse identified diagnostic text overlay and actual release executable, debug=false. Preserve selected art and default effects, owner data and retained deliverable. Resource counters describe engine texture accounting, not physical driver VRAM. Render boundaries cannot prove absence of unsampled within-frame peaks.

## Current state
`output/all-crew-storage-2026-10-07/prepare-memory-lifetime.py` prepares an isolated physical QA adapter from the existing40room fixture. The candidate-only run adds render-post-draw memory sampling and ten actual scratch disk/staged checkpoint restores through fresh main scenes. No normal runtime/art/layout/archive changes.

## Verification
Initial attempt completed40room phases but save validation correctly rejected synthetic recovered-crew entries whose origins were not backed by real recovery pods. Evidence retained in `packaged-memory-lifetime/`; owner2936unchanged, adapter restored, process terminal. This is fixture incompleteness, not evidence of a game save regression. No save-validator bypass.

Corrected test uses normal SiteDiscovery.reveal for all actual expedition recovery sites, restores their three wards with normal cryo-room/recovered_derelict/rotation conventions, and derives roster IDs/names/origins from their pods. Core roster preserved. This changes only transition fixture scope from40 to43rooms. Free-build/failure fixture flags disabled before the normal RunSave.write; write/read passes normal validation. The preceding measured active workload remains40rooms and uses the existing identical source selection and gameplay fixture.

Actual release run clean: nine40room idle/pan/zoom1/2/4x phases, then ten scratch disk checkpoint staged restores of paused43room/four-crew station. All ten preserve exact crew snapshots and room dictionaries after twelve settled render frames; actual Bill provider path guarded, missing presentation0, router released at every exit. No simulated title menu interaction or resumed/endurance/target-platform acceptance.

Render-boundary texture peak across startup, active40room workload and43room transitions:2348.995MiB (~2.294GiB). At1475 sampled post-draw boundaries, memory-probe total4454us/mean~3.02us/max30us. Probe attaches before session presenters' post-draw trim, but does not sample inside draw callbacks/GPU driver allocations. No full peak-memory release certification.

Equivalent restored43room states:2067.421->2067.738MiB over ten restores, +0.3162MiB (~0.0153%). First exit231.987MiB, subsequent exits234.604->234.885MiB, final234.920MiB. After initial warm difference, both restored/exit counters rise by exactly0.035133MiB (~36,840bytes) each cycle. Warm exit growth~0.135%; below5% investigation threshold, but sustained tiny growth remains unassigned and prevents a zero-growth claim. No causal conclusion from byte count alone. Investigate retained UI/art/engine resources before closure; two-hour soak still required.

40room p95 remains33.992–64.333ms, max89.573ms; no FPS improvement claim from candidate-only memory instrumentation run. Normal rendering/production behavior not changed. Exact full source/overlay/basepack/EXE/physical adapter identity retained. Both attempts' owner fingerprints2936unchanged; successful adapter restored byte-identically and process terminal.

Evidence: `output/all-crew-storage-2026-10-07/packaged-memory-lifetime-valid/` identity/owner/lifetime/candidate JSON, logs and screenshot. Historical failed fixture retained separately.

## Next action
Investigate the small repeated texture-accounting increase with scoped ownership telemetry; run12room coverage and resumed/endurance measurements. Use measured2.294GiB render-boundary headroom as limited evidence for a private bounded drone working-set trial, not an automatic cache-budget increase. Compare upload counts/cost, memory peaks/lifetime, exact art and state before adoption. Keep redraw-only zoom bursts in scope. Full frozen combined candidate/PCK audit, normal title/Continue/UI/nine reports, target PC and actual Mac/sign/notary gates remain open.
