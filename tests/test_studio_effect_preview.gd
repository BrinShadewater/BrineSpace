extends SceneTree
## Studio preview buttons (owner, Sept 28): each room offers only the previews the game can
## show, each preview animates the same view state the live game sets, and nothing is saved.
const Editor = preload("res://scripts/room_layout_editor.gd")
const Store = preload("res://scripts/room_layout_store.gd")
const Effects = preload("res://scripts/studio_effect_preview.gd")
const Airlock = preload("res://scripts/airlock_cycle.gd")
var failures := 0

class HazardCanvas extends Control:
	var effects
	var drawn := false
	func _draw() -> void:
		effects.draw_hazards(self, size / 2, 1.0)
		drawn = true

func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
		push_error(label)

func ids(room_id: String) -> Array:
	var e = Effects.new()
	e.room_id = room_id
	return e.actions().map(func(a): return a[1])

func run_for(e, seconds: float) -> void:
	var t := 0.0
	while t < seconds:
		e.advance(0.05)
		t += 0.05

func _init() -> void: call_deferred("run")

func run() -> void:
	# Buttons match what the game can show in each room.
	check(ids("airlock").has("cycle_out") and ids("airlock").has("cycle_in"), "Diving Airlock offers both cycles")
	check(ids("salvage_drone_bay").has("return_cargo") and ids("mining_drone_bay").has("return_cargo"), "Mining and salvage bays offer a cargo return")
	check(ids("construction_drone_bay").has("launch") and not ids("construction_drone_bay").has("return_cargo"), "Construction bay launches without cargo")
	check(ids("survey_probe_bay").has("probe"), "Survey bay launches the probe")
	check(ids("reactor").has("fire") and ids("galley").has("fire"), "Machinery rooms can burn")
	check(not ids("med_bay").has("fire") and not ids("corridor").has("fire"), "Fire only where machinery heat ignites it")
	for room_id in ["med_bay", "corridor", "airlock"]:
		check(ids(room_id).has("flood") and ids(room_id).has("clear"), "Every room can flood and clear: " + room_id)

	# Airlock: cycle out floods and opens the hatch; cycle in drains back to dry.
	var e = Effects.new()
	e.room_id = "airlock"
	e.start("cycle_out")
	run_for(e, 1.5)
	check(Airlock.pose({"airlock_cycle": e.airlock}).inner < 1.0, "Cycle out seals the inner door first")
	run_for(e, 10.0)
	var out: Dictionary = Airlock.pose({"airlock_cycle": e.airlock})
	check(out.phase == "exterior" and out.outer == 1.0 and out.water == 1.0, "Cycle out ends flooded with the outer hatch open")
	e.start("cycle_in")
	run_for(e, 12.0)
	check(e.airlock.is_empty(), "Cycle in drains back to a dry chamber")

	# Drones: launch empties the dock, return settles the drone back in it.
	e = Effects.new()
	e.room_id = "salvage_drone_bay"
	e.start("launch")
	run_for(e, 0.6)
	check(preload("res://scripts/drone_dock.gd").pose(e.drone).depth > 0.0, "Launch lowers the drone into the well")
	run_for(e, 1.0)
	check(e.drone.get("phase") == "outbound" and not preload("res://scripts/drone_dock.gd").pose(e.drone).present, "Launched drone leaves the dock")
	e.start("return_cargo")
	check(not e.drone.cargo.is_empty(), "Cargo return carries a load")
	run_for(e, 1.5)
	check(e.drone.is_empty(), "Returned drone settles in the dock")

	# Probe, fire and flood advance and then stop on Clear.
	e = Effects.new()
	e.room_id = "reactor"
	e.start("fire")
	e.start("flood")
	run_for(e, 7.0)
	check(e.fire >= 0.9 - 0.001 and e.flood >= Effects.FLOOD_LEVEL - 0.001, "Fire and flood build up")
	var canvas := HazardCanvas.new()
	canvas.effects = e
	canvas.size = Vector2(600, 600)
	root.add_child(canvas)
	canvas.queue_redraw()
	await process_frame
	await process_frame
	check(canvas.drawn, "Hazards draw through the live game's fire and flood functions")
	canvas.queue_free()
	e.start("clear")
	check(not e.active(), "Clear stops every preview")
	e.room_id = "survey_probe_bay"
	e.start("probe")
	run_for(e, 5.0)
	check(e.probe_clock > 4.9, "Probe launch runs the survey clock")
	run_for(e, 30.0)
	check(e.probe_clock < 0.0, "Probe returns to idle after its trip")

	# Studio: buttons follow the open room, drive its view, and never write the layout store.
	Store.path = "res://output/studio-effect-preview/layouts.json"
	Store.loaded = true
	Store.data = {}
	preload("res://scripts/title_settings.gd").save_path = Store.path + ".cfg"
	var host := Control.new()
	root.add_child(host)
	var editor = Editor.open(host)
	editor.autosave_enabled = false
	editor.scale_actor.hide_all()
	for i in editor.entries.size():
		if editor.entries[i].room == "airlock": editor.index = i
	editor.load_room()
	await process_frame
	var labels: Array = editor.effects_bar.get_children().filter(func(c): return c is Button and not c.is_queued_for_deletion()).map(func(b): return b.text)
	check(labels.has("Cycle out") and labels.has("Flood") and not labels.has("Fire"), "Airlock shows its own preview buttons: " + str(labels))
	editor.effects.start("cycle_out")
	for i in 40: editor._process(0.25)
	editor.canvas.queue_redraw()
	await process_frame
	if "cycle_pose" in editor.room:
		check(editor.room.cycle_pose.outer == 1.0, "The Studio airlock view shows the open hatch")
	check(Store.data.is_empty() and not FileAccess.file_exists(Store.path), "Previews never write layouts")
	editor.queue_free()
	host.queue_free()
	await process_frame
	print("STUDIO EFFECT PREVIEW failures=", failures)
	quit(0 if failures == 0 else 1)
