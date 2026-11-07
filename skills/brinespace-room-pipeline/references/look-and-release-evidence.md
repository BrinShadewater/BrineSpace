# Station look and release evidence

## Find the right evidence

Read the active checkout's `docs/CURRENT_STATUS.md`, then its linked look/session
handoff and `docs/RELEASE_WORKFLOW.md`. The primary editable workspace can retain
older source plus unrelated local work while release receipts live in a selected
QA worktree. Follow those links rather than exporting the primary workspace to
capture one new feature. For the current signing/look continuation, the primary
workspace's `docs/SESSION_CLOSEOUT_SIGNING_AND_LOOK_2026-10-19.md` links the exact
signed ZIP, hashes, selected release source and recovered report. Newer receipts govern.

For inclusion questions, identify the actual ZIP/EXE/PCK and its receipt. Inspect
the PCK directory and relevant script/scene/autoload attachment read-only; no
game launch is needed to determine whether a preview script is shipped. Packaging
polish and EXE signing can leave the runtime PCK unchanged. A matching version
label, current editor source or valid signature does not establish feature inclusion.

## Recover a preferred look

Find the report in the profile used by that session. An isolated audition writes
reports beneath its scratch APPDATA, not the owner's normal report folder. Read
the launcher's resolved profile path when ordinary reports are older than the audition.
Inspect ZIP member names first; read only the note, relevant log/settings and
screenshot. Preserve the report and copy selected evidence into a task folder.

Record three distinct fields: report-observed settings, owner recollection and
reconstruction assumptions. A toggle log establishes the last recorded comparison;
unlogged slider changes may follow. A screenshot with closed controls establishes
appearance, not exact parameters. Missing fields do not mean the owner never
selected them or used defaults. Leave unknown values unset.

Check the actual dropdown/shader before interpreting “all filters”. In the
current audition, pixelation and tilt-shift combine with one selected colour/light
mode; the listed colour modes do not accumulate. Keep dated preferred values in
project notes, not as permanent skill defaults.

## Compare and continue

Reconstruct unknown values as labelled assumptions in an isolated profile and
compare the same station/camera at native scale. Protect HUD/card/inspector
readability and inspect motion as well as stills. When controls are meant for
players, validate saved preferences and an off switch along with changed render
behavior and cost. Source-preview checks retain their tested revision/platform;
packaged gameplay, native visuals and other platforms need their own evidence.

When F8 diagnostics are in scope, capture the effective look state at the same
boundary as its screenshot: enabled, pixel grid/blend, tilt radius, focus,
colour/light mode and strength, and dithering. Record this as pending if not implemented.

## Deliverable and closeout

Use `docs/RELEASE_WORKFLOW.md` for export/packaging/signing. Reuse an approved
active signing profile; keep private identity/billing material out of repo and
player archives. Sign after executable changes, then regenerate checksums and
archive. Verify trust/timestamp on the executable extracted from the final ZIP.
This verifies signing/package integrity, not gameplay or immediate SmartScreen reputation.

In the closeout, name the exact artifact and source/runtime identities; state
local-candidate versus live-publication status, confirmed versus tentative visual
choices, checks actually performed and the first useful next action. Notes/skill
maintenance does not itself launch a new export, cleanup or publication.
