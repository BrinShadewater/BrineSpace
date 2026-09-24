# September 23 stability test builds

Updated September 23, 2026. Project: BrineSpace.

## Objective and acceptance
Package the installed Continue-dialogue, open-empty human cryopod and near-closed
drone hatch fixes, then exercise the actual Windows release and inspect the Mac
bundle. Continue the later normal station to diagnose expansion limits.

## Accepted decisions and constraints
Normal costs, failures, finite sites and crew needs remain enabled. Automated
choices use normal building, paid rerolls and room/work controls. No resource,
blueprint or clock injection. Owner room layouts and marks remain intact.
No Higgsfield, source-art edits, publication, commit or deletion of previous builds.
Mac remains an ad-hoc local test candidate, not a notarized public release.

## Current state
- Build ID: **brinespace-6600876d650b0d68**.
- Source SHA256: `6600876d650b0d687043b3afa8768493cc18b991a43cc27aac0cc7bfc59c7cb7`.
- Commit: `f380c42c046de276b0efe26364e7596ca2410ec7` with working-tree changes included.
- Windows: `builds/BrineSpace-stability-2026-09-23/BrineSpace.exe` and its PCK.
- Mac: `builds/BrineSpace-mac-stability-2026-09-23/BrineSpace.zip`.
- Both include build metadata, frozen expected manifest, README checklist, NOTICE
  and SHA256SUMS. Exact artifact hashes are also in
  `output/stability-release-2026-09-23/release-checklist.json`.
- This pass changes release metadata/preset selection and documentation, not
  production gameplay or art. The three recent source fixes are now packaged.
- Room workflow `references/gameplay-preview-contract.md` records intake checks
  and finite-site/route diagnosis; the installed skill reference matches.

## Verification
- Manifest tests: eight passing; assertion-safety: two; Mac exporter: two.
- Maintained exporters verified selected Godot 4.7.2 templates. Both platform
  manifests have identical build metadata and source fingerprint.
- Each exact PCK audit: **15,619 assets; zero missing, changed, remapped or
  unexpected**. All three new open-pod PNGs ship; the authoring study does not.
- Mac structure: arm64 and x86_64, executable permissions, one PCK, no QA override.
  Native Apple Silicon launch, signature acceptance and gameplay remain untested.
- Actual Windows EXE, `debug=false`: New Game/transmission Continue, advancing
  simulation, visible station, disk Continue preserving crew/resources, core focus
  within 1.414 pixels, settled Fit and F8 report generation pass. F8 preserves
  checkpoint bytes. 527 crew/pod references and 49 bunk plus 49 earlier polish
  references match expected pixels. 66 hatch boundary cases render without errors.
- The initial actual-release continuation reaches cycle29 from22 in180 wall-clock
  seconds with normal rules, three crew and nine rooms. No repeated Bill wake line,
  missing art or engine/script errors. This is runtime acceptance, **not successful
  expansion**: Metal remains two and Food declines to minus three.
- Baseline diagnosis: the turbine intake faces a salvage deposit. Three Power
  generation serves five demand. The initial mining deposit is exhausted; both
  discovered remaining mining deposits have no route through the rock barriers.
  The live drone reaches full charge and reports route waiting. The half-charged
  saved battery alone did not explain the stall.
- A separate180-second comparison suspends the spent ward through normal controls.
  It also reaches cycle29/nine rooms with no errors; reducing load alone does not
  restore the blocked mining routes. Keep both runs as evidence, not balance fixes.
- Agent inspected packaged New Game and later station captures. Sampling/capture
  overhead and automated choices do not establish FPS, human pacing, audio listening
  or full animation/owner visual acceptance. Earlier Marsh six-journey evidence
  belongs to its September22 package; that entire suite was not repeated here.

## Clearance comparison and checkpoint
A210-second actual-release comparison from the same cycle22 checkpoint suspends
the spent ward, schedules reachable basalt (19,17), and uses normal paid rerolls
and construction. Clearing it raises Metal from two to six; four pays for Solar
Array (18,19), rotation2. Further mining funds Current Turbine (19,17), rotation3,
with a clear intake. Solar construction completes: cycle31/ten rooms/three crew,
generation six against four demand, reserve ten, Food three and Oxygen nineteen.
Zero fixture/engine errors;221 bounded actor captures. The frozen checkpoint was
read back from its primary file and inspected visually in the actual EXE.

At cycle31 the turbine remained queued: Veld's work cell was the suspended ward
(19,18), so normal construction correctly held for access. A90-second follow-up
resumed that room through its normal control. Veld finished the paid turbine:
**cycle35, eleven rooms, three crew, no queued orders**. Generation ten against
five demand; stored Power eleven, Food six, Oxygen twenty-three, Metal four,
Integrity100. Zero errors/failures;146 bounded captures. The primary frozen save
was read back and checked for cycle35/eleven rooms/no orders. Agent inspected the
final actual-release station capture. No balance or access checks were bypassed.

Resume a disposable copy of
`output/stability-release-2026-09-23/resume-access/checkpoint-frozen.loop` next.
`expansion-summary.json` preserves comparison endpoints. The original blocked
intake remains in the station; normal clearance, new generation and restored work
access resolved this specific supply stall. Finite-resource planning and a thin
food buffer still need playtesting; this is not indefinite-survival acceptance.

## Next action
Keep the later frozen checkpoints untouched and resume disposable copies.
Continue resource-buffer/route decisions through normal controls, owner visual
review and the included Apple Silicon checklist. Do not rebuild for documentation
alone. No balancing or clearance bypass was introduced to achieve these results.
