extends SceneTree
const ROOMS := ["pressure_control","listening_post","isolation_vault"]
var game
func _init() -> void: call_deferred("run")
func settle() -> void:
	for i in range(8): await process_frame
	await RenderingServer.frame_post_draw
func run() -> void:
	preload("res://scripts/title_settings.gd").initialized=true
	root.mode=Window.MODE_WINDOWED
	root.content_scale_size=Vector2i(1920,1080)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://composed_%d.meta" % OS.get_process_id()
	game.run_save_path="user://composed_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene=game
	game._confirm_doctrines()
	game._set_paused(true,false)
	game.selected_card_id=""
	game.hovered_card_id=""
	game.hover_cell=Vector2i(-1,-1)
	await settle()
	DirAccess.make_dir_recursive_absolute("res://output/rare-rooms-v1")
	for q in range(4):
		var width := 1600
		root.size=Vector2i(width,roundi(width*9.0/16.0))
		Input.warp_mouse(Vector2(width-50,80))
		game.selected_card_id=""
		game.hovered_card_id=""
		game.hover_cell=Vector2i(-1,-1)
		await settle()
		game._set_grid_zoom(0.60)
		await settle()
		for room_id in ROOMS:
			assert(not preload("res://scripts/room_database.gd").get_room(room_id).is_empty())
			game.placed_rooms.clear()
			game.occupied.clear()
			game.wrecks.clear()
			game.selected_rotation=q
			game._place_room(room_id,Vector2i(20,20),true)
			game.occupied[Vector2i(20,20)].rotation=q
			assert(game.placed_rooms[0].rotation==q)
			game._set_paused(true,false)
			game._refresh_all()
			var at: Vector2=Vector2(20.5,20.5)*game.get_cell_size()-game.grid_scroll.size*0.5
			game.grid_scroll.scroll_horizontal=roundi(at.x)
			game.grid_scroll.scroll_vertical=roundi(at.y)
			game.grid_view.queue_redraw()
			await settle()
			var frame:=root.get_texture().get_image()
			assert(frame.get_size()==root.size)
			assert(frame.save_png("res://output/rare-rooms-v1/%s-%d.png" % [room_id,q])==OK)
	game.placed_rooms.clear()
	game.occupied.clear()
	for spec in [["brine_core",Vector2i(20,20)],["pressure_control",Vector2i(20,19)],["command_center",Vector2i(21,20)],["storage_bay",Vector2i(22,20)],["listening_post",Vector2i(20,21)]]:
		game._place_room(spec[0],spec[1],true)
	game.running=true
	game.resources.power=30
	game.powered_room_cells={Vector2i(20,19):true,Vector2i(20,21):true}
	var control=preload("res://scripts/rare_branch_control.gd")
	var controller: Dictionary=game.occupied[Vector2i(20,19)]
	assert(control.select(game,controller,Vector2i(21,20),Vector2i(20,20)))
	assert(control.commit(game,controller))
	assert(game.resources.power==26)
	control.tick(game)
	assert(not game.occupied[Vector2i(22,20)].get("flooded",false))
	control.tick(game)
	assert(game.occupied[Vector2i(22,20)].flooded)
	assert(not game._simulate_room_economy().working_cells.has(Vector2i(22,20)))
	assert(not game._placed_rooms_connected(game.occupied[Vector2i(20,20)],game.occupied[Vector2i(21,20)],Vector2i.RIGHT))
	control.release(game,controller)
	assert(not game.occupied[Vector2i(22,20)].has("branch_owner"))
	var listening=preload("res://scripts/listening_post.gd")
	game.drone_fleet.sites={Vector2i(30,30):preload("res://scripts/harvest_sites.gd").make_site("mining")}
	assert(listening.begin(game,Vector2i(20,21),"mining"))
	assert(not listening.begin(game,Vector2i(20,21),"mining"))
	for i in range(3):listening.tick(game)
	assert(game.drone_fleet.sites[Vector2i(30,30)].discovered)
	assert(game.drone_fleet.sites[Vector2i(30,30)].units==12)
	assert(not listening.begin(game,Vector2i(20,21),"mining"))
	controller.id="isolation_vault"
	game.resources.power=20
	game.resources.metal=10
	assert(control.select(game,controller,Vector2i(21,20),Vector2i(20,20)))
	assert(control.commit(game,controller))
	assert(not game.occupied[Vector2i(22,20)].has("branch_owner"))
	game.occupied[Vector2i(22,20)].local_incident=true
	control.tick(game)
	assert(game.occupied[Vector2i(22,20)].isolated)
	var integrity_before: int=game.resources.integrity
	preload("res://scripts/local_incidents.gd").resolve(game)
	assert(game.resources.integrity==integrity_before)
	assert(preload("res://scripts/local_incidents.gd").repair(game,Vector2i(22,20)))
	assert(game.resources.metal==8)
	control.release(game,controller)
	assert(not game.occupied[Vector2i(22,20)].has("isolated"))
	game.architect_run={}
	game.recovered_crew=[]
	game.drone_fleet.synchronize(game.placed_rooms)
	var save=preload("res://scripts/run_save.gd")
	assert(save.write(game,game.run_save_path)==OK)
	assert(not save.read(game.run_save_path).is_empty())
	print("ISOLATION PASS: reserve arm, incident containment, paid repair, release; checkpoint read/write passes")
	print("RARE ROOMS PASS: paid flooding, production exclusion, boundary closure, release, finite investigation")
	var paths=[game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		for suffix in ["",".bak",".tmp"]:
			if FileAccess.file_exists(path+suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	print("RARE ROOM ART PASS: three single-door interiors at four rotations")
	quit()
