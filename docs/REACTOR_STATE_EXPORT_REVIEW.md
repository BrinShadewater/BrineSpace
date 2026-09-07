# Reactor state checks in Windows export

## Build and scope

`output/batch-two/reactor-state-package-v1/BRINE.pck` SHA-256:
`85DBC223D24F3CFA623E80B6B0238B040658DA317E4B7DF8D7117B9BB855DEFF`.

The export bridge now dispatches `reactor_effects` and `reactor_lighting` without
changing their assertion bodies. Seven bridge tests pass; the recorded source
set now contains twenty fixtures/dependencies. Editor import assigns both new
generated scripts their paired UIDs. Floor-hook and native dressing-host gates
pass before export.

## Reactor-specific exported runs

Both runs use the same PCK, an external temporary working directory, and the
actual 1600x900 window. Both exit 0, reach their subject-specific PASS markers and
have no ERROR/SCRIPT ERROR entries. Raw-image warnings remain.

- `output/reactor_effects-export-v1`: 48 individual prop operation comparisons,
  four production-clock pause/resume checks, and input isolation pass.
- `output/reactor_lighting-export-v1`: four actual economy suspension/resume
  cycles, half/full light fades, paused intermediate pixels, restored brightness
  and input isolation pass.

All 48 Reactor-prefixed full PNGs have verified 1600x900 dimensions. The five
inherited Nursery setup images in each run are not counted as Reactor evidence.
The exported q0 suspended lighting image was visually inspected and retains the
low shell and recognizable machinery in darkness. This is not every-frame
visual acceptance or a multi-resolution result.

External working directory:
`C:/Users/Alex/AppData/Local/Temp/brine-reactor-state-a153e399c5584f5bbf0bbc93115090a4`.
The reused test metadata retains its original native-scope wording; it does not
self-certify export. The executable invocation, PCK hash, external directory and
terminal logs above establish that these particular runs were exported.
Native negative controls remain recorded in the individual reviews; they were
not rerun in this package.

## Mixed station follow-up and retained failure

The helper's first runtime fails because this invocation omitted additional
manifests while requesting three crew. Its fixture correctly rejects the absence
of a real Cryo Chamber. Do not label the helper run successful or fabricate its
missing `verification.json`.

The same PCK is subsequently run with batch-two, whole-room, routing and
construction manifests in `output/reactor-state-exported-tour-v1`. It exits 0,
without engine/script errors, and reports:

- 45 scheduled arrivals/visited room instances, 124 reciprocal door transitions,
  and 9476 Bill collision/speed samples.
- Three active and progression-present architects after normal recovery/thaw
  entry points from the fixture's pre-repaired ward conditions.
- 29 selected source hashes, 58 raw PNG decodes, 42 component images and 26
  composition profile hashes/parses pass.

These are room instances, not 45 unique room identities. Destinations are
scheduled by the fixture; the route oracle samples Bill, not each architect's
continuous movement or every overlapping pixel. No full-set art acceptance is
inferred from the fitted overview.

Tour external working directory:
`C:/Users/Alex/AppData/Local/Temp/brine-reactor-tour-6984349dbc5e42338204c14181dcfd61`.

This closes the Reactor native-to-export state follow-up at 1600x900. Wider room
finishing, broader crew overlap and owner aesthetic review remain separate.

After packaging, the shared station fixture gained an Anomaly-tour branch. The
final bridge freshness check correctly failed its old station body/source hash.
Regenerating from the current source restores all seven checks without weakening
assertions. This does not change the already-tested PCK: its results describe the
packaged revision, not that later station-fixture addition.
