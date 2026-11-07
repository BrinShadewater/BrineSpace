# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: structural idle regression

## Objective and acceptance

Investigate normal-idle regression/slow burst without visual or crew changes;
repeat average FPS and 4× placement hitches. Benchmarks and bounded investigation
complete; root cause unresolved because the remaining scheduler trace is denied.

## Accepted decisions and constraints

Keep structural candidate private. Preserve the original mixed study and all valid
rows. No speculative game fix, power/priority/affinity change, release or Mac claim.
Scratch APPDATA/profiles, serial muted visible secondary QA, preserve owner editor
46624 and 20 GiB reserve. Prior profile-incident caveat remains.

## Current state

Normal source/UID/tests and both frozen 24-source/PCK lanes unchanged. New files:
`docs/STATIC_IDLE_PERFORMANCE_2026-10-15.md`, this handoff,
`docs/superpowers/plans/2026-10-15-static-idle.md`; CURRENT_STATUS updated.
Helpers/profile in `output/static-idle-20261015/`; evidence in
`C:/bs-static-idle-20261015/`. No commit/export. Existing dirty work preserved.

Fresh normal idle 53.79→54.37 FPS, 4× idle 47.30→47.64, 4× placement 44.71→45.15.
Including original normal idle is 54.27→54.18 FPS. Fresh action mean
58.109→57.618 ms; following >50 ms 3→5, whole 4× placement 7→10. Mixed pacing,
0/16 fresh 60 FPS gates. No original sustained idle burst in fresh acceptance runs.

## Verification

3,840 fresh release frames / 16 exact state-camera pairs, plus separate 3,840
diagnostic frames / 16 pairs. No idle structural invalidations or demonstrated
persistent buffer growth. Diag1 CPU-busy candidate burst differs from reference
wait-like hitch, but its heavy collector prevents causal/acceptance use. Diag2
collector cost reduced to 0.26–0.54 ms/sample; reverse idle burst absent.
Approximate sampling/CPU granularity and coarse desktop activity are documented.

Both prior lanes/packs exact; prior 1,148 raster pairs/38 cache checks/17 station
pairs/12 repeats reused, not rerun. All 17 owner and 16+16 binary guards pass;
2,948 final protected files equal initial/prior. No changed game behavior.

## Next action

Valid bounded WPR scheduler profile failed **0x80070005 Access is denied**; status
confirms no recording. Local parser exists. Next useful step needs an
administrator-enabled scheduler capture aligned to the same frozen fixture's
burst. Do not attribute the original to a process, driver or core migration yet.
