# Reactor composition integration

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Make Reactor read as a functional machinery room through large/medium equipment,
with usable circulation. Installed for playtesting; owner visual acceptance and
the broader animation, room and performance goal remain open.

## Accepted decisions and constraints
Preserve the ten named owner layouts and library marks. No Higgsfield or generated
raster edits, no export, commit or publication. Quarantine and Command Center were
reviewed but not changed.

## Current state
Four room-reactor saved/default keys updated; assets/room-cards-v2/reactor.png
rebaked. Backups, registry hashes, source shortlist and captures are under
output/reactor-composition-2026-09-21. All other layouts and every library JSON
remain unchanged.
The former small control housing, loose gauges, coolant canisters, warning lamp,
red tank and two retained service strips are hidden in this layout. Three bought
props now establish the work areas: lbt2-06 reactor [-174,-180] at .76 scale;
mb-46 cooling unit [48,-180] at .85; npp2-107 operator console [-174,48] at 1.2.
The open lower-right area is service/circulation space, not an accessory-fill target.
No gameplay, material textures, source registrations or crew behavior changed.

## Verification
Candidate and installed defaults each pass four views/640 walking samples.
All four fresh-default captures pixel-match the saved-layout candidate. Live 52%
and 75% scale captures completed; native room crop and final card inspected.
Four controlled maintenance trips each complete 140 clear movement samples and
start checking equipment. The fixture funds the room and forces maintenance;
it is not autonomous expedition/balance acceptance. One-room card bake exited 0.
Existing animated reactor overlays bind only to hidden legacy props; this change
does not add animation to the bought reactor/cooling unit or certify motion.

## Adjacent audit
output/quarantine-composition-2026-09-21 contains Quarantine, Command Center and
Reactor baseline captures. Their 12 combined views/1,920 walking samples pass.
Quarantine already groups treatment, washing and filtration coherently; retained.
Command Center has an incongruous small wooden crate and separated control islands;
possible future composition pass, no modification made here.

## Next action
Gather owner room feedback and continue animation/operation presentation review.
The existing action-polish packages predate this layout, Hydroponics r3 and the
navigation cancellation fix; batch future exports at a meaningful checkpoint.
