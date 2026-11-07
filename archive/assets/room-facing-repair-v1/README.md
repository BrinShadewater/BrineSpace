# Tidal south-facing repair — September 12, 2026

Engineering department; maintained matte slate steel and restrained brass. The
south-wall bank faces north, so the viewer sees its rear. V2 adds opaque vessel
jackets, a rear shield and service connectors to make that direction clearer.
This changes visible construction, not merely color. Other directions retain
their artwork. Original raster and previous registration are preserved.

Selected source: `tidal-south-v2.png` (2118×742, true alpha). Read-only alpha
registration at threshold 128 produced one component / five polygons, region
64,66,1987,628. No raster resampling or recoloring. Active binding:
`rooms/full-wall-v1/registrations/side-tidal-condensation-wall-south.json`.
The adjacent revision registration preserves source hash and provenance.

Reference/edit target: `assets/material-polish-v1/tidal-south.png`.
Built-in imagegen generated two candidates. V1 repeated the old facing cues and
increased shine; rejected and retained under
`output/room-facing-2026-09-12/tidal-rejected-v1.png`.

V2 exact prompt:

> Create a substantially corrected REAR-FACING companion view of this machine, preserving its wide shallow overhead pixel-art orthographic proportions and dark matte engineering palette. This is an EDIT target, but the exposed front surfaces MUST change. The viewer looks at the BACK of a machine whose operator stands on the far side. Replace the visible blue glass faces of ALL five vessels with opaque dark grey rear cylinder jackets and slim rear service pipes. Replace the exposed forward faces of the large left serpentine tubes with a matte structural back shield reaching about two thirds of their height; only the upper curved pipe shoulders peek above that shield. Across the nearest bottom edge show a solid rear equipment casing, quietly panelled, with two subtle recessed cable connectors and no handles, screens or controls. Vessel round top caps remain visible from overhead. Preserve width-to-height ratio approximately 3.1:1, three recognizable bays, low silhouette, straight horizontal base, same shallow overhead camera. Restrained brass joints, NO shiny edge highlights, NO bloom, NO text. Clearly different construction visibility from the provided front-like image. No floor. Single isolated sprite on true transparent background.

Native room review: south view has clearer rear construction and open circulation.
The slightly shallower silhouette follows the new source aspect ratio; saved
positions/scales and floor collision were not edited. Rotations 0,1,3 are
pixel-identical RGB comparisons. Current card uses unchanged rotation 0.
176 preferred-layout collision/route cases and side-wall regressions pass.
Agent visual review only; owner acceptance and packaged review remain pending.
