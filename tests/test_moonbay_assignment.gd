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
		if pilot.moonbay_assignment.get("in_airlock",false): break
	check(pilot.moonbay_assignment.get("in_airlock",false) and not pilot.moonbay_assignment.onboard and pilot.goal=="moonbay","Crew walks into the airlock and waits before entering the wet bay")
	Mission.tick(station,13.0)
	check(Mission.mission_state(station.occupied[anchor]).phase=="seal","Pressure cycle begins with the crew inside the airlock")
	pilot.helmet_equipped=true; pilot.tank_oxygen=60.0
	var seen := {}
	for step in range(6000):
		var phase: String=Mission.mission_state(station.occupied[anchor]).phase
		seen[phase]=true
		if phase=="idle": break
		preload("res://scripts/room_flooding.gd").step_crew(station,pilot,"bill",0.1)
		Mission.tick(station,0.1)
		Mission.advance_crew(station,pilot,0.1)
		if Mission.mission_state(station.occupied[anchor]).phase=="idle": break
		if pilot.dead or pilot.goal!="moonbay":
			print("MOONBAY PRESSURE DIAG phase=",phase," foot=",pilot.foot," medium=",pilot.movement_medium," path=",pilot.path," assignment=",pilot.moonbay_assignment," activity=",pilot.activity)
			if phase!="unload": break
	check(seen.has("boarding") and seen.has("exit_bay") and seen.has("drain"),"Actual crew completes both wet-side crossings and return drainage")
	check(Mission.mission_state(station.occupied[anchor]).phase=="idle" and not pilot.dead and pilot.moonbay_assignment.is_empty(),"Crew exits the drained airlock and survives the complete mission")
	var view = preload("res://rooms/large-rooms/moonbay.gd")
	for q in range(1,4):
		var rotated_room: Dictionary=station.occupied[anchor]
		rotated_room.rotation=q; rotated_room.erase("moonbay_mission")
		# Isolate the rotation fixture: the original east corridor/south starter core
		# would obstruct the ocean face after rotation, which correctly rejects placement.
		station.placed_rooms=[rotated_room]
		station.occupied.clear()
		for cell in preload("res://scripts/room_footprint.gd").cells(anchor,Vector2i(2,2)):
			station.occupied[cell]=rotated_room
		station._refresh_all()
		station.powered_room_cells[anchor]=true
		station.unpowered_room_cells.erase(anchor)
		pilot.goal=""; pilot.path.clear(); pilot.moonbay_assignment.clear()
		pilot.movement_medium="dry"; pilot.helmet_equipped=true; pilot.tank_oxygen=60.0
		pilot.foot=(Vector2(anchor)+Vector2.ONE)*pilot.CELL+view.exit_point(rotated_room)
		station.drone_fleet.sites[target]=Harvest.make_site("salvage",3)
		var rotation_problem := Mission.dispatch(station,rotated_room,"bill",target,"survey")
		check(rotation_problem.is_empty(),"Rotation %d starts an actual pressure journey: %s" % [q,rotation_problem])
		var rotation_seen := {}
		for step in range(6000):
			var state := Mission.mission_state(rotated_room)
			rotation_seen[state.phase]=true
			check(view.visual_state(rotated_room).chamber_water==1.0,"Bay stays full during actual rotation %d journey" % q)
			check(not (view.door_amounts(rotated_room).x>0.001 and view.bay_door_amount(rotated_room)>0.001),"Crew doors remain interlocked during rotation %d" % q)
			if state.phase=="idle": break
			preload("res://scripts/room_flooding.gd").step_crew(station,pilot,"bill",0.1)
			Mission.tick(station,0.1); Mission.advance_crew(station,pilot,0.1)
			if pilot.dead:
				print("MOONBAY ROTATION DIAG q=",q," phase=",state.phase," foot=",pilot.foot," medium=",pilot.movement_medium," assignment=",pilot.moonbay_assignment)
				break
		check(rotation_seen.has("boarding") and rotation_seen.has("exit_bay") and Mission.mission_state(rotated_room).phase=="idle" and not pilot.dead,"Rotation %d completes fill, board, return, drain and dry exit" % q)
	var recovery_room: Dictionary=station.occupied[anchor]
	station.drone_fleet.sites[target]=Harvest.make_site("salvage",3)
	check(Mission.dispatch(station,recovery_room,"bill",target,"survey").is_empty(),"Wet-route recovery fixture dispatches")
	var recovery_state := Mission.mission_state(recovery_room)
	recovery_state.phase="boarding"; recovery_state.progress=1.0; recovery_state.chamber_water=1.0
	recovery_state.station_open=false; recovery_state.ocean_open=false
	pilot.foot=(Vector2(anchor)+Vector2.ONE)*pilot.CELL+view.airlock_point(recovery_room)
	pilot.moonbay_assignment.leg="board"; pilot.moonbay_assignment.onboard=false; pilot.moonbay_assignment.in_airlock=false
	pilot.moonbay_assignment.arrival=(Vector2(anchor)+Vector2.ONE)*pilot.CELL+view.boarding_point(recovery_room)
	pilot.path.clear(); pilot.state="idle"; pilot.tank_oxygen=60.0
	Mission.advance_crew(station,pilot,0.1)
	check(recovery_state.phase=="exit_bay" and not pilot.moonbay_assignment.is_empty(),"Lost wet route keeps the crew reserved for a safe return cycle")
	check(Mission.valid_rooms(station.placed_rooms,{"bill":pilot.snapshot()}) and preload("res://scripts/bill_npc.gd").valid_snapshot(pilot.snapshot()),"Interrupted wet passage remains a valid checkpoint")
	for step in range(1200):
		if recovery_state.phase=="idle": break
		preload("res://scripts/room_flooding.gd").step_crew(station,pilot,"bill",0.1)
		Mission.tick(station,0.1); Mission.advance_crew(station,pilot,0.1)
	check(recovery_state.phase=="idle" and pilot.moonbay_assignment.is_empty() and not pilot.dead,"Interrupted wet passage drains and returns crew to dry air")
	root.remove_child(station)
	current_scene = null
	station.free()
	print("MOONBAY ASSIGNMENT ","PASS" if failures==0 else "FAIL"," / ",failures," failures")
	quit(0 if failures==0 else 1)
