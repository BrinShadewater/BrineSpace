# iPad cryo fallback texture demand

Validation 2 **brinespace-7675a83dea541541** is installed on the physical iPad. Unused cryo fallback art now follows the existing tablet demand policy, removing **13.987 MiB of engine texture allocations** at the same paused checkpoint. First redraw remains about **2.2 seconds**; this build is for validation and is not release-cleared.

## Source and change

Checkout `/Users/Shared/BrineSpace-native-validation-20261017`, branch `codex/ipad-memory-placement-2026-10-17`, HEAD `81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus accepted dirty work. Starting installed source was **f829898722272cfe**, preserved in the previous habitat/Veld handoff. Frozen Mac and Windows releases are unchanged.

`rooms/underwater/batch-two/cryo_chamber_view.gd` demand-loads the six canonical generic wake frames one at a time and defers its original equipment sheet through the inherited tablet loader. Named crew still use their canonical animation art. Desktop/editor preload behavior, original image bytes and gameplay rules are preserved. Added a paired-UID native regression in both native and tablet-memory test lanes. Independent read-only review found no actionable issue.

## Verification

- Native red/green regression, exact generic wake pixels/source bytes and cache reuse pass. Whole seven- and forty-room viewport pixels match the baseline exactly; each reduces texture allocations by13.987 MiB.
- All **24 exact-package fixtures**, selected-asset/script audits and strict code signing pass. Signed app/PCK/executable hashes match the candidate receipts. All four temporary export configuration changes are byte-exact restored; owner Mac profile fingerprints are unchanged.
- Physical iPad13,18, A14,4GB, iPadOS27.2: same paused seven-room checkpoint texture accounting falls710.350→696.363MiB. First setup4.149s, repeat3.051s, first redraw2.214s. Baseline first setup9.903s was an outlier; repeat3.127s/redraw2.286s. This single pair does not establish a loading speedup.
- Normal-rule **56-room/four-crew** fixture completed **30.277 active minutes**, cycles69→164. All four crew remained active and alive; no logged errors or crash. Initial reserves and connected support rooms were fixture preparation; normal costs, caps and survival rules ran on device. This is not organic recruitment acceptance.
- Sampled process peak2,384,629,520bytes/end2,346,503,928bytes. First/last-minute medians grow33,882,184bytes; opening warmup affects the first window. Sparse active buckets have median12.17FPS/minimum5.14FPS/maxframe340.202ms. They are sampled buckets, not full-run frame statistics. The large fit-to-station view remains slow and memory growth is not cleared.
- Actual card return, pinch zoom, rotation button, Codex scroll, background/reopen and Save/Continue pass. Two-finger tap/pan are not automated by this helper. Full saved gameplay state and exact timer match; only path/timestamp/event history change. Continue's existing1× reset required manual4× reselection.
- After final normal launch, all five incoming save/checkpoint files are **SHA-exact**. Owner station remains cycle64/seven rooms, paused4×, menu closed. Final screenshot visually inspected.

## Remaining work

The first redraw still performs environment/floor PNG decoding and texture adoption. Short diagnostic stack samples attribute loading work but carry profiler overhead; do not treat them as benchmark evidence. Next isolate the first visible grid decode/adoption work at the same checkpoint, then compare cold/repeat loading and the large four-crew viewport. Count actual retained texture bytes before changing owner retirement; growing owner registrations alone do not prove a leak.

Read-only packaging inventory found458,459,184bytes of byte-identical duplicate payloads and814,562,357bytes of world-review PNGs. These overlap; directory names do not prove unused assets. No pruning/dedup format change was applied. Any future shared-offset PCK experiment must preserve recovery-tool compatibility.

## Artifacts and recovery

Evidence and current signed app/export: `/Users/Shared/BrineSpace-ipad-optimization-20261019/cryo-fallback-demand`. Detailed machine-readable identity/results are in [portable evidence](evidence/IPAD_CRYO_FALLBACK_DEMAND_2026-10-19.json); local `FINAL_VERIFICATION.json`, `full-device-pipeline.log`, `soak-summary.json`, `physical-loading-comparison.json` and `final-owner-restoration.json` hold receipts. Source SHA256: `7675a83dea541541145047b83046e27db34c72940751ef450684b9e8f8f689fd`; PCK: `f36fb864fc201067c10b4231d38c562f3ef6dd31073870bf740cde6e04e009ba`; signed executable: `e8e62b0be2998e111deb15e614151164f690cf794022c5e99687c3a28cffce8d`.

Completed isolated test caches were removed with an inventory receipt; saves and unique evidence remain. Preserve the current7675 full PCK/app, protected7bb root donor, all recovery archives and `DONOR_RECOVERY_ORDER.md`. Old QA pack recovery status is recorded in local `previous-qa-recovery.json` when complete. No commit, push or release upload was performed.

Previous f829 and same-pack diagnostic PCK copies are now recovery-archived in `accepted-f829-rollback-preserved.recovery.json.gz`; full stream reconstruction was verified before removal. Keep the current7675 donor and protected7bb donor. This removed duplicate logical payloads but did not immediately increase measured free space (APFS sharing/snapshots may retain blocks); do not claim16GB reclaimed.
