# Desalination matching machinery — October 19, 2026

The owner requested recolouring the remaining props to match the accepted
blue-green membrane machine. Filter vessels, intake pump, water-quality console
and spare-cartridge bank now use matching muted matte painted finishes. Steel
vessel bodies, dark pipework, charcoal panels and functional display colours
remain distinct. Floor, clinical shell, service details and gameplay are unchanged.

The built-in image generator made four separate edits, using each original prop
as the edit target and the accepted membrane skid only as a paint/style reference.
Raw images, exact prompts, source hashes, dimensions, normalization and 23 alpha
probes are recorded in `assets/desalination-unit-v1/matching-props.provenance.json`.
These are generated siblings, not pixel-identical recolouring. All four shared
green originals and the accepted membrane sprite are retained unchanged.

Game-size exports keep the original source canvases: vessels **317×325**, pump
**276×288**, console **331×232**, cartridges **294×281**. Godot crops around all
alpha >4 with padding, aspect-fits using Lanczos and pads into those canvases.
Display widths, collision metadata and all five prop positions remain the same.
Three Desalination-only registrations were added; the existing Desalination
cartridge registration now points to its own matching sprite. Other registrations
and other rooms' layouts remain unchanged. Only this room's four layout keys and
its floor-detail host reference were updated.

Native run `output/test-runs/20261019-143756-native` passes **139 checks /0 failures**:
actual paid architect construction, production, suspension/resume, staged
Save/Continue, all four real crew routes, five live props and actual Studio
rotations. Scoped layout lint: four orientations, zero findings. One card rebaked.
Agent visual review covers native station, Studio, four orientations and the card;
owner visual acceptance remains separate.

Current previews: [Studio](../output/desalination-matching-props-20261019/studio.png),
[four orientations](../output/desalination-matching-props-20261019/orientations.png),
[station](../output/desalination-matching-props-20261019/station.png),
[card](../assets/new-room-cards/desalination_unit.png). Earlier art-stage captures
and receipts are preserved in their original task directories.

All test/export helpers use isolated APPDATA. Gameplay and selected-filter source
hashes remain unchanged; the owner game was left running. Full preservation
results and source hashes are in `output/desalination-matching-props-20261019/FINAL.json`
and `HANDOFF.md`. No new release export, signing, upload, publication, general
performance or platform acceptance. Human visual/pacing review and relevant new
package validation remain separate.
