# Individual Medical Bay / Reactor export follow-up

Later Reactor-only revision: steel hull/card v4 passes standalone v17 at all
three actual sizes. See `REACTOR_STEEL_EXPORT_V17.md`; the v16 evidence below
continues to describe Medical Bay v5 and Reactor v3 precisely.

## Completed individual runs

Medical Bay card v5 and Reactor card v3 pass the unchanged source-fixture
assertions in standalone v16 at actual 1280x720, 1600x900 and 2560x1440.
Accepted records are `output/batch-two/foundation-export-1280-v1`,
`foundation-export-1600-v1` and `foundation-export-2560-v2`, each containing
`verification.json`. Each size has 69 Medical Bay plus 134 Reactor full-frame
PNG-header checks: 609 across the six accepted runs. All exit zero with no
ERROR/SCRIPT ERROR entries and pass input isolation. Raw-image warnings remain.

Medical Bay covers four rotations, complete assembly/contour retention,
independent host working/offline comparisons and removed-neighbor wall infill.
Reactor covers four rotations, repaired-loop retention, room-level active/offline
comparisons, its inherited Nursery preamble and mature-station fit. Both manipulate
renderer state directly; neither is a complete economy-shortage suite. Reactor's
inherited paused pairs test Nursery, not independent Reactor-host pause. Legacy
path-helper samples do not certify current autonomous NPC behavior.

Reviewed full frames: 1280 Medical q2 sealed and Reactor q1 connected;
1600 Medical q0 connected; 2560 Medical q3 sealed. Props remain upright and the
reviewed infill is intact. This is not an all-frame seam or final art approval.
The 2560 v1 Reactor timeout below remains rejected; v2 uses the same executable
and PCK with a 120-second limit and unchanged assertions.

## Missing assets resolved: v16

The three referenced v2 seabed images are now present with import metadata.
Fresh standalone v16 passes external-directory loading and controlled traversal:
24 arrivals/visited rooms, 62 transitions, 4,734 movement samples, 16 room-source
hashes/32 raw PNG decodes and three additional component hashes/decodes. No
ERROR/SCRIPT ERROR entries were reported; raw-image warnings remain.
PCK SHA256: `4BBF5F8E1120C01EBB6407E223932EC5F5B32423842EF9046462D2DDDB65AAC7`.
V14/V15 failures below are preserved as historical evidence, not current blockers.

The first 2560 Reactor run reached 93 full-frame sidecars before the runner's
60-second timeout. No engine errors were reported, but it did not complete and
is not accepted. Evidence remains in `foundation-export-2560-v1`. The runner now
allows an explicit 60–180-second limit (default still 60), records it in new
verification JSON, and stops only its own process on timeout. The retry uses
120 seconds without changing assertion or dimension checks.

The export bridge now includes the existing Medical Bay and whole-room Reactor
fixtures, changing inheritance only. Five Python tests check all generated
assertion bodies and 15 recorded source hashes. Reactor's source fixture now
labels its result `reactor` when `--reactor` is selected; other subjects retain
their existing label. The runner accepts both explicit room IDs, passes the
Reactor flag and checks each fixture's actual rotation capture naming. Its
default ten-room selection is unchanged.

Godot assigned the two new generated-script UIDs during export. The read-only
UID audit passes 49 canonical, distinct script/UID pairs. No UID was invented.

## Verification interruption

V14 failed clean-log acceptance despite completing its controlled tour: six
sub-biome v1 prop images were unavailable inside that exported build. A subsequent
explicit editor import completed and all nine v1 images had import metadata.
V15 then encountered a newer shared renderer referencing these absent files:

- `assets/environment/sub-biomes-v1/sulfur-anhydrite-v2.png`
- `assets/environment/sub-biomes-v1/sponge-vase-sponges-v2.png`
- `assets/environment/sub-biomes-v1/sponge-sea-fans-v2.png`

At inspection these v2 paths did not exist in the checkout. Preserve V14/V15
logs under `output/batch-two/windows-validation-v14` and `windows-validation-v15`.
Neither build is accepted. No seabed source was reverted, no fallback inserted,
and no error gate weakened. The import attempt is not evidence that import alone
resolves the earlier v1 failure; the shared inputs changed between builds.

Once the referenced art exists, rebuild to a new output directory and run
`check_exported_batch_two.ps1` with `-RoomIds @('med_bay','reactor')` at 1280,
1600 and 2560 with input isolation. Individual packaged state coverage remains
unverified. Existing v13 mixed-station evidence remains valid for that recorded
build only. Legacy route helpers in the individual fixtures do not establish
current autonomous NPC behavior; state and pause scope follows each source body.
