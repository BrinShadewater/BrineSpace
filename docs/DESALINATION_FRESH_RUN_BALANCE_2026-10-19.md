# Desalination fresh-run check — October 19, 2026

The owner accepted the revised equipment scale and requested a fresh run to judge
early Water pressure. A matched pair of fresh-profile, seed **4404** runs reached
**cycle 20 /400 simulated seconds** using normal offered cards, paid construction,
crew emergence, mining deliveries, resource costs, paid rerolls and failure rules.
No supplies, rooms, deck cards, cleared terrain, unlock purchases or perks were
injected. The control paid for the same Desalination Unit and suspended it through
the ordinary inspector control after completion.

| Outcome at cycle 20 | Desalination active | Desalination suspended |
| --- | ---: | ---: |
| Water remaining | 22 | 0 |
| Lowest Water reserve | 4 | 0 |
| Galley cycles missed for Water | 0 | 6 |
| Blackout cycles | 0 | 0 |
| Survived /Integrity | Yes /100 | Yes /100 |

The blueprint entered the hand at **64.3 simulated seconds /cycle 3**, after the
fourth normal paid order. The unit was ordered at **106.0s /cycle 5**, spent its
normal **5 Metal**, and completed at **135.4s /cycle 6**. First Water production was
cycle 7. The Galley completed at 213.8s /cycle 10 and drew 1 Water each functioning
cycle from cycle 11. The active unit ran for 14 cycles, making 28 Water; the Galley
used 10, leaving **4 +28 −10 =22**. The suspended case used its initial 4 Water by
cycle 14, then lost Galley service in cycles 15–20.

Both paid build sequences, placements, rotations and timing matched: Solar Array,
Mining Drone Bay, Current Turbine, Hydroponics Bay, Desalination Unit, Corridor,
Galley and Salvage Drone Bay. The automated policy reads the visible hand,
resources, descriptions, learned recipes and placement warnings. It never looks
ahead into the draw pile or hidden recipes. It checks clear turbine/Desalination
intakes and harvesting routes before spending. All simulation uses production
gameplay; the wrapper only supplies deterministic seeds, advances time in 0.1s
steps and acknowledges presentation pauses. Cycles retain their normal 20 seconds.

This demonstrates a useful Water reserve and prevents the observed Galley shortage
in this opening. Both runs survived because the basic Hydroponics Bay continued
feeding the crew; this is **not a demonstrated survival-rate improvement**. Crew
and the basic Hydroponics Bay do not directly spend Water. No between-tick Water
consumption occurred here, so sprinkler/fire demand was not tested. Other site
seeds, strategies, larger Water consumers and human pacing remain separate. The
control also paid for the unit, so this isolates operation rather than comparing
its opportunity cost against spending those 5 Metal elsewhere. No balance values
were changed following this limited result.

The first probe completed gameplay but hit an audio cleanup error at shutdown.
Its evidence is retained under `initial-attempt`. The wrapper now disables the
persistent music processor before stopping audio, following the existing paid-run
fixture. A fresh-profile rerun reproduced both outcomes and exited **0, with zero
script/engine errors and zero harness errors**. No production music code changed.

A separate genuinely fresh playable run is open paused at **cycle 0 /one Core**,
with **18 Metal /6 Power /4 Water /12 Food /12 Oxygen** and the normal
Solar/Mining/Hydroponics hand. **Space begins play.** This has no restored or
prebuilt station and no progression perks. Profile:
`C:/bs-water-fresh19/20261019T231512Z/Godot/app_userdata/BrineSpace`.
The prior equipment trial remains open and untouched.

Evidence: [handoff](../output/desalination-fresh-run-20261019/HANDOFF.md),
`opening-results.json`, `opening.log`, `probe-process.json`, `FINAL.json` and
`playable/ready.json` in `output/desalination-fresh-run-20261019`.
Tests and the playable run use separate scratch APPDATA folders. All 16 protected
source/art inputs and signed ZIP size/mtime are retained. No export, signing,
upload, Git integration or new platform/performance acceptance.
