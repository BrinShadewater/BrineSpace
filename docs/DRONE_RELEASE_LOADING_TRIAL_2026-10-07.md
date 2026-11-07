# Drone release loading and package trial

Updated: October 7, 2026 · Project: BrineSpace · Task: performance and release readiness

## Objective and acceptance

Verify the lossless drone integration in actual debug=false Windows packaging. Resolve cold-loading warnings and account for every selected package dependency before admission. Preserve responsive loading, pixels, timing, normal crew/flood behavior and the original PC/Mac release gates.

## Accepted decisions and constraints

Experimental exports only; no publication or normal checkout admission. Use the maintained exporter, matched 4.7.2 templates, isolated profiles and a physical source selection. Keep the accepted Windows package and original frozen inputs unchanged. No synchronous production loading workaround or engine upgrade accepted.

## Current state

Evidence: `output/drone-compiled-2026-10-07/`. Physically copied the accepted baseline's 36,651 inputs into `C:/Users/Alex/AppData/Local/Temp/bs-drone-compiled-5qazhm_g`; checked baseline hashes (export preset metadata excepted) and nonempty Git index equality to HEAD. Initial experimental selection has 36,698 inputs, including 32 encoded PNGs and relocated whole runtime paths. Main's reviewed diff is only the Grid script path; crew and flood code stay normal. Palette default enabled explicitly in the private frozen Grid, without gameplay validation features.

First **parallel-script** package: `brinespace-6effc70a62952305`, source SHA256 `6effc70a62952305f8a0b308b5a165c9bf418b4c5cc5c8c7fe7647dbb6ab380f`; EXE 109,283,328 bytes / PCK 3,647,293,175 bytes. Maintained export clean. Runtime selection 36,289 files / 3,617,173,729 source bytes. Ten new scripts and four shaders have paired unique UIDs, with no copied-baseline UID collisions (initial expectation of fourteen **scripts** was corrected to ten scripts plus four shaders).

The maintained Windows preset uses `script_export_mode=0`. Actual QA confirms raw Main script available in this PCK. This is an actual compiled **release executable**, not a binary-token script export. Godot distinguishes text, binary tokens and compressed binary tokens in its [export preset documentation](https://docs.godotengine.org/en/stable/classes/class_editorexportpreset.html). No token-mode change has been made.

## Verification

Outside-checkout maintained raw asset audit: 35,811 checked, zero missing/changed/remapped/unexpected. A deliberately broader private audit additionally checks scripts, shaders, scenes, fonts and audio. It finds 36,287 checked, zero missing/changed, 55 loadable remaps, **two unexpected originals**: `res://scripts/main.gd` and `res://scripts/grid_canvas.gd`. No selected text/resource source explicitly references those originals in the parallel candidate. The first package is therefore **not accepted as a full dependency audit pass**. Logs/failure evidence preserved; no silent allowlist added.

Actual debug=false QA copy, new isolated profile/process per lane, **load only, no instantiation/gameplay**:

- Threaded scene loading: 1.333 seconds, 38 RefCounted exit leaks / one warning.
- Synchronous scene loading: 1.348 seconds, zero leaks/warnings.

Thus the cold-loading warning also affects the actual text-script release runtime; the editor-only explanation is rejected. These times exclude application bootstrap, required art/crew readiness and dialogue; disk cache is uncontrolled. No loading gate or FPS/memory certification follows.

All completed runs preserve all 2936 owner files. QA overrides reside only beside a physical package copy. Previous normal release remains untouched.

## Next action

A second **in-place frozen** candidate is building: restore Main/title to the accepted original bytes, put experimental Grid at `res://scripts/grid_canvas.gd`, retain eight provider scripts/four shaders at their trial paths. This matches the intended release integration rather than carrying duplicate Main/Grid identities. Archive the five parallel source/UID/scene files outside the frozen project; resolved individual paths were checked inside the intended freeze before moving. Neither owner checkout nor accepted source snapshot is changed. `inplace-source.json` records the changes; first package/QA/evidence are preserved.

Native export plus broad package audit is live under unified session **37956**. Latest manifest identifies `brinespace-7a35d34088274fba`, SHA256 `7a35d34088274fba739cb974e749286708d1f304ee0f77eb8d61deea208030cc`; no successful second-package completion claim yet. Poll this handle and inspect terminal status; never restart on an observation timeout. After success, run `prepare-qa-inplace.py` then `run-load-inplace.py` for the actual normal-path cold loader. If warnings remain, test a separately preserved binary-token or minimal loader remedy, with behavioral checks and responsive loading acceptance before admission.

The broader private audit now includes selected `.txt` notices as well. Finish actual packaged lifecycle and matched station measurements after clean loading/package evidence. Full frame/memory/loading/original bugs/endurance/target hardware/Mac requirements remain open. No itch upload.
