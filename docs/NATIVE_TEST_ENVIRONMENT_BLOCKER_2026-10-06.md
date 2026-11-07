# Project handoff

Updated: October 6, 2026 · BrineSpace · Native test environment blocker

## Objective and acceptance
Continue the full PC/Mac performance/release plan. Recover reliable process startup/exit before accepting native pixels, pacing, memory or packaged gameplay. Game performance and release gates remain open.

## Accepted decisions and constraints
No engine/renderer upgrade, quality reduction, global Windhawk/Windows setting changes or reboot performed. A reboot requires owner permission because other applications may have unsaved work. All diagnostic engine/Python copies are byte-identical to the installed 4.7.2 engine and bundled Python; copies live only in the named QA output directory. Scratch profiles and owner fingerprints remain required.

## Current state
Current acceptance supersedes this historical blocker:
`docs/HAND_REFRESH_OPTIMIZATION_2026-10-06.md`. Three native station pairs and the
permanent hand test now exit cleanly; fresh QA/installed --version controls exit
0, so the earlier 0xC06D007F is not reproduced. No reboot/system change performed.

Latest continuation: execution resumed without reboot or global changes. Empty
headless/native controls exit 0; the permanent hand test exits 0 with 74 checks
and 12 exact image comparisons. All 2,936 owner files unchanged. Earlier failures
remain preserved under output/hand-reuse-2026-10-06/pre-recovery/. Version-only
control still exits 0xC06D007F with no output; its cause remains unexplained.
Native game validation can proceed; full environment/release certification is
not established. The paragraphs below retain the earlier blocker evidence.

Normal Main/DraftCard hand reuse remains implemented but unaccepted pending native validation. The latest headless fixture uses observable geometry settling and explicit hover calls; physical pointer input is disabled only in the fixture. Fifty behavioral checks report zero failures. One repeat measures 100 row/fan refreshes at 8.445/8.851 ms versus baseline 380.350/392.885 ms. This is CPU fixture evidence, not station FPS acceptance.

Evidence: output/hand-reuse-2026-10-06/. run.py now records exact PID, command, profile, module observations and bounded timeout/termination status. process-command.py and desktop-state.py are read-only process/desktop diagnostics. startup-control/ is a minimal project containing no game scripts, autoloads or assets. Physical engine and Python copies and hash manifests reside under its steamapps/common/BrineSpaceQA/ directory, covered by Windhawk's existing game exclusion (InjectIntoGames=0).

## Verification
Windhawk 1.7.3 DLL observed in original stalled fixtures. Copying the engine into its existing exclusion removes that DLL (recorded module observations), but does not fix native startup or headless exit. A byte-identical QA Python copy also has no Windhawk DLL loaded; controls launched from it still fail. Windhawk is therefore an observation, not a proven cause; no customization settings were changed.

Both ordinary-parent and clean-parent controls: --version prints 4.7.2 then hits a 45-second exit timeout; empty-headless verifies the scratch profile and completes its frame, then hits an exit timeout; empty-native prints only the engine header and times out before running the script. Ordinary-parent empty-native termination remains pending after its bounded kill wait. All completed diagnostic batches preserve 2,936 owner non-log files. No native pixel pair, actual station FPS, GPU memory or packaged acceptance obtained.

Win32 process queries for original fixtures show non-STILL_ACTIVE exit values (0 headless, 1 native) with a zero-duration wait returning WAIT_TIMEOUT. Shell print/exit controls also fail to report terminal completion. The current process window station, thread desktop and input desktop all name WinSta0/Default/Default. This narrows the blocker to the testing environment/runtime rather than BrineSpace content; exact cause remains unproven.

Primary references: [Windows process exit](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-exitprocess), [exit status](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getexitcodeprocess), [Windhawk injection/exclusions](https://github.com/ramensoftware/windhawk/wiki/Injection-targets-and-critical-system-processes). Windows documents DLL-detach deadlocks as a possibility; these observations do not establish one or identify a faulty DLL.

## Next action
Obtain explicit recovery/reboot permission; do not launch more identical tests while the host remains stuck. After recovery, require version/empty-headless/empty-native controls to launch and terminate cleanly before running game tests. Then finish native retained/fresh card pixels and input coverage, move accepted regression into tests/index.json, and run matched 40-room station measurements. Original bug closure, memory budgets, native endurance, packaged Windows/Mac checks, signing/notarization and release delivery remain unfinished. No upload or visibility change authorized by this work.
