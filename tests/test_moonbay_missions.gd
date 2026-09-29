extends SceneTree

const Mission = preload("res://scripts/moonbay_missions.gd")
const Main = preload("res://scripts/main.gd")
const Rooms = preload("res://scripts/room_database.gd")
const Sites = preload("res://scripts/site_generator.gd")
var failures := 0

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func finish(game, room: Dictionary) -> void:
	for _step in range(900):
		Mission.tick(game,1.0)
		if Mission.mission_state(room).get("phase","") == "idle": break

func _init() -> void:
	var layout := Sites.generate(20260928)
	var deep: Vector2i = Vector2i(-1,-1)
	var hazard: Vector2i = Vector2i(-1,-1)
	for cell in layout.sites:
		if layout.sites[cell].get("moonbay_deep",false):
			if layout.sites[cell].get("hazardous",false): hazard=cell
			else: deep=cell
	check(deep.x>=0 and Sites.distance(deep)>=14, "Generator includes a deep site beyond diver range")
	var game = Main.new()
	game.site_layout = layout
	game.drone_fleet.sites = layout.sites.duplicate(true)
	var room: Dictionary = Rooms.get_room("moonbay")
	room.pos = Vector2i(10,10)
	room.rotation = 0
	game.placed_rooms.append(room)
	game.occupied[room.pos] = room
	game.powered_room_cells[room.pos] = true
	var survey_target: Vector2i = Vector2i(-1,-1)
	for cell in game.drone_fleet.sites:
		if not game.drone_fleet.sites[cell].discovered and cell != deep:
			survey_target = cell
			break
	check(survey_target.x>=0,"A survey target exists")
	if survey_target.x>=0:
		check(Mission.dispatch(game,room,"bill",survey_target,"survey").is_empty(),"Survey dispatches")
		check(Mission.mission_state(room).phase=="approach","Mission starts with crew approach")
		finish(game,room)
		check(game.drone_fleet.sites[survey_target].discovered,"Survey reveals target")
		check(Mission.mission_state(room).phase=="idle","Survey returns to dry idle")
		var metal_before: int = game.resources.metal
		check(Mission.dispatch(game,room,"bill",survey_target,"recover").is_empty(),"Recovery dispatches to surveyed site")
		finish(game,room)
		check(game.resources.metal>metal_before,"Recovery credits cargo once on return")
		var credited: int = game.resources.metal
		for _step in range(20): Mission.tick(game,1.0)
		check(game.resources.metal==credited,"Cargo is not credited twice")
	if deep.x>=0:
		game.drone_fleet.sites[deep].discovered = true
		check(Mission.dispatch(game,room,"bill",deep,"deep_access").is_empty(),"Deep access dispatches")
		finish(game,room)
		check(game.drone_fleet.sites[deep].get("deep_accessed",false),"Deep access records arrival")
	if hazard.x>=0:
		game.drone_fleet.sites[hazard].discovered = true
		check(Mission.dispatch(game,room,"bill",hazard,"deep_access").is_empty(),"Visible hazardous site can be assigned")
		Mission.mission_state(room).hazard_roll = 0.0
		finish(game,room)
		check(Mission.mission_state(room).damage>0 and Mission.mission_state(room).last_result.contains("Hazard"),"Hazard damages sub and forces early return")
		check(not Mission.dispatch(game,room,"bill",deep,"deep_access").is_empty(),"Damaged sub cannot launch")
		var metal_before_repair: int = game.resources.metal
		check(Mission.repair(game,room).is_empty() and game.resources.metal==metal_before_repair-4,"Repair spends Metal and restores launch")
	var missing: Vector2i = Vector2i(-1,-1)
	for cell in game.drone_fleet.sites:
		if not game.drone_fleet.sites[cell].discovered and cell != survey_target:
			missing = cell
			break
	if missing.x>=0:
		check(Mission.dispatch(game,room,"bill",missing,"survey").is_empty(),"Mission can depart for a currently known target")
		game.drone_fleet.sites.erase(missing)
		finish(game,room)
		check(Mission.mission_state(room).last_result.contains("absent") and Mission.mission_state(room).phase=="idle","Removed target returns safely")
	check(Mission.dispatch(game,room,"bill",Vector2i(0,0),"survey") != "","Missing target rejects safely")
	game.free()
	print("MOONBAY MISSIONS ", "PASS" if failures==0 else "FAIL", " / ", failures, " failures")
	quit(0 if failures==0 else 1)
