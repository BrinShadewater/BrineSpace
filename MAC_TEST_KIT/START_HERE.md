# BrineSpace Mac test kit — start here

This is **brinespace-d3cfa1890bafefe7**, matching the Windows candidate with the
Save improvements. It is a private test build for Apple Silicon and Intel.
Windows testing is complete for the scopes in this kit; native Mac acceptance is
the next task. Godot is not required just to play the exported app.

1. Transfer **BrineSpace.zip** intact. Transfer the optional
   **BrineSpace-source-d3cfa1890bafefe7.zip** too if you want Codex to inspect code,
   run source tests or make fixes. Keep the supplied archive checksum file.
2. Extract the game ZIP into a **new folder**, not an older BrineSpace install.
   Keep the app and this documentation together. Avoid copying an unpacked app
   through Windows tools, which can lose executable permissions. See the
   [Godot Mac packaging guidance](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_macos.html).
3. For the first QA pass, use a separate macOS login such as **brinespace-qa**.
   This protects your normal saves even if engine profile redirection behaves
   differently on Mac. A separate folder beside the app is not save isolation.
   Do not run the Windows APPDATA-only test recipe on your main Mac account.
4. Open this extracted folder in Codex on the Mac. Paste the contents of
   [PASTE_INTO_CODEX.md](PASTE_INTO_CODEX.md). It supplies the task and reading order;
   you do not need to explain the project again.
5. In that test account, first try launching **BrineSpace.app normally in Finder**.
   Record the actual first-launch result. This local export is ad-hoc signed and
   not notarized. If macOS blocks it, record the message; the owner can choose the
   app-specific **Open Anyway** action in Privacy & Security. Do not disable
   Gatekeeper globally or start by stripping quarantine. See
   [Apple's instructions](https://support.apple.com/en-us/102445).

The first practical test is intro → New Game → ordinary play → Save → Quit →
relaunch → Resume, followed by doors/lights/cards/crew and zoom/placement pacing.
The [detailed native plan](Context/NATIVE_MAC_TEST_PLAN.md) covers the full order.

The `Context/tools/mac_qa.py` helper verifies extracted files, gathers system and
signing information, and can launch with a captured log in the disposable account.
For example, from this folder with Python 3 installed:

```sh
python3 Context/tools/mac_qa.py verify
python3 Context/tools/mac_qa.py info --output Mac-results/system.json
python3 Context/tools/mac_qa.py launch --qa-account brinespace-qa --output Mac-results/launch
```

Verification/info do not launch the game. The launch helper refuses other accounts
unless you explicitly name your actual disposable QA account. It preserves the
normal default graphics/audio configuration. Test audio normally before using a
muted benchmark. It fingerprints the test profile and records the command/exit
result. It does not certify a test merely because a process started.

Keep at least **20 GiB free after extraction**. The optional source ZIP omits Git
history, import cache and platform export-tool binaries; all selected runtime
sources/assets and paired UIDs are included. It is an editable snapshot, not a
fresh clone of the current Git branch. Read [build/source details](Context/BUILD_AND_SOURCE.md).

Send back `Mac-results/`, your completed [results template](Context/TEST_RESULTS_TEMPLATE.md),
and any F8 report ZIPs. Do not upload reports automatically. Native Mac results,
not the Windows FPS numbers, decide whether this platform passes.
