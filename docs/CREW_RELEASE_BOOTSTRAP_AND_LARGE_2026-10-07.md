# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: private release bootstrap and active large-station evidence

## Objective and acceptance
Attribute startup delay and test the compressed crew provider under actual active
40-room release gameplay. Preserve full PC/Mac release gates and selected visuals.

## Accepted decisions and constraints
Private build dbe44a995a5708be only; no normal provider admission or upload. Actual
debug=false EXE/PCK/guarded isolated profile; QA adapters restored after terminal
processes. Dedicated free-build/failure suppression stays fixture-only.

## Current state
Bootstrap trace driver `output/compressed-crew-2026-10-06/trace-crew-release-bootstrap.py`;
early script/parent events under `output/crew-release-2026-10-07/bootstrap-trace/`.
Active current-source 12-type40-room fixture adapted for packaged execution by
`run-crew-release-large.py`; evidence under `large-active/`.
Normal source/art/PCK unchanged. Physical QA fixture and report guard restored.

## Verification
Three traced learned-order launches clean,engine uptime at ready5,664.523/
5,609.365/5,567.863ms,request-to-ready4,327.661/4,330.810/4,341.084ms.
Scene requests at engine1,336.746/1,278.541/1,226.771ms. Parent engine banner~131–
136ms,graphics banner~514–616ms; benchmark_init engine~1.190–1.289s. Report super
enter12.037/4.150/1.474ms,ready<.1ms,resize.069–.204ms; scene load~1.088–1.135s.
Prior14.521s pre-scene delay does not recur. This rules out those measured stages
as long delays in these runs, not the historical cause or future guarantee.
report_enter insertion did not match CRLF guard declaration; do not pretend that
earlier boundary exists. super-enter/ready boundaries and parent prints did match.
Owner2,936 unchanged; adapters restored; all processes terminal.

One actual release native1920x1080 uncapped active40-room trial:15 phases ×60
frames,idle/pan/zoom/lighting/interface at1/2/4x; deterministic Node process1/60step.
Veld,James and Marsh active,production/drones on; farms/storage/Moonbay/Tidal included.
Clean logs/exits,no missing art or presentation routes. Selected presentations
Veld177/James222/Marsh69 distinct frames,total468;3,249resolutions,1,912uploads,
4 reusable GPUslots/18 retained spills. Source payload98,326,303lossless bytes;
raw-equivalent1,066,970,976bytes is not retained decoded RAM.

Reported texture phase endpoints2,362.991–3,037.150MiB (~2.31–2.97GiB),end
2,732.774MiB (~2.67GiB). All15 endpoints below3GiB,highest leaves34.850MiB;
within-frame peak not sampled,only one candidate run,no matched normal package.
Do not certify whole memory gate/endurance/hardware or claim matched savings.
Start settled2,239.975MiB. Actual12-room2GiB gate remains untested.

p9531.345–62.993ms/p99max90.428ms;zero measured frames>100ms.60FPS gates fail.
Worst zoom2x frame90.428ms:step4.461ms,engine wait85.934ms,aggregate draw callback
time59.058ms/269callbacks (not269 whole-grid redraws). Root renderCPU12.049ms,
GPU9.164ms,separate scopes. Drone current-frame uploads0. Largest draw labels:
live_rooms17.393ms,wall_slots8.859,floors6.849,detail_room_setup6.782,
env_terrain_cells6.656,large_prop_retained5.851,large_child_base5.591.
Labels overlap; do not sum or call exclusive cause. CPU crew3.599ms much smaller
than aggregate draw preparation. Prior104ms stall remains open,not disproved.

Automatic reports enabled/one saved. Inspected its isolated zip:1172.502ms hitch
at uptime~2.5s,drawcalls0,nodes21,texture18.269MiB,live_station unavailable/no active
station. It captures pre-game scene-loading work,not one of900 measured frames.
Archive details in large-active/auto-report-inspection.json. Do not silently drop
it or claim no stalls across the entire executable session.

Final1920x1080capture inspected:room/UI/card/portrait art present; large synergy
toast and card hand obscure station. No full motion/lighting/nine-bug acceptance.
All owner fingerprints2,936 unchanged; all processes terminal/adapters restored.

## Next action
Prioritize measured redraw preparation across room walls/floors/large bases and
terrain; keep navigation/drone upload speculation secondary to the current data.
Add per-frame reported-memory samples outside timing to verify small3GiB headroom,
then repeat candidate comparison and save/title/Continue/Studio ownership.
Keep pre-scene delay awaiting reproduction with early tracing available. No memory,
60FPS,soak,minimumhardware,Mac signing/play or full release certification claimed.
