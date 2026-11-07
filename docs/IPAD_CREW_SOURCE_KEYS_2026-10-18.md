# iPad crew source identity index — October 18, 2026

Validation 2 **brinespace-0e63ab6e9c2e7500** installed on physical iPad13,18 (A14,4GB,iPadOS27.2). Source starts at81b2f9a4a36eb0e3162d86ccfb4e9ef735836122 on `codex/ipad-memory-placement-2026-10-17`, plus accepted uncommitted changes; prior installed build4d908213bdc57c32. No commit/push/public release this pass. Frozen/public Mac/Windows deliveries and protected integration checkout unchanged.

## Change

Warm prepared crew caches still read/hash8500original PNG buffers for James/Bill. The maintained manifest producer now creates a compact selected-source identity table before calculating the final manifest fingerprint. Installed iOS/non-editor bundles use it to avoid repeated original reads. Mutable/editor/unknown/missing/bad-table cases retain ordinary source reads; existing prepared-cache checksum/layout/ZSTD validation and bounded four-worker preparation remain. Strict table size/count/checksum/order validation and binary lookup retain2012352bytes (~1.92MiB); **this adds metadata, not a measured RAM reduction**. Desktop policy unchanged. No original artwork/audio/gameplay/save-schema changes. Same-entry dependency comparison and actual package delta add only source_keys.gd/indexJSON; only worker_batch.gd changes in the playable package.

## Validation

Six new Python and ten existing manifest checks pass; generator red3/green0. Native fixture red4/green0; seven focused native fixtures pass. All31443lookup identities match manifest; all11652James frame fingerprints/pixels/layout/extents match across four balanced runs. Quiet native warm interface/grid baseline2.229–2.474s versus indexed1.569–1.574s; initially empty-cache baseline2.776–3.194s versus2.440–2.458s. Counter938437134B unchanged. Isolated profiles/owner-save guards pass. Independent review has no actionable findings.

Nine exact-package fixtures (crew identities/cache/workers/decode/cacheindex/legacyoverlays/HullUI175/Save/touch), asset/source audits, strict signature, signed/export PCK equality and export-setting restoration pass. SourceSHA `0e63ab6e9c2e75009cb2205dc5287eada98c940a7379d67f1e717574ae029bcb`; PCKSHA `8a5112019cb2875900c617f8ea34dc8073b14a684cb7977dc400142b52858c12`; executableSHA `68a1988d8caf9005b6f8408024aa04b05133ed8c735afb576ca0ef5e13fb987d`. Default diff whitespace flags repository CRLF; CR-at-EOL-aware check passes.

## Physical result and limits

First/repeat station4.402/3.659s, interface-grid2.848/2.594s, compared with prior separate5.089/4.282s and3.436/3.231s. Encouraging observations, cache/device uncontrolled. Save76/107ms, errors0/automaticreports0. Texture900.528/840.372MiB unchanged.215valid1Hzsamples peak1.959GB/last1.813GB across two paused seven-room loads/menu/report capture; **no causal whole-process RAM savings**. Retained paused loading hitches3929/3292ms remain.

All five save/checkpoint hashes match before/after installation before launch. Full gameplay state and timer parity pass at cycle64/seven rooms, including resources/cards. Existing Continue resets speed to1x; manually restored original4x before saving while paused. Saved_at/event_history/scroll/camera-center differ after UI checks, not a whole-file parity claim. Final station paused/menu closed/PID5548alive. Same two-hour helperPID58831 reused across installation, active51m08s, no additional authorization; left running. Recheck helper status before reuse, do not restart routinely.

Initial/first-use loading, long-session/larger-station memory headroom, Continue speed restoration and iPad release gates remain open. No claim all stalls are fixed or release-ready.

Portable evidence: [source-keys](ipad-memory-placement-evidence-2026-10-18/source-keys/physical-summary.json). Full local evidence and signed app: `/Users/Shared/BrineSpace-ipad-optimization-20261018/crew-source-key-index-pass` (DerivedData/Build/Products/Release-iphoneos/BrineSpaceiPad.app). Keep owner save copies/private process inventory outside Git. Earlier mismatched-entry comparison retained locally as explicitly non-acceptance; corrected same-entry comparison is portable.
