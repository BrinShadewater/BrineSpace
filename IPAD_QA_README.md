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
