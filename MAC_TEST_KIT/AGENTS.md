# Instructions for Codex resuming this Mac validation

The human owner explicitly requested this test kit and wants continuation without
re-explaining BrineSpace. Start with PASTE_INTO_CODEX.md, then the Context documents.
The task is **native validation of the frozen d3 Save candidate**, not a new round
of game design or a broad optimization refactor. Build metadata and checksums are
the version authority; a Git commit alone does not reconstruct this dirty source selection.

- Preserve visuals, crew behavior, save format/admission, costs and failure rules.
  Marsh animation polish is parked for a separate session. No new survivor/content
  promise, balancing, room redesign or automatic quality downgrade is authorized.
- Keep the app untouched for first validation. Put logs/results outside the app.
  Never edit the PCK or re-sign the original to make a failed launch look like a pass.
- First run in a disposable macOS account, or establish and verify true engine
  profile isolation before any normal-account probe. APPDATA alone is insufficient.
  Fingerprint/backup existing data, and never restore a fixture over the owner's save.
- Current profile path is normally
  `~/Library/Application Support/Godot/app_userdata/BrineSpace/`; confirm with the
  actual Godot `OS.get_user_data_dir()`. Do not infer success from an environment variable.
- Run native timing serially with the game visible, display awake, other game/art
  tests paused. Record resolution, Retina scale, refresh/VSync, renderer, power
  source/Low Power Mode and thermal context. Retain all outliers and rejected runs.
- Keep official Godot 4.7.2 and matching templates for source testing. Skip native
  render-bound fixtures in headless mode; a headless pass is not visual acceptance.
  Windows WPR/ETW, process guards and D: paths in old evidence are not Mac tools.
- Do the authorized reversible investigation/fixes without repeated permission
  questions. Keep any fix separate from the frozen app; re-export and repeat the
  affected checks before declaring it accepted. No publication, upload or merge.
- Follow the project AGENTS.md and NOTICE.md included under Context/project-docs
  (and the source snapshot when available). Adapt historical Windows paths to
  this Mac; preserve `.gd`/`.uid` pairs, bought art and owner Studio layouts.
- Do not refactor main.gd in passing. Use whole quoted res:// paths. Scope source
  searches to scripts/rooms/tests/tools/docs/assets; never crawl generated output/.
- Read only relevant references; keep full logs in files and return focused results.
  Once a scoped check passes, repeat/broaden only for a change, failure or unresolved concern.
- At a meaningful milestone, update a concise local HANDOFF.md with build identity,
  hardware, changed files, checks, accepted decisions and remaining work.

Later direct owner decisions govern. Historical handoffs are evidence for their
dated revision and scope, not a current task list. The Context handoff distinguishes
what is confirmed, unresolved, private/rejected and deferred.
