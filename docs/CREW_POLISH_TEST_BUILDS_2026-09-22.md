# Crew polish test builds

Updated: September 23, 2026. Project: BrineSpace. Task: rotated expeditions and current Windows/Mac candidates.

## Objective and acceptance

Exercise Marsh's complete cargo trips through four rotated airlocks and package
the current crew work. Windows actual-release acceptance passes for the scope
below. Native Apple Silicon testing and owner motion acceptance remain open.

## Accepted decisions and constraints

Preserve previous builds, source art, owner room layouts and library marks.
No Higgsfield, commit, push or publication. Normal costs/failures remain enabled;
the expedition fixture supplies a prebuilt station and does not establish balance.
Mac is a Universal 2 ad-hoc test archive, not a notarized public release.

## Current state

- Build ID: **brinespace-7a7cf72066849d92**.
- Source SHA256: `7a7cf72066849d926437314326814a090d77fafa34fd8a4d9656324f3d77c1be`.
- Source commit: `f380c42c046de276b0efe26364e7596ca2410ec7` with working-tree changes included.
- Windows: `builds/BrineSpace-crew-polish-2026-09-22/` (EXE and PCK together).
- Mac: `builds/BrineSpace-mac-crew-polish-2026-09-22/BrineSpace.zip`.
- Both folders include matching build metadata, frozen expected manifests,
  README test instructions, NOTICE and SHA256SUMS. Old candidates are preserved.
- Includes cryopod exit timing, Branforth south/north/west repair, Marsh maintenance,
  all swim/cargo turn families, visible underwater pickup/transport, real-renderer
  timing/clearance repairs and the cargo-preserving drainage transition. Earlier
  helmet, bunk, locker, room, camera and audio work remains included.
- `tests/test_marsh_expedition_presentation.gd` now covers four rotated deliveries
  plus empty and loaded recall, with optional single-rotation capture selection.

## Verification

- Release manifest tests: 8 passing. Release assertion-safety tests: 2 passing.
  Maintained exporters verified the selected Godot 4.7.2 templates.
- Both exact PCK audits: **15,616 raw assets**, zero missing, changed, remapped or
  unexpected. Windows and Mac build metadata/source identity agree. Mac bundle
  audit confirms arm64/x86_64, executable permissions, one PCK and no QA override.
- Actual Windows EXE, `debug=false`: New Game, transmission Continue, simulation,
  disk Continue preserving crew/resources, core focus (1.414px error), Fit and F8
  report generation pass. Report creation preserves checkpoint bytes.
- Actual Windows EXE: **six Marsh journeys, zero failures**. Four airlock rotations
  deliver cargo, plus outbound/loaded recall. All loaded journeys exercise all
  twelve expedition phases, six pickup poses, five drainage poses, four unload
  poses and cargo turns, with exact extraction/delivery accounting. Pause, power
  loss, loaded/draining checkpoint restore and death precedence checks pass.
- Packaged pixels match 524 current crew-frame references, 49 prior reviewed bunk
  samples and 49 prior reviewed locker/card PNGs. Actual-release stderr is empty;
  final fixture reports zero failures. This is not an all-character action playthrough.
- Agent inspected actual-release station view and arrival/rise/planted poses in
  all four rotated chambers. Captures use a controlled prebuilt station and manual
  expedition stepping; they do not establish realtime pacing, performance or owner
  visual acceptance. No new production gameplay change was needed this pass.
- Initial native rotation-1 failure was a fixture defect: route clearing deleted
  a cryopod ward, invalidating the crew roster and triggering backup-save recovery.
  Preserve cryo/charging wards and require the just-written primary checkpoint,
  including its expected airlock home. Corrected native rotation 1 passes; the
  final actual-release run exercises all six cases together. The failed initial
  run and subsequent parse correction are preserved in the evidence directory.
- Evidence: `output/crew-release-2026-09-22/`, especially `release-checklist.json`,
  `actual-release.log`, `release-rotations/report.json`, `release-drain-contact.png`
  and both PCK audit logs. QA autoload overrides exist only in an isolated runtime
  copy with a separate profile; neither playable folder contains an override.

## Next action

Run the included Apple Silicon checklist on the owner's M1-or-newer Mac. Record
model/chip, macOS version, this build ID and any launch/Gatekeeper message. Test
New Game/Continue, room rotation, crew/drone motion, audio, fullscreen/trackpad and
F8. Then review a normal expedition for motion, room coherence and listening;
the successful controlled fixtures do not close those judgments. No rebuild is
needed for this documentation closeout alone.
