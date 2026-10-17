# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: Veld expedition guards

## Objective and acceptance
Complete full master-matched Veld animation coverage, then cross-family polish.
This milestone adds phase checkpoints and safety events to staged cargo proof.

## Accepted decisions and constraints
Use real controller, locker request, oxygen and airlock APIs. No forced gear removal,
production validator relaxation or art/profile promotion. Scratch APPDATA, owner
profile fingerprints, retained failures. Current native art and masters preserved.

## Current state
review_veld_expedition_interruptions_v1.gd/.uid and Python runner are separate from
the six-journey fixture/evidence. Four actual journeys: normal delivery with every
phase-entry checkpoint; recall at sampling/pickup; oxygen threshold recall. Captures
and report in interruption-review-v1; hashes in interruption-evidence-v1.json.

## Verification
12,060 checks pass. Twelve current disk checkpoints restore exact pose, route/action
clock, chamber clock and simulation clock; paused position preserved. Eight station/
chamber power holds and48actual locker request guards. Exact extraction/credit rules,
all normal pickup poses and dry/alive return. No engine errors;2,914owner non-log
files unchanged. Initial phase-entry save rejected the fixture's60s breath reserve;
runtime max is15s, tank max60s. Corrected setup and preserved rejection intervals.
Prior native exterior/pickup/return/unload visual reviews remain; artwork unchanged.

## Next action
Install staged action/cargo/turn families and conservative profile, then prove all
normal-loader selected frames/metadata and full journeys. Retain broader traffic,
arbitrary mid-phase checkpoint and other safety-event coverage as open. Continue
remaining life/distress/recovery/death/full-set consistency and polish; full goal active.
