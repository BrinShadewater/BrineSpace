# Animation residency experiment

Updated: October 5, 2026 · BrineSpace · Isolated prototype, not shipped

## Objective and acceptance

Test whether inactive image storage can be released while preserving animation
frame objects, then restored without sampling changes. Measure actual engine
texture accounting and reload work. This is a mechanism test, not full-game
memory acceptance or proof that every transition can be prefetched in time.

## Accepted decisions and constraints

Use the selected six-frame Veld east carry bare clip, the actual CrewSpritePlayer,
CrewTextureBatch and CrewTexturePool. Preserve full PNG pixels, filter, dimensions,
metadata and frame identities. Do not change runtime code, save bindings, selected
art or frozen packages. No permanent decoded-image backup cache.

## Current state

Ownership review confirms frame-bank arrays retain CanvasTexture wrappers, whose
diffuse textures own image storage. Aliased banks and generated joined/reversed
clips can share those wrappers. Grid Bill bindings also retain arrays directly.
`crew_action_pack.gd` and mirror construction read images for composition; these
consumers require residency, not just a non-null frame object. Runtime adoption
must explicitly cover them, equipment, portraits and retained drawing commands.
The pool's lookup references are already weak and cleared after startup.

The output-only fixture loads the real clip, retains an aliased frame array, and
displays frame zero through Sprite2D. An explicit consumer pin protects that
wrapper. A separate direct ImageTexture reference protects frame one. Detaching
the other wrappers' diffuse textures expires four images; releasing the raw
reference expires a fifth. The pinned image remains visible and byte-identical.
This demonstrates the difference between wrapper ownership and raw-image ownership.

Reloading uses original source paths, one missing image per rendered frame, on the
main thread. A readiness check refuses to activate the incomplete bank. All six
original wrappers survive; only their image storage is rebound. This gate is a
fixture safeguard, not an approved gameplay delay policy. An unprepared transition
cannot simply wait in production without violating the timing requirement.

### Final native results

Three eviction/reload cycles on the owner's Windows RTX 4070 Ti system:

| Check | Result |
|---|---|
| Loaded clip decoded storage | 1,572,864 bytes / 1.50 MiB |
| Engine texture counter reduction each cycle | 1,747,620 bytes / about 1.67 MiB |
| Released decoded storage | Five 256x256 RGBA8 frames / 1.25 MiB |
| Image parity after reload | 108/108 byte-exact: 6 frames x 3 scales x 2 offsets x 3 cycles |
| Pinned image during eviction | Unchanged in all 3 cycles |
| Wrapper identity, aliases and original metadata | Preserved |
| Authored elapsed-frame selection checks | 30/30; playback snapshot unchanged |
| Full-bank preparation wall time | 41.044–41.472 ms across 5 render frames |
| Maximum individual decode/upload call | 1.215 ms |
| Maximum measured preparation frame interval | 8.556 ms with a 120 FPS cap |
| Owner non-log files | All 2,936 unchanged |

Engine texture accounting and decoded bytes are deliberately separate. The counter
delta is not a process working-set, driver residency or Mac unified-memory reading.
Repeated cycles return to the same loaded counter and release the same amount.
The result does not extrapolate linearly to the entire crew bank.

Reference screenshots are held as CPU byte arrays solely for fixture comparisons.
The prototype does not retain decoded source Images for reload. Timing excludes
comparison readback/validation, but these are small warm-file reloads in an otherwise
light fixture. No >50 ms interval was observed in the measured preparation frames;
this does not certify gameplay pacing, cold I/O, larger textures or minimum hardware.

## Verification

Evidence: `output/residency-research-2026-10-05/` contains `probe.gd`, `run.py`,
`result.json`, `run.log` and `owner-check.json`. Two native runs: initial pixel/
ownership test, then added preparation frame intervals and authored timing checks.
Both passed without engine errors. Scratch APPDATA, resolved-profile guard before
fixture writes, and before/after owner fingerprints used in both runs.

Changed only output experiment files and documentation: this handoff, the action
register and CURRENT_STATUS. No runtime residency manager or automatic eviction.

## Next action

The mechanism is viable for this clip, but its 41 ms readiness lead time exposes
the real integration problem. Before enabling eviction, build a bounded inventory
of active, imminent and direct-read consumers for one complete character and its
equipment. Pin every immediately reachable transition that cannot be prepared in
advance; never delay gameplay or display a null texture. Generated/composited art
needs a separate reproducible source recipe or must stay pinned.

Measure the reclaimable remainder with that conservative pin set in a real station.
If it is too small, residency will not meet the budget and requires a different
measured remedy. If sufficient, prototype bounded preparation under matched active
gameplay, cold/warm loads and interruption tests before changing production code.
Larger-image decode/upload limits must be byte/time-based, not simply one image per
frame. Release memory/performance gates and native Mac certification remain open.
