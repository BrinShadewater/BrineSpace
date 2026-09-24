# Mac limb polish release handoff

Updated: September21,2026. Project: BrineSpace.

## Objective and acceptance
Prepare the current build for Apple Silicon testing. Export and static bundle/PCK verification complete; native Mac execution and distribution acceptance remain open. Broader game-polish goal unfinished.

## Accepted decisions and constraints
No upload/publication or Higgsfield. Preserve earlier builds and owner profiles. Apple Silicon is the owner's available test hardware.

## Current state
builds/BrineSpace-mac-limb-polish-2026-09-21 contains BrineSpace.zip, expected manifest, build_info, SHA256SUMS, README/checklist, NOTICE and validation.txt. Build brinespace-1e25ea27901c0eae matches the verified Windows source SHA256 exactly. Includes Bill limb surfaces, Battery furnishing and companion restore texture reuse.

## Verification
Maintained tools/export_macos.py completed after official template SHA512/version/template checks. ZIP contains arm64+x86_64 executable with100755permissions, one PCK and no QA override. Extracted PCK exact audit passes15149assets with zero missing/changed/remapped/unexpected. Evidence: output/mac-limb-validation-2026-09-21. Native Mac execution remains false; Windows startup evidence is not Mac evidence. Local ad-hoc test build, not notarized or publicly distributed.

## Next action
Native Apple Silicon launch/NewGame/placement/animations/save-Continue/settings/audio/F8 checks using the included README. Record hardware, macOS version, build ID and any launch refusal verbatim. Continue independent room and gameplay polish while that hardware evidence is pending.
