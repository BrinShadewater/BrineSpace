# Procedural sites: owner review

The local implementation generates new geography per expedition and preserves it
through Continue. First sightings remain Veld → Branforth → Marsh. Normal costs,
salvage yields, rescue requirements and companion progression are unchanged.

## Scenery choices

[Native comparison under production lighting and fog](../output/procedural-sites-2026-09-23/native-scenery-audition-final.png)
shows existing/bought pairs above the rooms: rocks, coral, kelp, then timber,
left to right. [Light/dark seabed comparisons](../output/procedural-sites-2026-09-23/scenery-comparison.png)
and the [candidate sheet](../output/procedural-sites-2026-09-23/bought-candidates.png)
provide clearer source inspection.

| Role | Current choice | Review status |
|---|---|---|
| Low rocks | `uw1-188`, `mb-210`, 0.20–0.38 cells | Provisional bought-art choices |
| Timber | `mat-130`, `mat-131`, 0.35–0.55 cells | Provisional bought-art choices |
| Coral and kelp | Existing artwork retained | Bought candidates failed projection or edge-pixel checks |

The owner decision is whether the provisional rock/timber materials and scale fit
the seabed, and whether their silhouettes remain readable under gameplay fog.
Agent visual review is recorded; owner acceptance has not been assumed.
Decorative choices do not change collision, excavation or salvage yields.

## Map and Studio

- [Three generated map layouts](../output/procedural-sites-2026-09-23/map-comparison.png):
  diagnostic view of geography and separated recovery sites, not an in-game reveal.
- [Native Studio filter capture](../output/procedural-sites-2026-09-23/studio-filter.png):
  exterior art is excluded from new placement choices; existing placements remain
  renderable, movable and removable. Indoor aquarium/lab props and owner marks remain.

Human expedition pacing remains an owner/playtester judgement. Automated route,
resource and rescue tests establish their recorded mechanical scope, not whether
the spacing feels satisfying to play. Detailed verification and limitations are in
[the implementation handoff](PROCEDURAL_SITES_2026-09-23.md) and
[the routing/berth follow-up](PROCEDURAL_ROUTING_HANDOFF_2026-09-23.md).

No commit, push or release package has been made for this work. Existing downloads
predate these changes.
