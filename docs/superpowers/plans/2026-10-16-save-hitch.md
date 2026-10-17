# Save hitch investigation and implementation plan

> Execute sequentially in this chat with superpowers:executing-plans; preserve the existing dirty workspace and frozen releases.

**Goal:** Attribute the roughly114ms large-station Save frame, remove its largest unnecessary cost, and recheck Save/4× placement without changing artwork, crew behavior or checkpoint admission.

**Architecture:** First profile the unchanged e54e8a0eb8d58f65 Windows package with the exact corrected-v3 external fixture. Measure actual Save separately from the benchmark's readback verification. A diagnostic copy of the unchanged RunSave script adds stage clocks; it is not a release performance candidate. Only after attribution, make one narrow source fix and export a separate candidate from a preserved source selection.

**Tech stack:** Godot4.7.2/GDScript, Python orchestration, native Windows Compatibility renderer.

**Spec:** Owner's accepted proposal in this chat: profile snapshot creation, validation, asset rebinding and disk writes, fix the largest contributor, repeat Save and4× placement benchmarks.

## Global constraints

- Preserve appearance, crew behavior, save format/admission, error handling and backup semantics.
- Preserve canonical e54 Windows/source/Mac and b0 deliveries; no publication or commit.
- Scratch APPDATA and BRINESPACE_TEST_USER_DIR before all Godot launches; owner fingerprints before/after.
- Native jobs serial, visible secondary screen2, silent and input guarded; preserve owner Project Manager.
- Keep at least20GiB free on C:/D:. Full logs/evidence on D:/bs-save-hitch-20261016/; helpers under output/save-hitch-20261016/.
- No monolith refactor, animation changes or broad unrelated test batches.

## Review focus

- Empty cargo plan still needs complete floor/bank artwork identity.
- Active plan/stage/clock state must be captured fresh and detached.
- Manifest/equipment/artwork/timing changes must not reuse stale identity.
- Invalid saved bindings must remain rejected before scene mutation; old saves remain admitted.
- Actual Save costs must be distinguished from diagnostic/readback/render time.

## Tasks

- [x] Profile the unchanged package: actual Save, capture/base/cargo binding work, validation, serialization/checksum and file replacement; preserve exact source transformation/hash evidence for diagnostic clocks.
- [x] Select one measured cause. Add a failing regression covering its intended invariant and invalidation/failure cases, then implement the narrow fix. Selected cause: repeated immutable compressed-frame RGBA digest work. Three runtime files, bounded per-frame digest/key cache, loader prewarm; 18-check red/green regression and independent review complete.
- [x] Run focused checkpoint/crew correctness and native visual checks appropriate to the fix. Focused tests, native crew pixel tests and 424 normal cargo checkpoint checks pass. Separate maintained Windows export d3cfa1890bafefe7: 36,430 entries, exactly three changed scripts; exact asset/source audits pass, all 421 extra frozen scripts unchanged.
- [x] Repeat the same corrected-v3 full action order, two resolutions/two runs, all speeds; compare FPS, actual Save/readback, placement action and following60 frames. Four valid primary runs plus separate contemporary two-repeat 1080p baseline/candidate follow-up. Save benefit repeats; original 100.372 ms idle frame and slower warm sequence retained. No steady-state FPS gain claimed. Short actual normal-process release canary passes 39 checks.
- [x] Record acceptance, changed files, scoped checks, remaining release gates and storage/owner guards in CURRENT_STATUS and a concise handoff.
