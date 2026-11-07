extends SceneTree
const Main = preload("res://scripts/main.gd")
const Rooms = preload("res://scripts/room_database.gd")
var failures := 0
var checks := 0
func check(ok: bool, message: String):
	checks += 1
	if not ok: failures += 1; push_error(message)
func _init(): call_deferred("run")
func run():
	var game = Main.new()
	game.meta.discovered_synergy_ids.clear()
	var at := Vector2i(20,20)
	# Identical public geometry must give identical cues, with or without a recipe.
	# A reactor has four doors, so its rotations cannot affect these controls.
	for pair in [["current_turbine","hydroponics_bay"],["current_turbine","reactor"]]:
		var neighbor: Dictionary = Rooms.get_room(pair[1]).duplicate(true)
		neighbor.pos = at + Vector2i.RIGHT
		neighbor.display_name = "Visible neighbor"
		game.occupied = {neighbor.pos:neighbor}
		var matched := false
		for rotation in range(4):
			for facing in range(4):
				neighbor.rotation = facing
				game.selected_rotation = rotation
				if game._doors_connect(pair[0],rotation,Vector2i.RIGHT,neighbor):
					matched = true
					check(game._placement_experiment(pair[0],at) == "Experiment · connected to Visible neighbor.\nKeep connected rooms functioning; watch for a response.","Recipe and non-recipe geometry use the same cue")
					var text: String = game._placement_connections(pair[0],at)
					check(not text.contains("Cultivated Current") and not text.contains("Biomass"),"Undiscovered recipe and reward stay hidden")
		check(matched,"Pair exercised a connected orientation")
	# Exhaustively check rotation advice against actual door connectivity.
	var neighbor: Dictionary = Rooms.get_room("hydroponics_bay").duplicate(true)
	neighbor.pos = at + Vector2i.RIGHT
	game.occupied = {neighbor.pos:neighbor}
	var rotation_hints := 0
	for facing in range(4):
		neighbor.rotation = facing
		for rotation in range(4):
			game.selected_rotation = rotation
			var possible := false
			for alternative in range(4): possible = possible or game._doors_connect("current_turbine",alternative,Vector2i.RIGHT,neighbor)
			var connected: bool = game._doors_connect("current_turbine",rotation,Vector2i.RIGHT,neighbor)
			var text: String = game._placement_experiment("current_turbine",at)
			check(text.contains("rotation can") == (possible and not connected),"Rotation advice requires a real matching orientation")
			if text.contains("rotation can"): rotation_hints += 1
	check(rotation_hints > 0,"Rotation cases exercised")
	check(game._placement_experiment("hydroponics_bay",at).is_empty(),"Same room type does not invite a mixed-room experiment")
	check(game._placement_experiment("current_turbine",neighbor.pos).is_empty(),"Occupied target does not invite an experiment")
	# Public topology identical while hidden recipe membership changes.
	game.occupied.clear()
	for entry in [["storage_bay",at+Vector2i.LEFT],["salvage_workshop",at+Vector2i.RIGHT]]:
		var room: Dictionary = Rooms.get_room(entry[0]).duplicate(true)
		room.pos=entry[1]; room.rotation=1 if entry[0]=="salvage_workshop" else 0
		game.occupied[room.pos]=room
	game.selected_rotation=1
	var before: Dictionary = game.occupied.duplicate(true)
	var resources: Dictionary = game.resources.duplicate(true)
	var preview: String = game._placement_connections("corridor",at)
	check(not preview.contains("Unrecovered passage") and not preview.contains("Parts Passage"),"Unknown passage gives no recipe-dependent confirmation")
	check(preview.contains("Experiment"),"Passage has generic geometry guidance")
	var storage: Dictionary = game.occupied[at+Vector2i.LEFT]
	var control: Dictionary = Rooms.get_room("reactor").duplicate(true)
	control.pos=storage.pos;control.rotation=storage.rotation;control.display_name=storage.display_name
	game.occupied[storage.pos]=control
	check(game._placement_connections("corridor",at)==preview,"Hidden passage and non-recipe passage have identical public preview")
	game.occupied[storage.pos]=storage
	game.meta.discovered_synergy_ids["parts_passage"] = true
	var known: String = game._placement_connections("corridor",at)
	check(known.contains("Parts Passage"),"Discovered passage retains its explicit preview")
	check(before==game.occupied and resources==game.resources,"Preview is read-only")
	game.occupied.clear()
	check(game._placement_experiment("current_turbine",at).is_empty(),"No neighbors means no experiment cue")
	game.free()
	print("PLACEMENT EXPERIMENTS checks=",checks," failures=",failures)
	quit(1 if failures else 0)
