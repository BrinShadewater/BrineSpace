extends SceneTree
const OUT="res://character/james-west-carry-walk-keys-v1/arrival-controller-v321/"
const Bridge=preload("res://scripts/james_workshop_arrival.gd")
var checks:=0
var failures:=0
var observations:Array=[]
func check(ok:bool,why:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init()->void:call_deferred("run")
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
	if failures:quit(2);return
	root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true);game.meta.save_path="user://arrival321.meta";game.run_save_path="user://arrival321.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false)
	var actor=game.branforth_npc
	var player=game.grid_view.branforth_player
	var cell:=Vector2i(20,19)
	var room:Dictionary=game.RoomDatabaseScript.get_room("salvage_workshop").duplicate(true)
	room.pos=cell;room.rotation=0;room.water_level=0.0
	game.occupied[cell]=room;game.placed_rooms.append(room);game.powered_room_cells[cell]=true
	actor.rebuild(game);actor.active=true;actor.dead=false;actor.movement_medium="dry";actor.expedition.clear()
	actor.goal_cell=cell
	var contact:=Vector2.INF
	for id in actor.room_nodes.get(cell,[]):
		var point:Vector2=actor.graph.get_point_position(id)
		if actor.can_stand(point):contact=point;break
	check(contact.is_finite(),"Actual workshop collision-clear arrival contact")
	if not contact.is_finite():quit(2);return
	actor.foot=contact
	for gear in ["","diving-helmet"]:
		actor.helmet_equipped=not gear.is_empty()
		for origin in ["west","east","south","north"]:
			actor.goal="curiosity";actor.stage="workshop_carry";actor.state="walk";actor.direction=origin;actor.path.clear();actor.timer=0
			actor.arrive()
			check(actor.stage=="workshop_unload" and actor.state=="idle" and actor.direction=="north" and actor.timer==2.0,"Actual arrival keeps unloading instead of overriding with diagnostics")
			check(actor.workshop_arrival_origin==(origin if origin!="north" else ""),"Incoming facing retained")
			var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames.get(gear,{})
			var key:String=Bridge.KEYS.get(origin,"")
			var available:bool=not key.is_empty() and bank.has(key) and player.cycle_seconds(key,gear)+player.cycle_seconds("unload-north",gear)<=2.0
			for elapsed in [0.0,0.4,0.81,1.4,1.99]:
				actor.timer=2.0-elapsed
				# Match the simulation's actual clock, including timer subtraction at boundaries.
				var clock:float=actor.action_elapsed()
				var expected_key:String=key if available and clock<player.cycle_seconds(key,gear) else "unload-north"
				var expected_elapsed:float=clock if expected_key==key or not available else clock-player.cycle_seconds(key,gear)
				var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
				var expected:Texture2D=bank[expected_key][0]
				var cursor:float=clampf(expected_elapsed,0.0,player.cycle_seconds(expected_key,gear))
				var timing:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
				for i in range(bank[expected_key].size()):
					expected=bank[expected_key][i];cursor-=float(timing[expected_key].durations[i])/1000.0
					if cursor<0:break
				check(texture!=null and texture.get_image().get_data()==expected.get_image().get_data(),"Actual renderer exact turn/unload selection "+origin+" "+gear+" elapsed="+str(elapsed)+" expected="+expected_key+" clock="+str(expected_elapsed)+" action="+str(actor.action_elapsed())+" actualIndex="+str(bank[expected_key].find(texture)))
				observations.append({"gear":gear,"origin":origin,"elapsed":elapsed,"selected":expected_key,"turnAvailable":available})
			actor.timer=1.6
			var saved:Dictionary=actor.snapshot()
			check(Bridge.valid(saved),"Arrival checkpoint valid")
			check(preload("res://scripts/branforth_npc.gd").valid_branforth_snapshot(saved),"Full actor checkpoint admission")
			var file:=FileAccess.open("user://arrival321.snapshot",FileAccess.WRITE);file.store_var(saved);file.close()
			var loaded:Dictionary=FileAccess.open("user://arrival321.snapshot",FileAccess.READ).get_var()
			check(loaded[Bridge.FIELD]==saved[Bridge.FIELD],"Disk roundtrip retains incoming facing")
			await actor.restore_snapshot(game,loaded)
			check(actor.workshop_arrival_origin==saved[Bridge.FIELD] and absf(actor.timer-1.6)<.000001,"Actual actor restore retains arrival clock and direction")
			var paused_clock:float=actor.timer
			game.running=true;game.paused=true;game._process(.2)
			check(actor.timer==paused_clock,"Paused arrival simulation clock holds")
			var legacy:Dictionary=saved.duplicate(true);legacy.erase(Bridge.FIELD);check(Bridge.valid(legacy),"Old checkpoint remains valid without arrival field")
			var bad:Dictionary=saved.duplicate(true);bad[Bridge.FIELD]=42;check(not Bridge.valid(bad),"Malformed origin rejected")
			if available:
				actor.dead=true;check(Bridge.presentation(actor,player,.4,gear).is_empty(),"Death bypasses cosmetic arrival");actor.dead=false
				actor.movement_medium="flooded";check(Bridge.presentation(actor,player,.4,gear).is_empty(),"Flood bypasses cosmetic arrival");actor.movement_medium="dry"
	for path in ["res://scripts/james_workshop_arrival.gd.uid",OUT+"native_probe.gd.uid"]:
		if not FileAccess.file_exists(path):var uid:=FileAccess.open(path,FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var report:=FileAccess.open(OUT+"native-evidence.json",FileAccess.WRITE);report.store_string(JSON.stringify({"checks":checks,"failures":failures,"observations":observations,"scope":"actual arrive and renderer selectors using normal banks; disk field roundtrip, not title Continue or visual motion acceptance"},"  "))
	print("JAMES ARRIVAL: ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)
