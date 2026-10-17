# BrineSpace iPad QA preparation

Status: export source and template prepared; no iPad app compiled, installed or tested yet.
Base: accepted local Mac Escape fix brinespace-0aeb47064e40c288.
This separate source copy preserves the Mac build. iPad-only development preset, distinct bundle ID, project-only export; no publication.

1. Install Xcode from the App Store page opened in this session, open it once, finish component setup, and add your Apple account in Xcode Settings > Accounts.
2. Connect the unlocked iPad by USB and accept its Trust prompt. Xcode can guide any required Developer Mode setup.
3. Select a development signing team in Xcode. Its Team ID is required by Godot; enter no Apple password into chat or scripts.
4. Run tools/export_ipad_qa.py --team-id YOUR_TEAM_ID after Xcode is ready. --preflight-only checks requirements without exporting. The script generates build identity/manifest from actual bytes and exports an Xcode project under /Users/Shared/BrineSpace-iPad-QA-build.
5. Compile/sign/install locally using the connected iPad target, then measure actual launch, memory, frame rate, basic tap/drag, audio, Save/Resume and background/foreground behavior. Desktop/headless/simulator results do not establish iPad acceptance.

Official Godot 4.7.2 iOS template verified against the official TPZ SHA512, then extracted with recorded SHA256 in IPAD_QA_PREPARATION.json. Preflight currently stops because full Xcode and a real signing Team ID are absent.
Existing visuals/rules/assets retained. Compatibility rendering explicitly retained on mobile. Touch layout/zoom/cancel affordances have not been redesigned; first feasibility test will identify what is needed.

Prepared files: export_presets.cfg (new iPad QA preset), project.godot (explicit mobile Compatibility), tools/export_ipad_qa.py, IPAD_QA_PREPARATION.json, output/export-tools/4.7.2-stable/ios.zip. Export script syntax/preset validation checked; actual export requires Xcode and real Team ID.

## Xcode setup continuation — 2026-10-16
Xcode 27.1 (27A9275) first-launch setup passes; iOS/iPadOS27.1 SDK installed. Connected iPad product iPad13,18 (10th generation), OS27.2, detected over USB. Device details report unpaired; CLI pairing failed with kAMDInvalidHostIDError, so unlock/Trust and host pairing remain pending. No signing identities or Apple account teams yet. Xcode Apple Accounts sign-in opened; user is completing authentication directly. Export remains gated on actual signing Team ID; no app build/install claimed.

## Export and device compile complete — 2026-10-16
Selected Xcode team LP5CWU4BSX (from selected-team Manage URL). iPad now paired; Developer Mode disabled at last check. Owner asked to enable it on iPad. Export brinespace-b06d1300fe05541b produced /Users/Shared/BrineSpace-iPad-QA-build/BrineSpaceiPad.xcodeproj and PCK. Device-architecture unsigned Release build PASSES. App: DerivedData/Build/Products/Release-iphoneos/BrineSpaceiPad.app; bundle com.shadewater.brinespace.ipadqa, iPad-only, minimum OS15, SDK27.1. Signing certificate creation and device registration approval requested from owner; do not proceed with that action until answered. Actual signing/install/launch/native memory/performance pending. Logs/results under build folder.

## Signing approved and complete — 2026-10-16
Owner explicitly authorized signing certificate creation, private-key storage and iPad registration. Developer Mode confirmed Enabled; device connected/paired. Signed Release xcodebuild succeeds with automatic provisioning. Strict codesign passes. Profile team LP5CWU4BSX includes target iPad, expiry2027-10-17. Installation now running via devicectl; launch/native acceptance not yet claimed.

## Installation and launch completed

Signed device Release build succeeded. Strict signature verification passed. The provisioning profile includes the target iPad. devicectl installed com.shadewater.brinespace.ipadqa successfully, then launched it in the foreground without test arguments. PID 587 was present in the subsequent device process snapshot. Evidence: build/install-result.json, launch-result.json, processes-after-launch.json and IPAD_RESULTS.json. Native rendering, audio, touch, performance and save/resume acceptance remain pending user testing.

## Touch update in progress

Owner reports first build runs well; audio works with Silent Mode off. Approved two-finger pan/pinch, visible Rotate/Cancel/Fit Station, larger station/Inspector targets and 1.5x cards. Candidate brinespace-ba11d5aeabedf44d changes main.gd and draft_card.gd, adds tablet_controls.gd, removes no runtime files. Native touch fixture and desktop card-drag/menu recovery pass; iPad-aspect layout screenshot reviewed. Fresh export destination: /Users/Shared/BrineSpace-iPad-touch-QA-build. Signing, installation and actual device gesture confirmation pending.

### Review and real engine dispatch correction

Review identified hand-originated drag cancellation; expanded fixture reproduced that and deferred card-slot sizing (three failures), then native fixes passed. A further real-engine Input.parse_input_event/flush fixture established Godot emits emulated mouse before raw touch; manual raw-first fixtures missed it. Reproduced first-finger placement (three failures); helper now classifies the first synthetic left press before GUI and cancels synthetic canceled release before CardDrag. Native expanded engine-path fixture passes with 0 failures, including fresh hand presses after map/canceled gestures. Final review found no further important issues. Previous touch candidates are superseded; do not launch them as final. Corrected export: /Users/Shared/BrineSpace-iPad-touch-final-QA-build.

## Final touch update installed

Build brinespace-588d6c3f3bb5b0b0 exported, compiled, signed and strictly verified. Final exact-PCK native expanded touch fixture passes with real engine touch-to-mouse event ordering; raw asset audit checked 35,942 with zero differences/missing/remaps/unexpected. Final signed app installed over the same bundle and launched normally, PID 1020 present in subsequent device process list. Actual iPad gesture/layout acceptance remains for owner testing. Final results: /Users/Shared/BrineSpace-iPad-touch-final-QA-build/RESULTS.md and IPAD_RESULTS.json. Prior touch v1/v2 folders are superseded evidence.
