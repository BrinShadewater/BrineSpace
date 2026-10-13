# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: current drone upload cause and cache trial

## Objective and acceptance

Continue the complete performance/release plan. Remove recurring upload stalls
without changing selected pixels, dimensions, sampler/filter behavior, playback,
simulation, owner data or default quality. Full release gates remain open.

## Accepted decisions and constraints

Normal drone cache remains256MiB. Reject the current512MiB trial. No source/art/
delivery change from this diagnostic. Current accepted crew storage and ordered
room shadows remain installed. Do not repeat rejected cropping, indexed lookahead
or larger-cache variants unchanged. Native QA stays muted/secondary, isolated and
space-guarded; one retained physical PCK, no new full package/source copies.

## Current state

Private context labels record required render caller, sampled drone kind/state/
heading/home/frame and original decode-request context. Scope is bounded by the
existing eight upload events per frame. Dock preparation and draw contexts restore
their scope; no readiness, storage or playback decision changes.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`drone-upload-context-v2/{context-analysis.json,diagnostic-candidate.json,owner.json}`,
`drone-cache-current-performance/{paired-analysis.json,*.json,*.log,owner.json}`,
`drone-channel-storage.json`. Sources/packs are adjacent named folders. Drivers:
`prepare-drone-upload-context.py`, `run-drone-upload-context-v2.py`,
`analyze-drone-upload-context.py`, `prepare-drone-cache-current-trial.py`,
`run-drone-cache-current-trial.py`, `analyze-drone-cache-current.py`,
`check-drone-channel-storage.py` in `output/renderdoc-tools-2026-10-08/`.

## Verification

Corrected context run36582 terminal0: actual debug=false40-room station,1,620
measured lighting/connected-placement/demolition frames across1x/2x/4x, clean art/
engine guards, owner2,938 unchanged.231 frames upload resources; all13183041844
large-sheet bytes are attributed to visible draws. Unlabelled546848bytes are small
resources, not these atlas bursts. No dock/preparation large-sheet uploads occur.

Largest observed group:4x placement frame148,413.4375MiB/48.283ms image creation,
93.904ms whole frame. East collection body/cargo, South carry body/cargo and South
mining body belong to three different visible drones. Requests began1–5 engine
frames earlier. Another returning steering image is consumed225 frames after its
original request; pending decoded images can survive an intervening phase. No
inference that all job retention is waste: it can avoid a later decode.

Initial diagnostic32065 fails before gameplay: an inserted variable has wrong
indentation. Owned stalled process167948 stopped after authoritative process/log
inspection; wrapper restores config and owner guard is unchanged. V2 corrects
scope/indentation and adds null-script bootstrap exits. Keep failed evidence.

Current cache trial21956 terminal0: four actual-release runs/6,480 measured frames,
256/512MiB runtime budget guards, same source pack/metadata/selected pixels;
all18 phase-end states equal. Normal source unchanged.

| Metric | Forward256 /512 | Reverse256 /512 |
| --- | --- | --- |
| Mean frame time |29.102 /30.804ms|29.319 /30.266ms|
| Uploads |350 /296|350 /295|
| Uploaded data |12.278 /11.193GiB|12.278 /11.148GiB|
| Frames >50ms |65 /126|79 /126|
| Frames >100ms |6 /6|6 /7|
| Max upload group |367.50 /275.63MiB|275.63 /459.38MiB|

Fewer uploads do not produce better frame pacing here. Both candidate orders are
slower, so this variant is rejected. Per-frame reported texture peak is3056.237MiB
in all four runs, just15.763MiB below the3072MiB large-scene budget. Drone lookup
peak1149.751MiB exceeds both nominal budgets: the budget is soft because current/
recent/canvas-owned images must remain valid. This is sampled engine texture
accounting, not within-frame/driver VRAM or complete memory certification. It
supersedes assumptions based solely on2.74GiB phase endpoints for this workload.

Read-only seven-sheet channel audit: all seven measured bodies/effects/cargo/
wheel atlases have independent RGB and transparency, including invisible texels.
None qualifies for exact grayscale-alpha or opaque-RGB storage. No conversion
or altered PNG was written. Linear filtering can observe transparent-texel RGB,
so those texels are included rather than ignored.

All completed owner guards2,938 unchanged; no native processes remain, QA overrides
restored. Normal/delivery/cache-budget files untouched. Test output bounded;
latest observed C124.42GiB/D81.64GiB free. No multi-GiB copies or capture batches.

## Next action

Choose a materially different exact storage/upload remedy. Existing direct frame
cropping fails nearest and linear raster equality; preserve full-coordinate
sampling if exploring frame-backed storage. Existing indexed sources are exact
but their measured costs/preparation regressions remain rejected. Inspect the
specific original-UV/sampler mechanism or narrowly supported storage path before
new native trials. Retain actual job/upload contexts and per-frame memory readings
for future matched tests. Continue full navigation/bug/endurance/PC/Mac gates;
do not narrow success to lower upload counts or phase-end memory alone.
