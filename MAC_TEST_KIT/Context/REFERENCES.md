# Reading map for the next Codex session

Start with the new Context documents. Then read only relevant originals in
`project-docs/`. They retain dated scope and Windows paths; those are provenance,
not current Mac commands. The optional source carries the larger docs archive.

| Need | Included original / source location |
| --- | --- |
| Current owner constraints | AGENTS.md, NOTICE.md, README.md |
| Latest accepted direction | CURRENT_STATUS.md; later direct owner decisions govern |
| Prototype north star and gameplay | DEVELOPMENT_NOTES.md, north-star section |
| Latest Save fix and all outliers | SAVE_HITCH_2026-10-16.md |
| Earlier e54 normal two-hour Windows acceptance | FIXED_RELEASE_VALIDATION_2026-10-16.md |
| Lifetime cleanup cause | OBJECT_LIFETIME_2026-10-16.md |
| Original full-source Windows/macOS QA | WINDOWS_MAC_RELEASE_QA_2026-10-16.md |
| Export and native Mac distinctions | RELEASE_WORKFLOW.md, MAC_RELEASE_PLAN.md |
| Renderer trial and retained default | GODOT_RENDERER_HANDOFF_2026-10-15.md |
| Engine/method research, not blanket integration | GODOT_METHODS_HANDOFF_2026-10-15.md, GODOT_RESEARCH_HANDOFF_2026-10-15.md |
| Prior Windows stall/report/soak work | PRERENDER_HANDOFF_2026-10-16.md, REPORT_SOAK_HANDOFF_2026-10-16.md |
| Earlier CPU/room/navigation avenues | Optional source docs/*_HANDOFF_2026-10-14/15.md; inspect frozen code before calling a trial shipped |
| Exact current patch | patches/minimal-runtime.patch; code/ holds reference copies |
| Main/frozen source identity | evidence/source-inputs.json, root build_info/expected-manifest/parity |
| Measured comparison | evidence/benchmark-analysis.json, followup-analysis.json and CSVs |
| Native cargo checks | evidence/cargo-v2-verification.json and selected restored world captures |
| Actual 40-room Windows benchmark | windows-reference/benchmark.gd, SHA below; platform adapter required |
| Source subsystem tests | Optional source tests/index.json and tools/run_tests.py |

Exact corrected-v3 Windows benchmark SHA256:
`3a98f6bcff0744276c973da28fc38c67c7d09d159896bbb3d2ca1bde348c38de`.
Keep this original unchanged; version/hash any Mac port separately. The reference
scripts are not a ready-made Mac runner. Windows trace/process helpers and D: paths
must not be copied into shell commands on this machine.

Official platform references consulted for this kit:

- [Godot Mac packaging/signing](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_macos.html)
- [Godot command-line reference](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
- [Apple app-specific opening guidance](https://support.apple.com/en-us/102445)

Source/tutorial documentation can evolve. The actual 4.7.2 editor/template and
native execution determine supported flags and behavior; no latest-doc feature
is silently assumed to exist in the frozen build.
