# Matching open-empty cryopod handoff

Updated: September 23, 2026. Project: BrineSpace.

## Objective and acceptance

Remove the open-to-closed image snap at human crew release. Installed human pods
now remain open after their occupant leaves. Veld's paid recovery and native
pause/Continue checks pass; owner motion acceptance and packaged checks remain open.

## Accepted decisions and constraints

A spent human pod remains open; no closing timer or new gameplay/save field.
Keep the existing thaw duration, final1.2second exit sequence, release positions,
crew identity and owner layouts. Marsh's separate charging pod is unchanged.
Built-in image generation was used, not Higgsfield. No commit or publication.

## Current state

- `character/cryo-open-study-2026-09-23/` preserves the generated empty-open source,
  exact edit prompt, selected reference and build hashes/repair recipe. The edit
  removes Veld and reconstructs the concealed padding and front hardware.
- `tools/build_cryo_open_pods.py` reproduces Bill/Veld/Branforth's empty poses.
  Each retains its original wake5 canvas and visible housing/lid outside the
  central repair bounds (108,250)-(307,608). A12px margin blends the reconstructed
  interior; all former occupant pixels are replaced. The initial tight polygon
  left outline fragments and was widened before acceptance.
- Three418x627 runtime PNGs: `assets/material-polish-cryo-open-v1/`.
  Raw generation and existing occupied frames remain preserved; raster LFS applies.
- `scripts/architect_cryo_art.gd` caches matching empty poses and draws them with
  the same anchor/scale as occupied exit frames. It no longer substitutes the
  unrelated closed equipment crop when `recovered` becomes true.
- `tests/test_cryo_exit_timing.gd` also checks matching canvas, exact upper-housing
  and lid pixels, cleared former boot space and stable texture reuse.

## Verification

- Three runtime PNGs rebuild byte-exactly. Alpha bounds contain no leftover boots
  below the pod. The release dependency collector selects all three PNGs and none
  of the new authoring study. Existing package metadata was not regenerated.
- Cryo exit timing/art checks and architect recovery regression pass.
- Native pause/Continue: rendered pod-region pixels remain exactly equal while
  paused and after disk restoration. Crew remains released; no extra clock is used.
- Same paid-recovery scenario as the preceding review: normal production funds
  the eight-Metal repair, Veld thaws, joins and departs.120second native run reaches
  cycle14/eight rooms,90 captures, zero failures or captured engine/script errors.
  The final capture shows the empty open pod behind the walking character.
- Agent inspected the rebuilt sprites, restored room and live post-exit view.
  Veld is the complete gameplay sequence reviewed here; the other two variants
  have shared-renderer and asset checks, not new paid gameplay journeys.
- Release assertion-safety checks:2 passing. Manifest regression:8 passing.
  No full executable export or native Mac run. Existing test downloads predate
  this change and the preceding Continue-dialogue repair.
- Evidence: `output/cryo-open-handoff-2026-09-23/`: `asset-check.json`, `timing.log`,
  `architect-recovery.log`, `pause-restore.log`, `recovery/native.log`,
  `recovery/motion.json`, `restored.png`, `veld-thaw.gif` and the frozen two-crew save.
  GIF preserves sampled timing with a600ms ending hold; its repeat is presentation.

## Next action

Continue natural two-crew activity/room review from a disposable copy of the saved
expedition. Include open-pod art and Continue-dialogue repair in the next maintained
Windows/Mac export. Owner listening/motion review and Apple Silicon testing remain
separate from these checks. Rebuild this art with `python tools/build_cryo_open_pods.py`.
