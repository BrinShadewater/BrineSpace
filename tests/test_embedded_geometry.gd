extends SceneTree
var failures := 0
func _init() -> void: call_deferred("run")
func run() -> void:
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://embedded_geometry.meta"
	game.run_save_path = "user://embedded_geometry.loop"
	root.add_child(game)
	current_scene = game
	game.set_process(false)
	game.tick_timer.stop()
	var checked := 0
	for id in game.RoomDatabaseScript.all_rooms():
		var room: Dictionary = game.RoomDatabaseScript.get_room(id)
		room.pos = Vector2i(20,20)
		var view = game.grid_view._bill_room_view(room)
		if view == null or not view.has_method("configure_embedded"): continue
		for rotation in range(4):
			view.configure_embedded(rotation,[0,1,2,3],true,1.0,[])
			var original: Array = view.props.duplicate(true)
			view.configure_embedded(rotation,[1,3],false,2.0,[0])
			var cached_layout: Array = view.layout.duplicate(true)
			var cached_props: Array = view.props.duplicate(true)
			var cached_edges: Array = view.edges.duplicate(true)
			view.rebuild()
			view.configure_embedded(rotation,[1,3],false,2.0,[0])
			if view.layout != cached_layout or view.props != cached_props or view.edges != cached_edges or original != cached_props:
				failures += 1
				push_error("Cached geometry differs from rebuilt geometry: %s q%d" % [id,rotation])
			view.configure_embedded(rotation,[0,1,2,3],true,3.0,[])
			if view.edges.size() != 4:
				failures += 1
				push_error("Omitted wall leaked to next instance: " + id)
			checked += 1
	print("EMBEDDED GEOMETRY: %s; %d room/rotation cases" % ["PASS" if failures == 0 else "FAIL",checked])
	quit(failures)
