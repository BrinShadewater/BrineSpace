# Project handoff

Updated: October 15, 2026 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: follow-up Godot research

## Objective and acceptance

Research renderer appearance and hitch attribution while other sessions use the GPU.
Completed source/document investigation; no runtime reproduction or performance gain claimed.

## Accepted decisions and constraints

OpenGL remains the default. Preserve exact appearance, production assets/settings and
owner data. Keep `pacing1` excluded; clean three-backend comparison remains pending.
The research phase started no Godot, benchmark, OS trace, installation, posting or
engine patch. A subsequent resumption of the standing benchmark is recorded below.

## Current state

- New `docs/GODOT_FOLLOWUP_RESEARCH_2026-10-15.md`, this handoff and status entry.
- Linked from renderer comparison/resume notes; production code/delivery unchanged.
- Eight exact-engine source files and URL/SHA256 provenance:
  `C:/bs-godot-research2-20261015/`; private network/archive helpers:
  `output/godot-research2-20261015/`.
- Source audit identifies GLES unmipped-ImageTexture initial overcount: integer mip
  levels passed to a bool full-chain estimator; upload corrects object size but not
  Utilities' separate counter. Update reconciles; free removes estimate. Runtime
  reproduction pending. Do not call it physical VRAM use or a persistent leak.
- GL/ANGLE compilation counters always zero/unsupported; Mobile CANVAS counter counts
  requests, not duration. Official runtime symbols limit external stack attribution.
- Noise/threshold shader math and transparent LOD sampling are candidates for image
  differences, not proven causes. Private capture-event metadata journal has no bound
  in inspected cohort/fixtures; no measured size/timing or normal-source leak claimed.

## Verification

Independent source reviews support counter, precision and journal conclusions.
Eight archived hashes verified; documentation links/format checked. Only WPR found on
PATH; other tools' installation/trace capabilities not established. No new runtime
validation in the research phase. Prior image acceptance remains unchanged.

After research, `pacing2` resumed during a process gap; three forward runs / 5,040
frames completed. A foreign Godot process appeared during Mobile, so the guard
stopped the series before reverse runs. No accepted three-way timing result;
29 aggregate owner guards preserve 2,948 files. See renderer handoff for details.

## Next action

When native sessions finish or are paused, follow renderer handoff using fresh label
`pacing3`; do not rely on a short process gap. Separately
run the small create/update/release memory-counter reproduction; isolate LOD/fog/derelict
pixels; capture one short placement/zoom sequence with existing game markers plus WPR
CPU/GPU scheduling and an uncaptured control. Bound/remove private capture journal
before endurance admission. No global driver-cache clearing or revived rejected trial.
