extends SceneTree
## Construction reveals interior props one at a time with the preview dressing enabled.
## Every service route it would draw must have both endpoint hosts already placed.
var failures := 0
func _init() -> void: call_deferred("run")
func run() -> void:
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://construction_fitting_routes.meta"
	game.run_save_path = "user://construction_fitting_routes.loop"
	root.add_child(game)
	current_scene = game
	game.set_process(false)
	game.tick_timer.stop()
	var checked := 0
	var deferred := 0
	for id in game.RoomDatabaseScript.all_rooms():
		var room: Dictionary = game.RoomDatabaseScript.get_room(id)
		room.pos = Vector2i(20,20)
		var view = game.grid_view._bill_room_view(room)
		if view == null or not view.has_method("configure_embedded") or not "dressing" in view or view.dressing == null: continue
		var routes: Array = view.dressing.profile.get("routes",[]) + view.dressing.profile.get("surface_routes",[])
		if routes.is_empty(): continue
		for rotation in range(4):
			view.configure_embedded(rotation,[],false,0.0)
			var props: Array = view.props
			for count in range(props.size()+1):
				view.props = props.slice(0,count)
				view.set_meta("layout_editor_preview",true)
				view.set_meta("construction_fitting",true)
				for route in routes:
					var from_missing: bool = view.dressing.find_prop(str(route.from.host)).is_empty()
					var to_missing: bool = view.dressing.find_prop(str(route.to.host)).is_empty()
					if view.dressing.route_returned_to_tray(route):
						if from_missing or to_missing: deferred += 1
						continue
					if from_missing or to_missing:
						failures += 1
						push_error("Construction draws a route to an unplaced host: %s q%d props=%d %s->%s" % [id,rotation,count,route.from.host,route.to.host])
					checked += 1
				view.remove_meta("layout_editor_preview")
				view.remove_meta("construction_fitting")
			view.props = props
	if deferred == 0:
		failures += 1
		push_error("Fixture never reached a partially fitted route; coverage is vacuous")
	print("CONSTRUCTION FITTING ROUTES: %s; %d drawn routes, %d deferred" % ["PASS" if failures == 0 else "FAIL",checked,deferred])
	quit(failures)
