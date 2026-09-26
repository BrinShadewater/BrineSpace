# Limb polish Windows release handoff

Updated: September21,2026. Project: BrineSpace.

## Objective and acceptance
Provide current animation, room and restore work in a playable test build. Windows export/startup/report gates pass. Broader gameplay and owner visual acceptance remain open; Mac refresh is next.

## Accepted decisions and constraints
No publication or Higgsfield. Preserve prior builds and owner profiles/layouts. Mac target includes Apple Silicon hardware available to the owner.

## Current state
builds/BrineSpace-limb-polish-2026-09-21 contains EXE/PCK, build_info, expected manifest, SHA256SUMS, README and NOTICE. Build brinespace-1e25ea27901c0eae; source SHA2561e25ea27901c0eaec93421c22a838b790dfef14a1cbf82e97cd7032673c5a312. Includes current Bill limb repair, Battery furnishing and companion restore optimization. No override in deliverable.

## Verification
Maintained Windows export exits0. Exact-PCK audit:15149checked, zero missing/changed/remapped/unexpected. Actual release smoke exits0 with debug=false, zero failures and no logged engine errors, exercising normal startup/New Game/dialogue/Resume/simulation/F8. Gameplay/report screenshots inspected and copied to output/limb-release-validation-2026-09-21 alongside logs. Runtime override is confined to an isolated hardlinked test folder and unique app profile. This startup smoke does not prove a full expedition or gait acceptance.

## Next action
Export matching Mac via tools/export_macos.py, compare source fingerprint and exact PCK, then provide it for native Apple Silicon testing. The older Mac build predates the current changes. Continue visual/gameplay polish from owner feedback; broad goal unfinished.
