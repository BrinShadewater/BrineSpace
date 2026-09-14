# archive/

Asset batches that nothing in the runtime loads: superseded passes, review sheets,
candidate frames and generation sources kept for provenance. The folder carries a
`.gdignore` so the Godot editor does not scan or import it, and the paths below it
mirror where each batch used to live (`archive/assets/...`, `archive/character/...`).

`python tools/live_asset_manifest.py` regenerates `docs/ASSET_MANIFEST.md`; a batch
belongs here only when that manifest reports it fully unreferenced.
