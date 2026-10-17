# Character identity and tone consistency

September 27, 2026. Source integration complete; owner visual acceptance remains separate.

## Corrections installed

130 selected PNG paths changed. Veld's east head replacement cleared four extra rows of original collar, disconnecting the head. The source mask now preserves those existing authored rows. 34 byte-matched aliases were updated together across idle, kneel/sample/stand, interaction, seated endpoints and helmet fitting endpoints. Every previously visible pixel is unchanged; only the erased collar is restored. Feet, canvas and pivots stay fixed.

96 walk PNGs (Veld and Branforth, four directions, six poses, bare/equipped) use one fixed cloth-tone curve per character, pooled across all directions. The curves map the 10th/50th/90th luminance percentiles to canonical idle cloth and output only colours from the already locked neutral ramp. This corrects the lifted video-source shadows and midtones. Faces, hair, coloured markings, lamps, helmet heads, silhouettes and alpha are unchanged. No per-frame grading or adaptive palette is used. The curve and cutoff policy are saved in `curves.json`.

All original files and staged outputs are retained, with guarded before/after hashes in `mapping.json`. The seven palette JSON files themselves have not changed. This is deterministic source restoration and colour processing, using the owner's chosen pose-preserving method; no new image generation or invented inbetweens.

## Verification

- Four focused Python tests pass: source pixel preservation, collar connectivity/bounds, locked cloth shades, matching tone quantiles, exact helmet joins and action timing.
- `python tools/audit_character_colour_lock.py`: seven locked palettes, 8,575 PNG paths, 1,444 selected state variants, 8,343 distinct selected paths; zero unexpected changes. The larger PNG count includes retained/unselected files.
- Native real-loader review: 792 checks, zero failures. Every corrected body/equipment export is compared against its staged pixels, with representative source-game captures under `native/`. The isolated APPDATA run preserved every real profile file. The first probe failed because its expected-file path was joined twice; the corrected probe passed without changing game art or code.
- Local comparison viewer includes all 346 Veld/Branforth body states with current timing and pivot registration. Agent-reviewed collar and directional tone samples; this is not exhaustive visual acceptance of every legacy state.

## Continue or rebuild safely

`tools/prepare_veld_east_identity_chain.py` contains the corrected source mask. The existing complete character builder calls it. After a source rebake, apply the locked palette once from the unmapped source, then run `python tools/repair_crew_consistency.py install` for this frozen revision. It accepts only recorded before/after hashes and refuses unknown or intervening edits. Do not run `prepare` against installed art or reapply the tone curve. For newly authored walk sources, use the saved curve after palette mapping, the corresponding bare-pose collar cutoff, and a separate staged review; never silently accept them into the lock.

The old palette baseline is historical. Do not overwrite it or force its installer past manifest/hash guards. The current colour audit combines that original pass with this explicit correction record. Existing review generators now display current selections. Original helmet handoff hashes remain frozen, with the collar correction explicitly accounted for in the join fixture.

## Limits

A hash lock prevents accidental drift; it does not prove that every legacy drawing has matching anatomy or material placement. Existing Veld/Branforth walk source softness and the more cartoon-like Marsh work/swim drawings still need source-art work. No pixel-density change, new poses, gameplay change, full locker playtest or executable rebuild is claimed.
