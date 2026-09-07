# Crew detour graph-join repair

V33 stopped near Crew Lounge with static geometry clear and an active colleague
blocking Bill's immediate direction. `tools/probe_lounge_traffic.gd` reconstructs
the recorded positions using native Lounge q1/Battery q0 geometry. With no peer,
the controller arrives. With the recorded stationary peer, it never moves and
abandons the path. A safe eight-unit east offset admits a successful detour.
The nearest static-clear graph join is not crew-clear from the original foot.

`detour_around_crew()` now selects the closest graph join whose approach clears
both static geometry and peers. It still applies the existing graph exclusion,
smoothing, movement speed and avoidance checks. No artwork, room footprint,
door width, clearance radius, retry limit or destination policy changes.

The literal-position progress regression fails before the fix (one missed
arrival) and passes afterward with/without the peer, checking standability,
per-tick speed and peer clearance. Logs: `output/lounge-traffic-{red,green}-v1.*`.
This two-room stationary-peer reconstruction is not an exact three-crew replay.

Existing regression results (`output/lounge-join-*-v1.*`): crew polish and
Branforth three-crew tests pass, both reporting 20.61 minimum separation;
Bill NPC passes 140 room/rotation checks. All three child exits are 0 without
engine errors. Raw-image warnings remain in native loading. Fresh V34 packaged
tour verification is in progress and must be recorded separately. Full native
sprite motion review and broader autonomous traffic coverage remain open.

V34 completes all 30 packaged tour arrivals and 84 transitions with 6341
collision/speed samples. Controller SHA256:
`dc9bad330ea14044427b58edcd5dfcc0f93b8fdc73aa47d00f22b49e8cb6785c`.
PCK SHA256: `781979f9a24003db0e0490699322119a925dab6de895a0534ee90a26d785b6f7`.
The new native furnishing-host export gate passes (26 views, 22 profiles, 192
references). V34 is still rejected overall: Hull Integrity's dressing profile
fails JSON loading at `shield_generator_view.gd:16`. The tour's successful
movement is separate from this remaining package dependency error. No clean
whole-build claim or broad autonomous-traffic acceptance follows from this run.

V37 resolves the separate missing room-JSON dependency and passes the whole debug
package check: 30 arrivals, 84 transitions and 6365 movement samples, no engine
errors. See `ROOM_DRESSING_HOST_AUDIT.md` for exact package hash and isolated
profile evidence. Broader autonomous traffic and sprite review remain separate.
