# Margot integration handoff

Updated: September 9, 2026. Project: BrineSpace. Task: add Margot as a companion.

## Objective and accepted decisions

Owner supplied her white/tabby cat in a green frog hat, requested a revised
background, then authorized game integration. Portrait V2 is the selected source.
Margot is a companion, separate from architects, rescued from a small working
pet pod beside two broken human pods containing skeletons. Unlocked companions
are optionally selected before future expeditions.

## Current state

- `character/margot-v1/`: authored four-direction idle/walk, sources, prompts,
  hashes, manifest and moving review. `tools/build_margot_assets.py` rebuilds it.
- `character/companions/`: canonical portrait, three pod identities (pet has
  occupied/empty states), updated roster manifest and visual review page.
- `scripts/companions.gd`, `companion_npc.gd`, `meta_state.gd`,
  `architect_selection.gd`: paid rescue south of core, 8-second powered thaw,
  social movement, persistent unlock and selection. Cat never uses robot restart
  wording; pod remains closed/occupied until she emerges.
- Narrow hooks in `grid_canvas.gd`, `bill_npc.gd`, `wreck_field.gd`,
  `drone_fleet.gd`, wreck view and `run_save.gd`: pod collision/rendering,
  recovery work, checkpoint V2 with robot-only V1 compatibility, recap persistence.
- Found cryo room has three dedicated props, costs 8 Metal/18 seconds to reconnect,
  then 1 Power/cycle normal room upkeep. No blueprint or player layout overrides.

## Verification

Godot import and generic manifest validator pass. Expanded `test_companions.gd`
covers paid repair, missing doors/resources/power, pause, partial thaw Continue,
once-only unlock, all three actors, disk reload/selection, Margot-only new loop,
old robot-only checkpoint migration and malformed saves. Existing run-save,
wreck-clearance and architect-recovery fixtures pass.

Native `playtest_companions.gd` passes all three rescues, 500 movement ticks at
0.1 seconds, independent RNG, clear foot positions, paused playback, and picker
at 1600x900/960x540. Captures: `output/companions-native/`; logs:
`output/margot-{import,test,native,run-save,wreck,architect}.log`.
Reviewed native pod scale, distinct skeletons, cat emergence and crew comparison.
Fixtures explicitly construct links; this is not a normal-play balance trial.
The wreck fixture reports two retained resources at exit despite passing
assertions; no general leak/performance claim. Final companion and native runs are clean.

## Next action and limits

Subsequent style consistency pass: portrait V3 replaces V2 at the canonical runtime
path, with broader fur clusters, quieter ivory highlights and cooler slate shadows.
Bill's portrait supplied rendering guidance; Margot's identity and cryopod background
remain. Source, prompt and hash are in `character/margot-portrait-v3/`. Small gameplay
sprites were reviewed and retained: their existing 28-34-pixel scale already groups
fur into broad shapes. Native selector review: `output/margot-style-v3-native.log`.

Owner pod correction: replaced the ambiguous occupied pet-pod interior with one
curled Margot and reduced both pet states from 34 to 29 source pixels wide.
Updated its collision rectangle to 38x64 at the same registered position. The
two skeleton-pod exports remain byte-identical. Original and revised sources,
exact prompt and deterministic region selection are retained in the pack.
Native correction check: `output/margot-pod-v2-native.log`; current review images
use the revised pod.

Owner review of gait/pacing remains. Margot inherits companion social behavior;
feeding, drowning, damage and special jobs are outside this implementation.
Local Godot source is ready; existing executable has not been rebuilt. Preserve
concurrent game/recap work and selected robot assets.
