# Project handoff

Follow-through: [OWNER_REPORT_FIXES_2026-09-27.md](OWNER_REPORT_FIXES_2026-09-27.md)
records subsequent edits and native replay evidence. The table below preserves
the initial triage state, not the latest resolution status.

Updated: 2026-09-27 · Project: BrineSpace · Task: recover latest owner bug reports

## Objective and acceptance

Owner reminded us of submitted bug reports after the generated-prop installation.
Recover the actual notes and screenshots; distinguish report evidence from fixes.

## Accepted decisions and constraints

Read-only inspection of the real profile's bug-report ZIPs. No game execution,
save restoration, artwork replacement or gameplay edits during this triage.
Future reproductions must copy report saves into scratch APPDATA and reset
run_save_path after restoring a checkpoint.

## Current state

19 reports dated September 26–27: 12 owner notes and 7 automatic performance
captures. Exact filenames/notes are saved in
`output/owner-report-triage-2026-09-27/notes.json`. Three screenshots were copied
there for visual identification. Reports remain intact in the owner's folder.

| September 27 report time | Owner issue | Triage |
| --- | --- | --- |
| 00:27:49 | Hallway riser overlaps room | Reproduction/fix status unverified |
| 00:28:34 | Water behind hallway too dark | Visual repro needed |
| 00:29:51 | Veld flashes different colours | Later palette work exists; replay not yet verified |
| 00:30:14 | No windows on north riser walls | Preview-window work is not proof of live fix |
| 00:30:43 | Drone-bay assets too bright cyan | Later installed art needs report-matched comparison |
| 00:31:07 | Mining bay lacks drone and launch pad | Screenshot confirms absence at capture; loaders alone do not resolve it |
| 00:32:46 | Lag spikes | Saved diagnostics available; replay pending |
| 00:33:28 | Always show signed Power change and amount | Current main.gd still replaces nonnegative change with FULL at capacity |
| 00:33:43 | Remove this hatch | Screenshot selects Construction Drone Bay; circular floor hatch visible |
| 00:34:05 | More muted cyan | Screenshot selects Salvage Drone Bay; exact component(s) not pinpointed by note |
| 00:34:47 | Button to repair the clicked room | Inspector-action implementation not established by this triage |
| 00:35:41 | Lagging again | Separate saved performance snapshot |

Automatic captures include a 10.683-second stall and sustained under-20-FPS event
around midnight, then Studio stalls of 1.915 seconds, 449 ms and 474 ms at
02:50–02:54. These are report-time measurements, not current performance results.

## Verification

Read report.txt for all 19 ZIPs; inspected the mining, hatch and muted-cyan
screenshots. No September 27 report-ID references were found in the searched
markdown docs. The September 23 five-report fix handoff covers older reports.
Source inspection confirms the Power chip still substitutes FULL for a positive
or zero change at capacity. Other issues remain unclassified pending reproduction;
none is declared fixed based solely on later art or animation installation.

## Next action

Reproduce the functional issues and lag from isolated report copies, investigate
missing mining drone/pad versus saved layout/state, and verify subsequent Veld and
drone art against these captures. Preserve the ten distinct issue groups, including
both manual lag reports and both cyan notes, through fixes and native retesting.
