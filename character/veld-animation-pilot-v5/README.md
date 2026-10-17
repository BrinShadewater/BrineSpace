# Veld pilot v5: scanner continuity

Four clips / 24 frames. The scanner action now uses the right-facing idle's head,
body angle and proportions. The actual idle-east frame 000 supplies inspection
frames 000 and 005 byte-for-byte; the middle four frames use the repaired source.
`frameDerivations` records that reuse. Diagnostic material masks measure source
processing, including unused generated endpoints, rather than overriding derivations.

Scanner timing: 160/180/180/480/180/160ms, total 1340ms. The longer reading hold
improves readability. The duplicate device was removed from the belt while held;
the initial rejected source and exact repair prompt remain under sources/.

Rebuild with build_pilot.py; run_native_review.py isolates APPDATA and captures
Godot playback; build_review.py assembles the comparison and idle-inspect-idle
sequence. All commands are Python scripts in this folder. Runtime art is unchanged.

Checks: 24 frames pass geometry/alpha validation; 100 native checks pass, including
both exact idle joins and the completed action's neutral hold. All 2670 real-profile
file hashes unchanged. Eighteen unaffected frames match v4 exactly. Inspection
foot-band bounds vary by at most one source pixel; every ground row remains 171.

The longer capture spans a walk loop. The probe's expected timed frame must use
modulo for a looping walk because frame_at_elapsed itself clamps; that test-only
reference-clock correction is recorded in the retained diagnostic log. Runtime
playback code was not changed. Capture duration now covers the whole scanner action.

Remaining: full hair/ivory/steel material audit, other facing directions, helmet
coverage and station integration. Candidate visual acceptance remains pending.
