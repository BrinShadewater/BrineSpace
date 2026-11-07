# Layered room pilot: first components

The floor and growth rack are separate imagegen outputs, not a complete room.
They do not increase the 34-identity room count or replace a live texture.

## Observed results

- Floor: opaque RGB, 1254 square; no baked machinery or walls. Panel scale is
  coarser than the source room and cross-room repetition seams are untested.
- Rack: RGBA, 1254 square, exterior sample (10,10) is transparent. Main subject
  remains in the upper-left, but it grew and shifted relative to the source.
  Full nonzero-alpha bounds extend to (1194,1228), beyond the visible rack.
  Investigate faint residual pixels before treating its bounding box as geometry.
- Neither layer was cropped, resized or normalized. This preserves the supplied
  source canvas rather than silently changing placement again.

Floor SHA-256: 963d236cf48202526039fd3d8785270ef8606a9ba1997031740e73ba85139123

Rack SHA-256: 2a9359c3561cfc5f53fee7d785e8c735e34321dbc9f5822b43718df7884ae015

## Next assembly contract

Use the clean floor beneath extracted props; do not draw the original complete
room beneath the rack, which would leave duplicate machinery. Register each prop
with an explicit source rectangle, room-local placement, ground/depth anchor,
solid footprint, and approach/work point. Visual bounds, solid footprint and
depth anchor are different data, not three names for the alpha bounding box.

Inspect near/far character overlap using the actual walker sprite, then add the
irrigation effect attached to the rack. Test all room rotations with directional
prop artwork; rotating this single cutaway rack image is not sufficient.

Shared walls and measured door sockets remain required. The floor candidate is
not yet a seamless tileset. These component assets establish the extraction path,
not a claim that the inhabited-room prototype is implemented.
