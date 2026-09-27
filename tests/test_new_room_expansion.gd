extends SceneTree
const Probe=preload("res://scripts/survey_probe.gd")
const DB=preload("res://scripts/room_database.gd")
const Main=preload("res://scenes/main.tscn")
const Save=preload("res://scripts/run_save.gd")
var failures:=0
var checks:=0
func check(ok:bool,message:String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:call_deferred("run")
func run() -> void:
	var game=Main.instantiate()
	game.meta.save_path="user://new-room-expansion-test-meta.json"
	game.run_save_path="user://new-room-expansion-test.loop"
	root.add_child(game)
	current_scene=game
	game.set_process(false)
	game.tick_timer.stop()
	game.paused=true
	var original:Dictionary=Save.capture(game)
	var definitions:Array=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/new-room-expansion/definitions.json"))
	check(definitions.size()==28,"28 additional definitions")
	for entry in definitions:
		var data:Dictionary=DB.get_room(entry.id)
		check(data.size==Vector2i.ONE,"Single-cell room: "+entry.id)
		check(game.grid_view._uses_layered_art(data),"Layered art: "+entry.id)
		check(game.grid_view._bill_room_view(data)!=null,"Live view: "+entry.id)
	# Exercise the real runtime collections, not an animation-only mock.
	game.wrecks.clear();game.occupied.clear();game.drone_fleet.orders.clear()
	game.placed_rooms.clear();game.powered_room_cells.clear()
	game.hardware.power=true
	for q in range(4):
		var room:Dictionary=DB.get_room("survey_probe_bay").duplicate(true)
		room.pos=Vector2i(12+q*4,20);room.rotation=q;room.survey_clock=0.0
		game.placed_rooms.append(room);game.occupied[room.pos]=room;game.powered_room_cells[room.pos]=true
		check(Probe.clear_route(game,room),"Clear route q"+str(q))
		var old:Vector2=Probe.pose(0,q).position
		for i in range(1,9601):
			var p:Dictionary=Probe.pose(float(i)/300,q)
			check(old.distance_to(p.position)<1,"Continuous mission q"+str(q))
			old=p.position
		check(old.distance_to(Probe.pose(0,q).position)<.001,"Exact loop seam")
	var room:Dictionary=game.placed_rooms[0]
	Probe.advance(game,1)
	check(room.survey_clock==0,"Pause holds mission")
	game.paused=false;game.hardware.power=false;Probe.advance(game,1)
	check(room.survey_clock==0,"Power switch holds mission")
	game.hardware.power=true;game.powered_room_cells.erase(room.pos);Probe.advance(game,1)
	check(room.survey_clock==0,"Unfunded bay holds mission")
	game.powered_room_cells[room.pos]=true;room.suspended=true;Probe.advance(game,1)
	check(room.survey_clock==0,"Suspended bay holds mission")
	room.suspended=false
	var obstacle:Vector2i=room.pos+Vector2i.UP
	game.occupied[obstacle]={"id":"corridor","pos":obstacle}
	Probe.advance(game,2.1)
	check(room.survey_clock==0 and room.survey_blocked,"Blocked launch is held before beacon")
	game.occupied.erase(obstacle);Probe.advance(game,2.1)
	check(is_equal_approx(room.survey_clock,2.1) and not room.survey_blocked,"Cleared route resumes")
	check(Probe.pose(room.survey_clock,0).beacon,"Circular prelaunch signal interval")
	check(Probe.lamp(game,room)=="blue","Active probe blue status")
	game.paused=true;check(Probe.lamp(game,room)=="red","Paused probe red status");game.paused=false
	room.survey_clock=7.0
	game.occupied[obstacle]={"id":"corridor","pos":obstacle}
	Probe.advance(game,.1)
	check(room.survey_clock==7.0 and room.survey_blocked,"New obstruction holds last safe phase")
	game.occupied.erase(obstacle);Probe.advance(game,.1)
	check(is_equal_approx(room.survey_clock,7.1),"Interrupted mission resumes without repositioning")
	room.survey_clock=11.99;Probe.advance(game,.02)
	check(Probe.lights(game).size()>0,"Scan enters real survey system")
	game.surveyed_water.clear();game.grid_view.underwater_visibility.last_survey=-1000
	game.grid_view.underwater_visibility.survey(game)
	check(not game.surveyed_water.is_empty(),"Scan records explored water")
	var phase:float=room.survey_clock
	check(Save.restore(game,original),"Restore untouched site before checkpoint test")
	var saved:Dictionary=Save.capture(game)
	var saved_probe:Dictionary=DB.get_room("survey_probe_bay").duplicate(true)
	saved_probe.pos=Vector2i(0,0);saved_probe.rotation=0;saved_probe.survey_clock=phase
	saved.state.placed_rooms.append(saved_probe)
	check(Save.problem(saved).is_empty(),"Checkpoint accepts probe mission: "+Save.problem(saved))
	room.survey_clock=0
	check(Save.restore(game,saved),"Checkpoint restores")
	check(is_equal_approx(float(game.placed_rooms[-1].survey_clock),phase),"Probe phase survives reload")
	var broken:Array=game.placed_rooms.duplicate(true);broken[0].survey_clock=NAN
	check(not Probe.valid_rooms(broken),"Reject invalid mission time")
	for r in broken:r.erase("survey_clock");r.erase("survey_blocked")
	check(Probe.valid_rooms(broken),"Older room snapshots remain valid")
	game.hide()
	game.queue_free()
	await process_frame
	print("NEW ROOM EXPANSION: %d checks, %d failures"%[checks,failures])
	quit(1 if failures else 0)
