# Crew underwater expansion

In production for Major Bill, Dr. Veld and Chief Engineer Branforth. All artwork
and helmet fittings remain provisional; mechanical checks are not visual acceptance.

New [east/west swim stroke revisions](revisions/README.md) replace 36 runtime frames
with clearer arm propulsion across all three crew, including matched helmet fits.
The normal loader passes all six native body/helmet phases. Continuous motion
and swimming route clearance remain under review.

## Packaged and loaded

| Coverage | Clips | Frames | Actors |
| --- | ---: | ---: | --- |
| Swim and tread, four directions each | 24 | 144 | All three |
| Ground and water death, east | 6 | 36 | All three |
| Helmet donning and removal, east | 6 | 36 | All three |
| Helmet fittings for water and death | 30 | 180 | All three |
| Dry helmet fittings | 40 | 240 | All three; run is Bill only |

Dry fittings cover idle/walk in four directions, east interaction/kneel/repair/stand,
and Bill's four run directions. Original dry artwork remains the source. Transition
canvases are 92 × 104 with pivot (46, 98); other water/death canvases are 92 × 92; revised east/west swims are 104 × 92.
Removal derives from reversed donning frames with separately authored timing.

[Shared review](review.html) includes 36 extension clips and 40 dry counterparts.
Rebuild with `python character/crew-underwater-v1/build_review.py`; validate with
`python character/crew-underwater-v1/check_pilots.py` from the repository root.

## Runtime and verification

The shared NPC controller selects swimming/treading by movement medium, preserves
terminal death, and commits helmet state after timed equip/remove completion.
Simulation time controls equipment actions, including pause and save restoration.
`request_helmet_at_locker` checks a route to an explicit interaction point, walks
there, then starts the action. Unsafe travel, topology rebuild and death discard
pending work. Saved requests require consistent destinations, medium and gear.

Current checks: 36 base clips plus 30 water/death and 40 dry fittings pass pixel
validation. `tests/test_crew_death_save.gd` passes real disk round trips for all
three pending locker routes and both mid-action states, swept travel checks,
interruption, contradictory-save rejection and existing death checkpoints.
`tests/playtest_crew_water.gd` passes native sampled donning, removal, equipped dry
poses, treading and death playback. Removal samples at 500, 720 and 1100 ms were
visually inspected for all three crew; overhead poses remain within the canvas.
These samples do not establish continuous smoothness. Native logs also contain
room-resource warnings outside these animation assertions; this is not a
clean export or whole-game validation.

## Still required

- Refine swim/tread limb motion, directional projection and transition endpoint fit.
- Refine the now-integrated pickup/deposit joins and idle/equipped endpoints;
  see [current locker selections and defects](locker/README.md). Older captures
  may predate the selected actor-specific pickup revisions.
- Connect real flooding and exterior navigation to medium/equipment behavior.
- Review continuous motion and collisions in actual deployment locations.

The buildable Diving Airlock now provides a real locker approach and inspector
Fit/Return controls for all three architects. Its single fitting station reserves
through pending requests and active actions; gear is reusable, without finite
stock. `tests/test_airlock.gd` covers the production locker, rotation clearance,
power interruption and real disk saves. Full suit changing and exterior travel
are not implemented. The older equipment tests still use explicit fixture points.
Older experiment notes and superseded counts are preserved in
[the pilot history](README-pilot-history.md). Current manifests and source hashes
supersede older capture evidence when files have been rebuilt.
