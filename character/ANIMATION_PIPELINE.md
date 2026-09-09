# Current character animation pipeline

Start from [ACTIVE_ASSETS.json](ACTIVE_ASSETS.json), the runtime consumers and
`docs/CURRENT_STATUS.md`. Older dated handoffs and source folders preserve history.
They do not select the game assets.

1. Inspect the affected sources and actual frame directions. Preserve exact prompts,
   source PNGs and rejected candidates. Check transparent gutters before extraction.
2. Change only the requested identity/state. Use authored anatomy anchors and a shared
   scale through the action; props, raised tails and flames must not set body scale.
   Preserve accepted dry pixels when adding a separate water pack.
3. Package locally. `tools/build_animation_expansion.py` rebuilds v5 from its local
   sources; `tools/build_companion_water.py` rebuilds the independent water extension.
   Builders write assets: inspect their scope before running them. Normal closeout
   needs the read-only audit, not a full regeneration.
4. Check active manifests with `tools/audit_character_bindings.py`. It verifies real
   PNG bytes, dimensions, binary alpha, durations, declared bindings and portrait
   availability. It records content hashes in `output/character-closeout/bindings.json`.
5. Run the affected runtime fixture. `test_animation_expansion.gd` covers dry actions
   and clocks; `test_companion_repair.gd` covers paid torch assistance;
   `test_companion_water.gd` covers real flooded-room routes and saves. Use Godot 4.6.1
   through `tools/run_companion_check.py` and preserve logs. Native fixtures create
   isolated save names; don't substitute the player's live save.
6. Inspect the intended actor in native room captures at gameplay scale, plus ordered
   animation phases/GIFs. Zoom can refresh inspector metadata: settle zoom first,
   set the cell, then focus. A wrong-room capture is not visual evidence.
7. Update the inventory, visual bible and dated handoff with exact selected packs,
   checks and remaining legacy coverage. Synchronize changed skill references with
   the installed mirror. Distinguish source integration from a rebuilt executable.

Current additions are installed: Marsh v5 base; River/Josh/Margot v5 base/actions;
River/Margot water extensions. Josh's torch frames are retained in v5. Some older
Marsh secondary and helmet states remain legacy art; don't count them as newly authored.

All three companions are separate from architects. Optional pre-expedition selection,
rescue unlocks, Margot's frog bonnet and Josh's tracked base remain established direction.
