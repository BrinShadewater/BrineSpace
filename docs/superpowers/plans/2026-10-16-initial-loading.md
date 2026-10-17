# Initial Windows loading investigation plan

> Execute sequentially in this chat; use the systematic debugging and verification skills. Preserve the existing dirty workspace and frozen Windows/Mac pair.

**Goal:** Attribute initial New Loop and Continue loading, improve a measured avoidable cost if practical, and demonstrate unchanged artwork and crew behavior.

**Architecture:** Observe the actual d3 release title/loading journey in a separate physical QA copy. Reuse existing startup and crew-batch clocks, distinguishing a new profile without its learned image list from a repeat profile. Select a narrow fix only after attribution, then compare a separate candidate with the same fixtures.

**Tech stack:** Godot 4.7.2, Windows Compatibility renderer, Python, native secondary display.

**Spec:** Owner request in this chat: profile initial loading on Windows without changing visuals or crew, keeping matching Windows and Mac builds frozen.

## Constraints and review focus

- Never mutate D:/bs-save-hitch-20261016/ source, Windows or Mac artifacts. No commit/publication.
- Scratch APPDATA and explicit resolved-profile proof before writes; owner fingerprints before/after every run.
- Serial native games, visible secondary display, silent and physical input disabled; retain errors and outliers.
- Distinguish profile-first from OS-cold boot, loading from intentional transmission/Continue waits, and diagnostic from acceptance timings.
- Preserve lossless pixels, all loaded poses/equipment, checkpoint admission, memory bounds, normal costs/failures and crew logic.
- Keep at least 20 GiB free on C:/D:. Evidence D:/bs-startup-20261016/; helpers output/startup-20261016/.

## Tasks

- [x] Profile normal New Loop and Continue in fresh/repeat profiles; collect stage/crew batch/prefetch observations and verify frozen identities. Frozen d3 new 12.844/5.520 s, Continue 12.413/7.257 s; fresh profiles with/without a pre-seeded order isolate the missing parallel decode coverage. OS cache uncontrolled. Add memory sampling to final matched comparison.
- [x] Select measured cause and write the smallest regression/experiment; implement only a supported improvement in a separate candidate. Two runtime files prime the existing bounded decoder from surviving crew batch paths only when no learned order exists. Expanded prefetch regression fails for missing feature, then passes including real compressed-batch pixel/extent/storage checks. Initial test-adapter parse/setup failures retained separately.
- [x] Validate image/metadata/crew/save invariants and actual packaged entry paths, then repeat loading comparison. Twelve valid primary runs, all six full crew identity pairs equal; focused/native/exact package checks pass. Two settling follow-ups retain early texture-sample limits.
- [x] Verify protected saves/frozen deliveries, document results and remaining gates in CURRENT_STATUS and a concise handoff. 2,948 owner files and106 frozen delivery checksums unchanged; duplicate QA pairs removed with restoration map.
