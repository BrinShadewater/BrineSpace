# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: sustained door validation attribution

## Objective and acceptance

Continue the full PC/Mac performance plan. Identify repeated work inside the measured~1.6ms normal door/light validator before changing its invalidation behavior.

## Accepted decisions and constraints

No normal renderer change this milestone. Preserve live crew proximity, opening frames, depth sorting, room lighting, airlock pose, branch ownership and topology mutations. No cross-frame cache admission without placement/demolition/rotation/layout and same-tick regression coverage.

## Current state

Private subclass of current normal Grid wraps seven helper calls only while `_door_light_state` runs. Private Main copy changes only the Grid preload, using actual normal crew/drone and installed Moonbay optimization. Art/owner layouts/runtime source untouched. Evidence and runner: `output/door-validation-profile-2026-10-06/`.

## Verification

Native mixed40 six phases complete, clean logs/no missing art, owner2,936 unchanged; handle terminal. Attribution-only wrappers add timing/call recording overhead: validator wall time rises to~2.1ms, so this is not an optimization or a new baseline. Nested stage values may overlap and do not predict achievable total gain.

Stable across phases:94 connectivity queries~397–408us;40 world-port list queries~198–207us;40 light queries~105–107us;56 nearest-crew queries~67–69us;28 cached door-part queries~35–39us;84 narrow-corridor checks~57–59us;78 layered-art checks~52–53us. Original normal validator already gathers crew feet per frame and caches door parts: those are not the leading repeated cost. Remaining wall time includes loop/key construction/comparison and instrumentation overhead.

Current connectivity depends on occupied neighbor, branch owner, adjacency, same-room identity, rotation/ports and authored ordinary door layouts. `_render_ports` enumerates ordinary doors through Main and large doors through RoomFootprint. Surface keys omit offscreen room structures by design; blindly reusing those keys for topology could miss offscreen neighbor edits. Any topology reuse must preserve these distinctions and live mutation behavior.

## Next action

Prototype topology preparation with explicit complete invalidation coverage, or bounded within-call port membership reuse, and measure it before normal admission. Continue remaining sustained preparation/rendering and private provider residency/admission. Full original loading/memory/frame, packaged bugs, endurance and Windows/Mac certification gates remain open.
