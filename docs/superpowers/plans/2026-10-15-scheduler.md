# Scheduler capture and idle burst investigation

Get bounded scheduler tracing working for the unchanged private structural
candidate/reference, investigate bursts, then repeat average FPS and 4× placement
hitches. No visual/gameplay/crew changes without evidence for a narrowly scoped fix.

1. Diagnose token access; prepare a concrete fixed-purpose elevation helper for
   WPR start/stop only. One normal Windows UAC consent; no persistent rights/policy,
   service, priority, affinity or power-plan changes. Game remains unelevated.
2. Freeze both prior 24-source/PCK lanes, release/native identity and protected
   profile. Preserve all prior results and 20 GiB free storage.
3. Four serial, bounded, no-stack scheduler captures in opposing lane orders,
   after warm-up handshake. Each measures 600 normal idle and 600 4× idle frames.
   Record tick/UTC/PID and main TID. Parse CSwitch/core/wait/ready events offline;
   verify event loss and time alignment before attributing a burst.
4. If causal evidence supports a game-code fix, validate it with appropriate
   pixel/state/behavior checks. Otherwise preserve uncertainty and unchanged code.
5. With tracing off, run two preselected original four-process, four-phase release
   benchmark comparisons (120 frames/phase). Retain all valid FPS/hitch rows,
   verify state/camera pairs and source/native/profile integrity.
6. Update CURRENT_STATUS, results and concise handoff with tracing setup, evidence,
   limits, files and next action. No export/Mac/long-soak claim.
