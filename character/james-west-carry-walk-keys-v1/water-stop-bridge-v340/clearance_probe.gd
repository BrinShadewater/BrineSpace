extends SceneTree
const OUT="res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/"
const Player=preload("res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/phase_player.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Isolated owner profile")
	if failures:quit(2);return
	var grid=preload("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var player=Player.new()
	for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides"]:player.set(field,grid.branforth_player.get(field).duplicate(true))
	player.install_bridges()
	var staged_grid=preload("res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/staged_grid.gd").new();staged_grid.branforth_player=player
	var actor=preload("res://scripts/branforth_npc.gd").new();actor.foot=Vector2(192,192);actor.movement_medium="flooded"
	var profiles:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/chief-engineer-branforth-v2/clearance.json"))
	actor.swim_clearance=profiles.swim;actor.tread_clearance=profiles.tread
	var samples:=0;var gear_samples:=0;var facing_resets:=0;var records:Array=[]
	for gear in ["","diving-helmet"]:
		var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
		actor.helmet_equipped=not gear.is_empty()
		for direction in ["west","east","north","south"]:
			actor.direction=direction
			for phase in range(1,5):
				var key:String="swim-stop-phase-"+str(phase)+"-"+direction
				var elapsed:=0.0
				for slot in range(bank[key].size()):
					var time:float=10.0+elapsed+float(clocks[key].durations[slot])/2000.0
					player.restore_snapshot({"key":"swim-"+direction,"equipment":gear,"phase":0.0,"last_time":9.9,"started":9.0,"last_position":Vector2.ZERO,"motion":{"state":"tread","direction":direction,"clip":key,"started":10.0}})
					var saved:Dictionary=player.snapshot()
					check(player.preview_water_transition("tread",direction,time,gear)==key,"Clearance predicts exact active stop row")
					check(player.snapshot()==saved,"Clearance prediction does not mutate playback")
					var other:String="diving-helmet" if gear.is_empty() else ""
					var other_bank:Dictionary=player.frames if other.is_empty() else player.equipment_frames[other]
					check(player.preview_water_transition("tread",direction,time,other)==key,"Gear prediction retains active clock")
					check(player.frame("tread",direction,time,Vector2.ZERO,other,true)==other_bank[key][slot],"Gear change uses corresponding selected source pose")
					gear_samples+=1;player.restore_snapshot(saved)
					for target in ["west","east","north","south"]:
						if target==direction:continue
						player.restore_snapshot(saved)
						check(player.preview_water_transition("tread",target,time,gear)==key,"Changed heading clearance retains entire active rise")
						check(player.frame("tread",target,time,Vector2.ZERO,gear,true)==bank[key][slot],"Direction change preserves current rise pose")
						check(player.frame("tread",target,10.0+player.cycle_seconds(key,gear)+.001,Vector2.ZERO,gear,true)==bank["tread-"+target][0],"Finished rise applies requested idle facing")
						player.restore_snapshot(saved);player.frame("tread",target,time,Vector2.ZERO,gear,true)
						if str(player.motion.clip).is_empty():facing_resets+=1
					player.restore_snapshot(saved)
					elapsed+=float(clocks[key].durations[slot])/1000.0
				var extent:Array=player.clip_extent(key,gear)
				actor.geometry={Vector2i.ZERO:{"open":[0,1,2,3],"blockers":[],"swim_blockers":[]}}
				actor.swim_region_cache.clear()
				check(actor.swim_segment_clear(actor.foot,actor.foot,direction,direction,false,extent),"Actual James collision accepts bridge in empty fixture room")
				player.restore_snapshot({"key":"swim-"+direction,"equipment":gear,"phase":0.0,"last_time":9.9,"started":9.0,"last_position":Vector2.ZERO,"motion":{"state":"tread","direction":direction,"clip":key,"started":10.0}})
				staged_grid.fixture_visual_time=10.01
				var renderer_saved:Dictionary=player.snapshot()
				check(staged_grid._water_transition_clear(actor),"Staged renderer admits exact whole stop bridge")
				check(player.snapshot()==renderer_saved,"Renderer clearance does not advance playback")
				var center:=Vector2((extent[0]+extent[2])/2.0,(extent[1]+extent[3])/2.0)
				actor.geometry[Vector2i.ZERO].swim_blockers=[Rect2(center-Vector2.ONE,Vector2.ONE*2)];actor.swim_region_cache.clear()
				check(not actor.swim_segment_clear(actor.foot,actor.foot,direction,direction,false,extent),"Actual James collision rejects blocker intersecting bridge")
				check(not staged_grid._water_transition_clear(actor),"Staged renderer rejects obstructed bridge or restart")
				records.append({"gear":gear,"direction":direction,"phase":phase,"extent":extent});samples+=1
	for stem in ["clearance_probe","staged_grid"]:
		if not FileAccess.file_exists(OUT+stem+".gd.uid"):
			FileAccess.open(OUT+stem+".gd.uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	FileAccess.open(OUT+"clearance-review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"collisionCases":samples,"gearSamples":gear_samples,"directionChangeResets":facing_resets,"records":records,"normalChanged":false,"scope":"Staged prediction and actual James collision primitive on synthetic room geometry; direction reset diagnostic, not native renderer route or whole-run acceptance."},"\t"))
	staged_grid.free();grid.free();print("JAMES STAGED CLEARANCE checks=",checks," failures=",failures," cases=",samples," gear=",gear_samples," direction resets=",facing_resets);quit(0 if failures==0 else 1)
