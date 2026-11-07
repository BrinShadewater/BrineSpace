# Project handoff

Updated: September 27, 2026 · Project: Brine Space · Task: crew animation cleanup

## Objective and acceptance
Improve the existing cast against the visual bible: consistent painted identity,
readability/detail, crisp edges and smooth motion. Overall request remains unfinished.

## Accepted decisions and constraints
Preserve cast identity, equipment handedness, world scale and gameplay. Marsh stays
helmet-free. Existing reversible-work authorization applies; no approval gate added.
Do not treat passing pixel/runtime checks as visual or owner acceptance.

## Current state
`character/crew-polish-v1/veld-painted-v2/` and the paired `-helmet/` folder now contain
20 matching Veld core states each (100 frame references each): four facings of idle,
walk, kneel, sample inspection and stand. High-resolution generated sources, exact
prompts, selection decisions and deterministic registration recipes are preserved.
`build_veld_painted.py` and `build_veld_equipment.py` reproduce the candidate locally.
The comparison page now includes actions, complete work sequence and helmet selection.
No production art/catalog bindings changed; prior 289-frame motion studies retained.
Native fixture: `tools/review_crew_polish.gd` and its paired UID.

## Verification
236 native sprite-player checks pass: phase selection, gear alignment/timing, shared
joins, pause and snapshot restore. 24 native captures saved. Scratch APPDATA isolation
was enforced by the existing `run_margot_check.py`; the real profile fingerprint is
unchanged. All 200 frame references pass size/alpha/transparent-RGB/clipping checks.
Below-collar body preservation passes for 100 equipped frames. Frozen 724-state /
4,413-reference production baseline still matches. JS syntax and selected browser
controls pass without console errors. Selected native/source-scale poses reviewed;
full motion, world contact and surrounding production action joins remain unaccepted.

## Next action
Walks still contain six poses; sample retrieval in the five-pose lowering is abrupt.
Do not install this incomplete subset over unrelated production action endpoints.
First improve continuous walk/retrieval source motion, then review native travel and
connected actions before expanding/choosing the remaining cast.
A Higgsfield Seedance 2.5 video attempt was rejected for insufficient credits, with no
job ID/result. Prompt, reference and failure record are in the sources folder. This
blocks that video route, not static image edits or local checks. No automatic retry.
Review: http://127.0.0.1:8791/character/crew-polish-v1/ . README contains rebuild commands.

## Follow-up: density, colour and style audit

Owner requested a consistency pass. `character/crew-polish-v1/audit_style.py` and
`audit_companion_style.py` measured 5,301 body-frame references / 959 states,
including the current crew, Veld candidate and three companion packs. Every
inspected export uses standingHeight148 (2.2672px/world unit) and binary alpha.
Visual consistency still fails: Veld/Branforth walking palette/softness, Marsh
work/swim anatomy/outline treatment, Bill side-action detail, and visible current
Veld east collar gaps. Companion sampled poses show no new discrepancy.

`style-review.html` and `review/style/REPORT.md` preserve same-scale light/dark
boards, scope limits and repair order. Veld east colour V3 was generated and
rejected: it made neutral cloth too warm and slightly altered silhouettes.
No production or prior candidate binding changed. First repair the collar, then
establish a correct material reference across idle/walk/work before propagating.
This audit is complete; the requested broader artwork corrections remain open.
