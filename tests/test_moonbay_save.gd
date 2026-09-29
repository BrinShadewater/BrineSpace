extends SceneTree

const MainScene = preload("res://scenes/main.tscn")
const Save = preload("res://scripts/run_save.gd")
const Mission = preload("res://scripts/moonbay_missions.gd")
const View = preload("res://rooms/large-rooms/moonbay.gd")
var failures := 0

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func _init() -> void:
	call_deferred("run")

func run() -> void:
	var game = MainScene.instantiate()
	game.meta.save_path = "user://moonbay_save_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://moonbay_save_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	var home := Vector2i(-1,-1)
	for y in range(8,35):
		if home.x>=0: break
		for x in range(8,35):
			var candidate := Vector2i(x,y)
			if game.get_footprint_placement_problem("moonbay",candidate,0).is_empty():
				home = candidate
				break
	check(home.x>=0,"Fixture finds an unobstructed ocean-facing Moonbay site")
	if home.x<0: quit(1); return
	game._place_room("moonbay",home,true)
	var actor = game.bill_npc
	actor.active = true
	actor.dead = false
	actor.foot = (Vector2(home+Vector2i.ONE)+Vector2.ONE*0.5)*actor.CELL
	actor.goal = "moonbay"
	actor.goal_cell = home+Vector2i.ONE
	actor.moonbay_assignment = {"home":home,"onboard":true}
	var room: Dictionary = game.occupied[home]
	var state := Mission.mission_state(room)
	state.crew = "bill"
	state.order = "survey"
	state.target = Vector2i(29,29)
	state.credited = false
	for phase in ["approach","seal","flood","launch","outbound","work","return","drain","unload"]:
		state.phase = phase
		state.progress = 1.0
		state.chamber_water = 0.5 if phase in ["flood","drain"] else (1.0 if phase in ["launch","outbound","work","return"] else 0.0)
		state.station_open = phase in ["approach","unload"]
		state.ocean_open = phase=="launch"
		var expected: Dictionary = state.duplicate(true)
		var checkpoint: Dictionary = Save.capture(game)
		check(Save.problem(checkpoint).is_empty(),"%s checkpoint validates: %s" % [phase,Save.problem(checkpoint)])
		if not Save.problem(checkpoint).is_empty(): break
		if phase=="work":
			check(Save.write(game,game.run_save_path)==OK,"At-sea mission writes a checkpoint")
			checkpoint = Save.read(game.run_save_path)
			check(not checkpoint.is_empty(),"At-sea mission reads from disk")
		check(Save.restore(game,checkpoint),"%s checkpoint restores" % phase)
		room = game.occupied[home]
		state = Mission.mission_state(room)
		check(state.phase==expected.phase and state.progress==expected.progress and state.chamber_water==expected.chamber_water and state.station_open==expected.station_open and state.ocean_open==expected.ocean_open,"%s chamber and mission phase survive Continue" % phase)
		check(game.bill_npc.moonbay_assignment.get("home",Vector2i(-1,-1))==home and game.bill_npc.goal=="moonbay","%s crew remains reserved after Continue" % phase)
		var visual: Dictionary = View.visual_state(room)
		check(visual.sub_present==(phase not in ["launch","outbound","work","return"]) and visual.chamber_water==expected.chamber_water,"%s room visual matches saved mission" % phase)
		check(Mission.station_visible(game,game.bill_npc)==(phase in ["approach","unload"]),"%s pilot visibility matches boarding state" % phase)
	var invalid: Dictionary = Save.capture(game)
	invalid.state.placed_rooms[-1].moonbay_mission.station_open = true
	invalid.state.placed_rooms[-1].moonbay_mission.ocean_open = true
	check(Save.problem(invalid)=="Moonbay mission state","Checkpoint rejects both hatches open")
	var old: Dictionary = Save.capture(game)
	for saved_room in old.state.placed_rooms:
		if saved_room.id=="moonbay": saved_room.erase("moonbay_mission")
	old.crew.bill.erase("moonbay_assignment")
	old.crew.bill.goal = ""
	check(Save.problem(old).is_empty(),"Old dry Moonbay checkpoint remains loadable")
	check(Save.restore(game,old),"Old checkpoint restores")
	check(Mission.mission_state(game.occupied[home]).phase=="idle" and View.visual_state(game.occupied[home]).chamber_water==0.0,"Old checkpoint defaults to a dry idle Moonbay")
	root.remove_child(game)
	current_scene = null
	game.free()
	print("MOONBAY SAVE ","PASS" if failures==0 else "FAIL"," / ",failures," failures")
	quit(0 if failures==0 else 1)
