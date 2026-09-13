# Crew social interaction handoff

Updated: 2026-09-12. BrineSpace source checkout.

## Objective and accepted direction
Owner wants autonomous crew to interact with each other as well as work, eat and sleep. First pass adds short nearby conversations using existing character gestures. No manual conversation commands, new art, relationships or dialogue tree.

## Current state
Crew in the same operating dry room with a clear line between them can pause idle, curiosity or primary work for a six-second exchange. They face each other and alternate speaker/listener states. Activity text identifies the partner. Each gets a 90-second cooldown and 15 curiosity relief after completing the exchange. Urgent human needs, helmets, life activity stages, travel, charging, active jobs and emergencies take priority. Interrupted pairs release both participants without overwriting a higher-priority goal. Workplace assignments are retained.

Changed: scripts/crew_social.gd (plus UID), scripts/bill_npc.gd (optional saved partner/cooldown, social goal validation and paired timer ownership), scripts/main.gd (simulation integration), tests/test_crew_social.gd (plus UID), tests/index.json. Old saves default to no partner and a short initial cooldown. Missing/nonreciprocal partners are released on the next simulation update.

## Verification
Primary workplace and social fixtures passed headless: output/test-runs/20260912-100124-headless. Native social fixture additionally exercises the actual actor update, turn-taking, pause, snapshot restore, hunger interruption, preservation of an emergency goal, builder exclusion and invalid cooldown rejection. Evidence: output/crew-social-native.log and output/crew-social.png. No executable rebuilt.

## Next action
Review encounter frequency in normal play. Current implementation is opportunistic proximity chat, not deliberate travel to visit another crew member. Dedicated talking art and longer-term relationships remain possible later additions. Previously recorded Branforth construction navigation concern remains outside this change.
