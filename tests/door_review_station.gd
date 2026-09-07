extends "res://tests/playtest_nursery_art.gd"
## Interactive isolated renderer fixture. Main simulation stays paused; no balance changes.
const CELLS := [Vector2i(0,0),Vector2i(1,0),Vector2i(1,1),Vector2i(0,1)]
const PRESETS := ["Bio","Life Support","Engineering","Mixed / generic"]
var preset := 3
var quarter := 0
var cells: Array = []
var leg := 0
var reverse := false
var playing := true
var mixed_power := false
var ready_for_review := false
var status: Label
var automatic_capture := false

func run() -> void:
	automatic_capture = not capture_dir.is_empty()
	if automatic_capture:
		if DirAccess.dir_exists_absolute(capture_dir):
			push_error("Refusing to overwrite review evidence")
			quit(1)
			return
		DirAccess.make_dir_recursive_absolute(capture_dir)
	game = MainScene.instantiate()
	game.meta.save_path = "user://brine_door_review_fixture.json"
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(viewport_width,roundi(viewport_width*9.0/16))
	root.title = "BrineSpace — Door review (isolated fixture)"
	await settle()
	game.pending_doctrines.assign(["biosphere","recovery"])
	game._confirm_doctrines()
	game._set_paused(true)
	game.set_process(false)
	game.set_process_input(false)
	game.set_process_unhandled_input(false)
	game.set_process_unhandled_key_input(false)
	# Prevent normal build/inspect clicks; fixture controls live above this shield.
	var layer := CanvasLayer.new()
	layer.layer = 100
	root.add_child(layer)
	var shield := Control.new()
	shield.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	shield.mouse_filter = Control.MOUSE_FILTER_STOP
	layer.add_child(shield)
	var panel := PanelContainer.new()
	panel.position = Vector2(20,770)
	shield.add_child(panel)
	var stack := VBoxContainer.new()
	panel.add_child(stack)
	status = Label.new()
	stack.add_child(status)
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation",8)
	stack.add_child(row)
	for i in range(4):
		var button := Button.new()
		button.text = PRESETS[i]
		button.pressed.connect(func(): preset=i; rebuild_review())
		row.add_child(button)
	for title in ["Reverse","Next door","Rotate","Power","Pause / play"]:
		var button := Button.new()
		button.text = title
		button.pressed.connect(func(): action(title))
		row.add_child(button)
	await rebuild_review()
	ready_for_review = true
	if automatic_capture:
		playing = false
		await verify_review()

func rebuild_review() -> void:
	ready_for_review = false
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	game.unpowered_room_cells.clear()
	game.offline_reasons.clear()
	game.grid_view.room_light_levels.clear()
	cells.clear()
	var ids := ["mycelium_nursery","life_support","reactor","hydroponics_bay"]
	for i in range(4):
		var cell := Vector2i(20,20)+Vector2i(Geometry.turn(Vector2(CELLS[i]),quarter))
		cells.append(cell)
		var id: String = ids[preset] if preset<3 else ids[i]
		game._place_room(id,cell,true)
		game.occupied[cell].rotation = posmod(quarter+(2 if i>=2 else 0),4)
		game.powered_room_cells[cell] = true
	game.hand.clear()
	game.selected_card_id = ""
	game.hover_cell = Vector2i(-1,-1)
	game._refresh_all()
	set_leg()
	apply_power()
	await settle()
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.43)
	game._center_grid_on_station_deferred()
	await settle()
	ready_for_review = true
	update_status()

func set_leg() -> void:
	var a: int = posmod(leg,4)
	var b: int = posmod(leg+( -1 if reverse else 1),4)
	game.test_walker_cell = cells[a]
	game.test_walker_next_cell = cells[b]
	game.test_walker_previous_cell = Vector2i(-1,-1)
	game.test_walker_progress = 0.0
	game.test_walker_state = "walk"
	expect(game._placed_rooms_connected(game.occupied[cells[a]],game.occupied[cells[b]],cells[b]-cells[a]),"Review circuit has compatible ports")

func apply_power() -> void:
	for i in range(4):
		var cell: Vector2i = cells[i]
		game.powered_room_cells[cell] = true
		game.unpowered_room_cells.erase(cell)
		game.offline_reasons.erase(cell)
		if mixed_power and i==2:
			game.powered_room_cells.erase(cell)
			game.unpowered_room_cells[cell] = "NEEDS POWER"
			game.offline_reasons[cell] = "NEEDS POWER"

func action(title: String) -> void:
	if not ready_for_review: return
	match title:
		"Reverse": reverse=not reverse; set_leg()
		"Next door": leg=posmod(leg+(-1 if reverse else 1),4); set_leg()
		"Rotate": quarter=(quarter+1)%4; rebuild_review()
		"Power": mixed_power=not mixed_power; apply_power()
		"Pause / play": playing=not playing
	update_status()

func update_status() -> void:
	status.text = "DOOR REVIEW — isolated save | %s | %d° | %s | %s"%[PRESETS[preset],quarter*90,"mixed power" if mixed_power else "powered","walking" if playing else "paused"]

func _process(delta: float) -> bool:
	if not ready_for_review or not playing: return false
	game.visual_time_seconds += delta
	game.test_walker_progress += delta/5.0
	if game.test_walker_progress>=1:
		leg=posmod(leg+(-1 if reverse else 1),4)
		set_leg()
	game.paused=false
	game.grid_view._advance_room_lights(delta)
	game.paused=true
	game.grid_view.queue_redraw()
	return false

func verify_review() -> void:
	playing=true
	var initial: float = game.test_walker_progress
	_process(0.1)
	expect(game.test_walker_progress>initial,"Interactive clock advances walker")
	playing=false
	initial=game.test_walker_progress
	_process(0.1)
	expect(game.test_walker_progress==initial,"Interactive pause freezes walker")
	for p in range(4):
		preset=p
		mixed_power=false
		await rebuild_review()
		for direction in [false,true]:
			reverse=direction
			for edge in range(4):
				leg=edge
				set_leg()
				game.test_walker_progress=0.5
				expect(game.grid_view._door_frame_for_pair(game,game.test_walker_cell,game.test_walker_next_cell)==9,"Review crossing fully open")
				await capture("preset%d-edge%d-reverse%s"%[p,edge,direction])
		mixed_power=true
		apply_power()
		game.paused=false
		game.grid_view._advance_room_lights(1)
		game.paused=true
		update_status()
		await capture("preset%d-mixed-power"%p)
		var before := root.get_texture().get_image().get_data()
		await settle()
		expect(before==root.get_texture().get_image().get_data(),"Review pause is pixel-stable")
	print("DOOR REVIEW %s: 4 presets, 32 bidirectional crossings, 4 mixed-power and pause comparisons"%("PASS" if failures==0 else "FAIL"))
	quit(0 if failures==0 else 1)
