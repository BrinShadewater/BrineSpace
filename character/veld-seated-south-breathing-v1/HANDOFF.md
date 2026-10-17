# Project handoff

Updated: 2026-10-01 · Project: BrineSpace · Task: Veld south seated breathing

## Objective and acceptance
Continue the full Veld set and master consistency. This milestone adds paired
south held breathing; it does not complete the full set or establish room use.

## Accepted decisions and constraints
Use exact final matte south neutral from veld-seated-south-coherent-v1. Local
breathing is permitted from a locked pose. No new generated poses/RGB, additional
grade, per-pose scale, normal selection, furniture or gameplay change.

## Current state
build.py creates12paired RGBA frames, held-only manifests and review GIFs/board.
Locally authored phases0/.5/1/.75/.25/0 use north breath maximum .363636px/side.
Expansion affects only y131:159 outside the central24px chest fitting region;
face/hair/helmet/collar/belt/hands/knees/boots exact. Measured existing helmet
fitting reaches y129, so breathing support starts below it. Six600ms slots form
a3.6sec loop with exact neutral start/end/down/rise joins. Original South down/
rise/static held pack remains unchanged. Preview index.html shows both gears,
neutral and station sizes. Native fixture/runner are test_veld_seated_south_breathing
and run_veld_seated_south_breathing; tests/index.json admits the native lane.

## Verification
65package checks,0failures,16deterministic PNG/metadata files.182native checks,
0failures,24.36sec engine0/no errors. Actual selected player plus fixture-only
held overrides, controlled Veld source hook follows visual clock across two
cycles/third seam, exact source admission, neutral joins, actor/player snapshot
admission and paused stability. Native paired148/82 board and source board
reviewed. All2931non-log owner files unchanged with scratch APPDATA.
Initial180checks/52failures retained in output interval: fixture incorrectly
treated finite frame_at_elapsed as a looping clock and drove held source by
actor timer. Corrected fixture to use the production visual clock; no runtime
change. Green hashes alone do not prove natural respiratory motion; amplitude
is deliberately subtle at gameplay size.

## Next action
Review paired South motion/contact where naturally requested; default lounge sit
resolver still requests North. Do not force South into that chair and call it
directional room acceptance. Natural North approach/exit/hazards, independent
East/West seated sources, rest/death joins and full-set polish remain. Candidate
unselected; no actual South furniture/service-loss/fresh Continue/owner acceptance.
