# Native Mac validation — run in this order

Keep the frozen app unchanged. Record PASS/FAIL/NOT RUN separately. Do not fix a
failed check by disabling graphics, failures, crew activity or the check itself.

## 1. Identity, account and first launch

Verify archive SHA256 against the supplied checksum file, then extracted package
files with `python3 Context/tools/mac_qa.py verify`. Confirm d3 build ID and PCK
`49a95db92f2382f52b56034a5af4515746a464d2695e2aa1e150ca83d0c09b12`.
The optional source has a separate complete archive-file manifest; verify it
before editing. Git commit `67e7db969f7c5d952a3c80830369715d703199c5` alone is not d3.

Use a disposable Mac account (default helper name `brinespace-qa`). Do not start
the game or source tests in the owner's normal account until true engine-level
profile isolation is established. Profile is normally under that login's
`Library/Application Support/Godot/app_userdata/BrineSpace/`. The helper's `probe`
mode verifies the actual engine path in the test account; HOME overrides still
need native verification before using any automated scratch-profile harness.

```sh
python3 Context/tools/mac_qa.py info --output Mac-results/system.json
python3 Context/tools/mac_qa.py probe --qa-account brinespace-qa --output Mac-results/profile-probe
```

Attempt first Finder launch and record any dialog exactly. Then collect:
`codesign --verify --deep --strict --verbose=2`, `codesign -dv --verbose=4`,
`spctl --assess --type execute --verbose=4`, and `xattr -l` for this app. The info
helper captures those statuses without changing the app/security settings.
Ad-hoc signing/notarization status and native launch are distinct gates. Preserve
original quarantine/signature evidence before any owner-approved app-specific launch
exception. Do not globally disable Gatekeeper, silently re-sign or clear all xattrs.

## 2. Ordinary gameplay and Save round trip

1. Intro/title/New Game, architect selection and transmission/Continue lead into
   a centred, visible station. Test normal audio before muted timings.
2. Build legal rooms at normal cost. Confirm normal resource spending, power
   allocation, suspension and failures are intact. Existing recipe/loop rules
   stay as described in PROJECT_AND_GOALS.md.
3. Let real crew move/work. Exercise an ordinary doorway, large hydroponics/riser
   door, lights, floors, props, water and exterior drones. Opening doors must not
   reveal black riser walls. No missing/magenta art or source placeholders.
4. Pause and Save. Record resources, placed-room ownership/rotation/state, active
   crew/equipment/contact, clock, live cargo return and room-owned floor case if
   available. Quit normally, relaunch the same test profile, Resume and compare.
5. Repeat Save/Resume during James cargo return before/after/midpoint/terminal/idle,
   both gears when practical. Exact clock/plan/pixels and finite completion matter;
   saving only to disk is not a restore test. Source fixtures can cover rare states
   after their Mac isolation/harness adaptation is verified.
6. Return to Title and re-enter several times, then Quit normally. Check scene
   release, audio drain and no accumulating obsolete router references.
7. Save an F8 report and confirm its screenshot, logs/diagnostics and saved-path
   location. Collect locally; no automatic upload.

Do not restore `fixtures/reported-12-room.save` over personal data. Copy it into
scratch storage first and reset `run_save_path` after restore: RunSave.restore
retargets autosave to the loaded path. A QA fixture's free-build flags are not
evidence that normal play should be free.

## 3. Visual, input and display acceptance

Check default window, fullscreen, resize, Retina logical/physical dimensions,
text glyphs including zeroes on room cards, card frame overlap and angled colour
lines, scrolling/trackpad pinch/zoom, keyboard shortcuts/F7/F8, modal focus, pause,
minimize/restore and normal audio. Compare close and far views, crew equipment,
door/light sorting, floor seams and large-room water. Capture actual native images;
an asset hash or headless run alone cannot establish display correctness.

No app should become stuck/unresponsive after focus changes or screen movement.
If F-keys are intercepted by macOS, use Fn where needed and document it. Do not
mistake a normal laptop refresh/VSync cap for CPU capacity.

## 4. Performance and long-run plan

- First record a normal fresh and restored 12-room station at 1×/2×/4×. Then the
  labelled large fixture. Use the same station, camera/zoom, viewport, backend,
  graphics/Reduced Motion, roster and warmup when comparing builds.
- Keep the display awake/window visible, other game/art jobs paused, and only one
  timed native run active. Record power source, Low Power Mode, display refresh,
  VSync, Retina scale, hardware/OS/backend and test duration. Do not change system
  power/priority/affinity to make a result pass.
- Capture mean frame ms/FPS, p95/p99/max, counts ≥50/100/400 ms, and action time
  separately from whole-frame time. Placement: action frame and following 60
  frames. Save: production Save versus any immediate validation readback. Retain
  zoom transitions, first-placement/first-load costs and every idle outlier.
- F7/F8 can establish manual native evidence. For CPU attribution on Mac use
  Instruments Time Profiler/appropriate native tools if available; no Windows
  WPR/ETW replay. Instrumentation and image readbacks can perturb tails; label
  diagnostic versus acceptance runs.
- Begin with a short real-process canary and confirm no errors/stuck actors or
  profile damage. If clean, run a longer actual normal-process soak as needed for
  release acceptance, tracking process memory/object/router lifetime and repeated
  title transitions. Keep history bounded/streamed. Do not automatically run a
  two-hour soak merely to repeat Windows results before first Mac smoke passes.

60 FPS target is about 16.7 ms; still-open Windows gates are not relaxed for Mac.
Static Universal 2 checks do not certify Intel; record each architecture actually tested.

## 5. Source tests and exact benchmark portability

With the optional source and official Godot 4.7.2 editor, imports complete first.
Use targeted groups from tests/index.json, not an unrelated full asset sweep:

```sh
python3 tools/run_tests.py --godot /Applications/Godot.app/Contents/MacOS/Godot --only test_cargo_binding_cache,test_run_save,test_save_integrity
python3 tools/run_tests.py --godot /Applications/Godot.app/Contents/MacOS/Godot --only test_crew_pose_cache,test_crew_router_pixels --native
```

These are commands to use **after** verifying the runner's macOS `user://` isolation.
It redirects HOME on Darwin; APPDATA-only fixture guards and Windows path/monitor
assumptions may need an external Mac adapter. Do not weaken checks or run against
real progress to avoid a SKIP. PASS-HUNG, unsupported and NOT RUN are not clean PASS.

`windows-reference/benchmark.gd` is the exact corrected-v3 fixture used for the
headline Windows cohort. It contains a hard secondary-display requirement and
Windows-oriented launcher/config assumptions. On one display it may refuse.
Before porting, copy it to a separate Mac harness; preserve room composition,
real carry-aware Bill factory, recovery roster fixture, camera trajectory, all
eight actions, three speeds, 120 samples/phase and Save readback semantics. Change
only platform launch/isolation/window selection, record original/adapted SHA256,
validate equivalent state/camera and source/PCK identities, and retain the refusal
history. Do not substitute an older vanilla fixture with the wrong Bill factory.

The original cargo native harness also created a second game before closing the
first router; the Windows adapter corrected teardown and factory subclass checks.
Its verified adapter is included as reference, with Windows output paths clearly
requiring replacement. Keep strict negative admission/pixel checks and observable
scene teardown; do not modify production Router.start just to satisfy an old test.

## 6. Return a concrete handoff

Use TEST_RESULTS_TEMPLATE.md. Include build/ZIP/PCK hashes, exact source differences
if any, actual commands, account/profile proof, hardware/backend/display settings,
raw results/outliers, screenshots/F8 reports, crash logs, visual/save outcomes,
changed files and unresolved gates. A failure is useful evidence; keep it rather
than repeatedly rerunning until an attractive average appears.
