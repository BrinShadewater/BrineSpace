# Cryopod pacing and other crew review

Updated September 22, 2026. Requested crew polish remains in progress.

## Objective and constraints
Review Veld, Branforth and Marsh and repair choppy cryopod emergence. Preserve
owner room layouts, existing art and normal thaw rules. No Higgsfield.

## Installed change
scripts/architect_cryo_art.gd now holds the closed pod during thaw, then plays
the five open/exit poses over the final 1.2 seconds (0.24 seconds per pose).
Previously six poses were divided evenly across the displayed thaw duration:
the core's seven-second display stage held poses for about 1.17 seconds each.
The core still takes ten seconds including its three-second power-up stage.
Ward timing, power/pause behavior, saved wake progress and release rules are
unchanged. Marsh's separate charging animation is unchanged. This is retiming
existing key poses, not newly authored in-between frames or a claim of full
animation smoothness acceptance.

## Verification
tests/test_cryo_exit_timing.gd and its UID added; registered in the crew subsystem.
Checks pass for closed thaw, ordered complete exit poses and final pose at
7/10/12-second durations. tests/test_architect_recovery.gd passes, including
release identities and checkpoint behavior. Native helper comparison captures
91 frames for Bill/Veld/Branforth; native station capture confirms Bill actually
releases and becomes active. All runs exit0 without logged engine errors.
Evidence: output/cryo-exit-review-2026-09-22, including comparison.gif, native.log,
timing.log, recovery.log, station.log and station/frame-*.png. These are working
source checks; the earlier exported Windows/Mac builds do not include this fix.

## Crew findings and remaining work
Production sprite playback captured Veld/Branforth/Marsh in four directions for
walking, carrying, swimming and repair: 48 combinations, 90 samples each.
Walk/repair samples visually inspected. Swim/repair boards needed taller cells
to prevent preview overlap; corrected and recaptured. These are bare-sprite
comparisons, not full station navigation, furniture contact or every action.
Evidence: output/other-crew-review-2026-09-22/{walk,carry,swim,repair}.

Branforth's north/south/west repair poses look coarser than his east repair pose;
review their preserved sources before choosing a pixel repair. Marsh's repair
pose reads close to standing idle, although its frame hashes are not identical
to idle. Do not call it a missing file or substitute idle based only on appearance.
Marsh's dedicated water/carry transition coverage remains absent as previously
identified. It needs a focused motion/source pass; no replacement clips were
installed in this review. Veld/Branforth lack dedicated run clips, but no new
controller requirement for them was established.

## Next action
Review the retimed cryopod preview for remaining pose jumps. Continue with
Branforth repair source consistency and Marsh action/transition readability;
do not equate a populated catalog with finished visual work.
