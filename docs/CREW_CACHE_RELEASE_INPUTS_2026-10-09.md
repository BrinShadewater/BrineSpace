# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: installed-cache release inputs

## Objective and acceptance

Export and validate installed lossless crew storage in actual debug=false Windows
and Universal 2 Mac candidates. Preserve prior delivery. Full original release
gates remain open, including large-station FPS and stutters.

## Accepted decisions and constraints

Use maintained exporters and the same physical input snapshot on both platforms.
Do not alter owner saves or close an unidentified live play session. Do not treat
editor-native pixels or private override packages as the new release's acceptance.

## Current state

New physical snapshot: `D:/bs-release-crew-cache-20261009/source`.
`freeze.json` verifies 57,785 copied files, 36,256 runtime selections and
3,593,543,176 selected bytes, including all ten production storage helpers.
Dependency closure/source hash verification completed. Prior delivery retained
at `D:/bs-release-20261009/`. New Windows candidate is built and smoke-tested;
Mac same-input export/audit is complete. Identities and scope are recorded below.

Local drivers: output/renderdoc-tools-2026-10-08/{freeze,build}-crew-cache-release.py.
Build wrapper preserves the original failed guard and accepts only a fresh,
time-bounded independent revalidation of the same freeze identity and all inputs.

## Verification

Freeze session50776 reached source verification and saved its completed snapshot,
then exited1 on the separate owner-folder fingerprint guard: 2,936->2,938 files;
settings/startup cache/session/save/comms/trace changed and two reports added.
Full change record remains freeze-owner.json; no unchanged-owner claim.

Observed external editor PID667496 launched from Explorer PID13184; its play child
PID660768 runs the normal project without test arguments. New report filenames
identify that same child PID. Read-only freezing launches no game/editor. These
observations attribute the concurrent writes to normal live play rather than
proving test damage; no owner files restored, deleted or changed by recovery.
User clarification on ownership was pending; neither process was closed by this
task. A subsequent authoritative process check found the play child gone and only
the editor still open.

Fresh revalidation completed October 9 at 23:38:54 UTC: all 57,785 snapshot and
checkout file hashes match, no gameplay process at either boundary, owner 2,938
files unchanged. Original freeze-owner.json failure retained; separate evidence
is freeze-revalidation.json (freeze SHA256 c79280af2e5b5b2f99abd70ce8154c855d7341237270dbc1050d72b22ef2241e).
Driver revalidate-crew-cache-freeze.py exited0. Build session67548 now runs:
14 Python release checks passed, resolved scratch directory verified and official
Mac-template preflight passed. Build session67548 subsequently exits0. Windows
candidate identity brinespace-cab0dd6874401f88; EXE SHA256
7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76;
PCK SHA256 e9d3f8460270b78b8eba5d29300349f1639ebd405965223e2b88f1be1ba6d297.
Build owner guard unchanged. Audit/smoke session23111 exits0: 35,779 packaged
entries checked, missing/changed/remapped/unexpected0; actual debug=false normal
entry/New Game/dialogue/visible simulation/F8 reports0 failures. Both captures
visually reviewed: station, cryo art, cards and report modal present without
missing-art placeholders. This is not animation-motion, original nine bugs or
performance acceptance. Audit and smoke owner guards unchanged.
Mac export/audit session96515 exits0 from the same physical source. Universal 2
bundle structural audit passes; all36,255 selected source hashes match Windows.
ZIP SHA256 ce673c7176fe47accf72c795d66f8ddbaf71fb2e9ea6e9329164ed745ae4ee87.
Mac PCK SHA256 e9d3f8460270b78b8eba5d29300349f1639ebd405965223e2b88f1be1ba6d297
is byte-identical to Windows. Exact pack audit35,779 entries with missing/changed/
remapped/unexpected0. Both export/audit owner guards2,938 unchanged. Ad-hoc testing
signature only; native Mac, Developer ID/notary/Gatekeeper remain unverified.

Next performance priorities retained in large-action-priorities.json: matched
private large-scene idle mean27.4ms, lighting33.11ms; construction/demolition
worst151.03/156.10ms. These diagnose separate sustained-budget and stutter work,
not their causes. No new packaged benchmark result yet.

Read-only current-report extraction retained under live-owner-reports/. Both
reports list zero engine errors. Second report has a 7,208.897 ms frame near
main-scene initialization and a later456.120ms draw-heavy frame. Last action can
be stale (2,051/14,914 ms respectively), callback timers may aggregate, and no
source/build identity or matched performance acceptance is established. Do not
infer placement or crew recovery as the cause from those labels alone.

## Next action

Profiler-overhead diagnostic session34751 now complete: eight packaged runs and
all48 selected phase-end state comparisons equal; owner unchanged. No consistent
large profiling penalty proven; neither-mode mean34.192/32.005ms still over budget.
See PACKAGED_PROFILER_OVERHEAD_2026-10-09.md for scopes and exact results. Known
idle editor667496 recorded and untouched; these are not final release acceptance.
Next inspect actual rendering/submission costs and make matched, visually verified
fixes. Then benchmark with competing engine activity absent and keep native Mac/signing
gates separate. No publishing authorized. Investigate the current live stall reports
with isolated reproduction and aligned stage attribution.
