# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: small-station cache gate and prop-clock observation

## Objective and acceptance
Continue full PC/Mac readiness. Test512MiB cache against tighter12room texture budget and investigate draw-counter mismatch without changing animation. Reject a memory-gate failure even if uploads decline. No normal cache increase, quality reduction or release certification.

## Accepted decisions and constraints
Retain normal256MiB soft lookup budget. The global512MiB candidate fails the initial small-station2GiB target and remains private. Keep combined crew provider private and selected art/filters/timing intact. New diagnostics observe clocks; no production game/renderer modifications this interval.

## Investigation and current state
LargeRoomCanvas.Props increments advances only from its draw callback, then passes slot.clock to contents.advance_live. It is not a simulation-step counter. RoomContentCanvas.paint reads machine_clock from view_state for library screens/effects. Private observer adds only last painted machine clock/process frame to DrawSlot. Source before instrumentation exactly matches selected release room_content_canvas.gd SHA b34de1189ab522bfbd9843fcb47d39c2303b65c7afd2095c8211ff2fe8dfd149. Overlay mounts before BugReport/renderer compilation; runtime property guard proves execution.

`output/all-crew-storage-2026-10-07/drone-twelve-clock-trial-clean-2026-10-08/`: matched actual debug=false synthetic12room/fourcrew/mixed4large-room/drones/production,256/512MiB,9idle/pan/zoom1/2/4x phases×180frames. Capture22animated prop slots per phase before/after post-draw fence, and record cumulative draw counters separately. Fence time excluded from frame samples. Same instrumentation/fences in both lanes; timings are not directly comparable to older unfenced runs.

Private helper generation initially inserted source block into an index string; corrected before launching. First launched loader had doubled carriage returns from decoding CRLF bytes then text-mode writing; owned errored process stopped, original loaders/adapters restored. Corrected LF writes, new evidence directory. Failed scripts/logs preserved; no owner data or normal runtime edits. No warning suppression.

## Verification
Both successful lanes clean/0missing, correct actual budget guard, all crew snapshots/drone states/phases/door/light/power/zoom equal. All22animated prop records×nine phases match both before and after render fence, including visibility, room/index/kind, slot/view/painted clocks. Absolute process frame excluded from equality. Example visible first-phase clock5.99999999999998 agrees across allthree clock sources. Cumulative prop counters also equal in this12room pair. This does NOT reproduce or retrospectively close prior40room4advance/26draw difference; need instrumented40room scope before closure. No full prop raster/motion acceptance.

Texture post-draw peak1848.369143->2276.250468MiB (~1.805->2.223GiB), +427.881325MiB.512MiB candidate exceeds2048MiB target by228.250468MiB; many endpoints~2091–2095MiB also exceed it. Active/recent/canvas ownership makes cache soft; extra memory is not limited to budget delta. Global increase rejected. This is synthetic12room, not historical reported station/driver VRAM certification.

Sampled completed-frame uploads184->131 (-28.80%), frames130->110, bytes5,113,946,032->4,679,301,584 (-8.50%), measured image-create464,708->453,600us (-2.39%). Deduplicate latest-upload frame only when equals sampler-1; excludes startup/fixture/gaps. Creation saving only11.108ms across1620frames, insufficient to substantiate whole-frame gain.

P95control/candidate idle/pan/zoom1x19.236/19.952,20.724/19.826,23.607/26.657ms;2x21.507/22.832,25.426/24.075,32.087/30.089ms;4x25.074/26.056,25.531/24.333,31.696/31.482ms. Five improve/four regress; all miss16.7ms. Max56.306->66.118ms. No reliable FPS gain.

Three actual paused15room scratch disk/staged restores per lane (three actual recovery wards) preserve exact room/crew state/router release. Restored1565.620317MiB flatallthree; warm/final exits234.533917MiB flat,0missing. Both owners2936unchanged; private adapters restored, both loader bytes verified against retained originals; all processes terminal. Original normal QA adapter/full PCK unchanged. Source/observer/loader/adapter/base/EXE/budget identities retained; comparison.json includes complete clocks/counter fields.

## Next action and remaining work
Do not adopt global512MiB. Smaller residency strategies require a substantial measured benefit,12/40memory gates and output checks; avoid more minor-cache work solely because it reduces counts. Refocus on larger renderer CPU/batching/layer costs. Existing40room idle profile reports~5068draw calls, live_rooms5.303ms, content_draw2.170ms, large retained props0.850ms, large bases0.572ms; counters/times use different units and overlap, so do not sum them. Use render/backend versus script attribution and matched workload to choose a material remedy. Instrument40room prop clocks if relying on counter parity for future adoption.

Full original gates remain: frozen combined candidate/exact outside-checkout PCK audit, historical reported station, original nine issues, normal title/Continue/menu/input/scale/motion review, actual targetPC/Mac/sign/notary and long native/headless endurance. No completion claim.
