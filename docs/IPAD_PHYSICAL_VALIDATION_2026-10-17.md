# Physical iPad validation — October 17, 2026

**Functional acceptance passed; bounded large-station stress completed; performance and memory headroom remain open.** No production gameplay/source fix, release approval, main merge or frozen-build change.

Integration base `585111ca3878e6ae60d044d745b395bdb2a7e9af`, via validation documentation `c60251531d603ac7b2bd4a02b56b2ec78e9bf7d2`. Branch `codex/mac-ipad-native-validation-2026-10-17`. Physical10th-gen iPad13,18, Apple A14/~4GB, iPadOS27.2 (24B5110a); Godot4.7.2 official, OpenGL ES3.0/Apple A14 GPU,2360×1640drawable. Xcode27.1, Apple Development automatic signing, strict signature and signed/export PCK equality passed.

Normal QA app **BrineSpace Validation**, `com.shadewater.brinespace.nativevalidation20261017`, build `brinespace-84d6658d7c53bb33`, PCK `301fc91be940ea2b7ed2836788bf253cc0a5548a1cbda4b60dd356e268188395`. Owner confirms New Loop reaches station; Save/Return/Continue restores station/resources/cards; pinch, two-finger pan/rotation, returning a card to hand, Codex scroll, Home Screen/reopen all pass and return paused/intact. Diagnostics corroborate normal construction/four rooms/zero logged errors. Audible playback/dialogue and every visual state were not separately accepted in this continuation.

New/Continue station build **11.751/12.479s**; scene-load0.898/0.081s; visible loading feedback77/23ms. Interface/grid setup10.796/11.134s dominates. One run each; not a loading speedup baseline. Passive physical footprint samples reached2.33GB loading→early play and2.58GB during Save/Continue/touch/resume. Earlier SIGKILLs coincided with unsuccessful debugger checks; clean retry succeeded without a code fix. An unexplained40.135s title frame is retained separately; background/resume/debugger activity prevents causal attribution. It is not pooled with controlled startup measurements and remains open. A production crash cause is not established.

Stress app **BrineSpace Stress**, `com.shadewater.brinespace.nativestress20261017`, build `brinespace-60df99e8247f3917` (source60df99e8247f3917d1cf689163466a1f81a62155e2450e00eae805472ff37af5), PCK `978f064b451de46e4ce14aaa1cbcce103c282381fa1f348b6c1583b6a4b4d4b9`. QA-only guard/benchmark autoload/empty scene; intro excluded. All shared game/art/audio bytes unchanged; delta documented. Asset audit36,187/zero missing/changed/remapped/unexpected;431selected+434known bundled scripts, metadata matched. Normal QA audit remains separate36,188assets.

Stress restored an independent frozen3-room QA input and built to40, then43rooms. One active Bill actor,40powered rooms, freebuild/failure exemptions only in fixture.37fixture+3measured placements,60zoom requests,5,400frames across9phases; no scripted rotation count. Input disabled, muted, deterministic simulation, fitted full station, VSync requested off. Speeds below are simulation, not absolute zoom. Instrumented workload completed in**317.03s**; no missing-art failures or automatic reports. Full camera/actor/raw-frame scope in [portable evidence](native-apple-validation-evidence-2026-10-17/physical-ipad/README.md).

| Phase | Mean FPS | p95 ms | p99 ms | Worst ms |
|---|---:|---:|---:|---:|
| idle 1.0× | 22.10 | 66.14 | 84.79 | 370.51 |
| zoom 1.0× | 18.05 | 99.00 | 129.41 | 150.05 |
| placement 1.0× | 17.59 | 84.14 | 115.70 | 316.66 |
| idle 2.0× | 18.68 | 83.02 | 116.20 | 302.50 |
| zoom 2.0× | 19.28 | 81.59 | 104.53 | 366.37 |
| placement 2.0× | 13.86 | 101.53 | 183.10 | 636.92 |
| idle 4.0× | 20.19 | 67.22 | 115.05 | 284.41 |
| zoom 4.0× | 20.23 | 70.54 | 112.93 | 282.91 |
| placement 4.0× | 23.82 | 52.95 | 96.54 | 395.49 |

Physical Activity Monitor371app samples over384.24s reached **2,853,736,472bytes (2.85GB /2.66GiB)**; near workload end~2.81GB. Trace includes startup/post-run collection and samples near1Hz; not lifetime peak or leak proof. Prior EXC_RESOURCE2867MB is not cleared by this5-minute success. Live/recent drone decoded images exceeded the64MiB reusable budget; that budget does not cap visible working sets or all live/GPU memory. Retain the637ms placement outlier. No claim of60FPS, sustained memory safety or Windows863ms/241ms/27.3s issues resolved.

Isolation: original `com.shadewater.brinespace.ipadqa` unchanged,47/47Documents SHA256 match before installation/after testing; both new containers empty before launch/input copy, HOME/Documents guard before BugReport writes. Ordinary validated progress4/4files match after separate stress. Normal app foregrounded after test; stress process deliberately terminated only after complete outputs/trace. Profile copies/signing/traces containing other apps remain local. Original Mac `last_session.json` preservation failure from earlier work remains disclosed in [native handoff](MAC_IPAD_NATIVE_VALIDATION_HANDOFF_2026-10-17.md).

Next: reduce live texture/room/crew working set and investigate placement/zoom hitches; repeat longer/higher-crew/multi-cell construction/rotation workloads, full/fractional compact-drone close-ups and lifecycle during pressure. No cross-platform release approval. Evidence and QA templates are on the validation branch; full local archive under `/Users/Shared/BrineSpace-native-validation-evidence-20261017`.
