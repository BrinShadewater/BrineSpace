# Synergy Discovery Progression Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn hidden room synergies into a discoverable progression chain that visibly functions while powered, stabilizes after three consecutive cycles, and permanently unlocks an immediately usable prototype blueprint.

**Architecture:** `SynergyManager` remains the authored recipe and door-topology layer. A new pure `DiscoveryManager` resolves powered links, stabilization counters, unlock-graph validation, and deterministic transition results; `main.gd` applies those results to saves, decks, feedback, and summaries. `grid_canvas.gd` renders only learned dormant links and powered functioning effects, keeping undiscovered recipes secret.

**Tech Stack:** Godot 4.6.1, GDScript, `SceneTree` headless test scripts, procedural `CanvasItem` drawing, JSON persistence through `FileAccess`.

**Spec:** `docs/superpowers/specs/2026-09-04-synergy-discovery-progression-design.md`

## Execution Record — 2026-09-04

This ledger tracks the delivered outcomes; the original step-by-step implementation recipe below is retained for provenance. The user's subsequent full gameplay, visual and UI pass expanded Tasks 6–7.

- [x] Task 0: preserved the existing run loop in `d7914a0`.
- [x] Task 1: authored the twelve-foundation, thirty-blueprint, twenty-five-pattern graph in `be99fe9`.
- [x] Task 2: separated connected and functioning links in `18f8832`.
- [x] Task 3: added persistent discovery and three-cycle stabilization in `44719ec`.
- [x] Task 4: delivered permanent unlocks, next-draw prototypes and terminal Research in `de4a40e`.
- [x] Task 5: enforced hidden-recipe secrecy and queued feedback in `9e7fea9`.
- [x] Task 6: delivered and visually inspected all six functioning FX profiles, dormant links and discovery bursts in the final polish commit containing this record.
- [x] Task 7: completed regression, native-scene playtest, visual matrix and documentation in the final polish commit containing this record.

### Scope refinements from playtesting

- A functioning room now requires consumable inputs as well as power. One shared start-of-cycle budget prevents double-spending and keeps forecasts consistent with operation.
- Water recovery closes the Biodome progression dead end. All ten doctrine pairs include survival foundations, while doctrine-specific weighting remains.
- Added room suspension, a pausing learned-only journal, a scalable HUD, compact cards, scrollable inspector/summary, and optional post-victory expeditions with one-time rewards.
- Reduced persistent FX line/mote scale from the initial proposed values to keep room artwork and doors readable. Discovery bursts still provide a short stronger accent.
- Used native viewport capture through `playtest_polish.gd` instead of movie export. The harness covers paid builds and a two-step prototype chain, plus staged fixtures for six FX families and victory/expedition transitions.
- The design viewport is now 1920×1080, opening at 1600×900. Captures also cover 1280×720 and 2560×1440.
- Added an on-screen camera assertion after screenshot inspection caught large zoom changes centering against stale scroll bounds.

### Verification evidence

All 17 GDScript files in `scripts/` and `tests/` pass Godot 4.6.1 `--check-only`. The main-scene headless smoke test exits `0`. All four test processes exit `0`, with no `SCRIPT ERROR:` or `ERROR:` entries:

```text
Run-loop tests passed: links, cascades, all doctrine pairs, directives, deck flow, and mastery are valid.
Discovery progression tests passed.
Gameplay polish tests passed.
Scene playtest passed: paid builds, two discoveries, prototype reuse, suspension, journal input, responsive layout, expedition and reboot.
```

The three regression suites contain 47 test cases; the real-scene playtest adds integration assertions. Native-render runs at both 1600×900 and 2560×1440 passed and captured doctrine selection, unknown candidate, first discovery, stabilizing 2/3, decrypted prototype, expanded active station, dormant room, journal and victory summary. All six motion profiles and successive flow frames were inspected; separate 1280×720 and 1920×1080 layout checks passed. `git diff --check` is clean.

Reproduce from README's Verification section. Local capture folders are `%TEMP%\brinespace-polish-playtest` and `%TEMP%\brinespace-polish-playtest-2560`; logs use `%TEMP%\brinespace-verified-*` and `%TEMP%\brine-polish-visual-final-*`. Generated artifacts are not committed. Test saves use isolated paths and do not overwrite `brine_save.json`.

The implementation range is `a17a8bb..HEAD` on `codex/synergy-discovery`, including the final polish commit containing this record. The branch remains in its worktree pending the user's integration choice. Full-length random balance runs across all ten doctrine pairs and reduced-motion/colorblind options remain follow-up work, not completed claims.

## Global Constraints

- Undiscovered recipes never expose their name, room pairing, reward, or partner hint in player-facing UI.
- A functioning link requires orthogonal adjacency, matching doors, and both endpoint rooms powered during the current cycle.
- Stabilization is per recipe, advances at most once per cycle, resets when no copy functions, and completes after exactly three consecutive cycles.
- Discovery persists immediately; permanent blueprint unlocks persist immediately on stabilization and do not require run victory.
- A newly decrypted blueprint receives one current-run prototype even when the selected doctrines would normally exclude it.
- A reward room already present in an older save still stabilizes its recipe but does not inject a duplicate prototype.
- Existing saves remain additive: previously unlocked rooms are never revoked and missing stabilization fields load as empty.
- The first pass uses procedural FX only and adds no external runtime dependency.
- Production changes follow red-green-refactor: run each new test while failing, implement only enough to pass, then rerun the full relevant suite.
- Godot executable for verification: `C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe`.

---

## File Structure

- Create `scripts/discovery_manager.gd`: pure powered-link resolution, per-recipe cycle transitions, and authored unlock-graph validation.
- Modify `scripts/synergy_manager.gd`: add discovery/unlock/FX metadata and the missing authored recipes; return topology without mutating knowledge.
- Modify `scripts/room_database.gd`: replace the all-room clean-save unlock set with the twelve-room foundation set.
- Modify `scripts/meta_state.gd`: persist stabilized synergy IDs and expose an idempotent stabilization method.
- Modify `scripts/main.gd`: coordinate connected versus functioning links, apply discovery transitions, inject prototypes, queue feedback, enforce secrecy, and summarize run discoveries.
- Modify `scripts/grid_canvas.gd`: render hidden, dormant, and functioning states correctly with procedural endpoint and doorway effects.
- Create `tests/test_discovery_progression.gd`: focused graph, powered-link, stabilization, persistence, and prototype tests.
- Modify `tests/test_synergy_manager.gd`: migrate the existing topology expectations and rebalance doctrine-deck assertions for the smaller clean-save pool.
- Create `tests/capture_discovery_state.gd`: deterministic visual states for discovery, stabilization, dormant links, and prototype rewards.
- Modify `README.md` and `docs/DEVELOPMENT_NOTES.md`: document the discovery loop and its current content frontier.

---

### Task 0: Preserve the Existing Run-loop Baseline

**Files:**
- Verify: `scripts/main.gd`
- Verify: `scripts/run_manager.gd`
- Verify: `scripts/synergy_manager.gd`
- Verify: `scripts/grid_canvas.gd`
- Verify: `scripts/meta_state.gd`
- Verify: `tests/test_synergy_manager.gd`
- Commit: existing run-loop work currently present in the working tree

**Interfaces:**
- Consumes: the doctrine, finite-deck, directive, Resonance, mastery, and visual-harness work already in the workspace.
- Produces: a clean committed baseline so later task commits contain only discovery-progression changes.

- [ ] **Step 1: Run the existing regression suite**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$logPath = Join-Path $env:TEMP 'brinespace-baseline-tests.log'
$proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script','res://tests/test_synergy_manager.gd','--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
Get-Content -LiteralPath $logPath
if ($proc.ExitCode -ne 0) { throw "Baseline tests failed with exit code $($proc.ExitCode)" }
```

Expected: exit code `0` and `Run-loop tests passed`.

- [ ] **Step 2: Confirm only the known run-loop files are dirty**

```powershell
git status --short
git diff --check
```

Expected: modified `README.md`, `docs/DEVELOPMENT_NOTES.md`, `scripts/grid_canvas.gd`, `scripts/main.gd`, `scripts/meta_state.gd`, `scripts/synergy_manager.gd`, plus untracked `scripts/run_manager.gd` and `tests/`; no whitespace errors. Stop if any unrelated path appears.

- [ ] **Step 3: Commit the verified baseline**

```powershell
git add -- README.md docs/DEVELOPMENT_NOTES.md scripts/grid_canvas.gd scripts/main.gd scripts/meta_state.gd scripts/synergy_manager.gd scripts/run_manager.gd tests
git commit -m "Build doctrine-driven reconstruction runs"
```

Expected: one baseline commit; the approved spec and this plan remain separate documentation commits.

---

### Task 1: Author the Discovery Graph and Validate Reachability

**Files:**
- Create: `scripts/discovery_manager.gd`
- Modify: `scripts/synergy_manager.gd:5-155`
- Modify: `scripts/room_database.gd:31-62`
- Create: `tests/test_discovery_progression.gd`
- Modify: `tests/test_synergy_manager.gd:90-225`

**Interfaces:**
- Consumes: `RoomDatabase.all_rooms()`, `RoomDatabase.STARTING_UNLOCKS`, and `SynergyManager.all_synergies()`.
- Produces: `DiscoveryManager.validate_unlock_graph(all_rooms: Dictionary, synergies: Array, foundation_ids: Array) -> PackedStringArray`; recipe fields `unlock_room_id: String`, `stabilize_cycles: int`, `fx_profile: String`, `fx_color: String`, and optional `terminal_reward: Dictionary`.

- [ ] **Step 1: Write failing graph-contract tests**

Create `tests/test_discovery_progression.gd` with a `SceneTree` runner and these first tests:

```gdscript
extends SceneTree

const RoomDatabaseScript := preload("res://scripts/room_database.gd")
const SynergyManagerScript := preload("res://scripts/synergy_manager.gd")
const DiscoveryManagerScript := preload("res://scripts/discovery_manager.gd")

var failures := 0

func _init() -> void:
	_test_foundation_pool_is_intentionally_small()
	_test_every_recipe_has_progression_metadata()
	_test_unlock_graph_reaches_every_room()
	_test_reward_rooms_continue_or_end_explicitly()
	if failures > 0:
		push_error("Discovery progression tests failed: %d" % failures)
		quit(1)
		return
	print("Discovery progression tests passed.")
	quit(0)

func _test_foundation_pool_is_intentionally_small() -> void:
	var expected := [
		"solar_array", "reactor", "mining_drone_bay", "hydroponics_bay",
		"life_support", "crew_hab", "research_lab", "storage_bay",
		"med_bay", "quarantine_cell", "corridor", "corner"
	]
	_expect_equal(RoomDatabaseScript.STARTING_UNLOCKS, expected, "clean saves should begin with the authored foundation")

func _test_every_recipe_has_progression_metadata() -> void:
	for synergy_value in SynergyManagerScript.all_synergies():
		var synergy: Dictionary = synergy_value
		_expect_true(int(synergy.get("stabilize_cycles", 0)) == 3, "%s should stabilize in three cycles" % synergy.get("id", "missing"))
		_expect_true(not str(synergy.get("fx_profile", "")).is_empty(), "%s should define an FX profile" % synergy.get("id", "missing"))
		_expect_true(not str(synergy.get("fx_color", "")).is_empty(), "%s should define an FX color" % synergy.get("id", "missing"))
		var has_unlock := not str(synergy.get("unlock_room_id", "")).is_empty()
		var terminal_reward: Dictionary = synergy.get("terminal_reward", {})
		var has_terminal_reward := not terminal_reward.is_empty()
		_expect_true(has_unlock != has_terminal_reward, "%s should define exactly one stabilization reward" % synergy.get("id", "missing"))

func _test_unlock_graph_reaches_every_room() -> void:
	var errors := DiscoveryManagerScript.validate_unlock_graph(
		RoomDatabaseScript.all_rooms(),
		SynergyManagerScript.all_synergies(),
		RoomDatabaseScript.STARTING_UNLOCKS
	)
	_expect_equal(errors, PackedStringArray(), "the authored discovery graph should have no unreachable rooms")

func _test_reward_rooms_continue_or_end_explicitly() -> void:
	var recipe_rooms := {}
	for synergy_value in SynergyManagerScript.all_synergies():
		for room_id_value in synergy_value.get("rooms", []):
			recipe_rooms[str(room_id_value)] = true
	for synergy_value in SynergyManagerScript.all_synergies():
		var reward_id := str(synergy_value.get("unlock_room_id", ""))
		if not reward_id.is_empty():
			_expect_true(recipe_rooms.has(reward_id), "%s should participate in a later or terminal recipe" % reward_id)

func _expect_equal(actual, expected, message: String) -> void:
	if actual != expected:
		failures += 1
		push_error("%s: expected %s, got %s" % [message, str(expected), str(actual)])

func _expect_true(condition: bool, message: String) -> void:
	if not condition:
		failures += 1
		push_error(message)
```

- [ ] **Step 2: Run the new tests and verify RED**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$logPath = Join-Path $env:TEMP 'brinespace-discovery-red-graph.log'
$proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script','res://tests/test_discovery_progression.gd','--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
Get-Content -LiteralPath $logPath
if ($proc.ExitCode -eq 0) { throw 'Graph tests unexpectedly passed before implementation' }
```

Expected: failure because `scripts/discovery_manager.gd` and recipe progression metadata do not exist.

- [ ] **Step 3: Implement graph validation**

Create `scripts/discovery_manager.gd`:

```gdscript
extends RefCounted
class_name DiscoveryManager

static func validate_unlock_graph(all_rooms: Dictionary, synergies: Array, foundation_ids: Array) -> PackedStringArray:
	var errors := PackedStringArray()
	var reachable := {"brine_core": true}
	for id_value in foundation_ids:
		var room_id := str(id_value)
		if not all_rooms.has(room_id):
			errors.append("Unknown foundation room: %s" % room_id)
		else:
			reachable[room_id] = true
	for synergy_value in synergies:
		var synergy: Dictionary = synergy_value
		var reward_id := str(synergy.get("unlock_room_id", ""))
		if not reward_id.is_empty() and not all_rooms.has(reward_id):
			errors.append("Unknown unlock target: %s" % reward_id)
	var changed := true
	while changed:
		changed = false
		for synergy_value in synergies:
			var synergy: Dictionary = synergy_value
			var reward_id := str(synergy.get("unlock_room_id", ""))
			if reward_id.is_empty() or reachable.has(reward_id):
				continue
			var requirements_met := true
			for room_id_value in synergy.get("rooms", []):
				if not reachable.has(str(room_id_value)):
					requirements_met = false
					break
			if requirements_met:
				reachable[reward_id] = true
				changed = true
	for room_id_value in all_rooms:
		var room_id := str(room_id_value)
		if not reachable.has(room_id):
			errors.append("Unreachable room: %s" % room_id)
	return errors
```

- [ ] **Step 4: Author the foundation and recipe metadata**

Replace `RoomDatabase.STARTING_UNLOCKS` with the exact twelve IDs from the test. Add the eight missing recipes from the spec to `SynergyManager.SYNERGIES`: `clinical_airlock`, `ore_buffer`, `load_balancing`, `core_diagnostics`, `sterile_observation`, `signal_triangulation`, `genomic_triage`, and `impossible_model`.

Add one reward and FX definition to every recipe. The non-terminal mapping must be:

```gdscript
const DISCOVERY_UNLOCKS := {
	"closed_air_loop": "biodome",
	"green_commons": "crew_lounge",
	"field_clinic": "med_office",
	"clinical_airlock": "cryo_chamber",
	"logistics_spine": "maintenance_bay",
	"ore_buffer": "ore_refinery",
	"load_balancing": "battery_array",
	"core_diagnostics": "data_archive",
	"sterile_observation": "xeno_lab",
	"biodome_atmosphere": "bio_lab",
	"crew_commons": "med_center",
	"safe_wake_protocol": "clone_lab",
	"industrial_chain": "salvage_drone_bay",
	"stable_power_flow": "shield_generator",
	"research_pipeline": "radio_lab",
	"containment_sector": "anomaly_lab",
	"signal_triangulation": "command_center",
	"core_relay": "holographic_core"
}
```

Recipes absent from `DISCOVERY_UNLOCKS` receive `"terminal_reward": {"research": 3}`. Assign profiles by theme using only `flow`, `power`, `signal`, `care`, `containment`, or `logistics`; assign a six-digit hexadecimal `fx_color`; set `"stabilize_cycles": 3`.

- [ ] **Step 5: Update doctrine viability assertions**

In `tests/test_synergy_manager.gd`, keep testing all ten doctrine pairs but replace the fixed `deck.size() >= 16` assertion with these contracts:

```gdscript
_expect_true(deck.size() >= 10, "%s should have a playable clean-save deck" % pair_name)
_expect_true(deck.has("solar_array") and deck.has("mining_drone_bay"), "%s should retain power and Metal essentials" % pair_name)
for doctrine_id in pair:
	var copies_for_doctrine := 0
	for room_id_value in RunManagerScript.doctrine(doctrine_id).get("rooms", []):
		copies_for_doctrine += deck.count(str(room_id_value))
	_expect_true(copies_for_doctrine >= 2, "%s should expose a repeatable foothold for %s" % [pair_name, doctrine_id])
```

- [ ] **Step 6: Run graph and legacy tests and verify GREEN**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$scripts = @('res://tests/test_discovery_progression.gd','res://tests/test_synergy_manager.gd')
foreach ($script in $scripts) {
  $logPath = Join-Path $env:TEMP ("brinespace-graph-green-" + ($script -replace '[^A-Za-z0-9]', '_') + '.log')
  $proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script',$script,'--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
  Get-Content -LiteralPath $logPath
  if ($proc.ExitCode -ne 0) { throw "$script failed with exit code $($proc.ExitCode)" }
}
```

Expected: both scripts exit `0`; graph validation reports no unreachable room.

- [ ] **Step 7: Commit**

```powershell
git add -- scripts/discovery_manager.gd scripts/synergy_manager.gd scripts/room_database.gd tests/test_discovery_progression.gd tests/test_synergy_manager.gd
git commit -m "Author hidden synergy discovery graph"
```

---

### Task 2: Separate Connected Links from Powered Functioning Links

**Files:**
- Modify: `scripts/discovery_manager.gd`
- Modify: `scripts/synergy_manager.gd:155-230`
- Modify: `scripts/main.gd:140-180, 1510-1610, 1665-1725, 1765-1780, 2375-2410`
- Modify: `tests/test_discovery_progression.gd`
- Modify: `tests/test_synergy_manager.gd`

**Interfaces:**
- Consumes: candidate link dictionaries with `cells: Array[Vector2i]` and `id: String`; current `powered_room_cells: Dictionary`.
- Produces: `DiscoveryManager.functioning_links(connected_links: Array, powered_cells: Dictionary) -> Array`; runtime `connected_synergy_links: Array` and existing `active_synergy_links: Array` redefined as powered functioning links.

- [ ] **Step 1: Add failing powered-link tests**

Append to `tests/test_discovery_progression.gd` and invoke both tests from `_init()`:

```gdscript
func _test_both_endpoints_are_required_for_functioning() -> void:
	var link := {"id": "closed_air_loop", "cells": [Vector2i(1, 1), Vector2i(2, 1)], "bonus": {"oxygen": 1}}
	var one_powered := {Vector2i(1, 1): true}
	_expect_equal(DiscoveryManagerScript.functioning_links([link], one_powered).size(), 0, "one powered endpoint should leave a link dormant")
	var both_powered := {Vector2i(1, 1): true, Vector2i(2, 1): true}
	_expect_equal(DiscoveryManagerScript.functioning_links([link], both_powered).size(), 1, "two powered endpoints should activate a link")

func _test_only_functioning_links_contribute_cycle_bonuses() -> void:
	var active := [{"id": "closed_air_loop", "cells": [Vector2i.ZERO, Vector2i.RIGHT], "bonus": {"oxygen": 1}}]
	_expect_equal(SynergyManagerScript.cycle_bonus(active), {"oxygen": 1}, "active links should contribute their authored bonus")
	_expect_equal(SynergyManagerScript.cycle_bonus([]), {}, "dormant links should contribute no bonus")
```

- [ ] **Step 2: Run the focused tests and verify RED**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$logPath = Join-Path $env:TEMP 'brinespace-discovery-red-power.log'
$proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script','res://tests/test_discovery_progression.gd','--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
Get-Content -LiteralPath $logPath
if ($proc.ExitCode -eq 0) { throw 'Powered-link tests unexpectedly passed before implementation' }
```

Expected: failure because `DiscoveryManager.functioning_links` is undefined.

- [ ] **Step 3: Implement powered-link filtering**

Add to `scripts/discovery_manager.gd`:

```gdscript
static func functioning_links(connected_links: Array, powered_cells: Dictionary) -> Array:
	var functioning := []
	for link_value in connected_links:
		var link: Dictionary = link_value
		var cells: Array = link.get("cells", [])
		if cells.size() >= 2 and powered_cells.has(cells[0]) and powered_cells.has(cells[1]):
			functioning.append(link)
	return functioning
```

- [ ] **Step 4: Split main runtime state and gate cycle bonuses**

In `scripts/main.gd`:

```gdscript
var connected_synergy_links := []
var active_synergy_links := []
```

Change `_check_synergies()` to populate topology only:

```gdscript
func _check_synergies() -> void:
	var result := SynergyManagerScript.evaluate(placed_rooms, occupied)
	connected_synergy_links = result.get("links", [])
```

After room power allocation and before `SynergyManager.cycle_bonus(...)` in `_apply_room_economy()`, set:

```gdscript
active_synergy_links = DiscoveryManagerScript.functioning_links(connected_synergy_links, powered_room_cells)
active_synergies.clear()
for link_value in active_synergy_links:
	var link: Dictionary = link_value
	active_synergies[str(link.get("id", ""))] = link
```

Use `connected_synergy_links` for placement-cascade detection and link-key snapshots. Keep directive metrics, Resonance tooltip active count, projected cycle bonuses, and actual cycle bonuses on `active_synergy_links`.

Remove discovery writes from `SynergyManager.evaluate`; update existing topology tests to call `evaluate(placed_rooms, occupied)` without a discovered dictionary.

- [ ] **Step 5: Run focused and legacy tests and verify GREEN**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$scripts = @('res://tests/test_discovery_progression.gd','res://tests/test_synergy_manager.gd')
foreach ($script in $scripts) {
  $logPath = Join-Path $env:TEMP ("brinespace-power-green-" + ($script -replace '[^A-Za-z0-9]', '_') + '.log')
  $proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script',$script,'--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
  Get-Content -LiteralPath $logPath
  if ($proc.ExitCode -ne 0) { throw "$script failed with exit code $($proc.ExitCode)" }
}
```

Expected: both suites exit `0`; disconnected topology still does not score and dormant links produce no resources.

- [ ] **Step 6: Commit**

```powershell
git add -- scripts/discovery_manager.gd scripts/synergy_manager.gd scripts/main.gd tests/test_discovery_progression.gd tests/test_synergy_manager.gd
git commit -m "Gate synergy effects behind powered links"
```

---

### Task 3: Resolve Discovery and Three-cycle Stabilization

**Files:**
- Modify: `scripts/discovery_manager.gd`
- Modify: `scripts/main.gd:125-180, 1335-1405, 1545-1565, 1665-1810`
- Modify: `tests/test_discovery_progression.gd`

**Interfaces:**
- Consumes: powered `active_synergy_links`, previous run-local progress, discovered IDs, stabilized IDs.
- Produces: `DiscoveryManager.advance_cycle(active_links: Array, previous_progress: Dictionary, discovered_ids: Dictionary, stabilized_ids: Dictionary) -> Dictionary` returning `progress`, `new_discovery_ids`, `new_stabilization_ids`, and `active_ids`.

- [ ] **Step 1: Add failing transition tests**

Append and invoke these tests:

```gdscript
func _test_first_functioning_cycle_discovers_and_starts_progress() -> void:
	var link := _test_link("closed_air_loop")
	var result := DiscoveryManagerScript.advance_cycle([link], {}, {}, {})
	_expect_equal(result["new_discovery_ids"], ["closed_air_loop"], "first functioning cycle should discover the recipe")
	_expect_equal(int(result["progress"].get("closed_air_loop", 0)), 1, "discovery cycle should count as cycle one")

func _test_duplicate_links_advance_once_and_stabilize_on_three() -> void:
	var first := _test_link("closed_air_loop")
	var second := _test_link("closed_air_loop", Vector2i(4, 4))
	var discovered := {"closed_air_loop": true}
	var cycle_two := DiscoveryManagerScript.advance_cycle([first, second], {"closed_air_loop": 1}, discovered, {})
	_expect_equal(int(cycle_two["progress"]["closed_air_loop"]), 2, "duplicate copies should advance one cycle")
	var cycle_three := DiscoveryManagerScript.advance_cycle([first, second], cycle_two["progress"], discovered, {})
	_expect_equal(cycle_three["new_stabilization_ids"], ["closed_air_loop"], "third consecutive cycle should stabilize once")

func _test_inactive_cycle_resets_unfinished_progress() -> void:
	var result := DiscoveryManagerScript.advance_cycle([], {"closed_air_loop": 2}, {"closed_air_loop": true}, {})
	_expect_equal(int(result["progress"].get("closed_air_loop", 0)), 0, "losing every functioning copy should reset progress")

func _test_link(id: String, origin := Vector2i.ZERO) -> Dictionary:
	for synergy_value in SynergyManagerScript.all_synergies():
		if str(synergy_value.get("id", "")) == id:
			var link: Dictionary = synergy_value.duplicate(true)
			link["cells"] = [origin, origin + Vector2i.RIGHT]
			return link
	return {}
```

- [ ] **Step 2: Run and verify RED**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$logPath = Join-Path $env:TEMP 'brinespace-discovery-red-stabilization.log'
$proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script','res://tests/test_discovery_progression.gd','--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
Get-Content -LiteralPath $logPath
if ($proc.ExitCode -eq 0) { throw 'Stabilization tests unexpectedly passed before implementation' }
```

Expected: failure because `DiscoveryManager.advance_cycle` is undefined.

- [ ] **Step 3: Implement the pure cycle transition**

Add to `scripts/discovery_manager.gd`:

```gdscript
static func advance_cycle(active_links: Array, previous_progress: Dictionary, discovered_ids: Dictionary, stabilized_ids: Dictionary) -> Dictionary:
	var active_by_id := {}
	for link_value in active_links:
		var link: Dictionary = link_value
		active_by_id[str(link.get("id", ""))] = link
	var progress := previous_progress.duplicate(true)
	var new_discoveries: Array[String] = []
	var new_stabilizations: Array[String] = []
	for id_value in progress.keys():
		var id := str(id_value)
		if not active_by_id.has(id) and not stabilized_ids.has(id):
			progress[id] = 0
	for id_value in active_by_id:
		var id := str(id_value)
		var link: Dictionary = active_by_id[id]
		if not discovered_ids.has(id):
			new_discoveries.append(id)
		if stabilized_ids.has(id):
			continue
		var next_progress := int(progress.get(id, 0)) + 1
		progress[id] = next_progress
		if next_progress >= int(link.get("stabilize_cycles", 3)):
			new_stabilizations.append(id)
	return {
		"progress": progress,
		"new_discovery_ids": new_discoveries,
		"new_stabilization_ids": new_stabilizations,
		"active_ids": active_by_id.keys()
	}
```

- [ ] **Step 4: Integrate one transition per game cycle**

Preload `DiscoveryManagerScript` in `main.gd`, add:

```gdscript
var synergy_stabilization_progress := {}
var run_discovered_synergy_ids: Array[String] = []
var run_stabilized_synergy_ids: Array[String] = []
```

Reset all three in `_start_reboot_cycle()`. After `_apply_room_economy()` has assigned functioning links and bonuses, call `_advance_synergy_discovery_cycle()` exactly once:

```gdscript
func _advance_synergy_discovery_cycle() -> void:
	var transition := DiscoveryManagerScript.advance_cycle(
		active_synergy_links,
		synergy_stabilization_progress,
		meta.discovered_synergy_ids,
		meta.stabilized_synergy_ids
	)
	synergy_stabilization_progress = transition["progress"]
	for id_value in transition["new_discovery_ids"]:
		_handle_synergy_discovery(str(id_value))
	for id_value in transition["new_stabilization_ids"]:
		_handle_synergy_stabilization(str(id_value))
```

At this task boundary, `_handle_synergy_discovery` persists discovery, records the run ID once, logs the authored effect, and uses the existing center toast. `_handle_synergy_stabilization` records the run ID once and logs completion; blueprint rewards are added in Task 4.

Placement cascades must use `UNRESOLVED PATTERN` for any new connected link whose ID is absent from `meta.discovered_synergy_ids`. Known links may use their authored names.

- [ ] **Step 5: Run the focused and legacy suites and verify GREEN**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$scripts = @('res://tests/test_discovery_progression.gd','res://tests/test_synergy_manager.gd')
foreach ($script in $scripts) {
  $logPath = Join-Path $env:TEMP ("brinespace-stabilization-green-" + ($script -replace '[^A-Za-z0-9]', '_') + '.log')
  $proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script',$script,'--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
  Get-Content -LiteralPath $logPath
  if ($proc.ExitCode -ne 0) { throw "$script failed with exit code $($proc.ExitCode)" }
}
```

Expected: both suites exit `0`; discovery begins at `1/3`, duplicates advance once, and inactive progress resets.

- [ ] **Step 6: Commit**

```powershell
git add -- scripts/discovery_manager.gd scripts/main.gd tests/test_discovery_progression.gd tests/test_synergy_manager.gd
git commit -m "Add powered synergy stabilization cycles"
```

---

### Task 4: Persist Stabilization and Inject Prototype Blueprints

**Files:**
- Modify: `scripts/meta_state.gd:5-115`
- Modify: `scripts/main.gd:125-180, 1335-1425, 1785-1905, 2540-2820`
- Modify: `tests/test_discovery_progression.gd`

**Interfaces:**
- Consumes: newly stabilized recipe IDs and recipe reward metadata.
- Produces: `MetaState.stabilize_synergy(id: String) -> bool`, persisted `stabilized_synergy_ids`, `_award_synergy_stabilization(synergy: Dictionary) -> void`, `run_decrypted_blueprint_ids: Array[String]`, `prototype_card_seen_cycle: Dictionary`, `_clear_prototype_marker(id: String) -> void`, and `_expire_prototype_markers() -> void`.

- [ ] **Step 1: Add failing persistence, reward, and clean-chain tests**

Append and invoke these tests:

```gdscript
const MetaStateScript := preload("res://scripts/meta_state.gd")
const MainScript := preload("res://scripts/main.gd")

func _test_stabilization_persists_idempotently() -> void:
	var save_path := "user://brine_discovery_meta_test.json"
	var meta = MetaStateScript.new()
	meta.save_path = save_path
	meta.stabilized_synergy_ids.clear()
	_expect_true(meta.stabilize_synergy("closed_air_loop"), "first stabilization should persist")
	_expect_true(not meta.stabilize_synergy("closed_air_loop"), "repeat stabilization should not reward twice")
	var loaded = MetaStateScript.new()
	loaded.save_path = save_path
	loaded.stabilized_synergy_ids.clear()
	loaded.load_from_disk()
	_expect_true(loaded.stabilized_synergy_ids.has("closed_air_loop"), "stabilization should survive reload")
	if FileAccess.file_exists(save_path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(save_path))

func _test_old_save_without_stabilization_loads_additively() -> void:
	var save_path := "user://brine_old_save_test.json"
	var file := FileAccess.open(save_path, FileAccess.WRITE)
	file.store_string(JSON.stringify({
		"unlocked_room_ids": ["biodome"],
		"discovered_synergy_ids": ["closed_air_loop"]
	}))
	file.close()
	var meta = MetaStateScript.new()
	meta.save_path = save_path
	meta.stabilized_synergy_ids.clear()
	meta.load_from_disk()
	_expect_true(meta.unlocked_room_ids.has("biodome"), "older unlocked rooms should remain unlocked")
	_expect_true(meta.discovered_synergy_ids.has("closed_air_loop"), "older discoveries should remain learned")
	_expect_equal(meta.stabilized_synergy_ids, {}, "a missing stabilization field should load as empty")
	if FileAccess.file_exists(save_path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(save_path))

func _test_blueprint_reward_unlocks_and_becomes_next_draw() -> void:
	var game = MainScript.new()
	var save_path := "user://brine_prototype_test.json"
	game.meta.save_path = save_path
	game.meta.stabilized_synergy_ids.erase("closed_air_loop")
	game.meta.unlocked_room_ids.erase("biodome")
	game.draw_pile.clear()
	game.discard_pile.assign(["corridor"])
	game._award_synergy_stabilization(_test_link("closed_air_loop"))
	_expect_true(game.meta.unlocked_room_ids.has("biodome"), "stabilization should unlock the authored blueprint")
	_expect_equal(game.draw_pile.back(), "biodome", "prototype should be the next card drawn")
	_expect_equal(game.run_decrypted_blueprint_ids, ["biodome"], "run summary should record the decrypt")
	game._refill_hand()
	_expect_equal(game.hand[0], "biodome", "an empty draw pile should yield the prototype before discard reshuffling")
	game.free()
	if FileAccess.file_exists(save_path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(save_path))

func _test_already_unlocked_reward_does_not_inject_a_duplicate_prototype() -> void:
	var save_path := "user://brine_existing_unlock_test.json"
	var game = MainScript.new()
	game.meta.save_path = save_path
	game.meta.stabilized_synergy_ids.erase("closed_air_loop")
	game.meta.unlocked_room_ids["biodome"] = true
	game.draw_pile.assign(["corridor"])
	game._award_synergy_stabilization(_test_link("closed_air_loop"))
	_expect_true(game.meta.stabilized_synergy_ids.has("closed_air_loop"), "the recipe should still stabilize")
	_expect_equal(game.draw_pile.count("biodome"), 0, "an older unlock should not inject a duplicate prototype")
	game.free()
	if FileAccess.file_exists(save_path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(save_path))

func _test_terminal_stabilization_grants_research_once() -> void:
	var save_path := "user://brine_terminal_reward_test.json"
	var game = MainScript.new()
	game.meta.save_path = save_path
	game.meta.stabilized_synergy_ids.erase("drone_foundry")
	var research_before := game.meta.total_research_points
	game._award_synergy_stabilization(_test_link("drone_foundry"))
	game._award_synergy_stabilization(_test_link("drone_foundry"))
	_expect_equal(game.meta.total_research_points, research_before + 3, "terminal Research should be awarded exactly once")
	game.free()
	if FileAccess.file_exists(save_path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(save_path))

func _test_prototype_marker_survives_one_full_cycle_or_clears_on_selection() -> void:
	var game = MainScript.new()
	game.prototype_card_seen_cycle = {"biodome": 4}
	game.cycle = 5
	game._expire_prototype_markers()
	_expect_true(game.prototype_card_seen_cycle.has("biodome"), "the NEW marker should survive one full following cycle")
	game.cycle = 6
	game._expire_prototype_markers()
	_expect_true(not game.prototype_card_seen_cycle.has("biodome"), "the NEW marker should expire after that following cycle")
	game.prototype_card_seen_cycle["biodome"] = 6
	game._clear_prototype_marker("biodome")
	_expect_true(not game.prototype_card_seen_cycle.has("biodome"), "selecting the prototype should clear its NEW marker")
	game.free()

func _test_three_functioning_cycles_complete_the_clean_unlock_chain() -> void:
	var save_path := "user://brine_clean_chain_test.json"
	var game = MainScript.new()
	game.meta.save_path = save_path
	game.meta.discovered_synergy_ids.erase("closed_air_loop")
	game.meta.stabilized_synergy_ids.erase("closed_air_loop")
	game.meta.unlocked_room_ids.erase("biodome")
	game.draw_pile.assign(["corridor"])
	game.active_synergy_links = [_test_link("closed_air_loop")]
	for _cycle_index in range(3):
		game._advance_synergy_discovery_cycle()
	_expect_true(game.meta.discovered_synergy_ids.has("closed_air_loop"), "the recipe should be learned")
	_expect_true(game.meta.stabilized_synergy_ids.has("closed_air_loop"), "the recipe should be stabilized")
	_expect_true(game.meta.unlocked_room_ids.has("biodome"), "Biodome should be permanent")
	_expect_true(game.draw_pile.has("biodome"), "the current run should contain a Biodome prototype")
	_expect_equal(game.run_discovered_synergy_ids.count("closed_air_loop"), 1, "discovery should be recorded once")
	_expect_equal(game.run_stabilized_synergy_ids.count("closed_air_loop"), 1, "stabilization should be recorded once")
	game.free()
	if FileAccess.file_exists(save_path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(save_path))
```

- [ ] **Step 2: Run and verify RED**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$logPath = Join-Path $env:TEMP 'brinespace-discovery-red-prototype.log'
$proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script','res://tests/test_discovery_progression.gd','--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
Get-Content -LiteralPath $logPath
if ($proc.ExitCode -eq 0) { throw 'Prototype tests unexpectedly passed before implementation' }
```

Expected: failure because stabilized meta state, backward-compatible loading, prototype and terminal rewards, and the full three-cycle reward boundary do not exist yet.

- [ ] **Step 3: Persist stabilized recipe IDs**

In `scripts/meta_state.gd` add:

```gdscript
var stabilized_synergy_ids := {}

func stabilize_synergy(id: String) -> bool:
	if stabilized_synergy_ids.has(id):
		return false
	stabilized_synergy_ids[id] = true
	save_to_disk()
	return true
```

Serialize `stabilized_synergy_ids.keys()` and load it with an empty-array default. Do not clear existing `unlocked_room_ids` during load, preserving older saves.

- [ ] **Step 4: Award blueprints and terminal Research**

In `main.gd` add and reset `run_decrypted_blueprint_ids` and `prototype_card_seen_cycle`. Implement:

```gdscript
func _award_synergy_stabilization(synergy: Dictionary) -> void:
	var synergy_id := str(synergy.get("id", ""))
	if not meta.stabilize_synergy(synergy_id):
		return
	if not run_stabilized_synergy_ids.has(synergy_id):
		run_stabilized_synergy_ids.append(synergy_id)
	var unlock_id := str(synergy.get("unlock_room_id", ""))
	if not unlock_id.is_empty():
		if meta.unlock_room(unlock_id):
			draw_pile.append(unlock_id)
			prototype_card_seen_cycle[unlock_id] = -1
			run_decrypted_blueprint_ids.append(unlock_id)
			_queue_center_toast("BLUEPRINT DECRYPTED\n%s" % RoomDatabaseScript.get_room(unlock_id).get("display_name", unlock_id))
		return
	var terminal_reward: Dictionary = synergy.get("terminal_reward", {})
	var research := int(terminal_reward.get("research", 0))
	if research > 0:
		meta.add_research_points(research)
		_queue_center_toast("PATTERN STABILIZED\n+%d RESEARCH" % research)
```

Change `_handle_synergy_stabilization` to fetch the recipe by ID and call this method. Add `SynergyManager.get_synergy(id: String) -> Dictionary` as a public lookup replacing the private `_get_synergy` use.

- [ ] **Step 5: Mark the prototype when it first enters the hand**

In `_refill_hand()`, after appending a drawn ID:

```gdscript
if prototype_card_seen_cycle.has(id) and int(prototype_card_seen_cycle[id]) < 0:
	prototype_card_seen_cycle[id] = cycle
```

Add the small lifecycle methods and call `_clear_prototype_marker(id)` from `_on_card_pressed()`. At the end of `_advance_cycle()`, call `_expire_prototype_markers()` so the marker survives the cycle in which the card first appears and one full following cycle:

```gdscript
func _clear_prototype_marker(id: String) -> void:
	prototype_card_seen_cycle.erase(id)

func _expire_prototype_markers() -> void:
	for room_id_value in prototype_card_seen_cycle.keys():
		var room_id := str(room_id_value)
		var first_seen_cycle := int(prototype_card_seen_cycle[room_id])
		if first_seen_cycle >= 0 and cycle > first_seen_cycle + 1:
			prototype_card_seen_cycle.erase(room_id)
```

The card-rendering label is added in Task 5.

- [ ] **Step 6: Extend victory and failure summaries**

Add these lines to `_show_reboot_summary()` using revealed display names:

```text
Patterns discovered: <names or None>
Patterns stabilized: <names or None>
Blueprints decrypted: <room display names or None>
```

Ensure meta writes occur before summary text is assembled so a stabilization on the terminal cycle appears immediately.

- [ ] **Step 7: Run tests and verify GREEN**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$scripts = @('res://tests/test_discovery_progression.gd','res://tests/test_synergy_manager.gd')
foreach ($script in $scripts) {
  $logPath = Join-Path $env:TEMP ("brinespace-prototype-green-" + ($script -replace '[^A-Za-z0-9]', '_') + '.log')
  $proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script',$script,'--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
  Get-Content -LiteralPath $logPath
  if ($proc.ExitCode -ne 0) { throw "$script failed with exit code $($proc.ExitCode)" }
}
```

Expected: both suites exit `0`; first stabilization persists, old saves remain additive, new unlocks become the next draw, old unlocks do not inject duplicate prototypes, and terminal Research is idempotent.

- [ ] **Step 8: Commit**

```powershell
git add -- scripts/meta_state.gd scripts/main.gd scripts/synergy_manager.gd tests/test_discovery_progression.gd tests/test_synergy_manager.gd
git commit -m "Unlock prototype blueprints from stabilized patterns"
```

---

### Task 5: Enforce UI Secrecy and Queue Discovery Feedback

**Files:**
- Modify: `scripts/main.gd:205-240, 420-455, 1715-1765, 2200-2320, 2600-3340`
- Modify: `tests/test_discovery_progression.gd`

**Interfaces:**
- Consumes: discovered and stabilized meta dictionaries, run-local stabilization progress, prototype markers.
- Produces: `_synergy_display_name(id: String) -> String`, `_card_synergy_hint(room_id: String) -> String` with no unknown-recipe leak, `_queue_center_toast(message: String) -> void`, and `_play_next_center_toast() -> void`.

- [ ] **Step 1: Add failing secrecy and queue-order tests**

Append and invoke:

```gdscript
func _test_unknown_card_hint_never_names_partner_or_recipe() -> void:
	var game = MainScript.new()
	game.meta.discovered_synergy_ids.clear()
	var hint := game._card_synergy_hint("hydroponics_bay")
	_expect_true(not hint.contains("Life Support"), "unknown hint should not name a partner")
	_expect_true(not hint.contains("Closed Air Loop"), "unknown hint should not name a recipe")
	_expect_true(hint.contains("EXPERIMENTAL"), "unknown hint should use universal experimental wording")
	game.free()

func _test_known_card_hint_may_name_learned_recipe() -> void:
	var game = MainScript.new()
	game.meta.discovered_synergy_ids = {"closed_air_loop": true}
	var hint := game._card_synergy_hint("hydroponics_bay")
	_expect_true(hint.contains("Closed Air Loop"), "learned recipe may appear on its room card")
	game.free()

func _test_cascade_name_stays_generic_until_discovery() -> void:
	var game = MainScript.new()
	game.meta.discovered_synergy_ids.clear()
	_expect_equal(game._synergy_display_name("closed_air_loop"), "UNRESOLVED PATTERN", "candidate cascades must not reveal unknown recipe names")
	game.meta.discovered_synergy_ids["closed_air_loop"] = true
	_expect_equal(game._synergy_display_name("closed_air_loop"), "Closed Air Loop", "known cascades may use the learned recipe name")
	game.free()

func _test_toast_queue_preserves_discovery_order() -> void:
	var game = MainScript.new()
	game.toast_playing = true
	game._queue_center_toast("PATTERN DISCOVERED\nFIRST")
	game._queue_center_toast("PATTERN DISCOVERED\nSECOND")
	_expect_equal(game.toast_messages, ["PATTERN DISCOVERED\nFIRST", "PATTERN DISCOVERED\nSECOND"], "simultaneous discoveries should retain their order")
	game.free()
```

- [ ] **Step 2: Run and verify RED**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$logPath = Join-Path $env:TEMP 'brinespace-discovery-red-ui.log'
$proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script','res://tests/test_discovery_progression.gd','--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
Get-Content -LiteralPath $logPath
if ($proc.ExitCode -eq 0) { throw 'UI secrecy tests unexpectedly passed before implementation' }
```

Expected: failure because the dedicated safe hint and feedback queue APIs do not exist.

- [ ] **Step 3: Centralize safe recipe text**

Implement `_synergy_display_name(id)` so unknown IDs return `UNRESOLVED PATTERN`, and use it anywhere placement cascades or logs could name a candidate. Implement `_card_synergy_hint(room_id)` so it filters `SynergyManager.all_synergies()` by `meta.discovered_synergy_ids` before reading names or partner rooms. If no learned recipe exists, return exactly:

```text
LINK  EXPERIMENTAL CONFIGURATION
```

Use this same generic line for every room while at least one recipe remains undiscovered. Update card rendering and inspector rendering to call the safe helper rather than reading raw recipe names.

Archive behavior:

- list discovered recipes only;
- append `STABILIZING n/3`, `STABILIZED`, or `DORMANT` based on runtime/meta state;
- show one aggregate `UNKNOWN PATTERNS REMAIN: n` line;
- never show an unknown recipe as its own row.

- [ ] **Step 4: Queue centered feedback instead of overwriting it**

Add:

```gdscript
var toast_messages: Array[String] = []
var toast_playing := false

func _queue_center_toast(message: String) -> void:
	toast_messages.append(message)
	if not toast_playing:
		_play_next_center_toast()

func _play_next_center_toast() -> void:
	if toast_messages.is_empty():
		toast_playing = false
		return
	toast_playing = true
	_show_center_toast(toast_messages.pop_front())
```

Replace the final tween callback with a method that hides the panel, clears `toast_playing`, and starts the next queued message. Route cascade, discovery, directive, stabilization, and blueprint messages through `_queue_center_toast`.

- [ ] **Step 5: Add revealed progress and prototype card treatment**

For a discovered recipe touching the selected room, show:

```text
Closed Air Loop · ACTIVE · STABILIZING 2/3
```

For a discovered connected but unpowered recipe, show:

```text
Closed Air Loop · DORMANT · POWER BOTH ROOMS
```

Add `NEW PROTOTYPE` to a card only while `prototype_card_seen_cycle` contains that room ID. Selecting the card removes the marker.

- [ ] **Step 6: Run tests and verify GREEN**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$scripts = @('res://tests/test_discovery_progression.gd','res://tests/test_synergy_manager.gd')
foreach ($script in $scripts) {
  $logPath = Join-Path $env:TEMP ("brinespace-ui-green-" + ($script -replace '[^A-Za-z0-9]', '_') + '.log')
  $proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script',$script,'--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
  Get-Content -LiteralPath $logPath
  if ($proc.ExitCode -ne 0) { throw "$script failed with exit code $($proc.ExitCode)" }
}
```

Expected: both suites exit `0`; no unknown partner or recipe name appears in tested card text.

- [ ] **Step 7: Commit**

```powershell
git add -- scripts/main.gd tests/test_discovery_progression.gd tests/test_synergy_manager.gd
git commit -m "Reveal synergy knowledge through play"
```

---

### Task 6: Render Persistent Functioning-room Effects

**Files:**
- Modify: `scripts/grid_canvas.gd:350-700`
- Modify: `scripts/main.gd:165-185, 2930-2990`
- Create: `tests/capture_discovery_state.gd`

**Interfaces:**
- Consumes: `main.connected_synergy_links`, `main.active_synergy_links`, `main.meta.discovered_synergy_ids`, recipe `fx_profile`, recipe `fx_color`, and `main.visual_time_seconds`.
- Produces: dormant learned link lines, powered animated doorway flows, and endpoint room-edge accents; unknown candidates remain invisible.

- [ ] **Step 1: Create a deterministic visual harness before rendering changes**

Create `tests/capture_discovery_state.gd` that accepts `--state=<name>` from `OS.get_cmdline_user_args()` and stages these exact states:

```gdscript
extends SceneTree

const MainScene := preload("res://scenes/main.tscn")
const DiscoveryManagerScript := preload("res://scripts/discovery_manager.gd")

func _init() -> void:
	call_deferred("_stage")

func _stage() -> void:
	var game = MainScene.instantiate()
	root.add_child(game)
	current_scene = game
	await process_frame
	game.testing_free_build = true
	game.meta.save_path = "user://brine_discovery_visual_test.json"
	game.meta.discovered_synergy_ids.clear()
	game.meta.stabilized_synergy_ids.clear()
	game.pending_doctrines.assign(["biosphere", "recovery"])
	game._confirm_doctrines()
	game._place_room("life_support", Vector2i(19, 20), true)
	game._place_room("hydroponics_bay", Vector2i(18, 20), true)
	for room_value in game.placed_rooms:
		game.powered_room_cells[room_value["pos"]] = true
	game.active_synergy_links = DiscoveryManagerScript.functioning_links(game.connected_synergy_links, game.powered_room_cells)
	var state := "active"
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--state="):
			state = argument.trim_prefix("--state=")
	match state:
		"unknown":
			game.meta.discovered_synergy_ids.erase("closed_air_loop")
		"dormant":
			game.meta.discovered_synergy_ids["closed_air_loop"] = true
			game.active_synergy_links.clear()
		"stabilizing":
			game.meta.discovered_synergy_ids["closed_air_loop"] = true
			game.synergy_stabilization_progress["closed_air_loop"] = 2
		"active":
			game.meta.discovered_synergy_ids["closed_air_loop"] = true
			game.meta.stabilized_synergy_ids["closed_air_loop"] = true
	game._refresh_all()
	game._center_grid_on_station_deferred()
	if FileAccess.file_exists(game.meta.save_path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(game.meta.save_path))
```

Run the `unknown` and `active` captures now. Expected before implementation: the states are visually indistinguishable or reveal the existing generic line, demonstrating the missing effect-state distinction.

- [ ] **Step 2: Render learned dormant links only**

In `_draw_synergy_links(main)`, iterate `main.connected_synergy_links`. Skip a link unless `main.meta.discovered_synergy_ids` contains its ID. If it is absent from `main.active_synergy_links`, draw one static line in its `fx_color` at alpha `0.18` and do not draw motes or endpoint glow.

- [ ] **Step 3: Render functioning profile effects**

For active links:

- draw a shared-door pulse using `0.55 + sin(main.visual_time_seconds * 4.0) * 0.2` alpha;
- draw two room-edge segments facing the shared doorway;
- draw two traveling motes along the center-to-center line with phase offsets `0.0` and `0.5`;
- use line width `max(2.0, cell_size * 0.018)` and mote radius `max(3.0, cell_size * 0.025)`;
- use `fx_profile` to vary motion: continuous for `flow`, stepped for `logistics`, fast for `power`, scanning for `signal`, mirrored for `care`, and alternating segments for `containment`.

Keep effects below placement holograms and above room textures. Do not draw a persistent effect for an unknown candidate.

- [ ] **Step 4: Add a one-time discovery burst**

In `main.gd`, store `discovery_bursts` as dictionaries containing `cells`, `color`, and `remaining` seconds. `_handle_synergy_discovery` appends one burst per newly discovered recipe using the first functioning link. `_process(delta)` reduces `remaining` and removes expired bursts. `grid_canvas.gd` draws expanding endpoint rings and a bright shared-door flash while `remaining > 0`.

- [ ] **Step 5: Capture and inspect all representative states**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$captureRoot = Join-Path $env:TEMP ("brinespace-discovery-fx-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $captureRoot | Out-Null
foreach ($state in @('unknown','dormant','stabilizing','active')) {
  $pattern = Join-Path $captureRoot ($state + '.png')
  $logPath = Join-Path $captureRoot ($state + '.log')
  $proc = Start-Process -FilePath $godotExe -ArgumentList @('--path','.','--fixed-fps','4','--write-movie',$pattern,'--quit-after','4','--script','res://tests/capture_discovery_state.gd','--log-file',$logPath,'--','--state=' + $state) -Wait -PassThru -WindowStyle Hidden
  Get-Content -LiteralPath $logPath
  if ($proc.ExitCode -ne 0) { throw "$state capture failed with exit code $($proc.ExitCode)" }
}
Get-ChildItem -LiteralPath $captureRoot -Filter '*.png' | Sort-Object Name
```

Inspect the last frame of each state. Required findings: unknown has no recipe line; dormant is visible but quiet; stabilizing and active effects are readable over every room category; the center playfield remains unobstructed; no effect covers card text or the objective panel.

- [ ] **Step 6: Run regression tests and parse checks**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$scripts = @('res://scripts/main.gd','res://scripts/grid_canvas.gd','res://tests/capture_discovery_state.gd')
foreach ($script in $scripts) {
  $logPath = Join-Path $env:TEMP ("brinespace-fx-parse-" + ($script -replace '[^A-Za-z0-9]', '_') + '.log')
  $proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--check-only','--script',$script,'--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
  Get-Content -LiteralPath $logPath
  if ($proc.ExitCode -ne 0) { throw "$script failed parse check" }
}
foreach ($testScript in @('res://tests/test_discovery_progression.gd','res://tests/test_synergy_manager.gd')) {
  $logPath = Join-Path $env:TEMP ("brinespace-fx-tests-" + ($testScript -replace '[^A-Za-z0-9]', '_') + '.log')
  $proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script',$testScript,'--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
  Get-Content -LiteralPath $logPath
  if ($proc.ExitCode -ne 0) { throw "$testScript failed" }
}
```

Expected: all parse and test processes exit `0`; capture logs contain no engine errors.

- [ ] **Step 7: Commit**

```powershell
git add -- scripts/main.gd scripts/grid_canvas.gd tests/capture_discovery_state.gd
git commit -m "Visualize functioning room synergies"
```

---

### Task 7: Complete End-to-end Progression Verification and Documentation

**Files:**
- Modify: `tests/test_discovery_progression.gd`
- Modify: `tests/capture_discovery_state.gd`
- Modify: `README.md`
- Modify: `docs/DEVELOPMENT_NOTES.md`

**Interfaces:**
- Consumes: the complete hidden discovery, powered effect, stabilization, save, and prototype flow.
- Produces: one clean-save end-to-end regression and current project documentation.

- [ ] **Step 1: Re-run the retained clean-chain regression**

The test added before Task 4 implementation already covers discovery, three functioning cycles, stabilization, permanent unlock, current-run prototype insertion, and de-duplicated run summaries. Re-run it unchanged before documentation and final verification:

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$logPath = Join-Path $env:TEMP 'brinespace-clean-chain-regression.log'
$proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script','res://tests/test_discovery_progression.gd','--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
Get-Content -LiteralPath $logPath
if ($proc.ExitCode -ne 0) { throw "Clean-chain regression failed with exit code $($proc.ExitCode)" }
```

Expected: exit `0`; no integration code changes are needed at this stage.

- [ ] **Step 2: Update project documentation**

In `README.md`, replace the current “all rooms available” implications with:

- twelve foundational blueprints on a clean save;
- hidden recipes discovered only through powered, door-connected experiments;
- three-cycle stabilization;
- prototype insertion and permanent unlocks;
- learned dormant versus functioning visual states.

In `docs/DEVELOPMENT_NOTES.md`, record these known limits:

- the first graph contains 25 authored recipes and 30 room blueprints;
- terminal recipes currently award Research rather than variants;
- procedural FX need colorblind and reduced-motion options;
- three-cycle stabilization and terminal Research values require full-run balance data.

- [ ] **Step 3: Run the complete verification suite**

```powershell
$godotExe = 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe'
$parseScripts = @(
  'res://scripts/main.gd',
  'res://scripts/grid_canvas.gd',
  'res://scripts/synergy_manager.gd',
  'res://scripts/discovery_manager.gd',
  'res://scripts/room_database.gd',
  'res://scripts/meta_state.gd',
  'res://scripts/run_manager.gd',
  'res://tests/test_discovery_progression.gd',
  'res://tests/test_synergy_manager.gd',
  'res://tests/capture_discovery_state.gd'
)
foreach ($script in $parseScripts) {
  $logPath = Join-Path $env:TEMP ("brinespace-final-parse-" + ($script -replace '[^A-Za-z0-9]', '_') + '.log')
  $proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--check-only','--script',$script,'--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
  Get-Content -LiteralPath $logPath
  if ($proc.ExitCode -ne 0) { throw "$script failed parse check" }
}
foreach ($testScript in @('res://tests/test_discovery_progression.gd','res://tests/test_synergy_manager.gd')) {
  $logPath = Join-Path $env:TEMP ("brinespace-final-test-" + ($testScript -replace '[^A-Za-z0-9]', '_') + '.log')
  $proc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--script',$testScript,'--log-file',$logPath) -Wait -PassThru -WindowStyle Hidden
  Get-Content -LiteralPath $logPath
  if ($proc.ExitCode -ne 0) { throw "$testScript failed" }
}
$smokeLog = Join-Path $env:TEMP 'brinespace-final-discovery-smoke.log'
$smokeProc = Start-Process -FilePath $godotExe -ArgumentList @('--headless','--path','.','--quit-after','5','--log-file',$smokeLog) -Wait -PassThru -WindowStyle Hidden
Get-Content -LiteralPath $smokeLog
if ($smokeProc.ExitCode -ne 0) { throw 'Main scene smoke test failed' }
git diff --check
```

Expected: every process exits `0`, both suites print their pass line, the main scene smoke test has no errors, and `git diff --check` reports no whitespace errors.

- [ ] **Step 4: Re-run the final visual matrix**

Capture doctrine selection, unknown candidate, first discovery, stabilizing `2/3`, dormant known link, active link, blueprint-decrypted feedback, and reboot summary. Inspect each at the project default `2560x1440` viewport and at `1600x900`. Confirm text remains legible, effects do not obscure doors, and modal input still blocks the playfield.

- [ ] **Step 5: Commit**

```powershell
git add -- README.md docs/DEVELOPMENT_NOTES.md tests/test_discovery_progression.gd tests/capture_discovery_state.gd
git commit -m "Document and verify synergy discovery progression"
```

- [ ] **Step 6: Report evidence**

Report the two test pass lines, main-scene smoke exit code, parse-check count, visual states inspected, clean `git diff --check`, and the commit range containing Tasks 0–7. Do not call the feature complete if any required visual state or clean-save end-to-end assertion is missing.
