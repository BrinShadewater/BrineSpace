# Cryo ward master polish — September 30, 2026

Five polished, staged replacement masters: two broken human pods, occupied closed
pet pod, empty closed pet pod, and empty open pet pod. Refined matte ivory shells,
cleaner padding and bevels, readable light frost, centred sleeping Margot and dark
failed human indicators. The full glass door rises vertically on rails.

Selected original: `sources/master-v4.png`. Built-in image_gen produced a material
study and a targeted open-body geometry correction. Both originals and exact prompts
are preserved; `sources/provenance.json` records references and hashes. Previous
revision remains in `character/cryo-ward-master-v3`.

Rebuild: `python character/cryo-ward-master-v4/build.py`. Component extraction and
one fixed scale per family produce transparent 512px frames, floor pivot256,448,
standingHeight148 and linear sampling. Human height264px and pet closed height160px
retain the prior world scale:116.45 and70.57 units respectively. Raised door adds
height without shrinking the body. Closed occupied/empty exports share160px height
and differ by1px in total width. Open export is91px wide versus95px closed; generated
states are closer, but not pixel-identical construction.

Five-component, canvas-fit and transparent-corner packaging checks pass; Git LFS
covers rasters. Agent inspected the original, master board and selected Bill/Margot
scale comparison. These are static source reviews, not native gameplay evidence.
The accepted cryopod reference view is retained; no four-direction family is claimed.

For animation, derive a single authoritative chassis and separately registered
door from the closed-empty master. Do not crossfade these independent whole-pod
masters. Corrected runtime layering, startup/exit and found/repaired native review
remain the next integration work. This pass changes no runtime binding, save,
release, or gameplay; no Godot run or owner-save access. Owner visual acceptance
remains separate from packaging checks.
