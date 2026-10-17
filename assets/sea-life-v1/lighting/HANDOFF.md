# Project handoff

Updated: September 29, 2026 · Project: BrineSpace · Task: lighting art style pass

## Objective and acceptance
Deliver the lighting sprites from Claude's five-batch handoff in the current
matte, fine pixel-scale style, with reproducible sources and native visual review.

## Accepted decisions and constraints
Warm/cool lamps preserve the exact original Bayer bands, runtime tint, brightness
and 0.30 alpha. Hull bubble positions, radii, fade, visual clock and quality counts
remain unchanged. Beacon rotation/orbit/pulse rates remain unchanged. Caustics use
the existing clock times motion and existing color/strength. Wide pool and three
shaft studies remain review-only pending owner selection. All installed art has
validated raw loading and procedural fallback; no gameplay change or new species.

## Current state
User requested style, color and pixel-density refinement. Six lighting PNGs
revised: quieter broad painted caustics from built-in imagegen, subtly irregular
three shaft studies and bubble rims, fine beacon dithering. Both lamp halos and
wide pool remain exact. All pivots, raster sizes, runtime colors and motion remain
unchanged. No code or fauna art changed this pass. Sea-life appearance/density
reviewed and retained; small fauna are approximately 0.7-1.5 world units per pixel,
ribbon 0.927, distant tidewalker 4.049 (existing exception). Optical caustic field
is 4.5 world units per texel, sampled linearly. Lamp Bayer clusters span 2.188
world units (correcting the earlier rounded two-unit description).
Before-pass rasters, provenance/bake and native captures are preserved in
review/before-style-20260929. New source: sources/caustics-painted-v2.png.
Exact edit prompt, style-audit.json, style-pass.jpg and reproducible review builder
record the pass. Runtime manifest refreshed and all five shipped hashes match.

Nine PNGs plus two preserved generated caustic sources, exact prompts/algorithms,
manifest, deterministic bake, raster validator, contact sheet, HTML review and
20 native captures in this folder. Runtime wiring: scripts/lighting_art.gd,
station_effects.gd, underwater_visibility.gd, underwater_fog.gdshader and
rooms/whole-room/room_lighting.gd. Three paired-UID test scripts and isolated runner
tools/check_lighting_art.py. Shared release manifest/preset/build metadata rebuilt.
The release ships exactly five lighting PNGs with matching hashes; source, shaft,
wide-pool and review files are excluded. Raw import roles refreshed.

## Verification
Style revision: 46 raster checks and 22 runtime checks pass; native isolated
fixture freeze and full-game comparisons pass and were visually reviewed.
Owner profile unchanged: output/lighting-20260929-194654. Twenty captures refreshed.
Only the raster/bake changed; previous quality/emergency/reliability evidence below
is from the original integration revision. No release executable/PCK tested.

Raster: 46 checks, including boundaries, exact repeat seams, hashes and identical
rebake. Godot lighting art: 22 checks, including halo pixel equality, fallback,
bubble freeze/counts and Low/Reduced Motion. Effects quality, light emergency and
reliability pass. Native fixture and full station captures pass and were visually
reviewed. Owner save-folder fingerprints unchanged on all three completed gate
runs: output/lighting-20260929-192359, -192432 and -192739.
Native fixture rendered-byte freeze passes. No release executable/PCK was tested.

## Next action
Session closed on codex/sea-life-art-closeout; lighting integration and preserved
studies are included. Procedural shafts remain active until owner selection.
Cards and the final frame are complete; the next batch is screen-effect maps,
only when requested. See docs/ART_SESSION_CLOSEOUT_2026-09-29.md.
