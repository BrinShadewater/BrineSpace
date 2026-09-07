# Reactor Engineering source revision

## Engineering hull follow-up: card v4

Reactor now overrides inherited pale wall materials locally. Its immutable donor
supplies steel wall samples `(125,45,220,38)` horizontal, `(55,110,31,220)` vertical
and `(56,46,29,33)` corner caps, mapped to the canonical 48-unit panel spans.
Restrained non-emissive orange trim sits inside the wall surface. Thickness,
three-unit top lift, four-unit fascia, sockets, equipment, floor and white lights
are unchanged. No other department's renderer was edited.

Card v4 is selected by the central catalog, both Reactor grid fallbacks and both
Reactor/whole-room manifests; card v3 survives. Inspected card v4 and native
`reactor-steel-state-v1/nursery-life-q2.png`: the dark shared wall is present.
V1 rejected two seam samples because Reactor lacked the existing dark-material
exception. V2 adds Reactor to the same bounded neutral-charcoal pixel criterion
used by Archive/Holo, without removing geometry or image-presence checks.

`output/batch-two/reactor-steel-state-v2.log` exits zero with no engine errors:
four rotations, loop retention, connected wall samples, aggregate working/offline
checks and mature-station fit pass. Its 134 full-frame captures independently
measure 1600x900. Legacy path checks are not autonomous NPC evidence. Five bridge
consistency tests pass; card v4 uses LFS. Raw-image warnings remain.

Fresh v4 standalone v17 passes all three actual sizes (1280x720, 1600x900,
2560x1440), 402 full-frame dimension checks, input isolation and the controlled
24-room tour. Selected horizontal/vertical shared connections were reviewed.
See `docs/REACTOR_STEEL_EXPORT_V17.md` for hashes and precise coverage limits.
Earlier v16 three-size evidence applies to card v3, not this wall revision.

## Cooler opening repair: card v3

Current individual export coverage: v16 passes at actual 1280x720, 1600x900 and
2560x1440, 134 dimension-checked full frames per size. The final size required a
120-second timeout; the incomplete 60-second attempt is preserved. See
`docs/FOUNDATION_ROOM_EXPORT_FOLLOWUP.md` for precise state and movement limits.
Earlier pending-export statements below describe their historical checkpoints.

Standalone follow-up: v13 verifies current source/card loading and controlled
arrival in a 24-room exported fixture at actual 1600x900. See
`docs/ROOM_REPAIRS_STANDALONE_V13.md` for scope; the individual exported state
suite and all-resolution coverage remain separate gates.

The conservative source-floor strip `(335,182,7,98)` inside the cooler return
loop is now omitted using cached polygon partitions with unchanged source UVs.
Pipework, its lower mounting plate, source image, prop placement and complete
collision reservation are retained. This visual opening is not a new walk path.
Native before/after cooler contrast renders and card v3 were inspected under
`output/batch-two/reactor-edge-{before,gap}-v1/`. Finer pipe margins remain open.

Card v3 replaces v2 in the catalog and both grid fallbacks. The manifest's stale
v1 reference is corrected to v3. PNG uses LFS; no original was overwritten.
`reactor-gap-station-v1.log` exits zero with no ERROR/SCRIPT ERROR entries,
checks four rotations with retained-pipe/base and excluded-gap points, and
captures actual 1600x900 frames. Existing aggregate motion/offline/pause and
station-fit checks pass; legacy path-helper assertions in this fixture do not
certify the current autonomous NPC controller. Raw-image warnings remain.

Fresh standalone coverage and Medical Bay cleanup are not completed by this
pass. The inherited pale wall finish was preserved, not reapproved as Engineering
compliance; departmental hull styling remains a separate review item.

`source-v1.png` replaces the older ivory donor in the existing reactor view.
The original donor and card remain available. Built-in image generation edited
the existing composition; the exact prompt is in `manifest.json`.

The central chamber, northwest cooler and southeast console retain their
gameplay footprints. Source silhouettes and pivots were re-registered because
the material edit slightly enlarged the cooler pipework and chamber base.
This is source-space polygon extraction, not dark-pixel removal or recoloring.
The engine still owns the four sockets, shared shell and perimeter route.

The 512-square card was baked through the same offline renderer and selected
in the shared card catalog and grid fallbacks. Legacy random reactor image
selection is collapsed to this card. Native card and 1600 pair overview were
visually reviewed: equipment remains south-facing with clear circulation and
stronger Engineering department materials.

Existing chamber and console animation remains. The cooler is static. The
source amber glass and orange panels are non-emissive material color; there is
no source glow halo. Small floor patches enclosed by cooler pipework remain a
known extraction tradeoff. No full per-host animation acceptance is claimed.

Validation uses `tests/playtest_whole_room_station.gd -- --reactor` with logs
and captures under `output/reactor-engineering/station-*`. Each run checks four
rotations, 404 nursery-to-reactor walker positions and another 1,212 reactor
perimeter-entry positions, aggregate powered/offline pixel differences, and
40-room station fit. The fixture also retains its separate nursery checks.
These are fixture checks, not a new normal-run balance or export acceptance.
