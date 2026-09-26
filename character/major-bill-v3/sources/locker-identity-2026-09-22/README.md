# Bill locker identity source

Built-in image generation, September 22, 2026. Exact prompt: prompt.txt.
generated-source.png is preserved unchanged; registration.json freezes its hash,
cell extraction, one scale, placement and 12-frame action ordering.

Canonical reconstruction: tools/build_bill_locker_identity.py, called by
tools/rebuild_bill_art.py. It receives current canonical bare/equipped idle frames,
preserves their exact padded endpoints and produces precomposed body action rows.
Bill's helmet-action renderer selects those rows before ordinary equipment logic.
Existing event timestamps and frame durations remain in the original manifests.

build_study.py is the historical study extractor. It writes output-only previews;
the canonical helper is the installed pipeline. No generation is required to rebuild.
See docs/BILL_LOCKER_IDENTITY_INTEGRATION_2026-09-22.md for current verification.
