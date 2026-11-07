# Matching Mac Save candidate and portable Codex handoff

Delivered October 16, 2026. **brinespace-d3cfa1890bafefe7**, built with the maintained
Godot 4.7.2 Mac exporter from `D:/bs-save-hitch-20261016/source/`. No runtime code,
artwork, crew behavior, save schema or graphics configuration changed for this task.

## Deliverables

All files are under **D:/bs-save-hitch-20261016/mac/**:

| File | Purpose | Bytes |
| --- | --- | ---: |
| BrineSpace.zip | Universal 2 app plus portable Codex context outside the app | 3,552,250,918 |
| BrineSpace-source-d3cfa1890bafefe7.zip | Optional editable source/assets/tests with context | 3,757,232,963 |
| ARCHIVES_SHA256SUMS | Transfer checksum for both ZIPs | |
| START_HERE.md / PASTE_INTO_CODEX.md | Human quick start and complete Mac-session prompt | |

Game ZIP SHA256:
`8afa0ada638939f8e263b3031752562d4c332c46a7857201e4579e374aeebcf1`.
Source ZIP SHA256:
`157b4ae797be415cce09b63cefeae02a4a798a7d9b04aa697b913cbde3f3de53`.

Main ZIP includes ten authored Markdown guides: quick start, Codex prompt and
AGENTS, project goals/decisions/code map, optimization history, scoped Windows
evidence, native test sequence, source/build provenance, references and a results
template. Curated project reports, exact fixture/analyses, Save patch/code/tests,
selected pixel evidence, normal 12-room/layout fixtures and Windows harness
references travel with it. Windows paths/old private experiments are labelled as
historical evidence, not Mac commands or current acceptance.

The native helper verifies extracted/archived files, records hardware and signing
statuses, checks actual user-data paths and captures launch logs in a declared
disposable account. It does not silently alter security settings, audio/graphics,
sign the app, upload reports or declare gameplay accepted on process start.
Mac native execution of these helper modes remains pending. Python archive
verification and the portable GDScript probe's Windows parse/path check passed.

## Identity and artifact verification

- All **36,430** runtime manifest entries match Windows, with no differences/case
  collisions. Full PCK and build metadata are byte-identical to Windows d3.
- PCK SHA256: `49a95db92f2382f52b56034a5af4515746a464d2695e2aa1e150ca83d0c09b12`.
- Universal 2 arm64/x86_64, executable mode 100755, one PCK, no shipped QA override.
- Every original app file and executable mode is unchanged after adding external
  documentation. This preserves the exported signature envelope; native
  `codesign`/Gatekeeper assessment remains a separate check.
- Main ZIP: **94 files streamed/CRC checked**; supplied helper independently
  verifies all 93 manifest payload files (self-hash manifest excluded).
- Source ZIP: **61,711 files verified**, all runtime inputs match the game, real
  asset bytes and paired UIDs included. No Git history/import cache/live profile.
  Five export SDK files (~1.5 GiB) omitted explicitly. Generated metadata/current
  handoff and post-freeze native router pixel test/UID overlays are recorded.
- `MAC_TEST_KIT/.gdignore` prevents Godot importing reference-code UID duplicates.
  Its metadata update preserved original source data; the final ZIP was fully
  reverified and checksums regenerated. Authored local documentation links pass.

An early assembly attempt found the post-freeze native router pixel test absent
from the source selection; the test and paired UID are now explicit reference/test
overlays. Its failure log is retained. No production fix or PCK change was needed.

## Scope and next action

Native Mac testing is the next task: first Finder/Gatekeeper result, ordinary
New Game/Save/Quit/relaunch/Resume, cards/crew/doors/lights/water/exterior, audio,
input/Retina/focus, then scoped native pacing/memory/source tests. Use the included
protocol and return template. First work uses a separate macOS QA account or
verified engine-level isolation; Windows APPDATA alone is insufficient. The
reference benchmark needs an explicit Mac monitor/launch/isolation adapter,
especially on one display; do not run the Windows fixture blindly.

Ad-hoc local testing distribution, not notarized/publicly promoted. No native
Apple Silicon/Intel acceptance, new timing result or performance improvement is
claimed by static packaging. Windows results remain scoped as in the Save report;
earlier e54 two-hour acceptance is not inherited by d3 or Mac.

All **2,948 protected player files unchanged**. Original Windows/Mac, e54 Windows/
Mac and d3 Windows 11/11/12/13/10-file checksum guards pass. New Mac folder manifest
covers 96 files. C:/D: free **123.612/76.762 GiB**; no Godot process remains.
No commit/upload/publication. Evidence: `mac-final-guards.json`, `platform-parity.json`,
Mac `kit-audit.json`, `source-audit.json`, `archive-identity.json`, checksums and
`MAC_TEST_KIT_HANDOFF.md` under the task evidence root.
