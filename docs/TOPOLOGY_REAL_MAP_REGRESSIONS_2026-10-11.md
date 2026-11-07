# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: plain topology trial real-map/regression results

## Objective and acceptance

Improve crew CPU cost without gameplay, navigation, save or visual regression.
Lean complete-input key remains private while current-station tail timing is
investigated. Full PC/Mac release gates remain open.

## Accepted decisions and constraints

No automatic quality change or owner data writes. Every key reads original inputs;
locked-cell updates/evaluation order preserved. No extra source/runtime copies or
screenshots; use isolated profiles, muted secondary display and 20GiB storage floor.
Do not use a pooled large-scene improvement to hide current-station tail regression.

## Current state

18 plain-actor native debug=false RTX4070Ti/1080p runs complete:19,440 measured
frames,108full gameplay states/camera paths/action-speed labels exactly match.
Source identities unchanged; owner2,938 files unchanged; job terminal and override
restored. No errors/missing runtime art. No topology attribution wrappers in these
runs. Reported/current/original-large scenes remain separate from mixed-large.

| Scene | Mean ms, original → trial | p95 ms | p99 ms |
| --- | ---: | ---: | ---: |
| Reported station |12.796→12.706|18.508→18.585|21.848→21.823|
| Current owner copy |12.299→12.476|18.237→21.106|26.874→30.986|
| Original40-room fixture |25.246→24.799|41.308→40.884|50.283→50.259|

Peak/end texture memory identical per lane in every scene. Reported mean-0.70%,
large-1.77%, current+1.44%; not a universal improvement. Current trial4>50ms versus
reference0; maxima45.838→61.679. Large maxima77.414→68.712,>50ms34each lane. No
>100ms frame either lane. Every p95 release gate still fails; current/large p99
also fail. This diagnostic overlay is not full-source package certification.

Evidence: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/topology-key-lean-original-maps/`
including comparison, identities, owner fingerprint and18reports/logs.

## Verification

Five existing tests adapted from SceneTree to Node with actual tree API delegates
run natively against the same source-guarded candidate overlay. Test assertions
preserved; screenshot output disabled. Navigation ownership90checks pass; prefix
1262checks/127892point records/984routes/126528sorted targets pass; rebuild stagger,
Moonbay save and RunSave/Continue pass. No engine errors on corrected runs. Owner
2,938 unchanged; regression job terminal/override restored. This checks candidate
logic; it does not certify native owner input/Studio flows or full release packaging.

First loader used a bare TEST token and rewrote BRINESPACE_TEST_USER_DIR, causing
parse errors before tests ran. Stopped only its verified private executable PID;
runner restored override and owner fingerprint was unchanged. Delimited tokens
corrected fixture. Failure log retained; five subsequent tests clean. Preparation:
`output/renderdoc-tools-2026-10-08/prepare-topology-navigation-regressions.py`.
Artifacts: sibling `topology-navigation-regressions/` results/owner/logs.

Current tail attribution: all four trial>50ms frames occur in pair2. Pair means
11.914→12.182,12.540→13.699,12.444→11.547. Zoom4x/frame27 step19.020→31.923ms with
no sampled upload; entire cause unresolved. Other three stalls show96,337,920-byte
collection/cargo/unload sheets with20.763/17.749/16.119ms upload work. Work can
overlap callback timing; not exclusive attribution. Do not infer external slowdown
or navigation causality without measurement. `current-tail-attribution.json` retained.

## Next action

Focused current station original/lean pair now active (session3066), with bounded
topology timers/hit counts and frame traces in `topology-current-attribution/`.
Finish same job; compare topology cost, per-frame work, cache misses, uploads and
complete state. Integrate only if this resolves material regression concerns.
Revised effects-source guard timing/integration, gameplay transitions/endurance,
original bugs, complete packages and Windows/Mac target certification stay open.
