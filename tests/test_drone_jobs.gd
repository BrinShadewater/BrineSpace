extends SceneTree
var game
func _init() -> void: call_deferred("run")
func run() -> void:
	game = load("res://scenes/main.tscn").instantiate()
	game.run_save_path = "user://drone_jobs_%d.loop" % OS.get_process_id()
	game.meta.save_path = game.run_save_path+".meta"
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	game.set_process(false)
	game.tick_timer.stop()
	game.paused = false
	var home: Vector2i = game.placed_rooms[0].pos
	var cell := home+Vector2i.DOWN
	game.selected_rotation = 0
	game._spend({"metal":2})
	var paid: Dictionary = game.resources.duplicate()
	game._place_room("corridor",cell)
	assert(not game.occupied.has(cell) and game.drone_fleet.reserved(cell),"Paid order reserves cell without operating")
	assert(game.get_placement_problem("corridor",cell).contains("scheduled"),"Duplicate construction rejected")
	game._update_wreck_clearance(3.0)
	var checkpoint = preload("res://scripts/run_save.gd").capture(game)
	assert(preload("res://scripts/drone_fleet.gd").valid(checkpoint.drone_fleet,game.placed_rooms),"In-flight checkpoint valid")
	assert(preload("res://scripts/run_save.gd").restore(game,checkpoint),"In-flight checkpoint restores")
	game.paused = false
	game._update_wreck_clearance(30.0)
	assert(game.occupied.has(cell) and not game.drone_fleet.reserved(cell),"Builder completes paid room")
	assert(game.station_sound.voices.has("build_complete"),"Paid construction completion emits its dedicated cue")
	assert(game.resources==paid,"Construction does not charge twice or award resources")
	var rock := Vector2i(17,20)
	game._toggle_wreck_work(rock)
	assert(not game.wrecks[rock].active,"Rock work requires mining bay")
	game._place_room("mining_drone_bay",rock+Vector2i.RIGHT,true)
	game.occupied[rock+Vector2i.RIGHT].rotation = 1
	game._toggle_wreck_work(rock)
	assert(game.wrecks[rock].active,"Mining bay enables rock job")
	game._update_wreck_clearance(1.0)
	assert(game.wrecks[rock].progress==0.0,"No drilling before launch and arrival")
	game._update_wreck_clearance(10.0)
	assert(game.wrecks[rock].progress>0.0 and not game.wrecks[rock].cleared,"Drone drills after arrival")
	var before: float = game.wrecks[rock].progress
	game.paused = true
	game._update_wreck_clearance(20.0)
	assert(game.wrecks[rock].progress==before,"Pause freezes job")
	game.paused = false
	game._update_wreck_clearance(30.0)
	assert(game.wrecks[rock].cleared,"Mining drone clears blocker")
	var old = preload("res://scripts/run_save.gd").capture(game)
	old.erase("drone_fleet")
	assert(preload("res://scripts/run_save.gd").restore(game,old),"Old checkpoints restore without fleet")
	print("DRONE JOBS PASS: paid construction, reservation, launch timing, clearance, pause, checkpoint and old-save compatibility")
	game.queue_free()
	var music = root.get_node_or_null("StationMusic")
	if music != null: music.queue_free()
	await process_frame
	music = root.get_node_or_null("StationMusic")
	if music != null: music.queue_free()
	await process_frame
	await create_timer(0.2).timeout
	quit()
