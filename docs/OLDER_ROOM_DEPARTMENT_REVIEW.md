# Older room department review

Source images for Hydroponics, Reactor and Med Bay were inspected against the
current underwater bible. This is an art audit, not acceptance of every state.

Hydroponics retains suitable white composite grow beds, green crops and glass
nutrient vessels. Its inherited generic dark floor was replaced with pale
moisture-resistant composite and restrained green perimeter service strips.
Card v7 is baked and selected in both card mappings; legacy alternate-image
selection is collapsed to that current card while originals remain intact.
The native card and 1600 nursery/ Hydroponics pair frame were inspected.

The existing whole-room station fixture passes with `--hydro`: four rotated
pair setups, 404 production walker samples, state captures and the inherited
mature-station checks. Evidence: `output/department-review/hydro-station*`.
Exit zero, no SCRIPT ERROR/ERROR lines. This finish-only change does not claim
new full host-effect coverage or export acceptance.

The harvest screen now has an engine-owned dark surface replacing the donor's
baked green readout. Three contained readout lines animate only while operating;
both endpoints use source-space registration so the marks scale with the host.
Card v7 shows the offline screen and was visually reviewed at native size.
The four main chassis status lenses are now engine-controlled as well, dark
when offline and green when operating. Small secondary controls remain donor
art; their markings are not asserted to be dynamic indicators.
Current screen-change fixture evidence is under `output/hydro-screen`.

Med Bay already has white/teal equipment and a pale teal floor; it does not need
the Hydroponics floor correction. Empty-bed waveforms have been replaced with equipment-readiness bars.
The supply cabinet indicator was enlarged after independent host testing found
its old alpha pulse invisible at station scale. Source-floor silhouettes remain
a separate cleanup concern. Med Bay also now uses whole-room card fitting,
correcting the cropped hand image observed in the station capture.

Reactor now uses `rooms/underwater/reactor/source-v1.png`: steel and orange
Engineering machinery with its existing central chamber/perimeter layout.
Source-space cutouts were registered again after the material edit. Runtime
source and current card are selected; originals remain. Native card and 1600
pair overview were visually reviewed. See the room's `REGISTRATION.md` for
fixture scope and the remaining cooler pipe-loop floor tradeoff. Gameplay is
unchanged; this is not full per-host or export acceptance.

Hydroponics now has a dedicated `tests/playtest_hydroponics.gd` fixture using
the shared per-host state harness. At 1600x900, all four assemblies passed
independent motion/offline checks in four rotations, visual containment and
pause checks; harvest marks stayed inside the display. Evidence is in
`output/hydro-indicators/station.log`. No SCRIPT ERROR/ERROR lines. Native
card v7 and operating room q0 were reviewed. This does not claim a new export
or every viewport pass for the indicator revision.

Med Bay evidence: `output/med-readiness/station-v2.*` passed four rotations,
808 entry-route samples and per-assembly powered/offline checks at 1600x900.
The first run is preserved: the supply-cabinet motion assertion failed.
The shared fixture summary now prints an assertion-failure count rather than
saying assertions passed on a failing run; its export bridge was regenerated.
No revised export or additional viewport acceptance is claimed.

## Stand, stool and Reactor edge polish

Med Bay's two IV stands now draw separate pole, bag, tube and foot silhouettes.
The console and stool also draw separately, exposing the live floor between the
stool feet and beneath the console. Card v3 was an intermediate IV-only bake;
card v4 is selected in both runtime mappings and the six-room export manifest.
Native card inspection caught the remaining stool patch before that final bake.

Reactor's cooler outline follows the upper pipe edge more closely, and the
console outline excludes the floor between its feet. The cooler's dark backing
is a real mounting plate and remains. Card v2 is selected; raster donors and
collision footprints are unchanged.

Evidence: output/reactor-polish/station.log (four rotated pairs,404 path samples,
state and pause captures) and output/med-readiness/stand-stool-polish.log (final
Med Bay revision). These are local1600x900 fixtures. The prior combined Windows
export predates these two card revisions; no new packaged acceptance is claimed.

## Packaged follow-up

The latest Med Bay card v4 and Reactor card v2 are included in
`output/room-rollout/windows-polish-34-v2`. The Windows debug build ran from
an external working directory:34 source hashes,68 source/card PNG decodes and
BRINE's component check passed. Bill reached51/51 rooms through135 reciprocal
transitions, with10377 collision/speed samples and zero assertions. This
supersedes the preceding unexported status for these revisions.

Pack SHA256: 8A66E69151B25888F93C9F2A39374D154ECA5DCB177D48381321942FAB385446. This remains a controlled-tour debug check.
