# Reactor steel hull: standalone v17

Reactor card v4 retains canonical geometry and south-facing equipment while using
the source's steel wall finish and restrained orange trim. No art was regenerated
for this verification pass.

## Packaged station

`output/batch-two/windows-validation-v17/verification.json` records a successful
external-directory Windows debug run: 24 scheduled arrivals, 24 visited rooms,
62 reciprocal transitions and 4,779 collision/speed samples. Sixteen selected
source hashes, 32 raw PNG decodes and three additional component hashes/decodes
pass. Logs contain no ERROR/SCRIPT ERROR entries; raw-image warnings remain.

PCK SHA256: `2CEF32820741CB263C36D0C67D9D821FFE254E00D386D039F03C2984B391AE26`.

This is controlled traversal using production movement, not autonomous
destination-choice or release acceptance. Individual state checks and visual
review are separate evidence below.

## Individual Reactor checks

Accepted evidence: `output/batch-two/reactor-steel-export-{1280,1600,2560}-v1/`.
All three runs use the above PCK, exit zero, report no engine errors, and pass
Escape/W/Space input isolation. Each has 134 full-frame PNG-header/sidecar
dimension checks: 402 total at actual 1280x720, 1600x900 and 2560x1440.
The runtime limit was 120 seconds with unchanged assertions. Five export-bridge
consistency tests also pass.

Coverage includes all four rotations, cooler-loop retention, connected-wall
samples, aggregate working/offline comparisons and 40-room station-fit checks.
Renderer state is manipulated directly, not driven through all economy failures.
Inherited paused pairs exercise Nursery, not independent Reactor-host pause.
Legacy route-helper checks do not establish autonomous NPC behavior.

Visually reviewed full frames: `nursery-life-q2.png` at 1280,
`nursery-life-q0.png` at 1600 and `nursery-life-q3.png` at 2560. The reviewed
horizontal and vertical connections retain a continuous shared wall with a
clear opening; machinery stays upright and inside the shell. These selected
frames are not exhaustive seam inspection or owner approval. Fine prop margins
and independent Reactor pause/current-controller coverage remain open.
