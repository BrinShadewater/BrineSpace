# Hazard systems playable release

Updated: 2026-09-12. Project: BrineSpace.

## Objective and accepted decisions
Owner approved hazard sounds, the combined fire/flood/repair test and a rebuilt playable version; nozzle artwork was explicitly skipped.

## Current state
Deliverable: builds/BrineSpace-hazards-20260912/BrineSpace.exe and adjacent PCK, README.txt, NOTICE.md, build_info.json and SHA256SUMS.txt. Existing fire build remains preserved. Current selected runtime room and character bindings were frozen alongside hazard changes, including currently selected derelict condition art. No alternate art selection, commit or upload was made.
Snapshot: output/hazard-release-20260912/source. Build ID: brinespace-dc4e1877474c8d84.
Source SHA256: dc4e1877474c8d844a05836bcd3d637c137caa15a1f20cdab0cc2adcdfa016ca.
Base commit: b2648fea378f3d8a5237e554ae2179e43ffb556c plus frozen working changes. Manifest: 10,197 files, 1,193,637,036 source bytes.

## Verification
Maintained Windows exporter passed. Empty-project PCK audit: 9,910 assets checked, zero missing/changed. Actual release EXE ran with debug=false and zero failures for New Game, simulation, F8 report, fire atlases, sprinkler activation/power-loss/extinction, authored hull atlas and hazard PCM/playback state. Native release startup and hull patch captures visually reviewed. Logs: output/hazard-release-20260912/pack-audit.log and actual-release-engine.log.
Source headless/native combined hazard sequence and existing audio regression passed; see HAZARD_AUDIO_2026-09-12.md for exact scope. Full crew repair sequence was tested against source; the actual-release smoke covers loaders and hazard state rather than replaying that whole sequence.
Temporary autoload existed only in isolated QA copy and is now override.cfg.disabled. Delivered directory never contained it. Test userdata: C:/Users/Alex/AppData/Roaming/BrineSpaceHazardRelease20260912.

Hashes:
```
1197d6631dc15835e481693156628250473be00af8ce1bfe092aaee036df88a7  BrineSpace.exe
0db9e207ce14d9488d312eca57ba6e023c51cc4f38621909de58f02758516dd4  BrineSpace.pck
1533082c83bac25b00dfaeca0d6f6328084e8f51f76750d32edff580dc445bab  build_info.json
2e9140653e1a9bcae96d89a736f44bbe2e520fe208ae301d9697d2626e6ebd10  README.txt
03301c6c5a25372c1867822237b54349994d147745a18e57e9be9ec5e07d27eb  NOTICE.md
```

## Next action
Owner playtest for subjective sound levels and expedition pacing. Further edits do not alter or inherit this frozen package acceptance.
