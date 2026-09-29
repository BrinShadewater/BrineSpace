extends SceneTree

const Mission = preload("res://scripts/moonbay_missions.gd")
const Main = preload("res://scripts/main.gd")
const Rooms = preload("res://scripts/room_database.gd")
const Harvest = preload("res://scripts/harvest_sites.gd")
const MainScene = preload("res://scenes/main.tscn")
var failures := 0

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func _init() -> void:
	call_deferred("run")

func run() -> void:
	var game = Main.new()
	var room: Dictionary = Rooms.get_room("moonbay")
	room.pos = Vector2i(10,10)
	game.placed_rooms.append(room)
	game.occupied[room.pos] = room
	var target := Vector2i(29,29)
	game.drone_fleet.sites[target] = Harvest.make_site("salvage",3)
	var actor = game.bill_npc
	actor.active = true
	check(Mission.crew_problem(game,room,"bill").is_empty(),"Available awake crew can be assigned")
	actor.expedition = {"kind":"salvage"}
	check(not Mission.crew_problem(game,room,"bill").is_empty(),"Existing expedition blocks assignment")
	actor.expedition.clear()
	actor.goal = "construction"
	check(not Mission.crew_problem(game,room,"bill").is_empty(),"Current job blocks assignment")
	actor.goal = ""
	actor.dead = true
	check(not Mission.crew_problem(game,room,"bill").is_empty(),"Injured or unavailable crew cannot launch")
	actor.dead = false
	check(Mission.dispatch(game,room,"bill",target,"survey").is_empty(),"Available crew can board a survey mission")
	check(not actor.moonbay_assignment.is_empty(),"Assigned crew is reserved from station jobs")
	check(not Mission.dispatch(game,room,"bill",target,"survey").is_empty(),"Occupied sub rejects another assignment")
	game.paused = true
	var paused_progress: float = Mission.mission_state(room).progress
	for _i in range(20): Mission.tick(game,1.0)
	check(Mission.mission_state(room).progress==paused_progress,"Pause holds the mission")
	game.paused = false
	game.hardware.power = false
	for _i in range(20): Mission.tick(game,1.0)
	check(Mission.mission_state(room).progress==paused_progress,"Power loss holds sealed mission phase")
	game.hardware.power = true
	check(Mission.recall(game,room),"Assigned mission can be recalled")
	check(Mission.mission_state(room).phase=="unload","Recall before launch returns crew without flooding the chamber")
	for _i in range(900):
		Mission.tick(game,1.0)
		if Mission.mission_state(room).phase=="idle": break
	check(actor.moonbay_assignment.is_empty(),"Returned crew is released to station work")
	game.free()
	var station = MainScene.instantiate()
	station.meta.save_path = "user://moonbay_assignment_%d.meta" % OS.get_process_id()
	station.run_save_path = "user://moonbay_assignment_%d.loop" % OS.get_process_id()
	root.add_child(station)
	current_scene = station
	station.wrecks.clear()
	station.drone_fleet.sites.clear()
	var anchor := Vector2i(20,18)
	station._place_room("moonbay",anchor,true)
	station._place_room("tee_corridor",Vector2i(22,19),true)
	station._refresh_all()
	var pilot = station.bill_npc
	pilot.active = true
	pilot.dead = false
	pilot.goal = ""
	pilot.primary_room = Vector2i(-1,-1)
	pilot.foot = (Vector2(22,19)+Vector2.ONE*0.5)*pilot.CELL
	if not station.Architects.present(station,"bill"):
		station.recovered_crew.append({"architect_id":"bill","alive":true})
	station.drone_fleet.sites[target] = Harvest.make_site("salvage",3)
	station.selected_room_cell = anchor
	var panel = station.find_child("MoonbayPanel",true,false)
	panel.refresh()
	check(panel.visible and panel.launch_button.disabled==false,"Moonbay inspector offers an available crew mission")
	var route_problem: String = Mission.dispatch(station,station.occupied[anchor],"bill",target,"survey")
	if not route_problem.is_empty():
		print("MOONBAY ROUTE DIAG foot=",pilot.foot," cell=",pilot.cell_at(pilot.foot)," start_nodes=",pilot.room_nodes.get(pilot.cell_at(pilot.foot),[]).size()," bay_nodes=",pilot.room_nodes.get(anchor+Vector2i.ONE,[]).size()," room_nodes=",pilot.room_nodes.keys()," occupied=",station.occupied.keys()," tee_doors=",station.get_room_doors(station.occupied[Vector2i(22,19)])," bay_doors=",station.get_room_doors(station.occupied[anchor])," connected=",station._connected_neighbor_cells(Vector2i(22,19))," problem=",route_problem)
	check(route_problem.is_empty(),"Assigned crew finds a walkable route to a live Moonbay: "+route_problem)
	check(not pilot.moonbay_assignment.is_empty(),"Live crew enters Moonbay assignment")
	panel.refresh()
	check(panel.recall_button.visible and panel.launch_button.disabled,"Moonbay inspector shows recall during a mission")
	for _step in range(600):
		Mission.advance_crew(station,pilot,0.1)
		if pilot.moonbay_assignment.get("onboard",false): break
	check(pilot.moonbay_assignment.get("onboard",false) and pilot.goal=="moonbay","Crew walks into the hangar and boards without taking another job")
	Mission.tick(station,13.0)
	check(Mission.mission_state(station.occupied[anchor]).phase=="seal","Launch cycle begins after boarding")
	root.remove_child(station)
	current_scene = null
	station.free()
	print("MOONBAY ASSIGNMENT ","PASS" if failures==0 else "FAIL"," / ",failures," failures")
	quit(0 if failures==0 else 1)
