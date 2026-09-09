# Crew blowtorch construction pack

Three architects, four directions each, six frames per loop: 12 clips / 72 transparent PNG frames. Runtime state is `weld`; each loop lasts 0.96 seconds. Existing 92x92 canvas, (46,86) foot pivot and 74-pixel standing height are retained. No opposite views are mirrored. Raw PNG loading is integrated in the station renderer.

## Sources and rebuild

`source/` preserves four generated sheets and their exact prompts. Bill's original north/south rows aimed sideways and are rejected; `bill-direction-v2.png` supplies only those two replacement rows. Original east/west rows remain selected. Veld and Branforth use their respective complete sheets. Existing `final/idle-east-strip.png` files in major-bill-v2, dr-veld-v1 and chief-engineer-branforth-v1 supplied identity references; Veld's new sheet additionally guided directional tool aim for Branforth and Bill's correction.

Run `python character/crew-construction-v1/build_pack.py` from the project root. The builder removes magenta, finds source row bands, scales using the dark body height, and registers the boots. It does not generate poses or mirror frames. Source colors are retained rather than forcing the earlier pack's 64-color palette. Each actor directory contains its manifest with source hashes and timing, 24 frames, contact sheet and four-direction GIF preview. Existing source packs are untouched.

## Review and integration

All three generic sprite-manifest validations pass with no warnings. Packaging checks confirm alpha, nonempty frames and unclipped bounds. Agent contact-sheet review confirms identities, directional tool aim and planted feet. Native tests cover all twelve actor/connection combinations, with stage screenshots in `output/crew-construction/`; the east Bill construction has a 100-sample native preview. Body movement is deliberately restrained, with the hand/tool and flame doing most of the motion.

This first playable pass switches between the existing walk/idle and the new welding loop. Separate tool-draw/holster transition sheets and helmet-equipped welding are not supplied. Manual construction uses a dry, unhelmeted architect. This is agent-reviewed prototype art, not owner visual acceptance.

PNG/GIF assets are covered by the repository's existing Git LFS attributes. No commit, push or exported playtest package was created.
