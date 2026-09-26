# Mac release preparation

Owner test hardware: Apple Silicon (M1 or newer), confirmed September 20, 2026.
Current local candidate: brinespace-6600876d650b0d68 in
builds/BrineSpace-mac-stability-2026-09-23. Matching Windows actual-EXE checks
and both exact PCK audits pass (15,619 assets, zero discrepancies). Universal2
bundle checks pass; native Mac execution and Gatekeeper acceptance remain open.
Includes Continue-dialogue, open-empty human pod and hatch rendering repairs,
alongside previous crew, room, camera and audio work.
See [current build evidence](STABILITY_TEST_BUILDS_2026-09-23.md) and the candidate
README for the Apple Silicon checklist. Older entries below are revision-specific history.

## Baseline and build inputs

Use the selected Godot 4.7.2 editor and matching official templates. The old local
Windows templates were actually 4.6.1 despite their surrounding documentation;
actual release startup rejected the version-4 PCK. tools/export_release.ps1 now
checks the template's own --version before building. Verified 4.7.2 Windows and
Mac templates are in output/export-tools/4.7.2-stable; preserve the downloaded
bundle and SHA512-SUMS.txt or restore them from the official release assets.

The current Windows validation must pass packaged-file audit and actual-release
New Game/simulation/F8 checks before promoting a Mac candidate. The manifest path
case audit found no tracked collisions or mismatched reference casing; this is
static evidence, not proof of behavior on a case-sensitive Mac filesystem.

## Planned Mac candidate

Use official Universal 2 templates for an app bundle supporting Apple Silicon and
Intel. First native testing will be on the owner's Apple Silicon Mac; Intel remains
unverified until tested. Add a separate macOS preset with the same runtime dependency
selection and raw-PNG exporter. Keep validation flags out of the playable preset.
Do not inherit the Windows icon, template paths or executable/PCK layout blindly.
The manifest builder now accepts `--preset` with an exact preset name (default:
`Windows Game`). It rejects missing or duplicate names before writing metadata.
Regression coverage verifies that selecting a Mac preset preserves the Windows
preset and platform-specific options. Five manifest checks and two release
assertion-safety checks pass.

September 21 implementation: `macOS Game` is now preset 4, using the verified
custom template, Universal 2, testing distribution and built-in ad-hoc signing.
Notarization is disabled for this local candidate. `project.godot` enables
`textures/vram_compression/import_etc2_astc`; the first export demonstrated that
Godot rejects Universal/arm64 without it, even with the Compatibility renderer.
The initial log also reports the absent default template path, but source inspection
confirms custom template existence supersedes that check; do not replace a verified
custom template merely because the combined configuration diagnostic includes it.

`tools/audit_macos_bundle.py` inspects bundle metadata, both Mach-O architectures,
executable ZIP permissions, a single PCK and absence of QA overrides. This does not
certify native execution or signature validity. Export evidence is in
`output/mac-release-2026-09-20`; the retry completed successfully September 21.
Candidate source ID: `brinespace-97c09d09887b0d5b`. Bundle audit confirms arm64 and
x86_64, mode 100755, one PCK and no QA override. Exact PCK audit: 15,085 checked,
zero missing, changed or unexpected files. No export errors or warnings.
Deliverable directory: `builds/BrineSpace-mac-2026-09-20`, containing the ZIP,
README test instructions, NOTICE, build_info and SHA256SUMS. Native Mac testing,
signature acceptance and notarization remain unverified. No public upload occurred.
The new repeat-build wrapper `tools/export_macos.py` is syntax checked but was
added after this candidate; its complete export invocation has not yet been exercised.
Its real `--preflight-only` invocation now passes, including the selected preset's
actual template hash, official archive SHA512 and editor version. Two focused
selection tests pass. No replacement ZIP was needed for this preflight correction.

## Acceptance on Apple Silicon

Test a clean install's title/New Game/dialogue/Resume path, station visibility,
room placement and rotations, Bill/crew animations, drones, environment lighting,
save/relaunch/continue, settings/fullscreen, audio, keyboard shortcuts, trackpad zoom,
and F8 report creation. Check write permissions and keep QA saves separate from the
owner's profile. Record macOS version, hardware, build fingerprint, frame behavior
and screenshots. Windows or headless checks cannot certify this lane.

Then verify distribution signing/notarization for the intended download channel,
with credentials supplied through the normal local tooling. Do not publish a
candidate or request account secrets in chat. Owner visual acceptance, known Bill
motion work and broader room decoration remain separate from launch compatibility.

## References

Godot documents Universal 2 app bundles and signing/notarization routes in
[Exporting for macOS](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_macos.html).
Templates: [official 4.7.2 release](https://github.com/godotengine/godot-builds/releases/tag/4.7.2-stable).
Project procedure: [RELEASE_WORKFLOW.md](RELEASE_WORKFLOW.md).

September 21 replacement: the maintained wrapper now completed a full export of
brinespace-e7c1ea935b573fd2, matching the verified Windows source fingerprint.
Candidate: builds/BrineSpace-mac-layout-turns-2026-09-21. Both architectures,
permissions and absence of QA overrides pass; exact PCK checks 15,146 assets with
zero discrepancies. The earlier wrapper-not-exercised note applies only to the
older candidate. Native Apple Silicon testing remains open. See
MAC_LAYOUT_TURNS_HANDOFF_2026-09-21.md and the candidate README.

Latest September21 candidate: builds/BrineSpace-mac-limb-polish-2026-09-21, build1e25ea27901c0eae, matches Windows and includes Bill/Battery/restore updates. Export, Universal2 structure and exact15149assetPCK audit pass. Native hardware checklist remains open. See MAC_LIMB_RELEASE_HANDOFF_2026-09-21.md.
