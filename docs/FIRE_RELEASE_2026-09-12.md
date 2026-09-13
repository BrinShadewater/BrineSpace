# Fire systems playable release

Build: brinespace-f04642316baa2ca3
Deliverable: builds/BrineSpace-fire-20260912/BrineSpace.exe and adjacent PCK.
Source fingerprint: f04642316baa2ca36b4214c9173b12a0f96d85d454a8a31c33ad9b127188144f
Base commit: b2648fea378f3d8a5237e554ae2179e43ffb556c plus frozen working changes.

## Scope

Includes fire/electrical warnings, crew wiring repair, authored flame/smoke/ember/
spark atlases, sprinkler fans and status feedback. Current selected room and
character bindings were frozen alongside these systems; no unfinished alternate
art selection was introduced. Runtime snapshot is output/fire-release-20260912/source.
Existing builds remain intact. No commit, publication or upload performed.

## Verification

Maintained exporter completed without errors. Build contains 10,186 manifest
files. Empty-project PCK audit: 9,902 assets checked, zero missing or changed.
Release manifest and assertion-safety Python checks passed (two each).
Actual release EXE, isolated user directory: New Game, simulation, F8 reporting,
four effect atlas loads, warning capture, sprinkler activation, power-loss status
and extinction passed with zero failures and debug=false. Actual release native
captures reviewed. Full expedition balancing remains outside this smoke test.

Evidence: output/fire-release-20260912/actual-release-final.log, pack-audit.log,
release-game.png, release-electrical-warning.png, release-fire-sprinklers.png.
Temporary override was used only in the separate QA copy and then disabled;
the deliverable never contained an override. Normal play uses prototype saves.

## Delivery

README.txt, NOTICE.md, build_info.json and SHA256SUMS.txt accompany EXE/PCK.
EXE SHA256: 1197d6631dc15835e481693156628250473be00af8ce1bfe092aaee036df88a7
PCK SHA256: 63c4536a13884ac4dd01478ea0cef273765f9947a880cf4c60f160b5f92d9545

Next: owner playtest. Later source changes do not alter or inherit this build's
verification. Preserve this package identity when reporting issues.
