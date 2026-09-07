# Ten-room checkout-independent PCK smoke

The station packager now accepts `--production-ten`, explicitly including the
batch manifest, each registered view/card and all ten individual fixtures, plus
the batch connection test. Existing import-remap handling and raw PNG inclusion
remain intact. This is a local dependency smoke pack, not a release export.

`output/production-ten/batch-smoke-v1.pck` contains 1,546 files with SHA-256 records
in its `.pck.json` sidecar. Required selected sources, views, cards and fixture
scripts for all ten rooms were checked against that inventory.

All ten room fixtures ran at 1600x900 using `--main-pack` from a newly created
external temporary directory recorded in `package-external-dir.txt`. Every
process exited zero and every subject-specific ROOM SCENE PASS banner was
verified. Captures cover four rotations and active/inactive/pause states.
The packaged connection sweep also passed all 6,400 cases and 294,516 routes.
No ERROR/SCRIPT ERROR entries appear in `pack-*.err`. The packaged Research Lab
station/draft/inspector frame was visually inspected with art and icons present.

Evidence is in `output/production-ten/pack-<room-id>.log`, matching stderr and
`pack-<room-id>-1600/` captures, plus `pack-connections.log`.

Raw Image.load warnings persist. Explicit packaging supplies those bytes; this
does not prove default export inclusion. No export preset or installed 4.6.1
export template was found. A standalone release remains unverified. Pixel seams,
production walkers and economy-driven states also remain separate acceptance
work. The pack remains local and is not published.
