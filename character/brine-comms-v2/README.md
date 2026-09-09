# BRINE tube comms portrait

Updated: September 8, 2026 · Brine Space

## Objective and accepted direction

Owner requested BRINE inside her actual tube for the comms portrait. Preserve her
recognizable face, chestnut bob, blue eyes, navy suit and restrained expression.

## Current state

`portrait.png` is the unmodified built-in imagegen output, referenced by
`scripts/crew_comms.gd`. The original `../brine-comms-v1/portrait.png` is retained.
The current portrait and `core-card-v6.png` supplied identity and chamber references.
`prompt.txt` records the exact prompt; `manifest.json` records dimensions and hash.

## Verification

Full-size and 1600/960 native panel visual reviews pass: tube collar and curved
glass remain recognizable without obscuring her face. `tests/playtest_crew_comms.gd`
passes speaker, reveal, replay and panel containment checks. Evidence is in
`output/crew-comms/brine-1600.png`, `brine-960.png` and `output/brine-tube-comms.log`.
Existing unrelated raw room-image export warnings remain.

## Next action

Owner visual review. Static portrait; no animation, dialogue or tube-room changes.
