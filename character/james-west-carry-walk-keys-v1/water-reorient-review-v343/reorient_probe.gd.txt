extends SceneTree
const OUT="res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/"
const Player=preload("res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/reorient_player.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func same(a:Texture2D,b:Texture2D)->bool:
	if a==null or b==null:return false
	var aa:Texture2D=a.diffuse_texture if a is CanvasTexture else a
	var bb:Texture2D=b.diffuse_texture if b is CanvasTexture else b
	return aa.get_image().get_data()==bb.get_image().get_data()
func clone(normal):
	var player=Player.new()
	for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides"]:player.set(field,normal.get(field).duplicate(true))
	player.install_bridges();return player
func _init()->void:call_deferred("run")
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile")
	if failures:quit(2);return
	var grid=preload("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var player=clone(grid.branforth_player);var fresh=clone(grid.branforth_player);var samples:=0;var rows:=0
	var fixture=preload("res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/staged_grid.gd").new();fixture.branforth_player=player
	var actor=preload("res://scripts/branforth_npc.gd").new();actor.foot=Vector2(192,192);actor.movement_medium="flooded";actor.state="walk"
	var profiles:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/chief-engineer-branforth-v2/clearance.json"));actor.swim_clearance=profiles.swim;actor.tread_clearance=profiles.tread
	for gear in ["","diving-helmet"]:
		var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
		for source in ["west","east","north","south"]:
			for target in ["west","east","north","south"]:
				if source==target:continue
				check(same(bank["swim-turn-"+source+"-"+target][0],bank["swim-"+source][0]),"Actual selected turn entry matches neutral swimming")
				check(same(bank["swim-turn-"+source+"-"+target][-1],bank["swim-"+target][0]),"Actual selected turn exit matches destination swimming")
				for phase in range(1,5):
					var key:String="swim-stop-phase-"+str(phase)+"-"+source
					var elapsed:=0.0
					for slot in range(bank[key].size()):
						var time:float=10.0+elapsed+float(clocks[key].durations[slot])/2000.0
						player.restore_snapshot({"key":"swim-"+source,"equipment":gear,"phase":0.0,"last_time":9.9,"started":9.0,"last_position":Vector2.ZERO,"motion":{"state":"tread","direction":source,"clip":key,"started":10.0}})
						var before:Texture2D=player.frame("tread",source,time,Vector2.ZERO,gear,true)
						var saved:Dictionary=player.snapshot();var predicted:String=player.preview_water_transition("swim",target,time,gear)
						check(predicted.begins_with("swim-reorient-"),"Changed heading selects pose-specific reorientation")
						check(player.snapshot()==saved,"Reorientation clearance prediction is read-only")
						check(same(before,player.frame("swim",target,time,Vector2(.02,0),gear,true)),"Changed-heading restart preserves exact current source pose")
						check(player.motion.clip==predicted,"Prediction matches actual playback")
						var restarted:Dictionary=player.snapshot();fresh.restore_snapshot(restarted)
						check(same(before,fresh.frame("swim",target,time,Vector2(.02,0),gear,true)),"Fresh reorientation restore preserves entry")
						check(same(player.frame("swim",target,time+player.cycle_seconds(predicted,gear)+.001,Vector2(.04,0),gear,true),bank["swim-"+target][0]),"Reorientation completes at selected destination neutral")
						check(not player.clip_extent(predicted,gear).is_empty(),"Complete reorientation collision extent present")
						elapsed+=float(clocks[key].durations[slot])/1000.0;samples+=1
		for key in bank:
			if not str(key).begins_with("swim-reorient-"):continue
			check(bank[key].size()==clocks[key].durations.size() and not clocks[key].loop,"Finite row clock coverage")
			check(str(key).length()<=64,"Checkpoint key contract")
			var target:String=str(key).get_slice("-",5)
			var elapsed:=0.0
			for slot in range(bank[key].size()):
				var time:float=20.0+elapsed+float(clocks[key].durations[slot])/2000.0
				player.restore_snapshot({"key":"swim-"+target,"equipment":gear,"phase":0.0,"last_time":19.9,"started":19.0,"last_position":Vector2.ZERO,"motion":{"state":"swim","direction":target,"clip":key,"started":20.0}})
				var saved:Dictionary=player.snapshot()
				check(same(player.frame("swim",target,time,Vector2.ZERO,gear,true),bank[key][slot]),"Reorientation finite clock selects authored slot")
				check(same(player.frame("swim",target,time,Vector2.ZERO,gear,true),bank[key][slot]),"Paused reorientation holds pose")
				fresh.restore_snapshot(saved)
				check(same(fresh.frame("swim",target,time,Vector2.ZERO,gear,true),bank[key][slot]),"Fresh restore holds every reorientation slot")
				check(same(player.frame("tread",target,time,Vector2.ZERO,gear,true),bank[key][slot]),"Stop during reorientation retains current finite pose")
				elapsed+=float(clocks[key].durations[slot])/1000.0
			player.restore_snapshot({"key":"swim-"+target,"equipment":gear,"phase":0.0,"last_time":19.9,"started":19.0,"last_position":Vector2.ZERO,"motion":{"state":"swim","direction":target,"clip":key,"started":20.0}})
			actor.direction=target;actor.helmet_equipped=not gear.is_empty();fixture.fixture_visual_time=20.01
			actor.geometry={Vector2i.ZERO:{"open":[0,1,2,3],"blockers":[],"swim_blockers":[]}};actor.swim_region_cache.clear()
			var saved:Dictionary=player.snapshot()
			check(fixture._water_transition_clear(actor),"Fixture renderer admits whole reorientation in empty room")
			check(player.snapshot()==saved,"Fixture renderer predicts reorientation without mutation")
			var extent:Array=player.clip_extent(key,gear);var center:=Vector2((extent[0]+extent[2])/2.0,(extent[1]+extent[3])/2.0)
			actor.geometry[Vector2i.ZERO].swim_blockers=[Rect2(center-Vector2.ONE,Vector2.ONE*2)];actor.swim_region_cache.clear()
			check(not fixture._water_transition_clear(actor),"Fixture renderer rejects obstructed reorientation")
			rows+=1
	for stem in ["reorient_player","reorient_probe"]:
		if not FileAccess.file_exists(OUT+stem+".gd.uid"):FileAccess.open(OUT+stem+".gd.uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	FileAccess.open(OUT+"reorient-review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":samples,"rows":rows,"normalChanged":false,"scope":"Staged changed-heading resume from all stop bridge poses; exact selected turn endpoints, finite rows, read-only prediction, fresh playback restore and completion. No native renderer, actual route, blocked-space or whole-run Continue acceptance."},"\t"))
	fixture.free();grid.free();print("JAMES STAGED REORIENT checks=",checks," failures=",failures," samples=",samples," rows=",rows);quit(0 if failures==0 else 1)
