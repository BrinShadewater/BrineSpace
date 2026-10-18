# Native Apple Validation Plan

**Goal:** Validate the reconciled integration on native Mac and a separate physical-iPad QA app without changing frozen builds or player data.
**Architecture:** Separate worktree at integration585111ca3; external evidence and generated QA overrides. No gameplay changes planned. Maintained exporters and matching official Godot4.7.2 templates.
**Spec:** User pasted request, retained locally in /Users/Shared/BrineSpace-native-validation-evidence-20261017/request.txt.

## Constraints / review focus
- Preserve integration branch and all original sources/installations/profiles; fingerprint before/after.
- Prove actual user directory before writes; restored checkpoints must be scratch copies.
- Distinct iPad bundle/container; no overwrite of existing QA app.
- Loading ordering, tablet guards, retained-frame leases, native renderer, release assertions and packaging are independent gates.
- Retain outliers; synthetic input, scoped fixtures, Mac RSS and physical-device results are distinct evidence.

## Tasks
- [x] Inventory original checkout and create validation worktree at exact requested tip; verify complete index and hydrate only integration LFS.
- [x] Fingerprint protected artifacts/profiles; review guidance/delta/runner; establish side-effect-free native isolation guard.
- [x] Run focused source headless/native/Python lanes; record failures and affected reruns.
- [x] Export fresh maintained Mac candidate, audit bytes/signature; run actual release journey and native interaction/rendering checks with verified scratch profile.
- [x] Build fresh isolated Mac parent where storage permits; balanced native loading/placement/zoom/memory comparison with no competing work.
- [ ] **PENDING physical gameplay/endurance:** Separate Release app installed; fresh identity/container verified and intro smoke passed. Still require physical-renderer lifecycle/input/compact/extended workload and whole-process memory capture.
- [x] Recheck protected files, produce scoped PASS/FAIL/BLOCKED handoff and portable evidence, commit/push validation branch only.

## Outcome

See ../../MAC_IPAD_NATIVE_VALIDATION_HANDOFF_2026-10-17.md. Parent comparison used fresh source/editor rather than a second exported app due storage. Physical lane blocked; one original diagnostic breadcrumb changed (preservation exception). No production code fixes. Publication checked separately at commit/push.

## Physical installation continuation

Owner closed the old app and authorized separate installation. Maintained Release build installed as com.shadewater.brinespace.nativevalidation20261017; empty Documents verified before launch, guarded intro smoke passed, old app Documents47/47 SHA256 unchanged. Initial signal9 during unsuccessful debugger check retained separately; no physical memory acceptance. Touch/gameplay/endurance remains pending owner testing. See native handoff and ipad-install evidence.

## Physical acceptance and bounded stress continuation

Owner confirms New/Save/Continue, pinch/pan/two-finger rotation/card return/Codex scroll and paused/intact resume. Separate stress app completed40→43rooms,5400frames/317s. Physical sampled footprint2.85GB, phase means14–24FPS, worst637ms; headroom/performance remains open. Original47Documents and ordinary validation progress4files unchanged. Longer/mixed-crew/multi-cell/rotation stress and detailed compact visual cases still pending. See IPAD_PHYSICAL_VALIDATION_2026-10-17.md.
