# Project handoff

Updated: October 5, 2026 · BrineSpace · Isolated Veld station presentation

## Objective and acceptance

Exercise the complete selected CPU-backed Veld bank in actual station drawing,
Studio overlap, disk save and Continue before normal-runtime enablement. Preserve
source pixels, frame identities, playback and the owner's profile.

## Accepted decisions and constraints

Reversible experiments remain authorized. Normal launch, selected art and exports
are unchanged. This is a native Compatibility / RTX 4070 Ti development fixture,
not packaged gameplay, minimum-hardware or Mac certification. Texture accounting
does not establish process-memory or unified-memory savings.

## Current state

New diagnostics/copies live in `output/private-veld-station-2026-10-05/`.
`grid.gd` changes only the copied selected Veld loading path; other actors use
normal storage. `bank.gd` adopts existing logical CanvasTexture frames and
attaches `display.gd` callbacks without replacing their identity or metadata.
`router.gd` resolves actual CanvasItem owners to private GPU leases. Retained
canvases keep their poses while another canvas redraws; root exit drops routing,
source-bank references and leases. Existing four-slot overflow policy is retained.

Polygon drawing bypasses Texture2D draw callbacks. The copied flood helper resolves
CPU textures before crew water drawing; it is reloaded only inside the isolated
process. Checkout `scripts/flood_visuals.gd` is unchanged. Raw-RID shader/mesh and
atlas-wrapped source paths require coverage before broader backend admission.
Routing metadata clears on scene exit; per-node metadata removal and repeated
draw submissions within one process epoch remain review items.

## Verification

- 68 native routing checks pass, including 60 exact raster comparisons across
  draw methods, transposition, clipping, tint, scale and actual dry/flooded crew
  helpers. No missing owner/texture requests; root teardown passes.
- Three alternating station reference/candidate pairs pass. Fresh selected Veld
  is unlocked only in scratch; standard core recovery creates the valid roster.
  Terrain seed and Veld decision RNG are fixed. The normal transmission Continue completes and process/input ownership restores.
  Both entries explicitly resume
  after Continue and run 120 ordinary 1/60 steps. End states match exactly across
  versions: site, movement, position, animation, pause state and clock. Each
  candidate entry routes 246/244 draws and 64/60 distinct poses, with no missing art.
- All three pairs agree: fresh game 3,125.21→2,638.45 MiB engine textures;
  Continue 3,011.08→2,524.28 MiB. Savings 486.76/486.80 MiB. Title allocations
  match between versions: 171.08 MiB first return, 174.55 MiB second return.
  The CPU bank retains 365.35 MiB decoded pixels. Studio close preserves Main's
  art ownership. Old scene/player and router release after save/return.
- All 2,936 owner non-log files unchanged after comparisons and routing checks.
  Original Main/grid/title/scene hashes remain unchanged. Reports, logs and
  source hashes are retained; `matched-summary.json` asserts state equality.

Ten visible transitions pass with zero failures/missing requests, at least 244
routed callbacks and 26 distinct poses each. Comparing first Continue to tenth
entry: game textures 2,524.28→2,524.43 MiB (+0.006%); title
174.55→174.84 MiB (+0.161%). Engine static CPU allocations increase
740.33→740.71 MiB in gameplay (+0.051%) and 310.48→310.85 MiB
at title (+0.121%); these are not OS working-set/RAM measurements.
Scene/player/router release on each exit.
First/tenth station screenshots reviewed: crew, compact needs meters, machinery,
room layers and card hand visible; this is not moving-water or whole-game visual
acceptance. Owner files unchanged. These short transitions are not the two-hour
soak. `endurance-summary.json` and captured PNGs retain evidence. A single
ObjectDB exit warning appears in both reference and candidate short probes and
remains unresolved. No reported engine errors. Earlier terrain-only seeded runs
had different NPC routes and are retained under `terrain-seeded-only/`; they are
superseded. Covered-station comparisons and a ten-transition run are also
retained under `covered-station-superseded/`; screenshot inspection caught an
unacknowledged transmission overlay. These are not visible gameplay acceptance.
An earlier fabricated roster prevented saving and was a fixture error,
not a backend lifecycle failure. The fresh fixture intentionally starts core-only;
it is not the reported 12-room station or a 40-room performance workload.

## Next action

Test the same controlled backend against reported 12-room and deterministic 40-room
workloads, with process RAM and uncapped pacing as well as texture counters.
Actual water/layering, gear/interruptions, offscreen re-entry and retained Studio
view coverage must precede default enablement. Other actors, historical Bill save
bindings, two-hour soak, packaged Windows, M1/Retina and signing remain open.
The memory and frame-time release gates remain failed; no upload is authorized.

Later workload measurements and the accepted emergency Metal guard are recorded
in `docs/VELD_WORKLOADS_METAL_GUARD_2026-10-06.md`. The CPU-bank RAM/FPS
tradeoff is now measured; normal animation storage remains unchanged.
