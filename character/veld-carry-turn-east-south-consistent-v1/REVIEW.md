# Project handoff

Updated: 2026-09-30. Project: BrineSpace. Task: Veld east/south cargo turns.

## Objective and acceptance
North pickup derived-v1 accepted and installed. First cargo turn pair,
east-south and south-east pivot-v2, owner accepted and installed on2026-09-30.

## Accepted decisions and constraints
Accepted directional carry masters define anatomy, materials and equipment.
Connected pivot with continuous two-hand case grip. Exact accepted carry frame
zero endpoints, matching the runtime destination frame-zero handoff. Original
800ms nonloop timing, facings, dry cargo metadata, canvas256, pivot128/224 and
standing height148 retained. Opposite direction reverses the same authored turn;
no equipment mirroring. Review GIF timing is independent of runtime.

## Current state
Built-in imagegen source-v1/prompt-v1 preserved; source-v2/prompt-v2 correct the
first draft's repeated side views. build.py slices6x2 source, registers boot
contact, uses one pooled neutral material curve per variant and retains face/hair
contrast. Four intermediate poses per variant; exact accepted endpoint pixels.
24 frames, two manifests, four GIFs, contact/native/browser preview and provenance
checks saved. Loader and ACTIVE_ASSETS select this accepted turn pair in both variants.

## Verification
102 packaging checks pass: original metadata, clipping, decoded GIF exteriors,
exact endpoint pixels and reverse equality. 123 candidate native checks pass,
including both equipment variants and runtime transition/destination handoff.
Source/contact/native reviewed visually. All probes used scratch APPDATA.
Installed north pickup separately passed59 actual-selection checks; real profile
unchanged in that interval. Turn interval real profile changes: three log files
and power_demand_ui.meta; attribution unknown, no restoration attempted.
Owner accepted. Installed selection passed123 native checks including runtime handoff,
with scratch APPDATA; profile delta details in native-installed-v1-checks.json.

## Next action
Acceptance complete. Next bounded continuation is another adjacent
direction pair; remaining north/east, north/west, south/west and180-degree turns
remain unchanged. No commit, push or export.
