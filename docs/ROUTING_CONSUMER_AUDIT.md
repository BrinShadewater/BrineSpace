# Routing consumer follow-up

Corridor and Corner use the procedural underwater geometry and surface module.
Their card catalog and base textures already selected v3 cards, but grid fallback
variant arrays retained six and nine older images. Both arrays now select only
the current card; random variant counts are one. Original art files are retained.

`tests/test_corridor_detail_bounds.gd` passes: 388 fitting corners contained in
the hull and clear of socket approaches. Logs: `output/routing-consumers`.
This check covers existing detail geometry, not new native visual acceptance.

`rooms/underwater/routing-export-manifest.json` records both source hashes and
cards for the combined export fixture. Its `render_module` is a surface helper,
not an instantiable room view. Do not feed it to view-based walker fixtures.
Combined export verification with this added manifest remains outstanding.

Follow-up completed in `output/room-rollout/windows-33-current-controller-v1`:
33 source hashes, 66 PNG decodes and all 50 physical tour arrivals pass using
Bill's current controller. See the combined controller export report for scope.
