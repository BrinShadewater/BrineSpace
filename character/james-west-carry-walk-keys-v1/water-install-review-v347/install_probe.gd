extends SceneTree
const OUT="res://character/james-west-carry-walk-keys-v1/water-install-review-v347/"
const Player=preload("res://scripts/james_water_player.gd")
const Clearance=preload("res://scripts/james_water_clearance.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func same(a:Texture2D,b:Texture2D)->bool:return a.get_image().get_data()==b.get_image().get_data()
func seed_player(player,key:String,gear:String,target:String)->void:
	player.restore_snapshot({"key":"swim-"+target,"equipment":gear,"phase":0.0,"last_time":19.9,"started":19.0,"last_position":Vector2.ZERO,"motion":{"state":"swim","direction":target,"clip":key,"started":20.0}})
func _init()->void:call_deferred("run")
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile")
	if failures:quit(2);return
	var grid=preload("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var player=Player.new()
	for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides"]:player.set(field,grid.branforth_player.get(field).duplicate(true))
	player.install_bridges()
	var actor=preload("res://scripts/james_cargo_actor.gd").new();actor.active=true;actor.state="walk";actor.movement_medium="flooded";actor.foot=Vector2(192,192)
	var game:Dictionary={"placed_rooms":[],"occupied":{},"wrecks":{},"drone_fleet":{"sites":{},"orders":[],"drones":{}}}
	var rows:=0;var completions:=0
	for gear in ["","diving-helmet"]:
		var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		actor.helmet_equipped=not gear.is_empty()
		for key in bank:
			if not str(key).begins_with("swim-reorient-"):continue
			rows+=1
			var target:String=str(key).get_slice("-",5)
			var end:float=20.0+player.cycle_seconds(key,gear)
			for state in ["swim","tread"]:
				for requested in ["west","east","north","south"]:
					seed_player(player,key,gear,target)
					var snapshot:Dictionary=player.snapshot()
					var predicted:String=player.preview_water_transition(state,requested,end+.001,gear)
					check(player.snapshot()==snapshot,"Completion prediction remains read-only")
					var tex:Texture2D=player.frame(state,requested,end+.001,Vector2.ZERO,gear,true)
					check(str(player.motion.clip)==predicted,"Completion prediction equals actual selection")
					check(same(tex,bank["swim-"+target][0]),"New command begins at completed source endpoint")
					if requested!=target:
						var duration:float=player.cycle_seconds(player.motion.clip,gear)
						tex=player.frame(state,requested,end+.002+duration,Vector2.ZERO,gear,true)
						check(same(tex,bank["swim-"+requested][0]),"Latest heading finishes on neutral destination")
						if state=="tread":
							tex=player.frame(state,requested,end+.003+duration+player.cycle_seconds("swim-stop-"+requested,gear),Vector2.ZERO,gear,true)
							check(same(tex,bank["tread-"+requested][0]),"Queued stop finishes upright after latest heading")
					completions+=1
			seed_player(player,key,gear,target);actor.foot=Vector2(192,192);actor.direction=target;actor.movement_medium="flooded";actor.path.clear()
			actor.geometry={Vector2i.ZERO:{"open":[0,1,2,3],"blockers":[],"swim_blockers":[]}};actor.swim_region_cache.clear()
			check(Clearance.clear(game,actor,player,key,20.01),"Actual subclass admits full bridge in open room")
			var extent:Array=player.clip_extent(key,gear);var center:=Vector2((extent[0]+extent[2])/2.0,(extent[1]+extent[3])/2.0)
			actor.geometry[Vector2i.ZERO].swim_blockers=[Rect2(center-Vector2.ONE,Vector2.ONE*2)];actor.swim_region_cache.clear()
			check(not Clearance.clear(game,actor,player,key,20.01),"Actual subclass rejects blocked full bridge")
			player.frame("swim",target,20.01,Vector2.ZERO,gear,false)
			check(str(player.motion.clip).is_empty(),"Blocked bridge cancels to existing locomotion fallback")
			seed_player(player,key,gear,target);actor.foot=Vector2(1000,1000);actor.geometry.clear();actor.movement_medium="exterior";actor.path=PackedVector2Array([actor.foot+Vector2(0,-24)])
			check(Clearance.clear(game,actor,player,key,20.01),"Open sea admits swept full bridge")
			# Registered blocker in a neighbouring room intersects the current body.
			actor.geometry={Vector2i.ZERO:{"swim_blockers":[Rect2(actor.foot-Vector2(192,192)+center-Vector2.ONE,Vector2.ONE*2)]}}
			check(not Clearance.clear(game,actor,player,key,20.01),"Exterior rejects registered prop intersecting full bridge")
			# Blocker beyond the current pose but within the travelled envelope.
			actor.geometry[Vector2i.ZERO].swim_blockers=[Rect2(actor.foot-Vector2(192,192)+Vector2(center.x,extent[1]-12),Vector2.ONE*2)]
			check(preload("res://scripts/crew_expedition.gd").exterior_pose_clear(game,actor,extent),"Future exterior obstacle is clear at current position")
			check(not Clearance.clear(game,actor,player,key,20.01),"Swept exterior clearance rejects future obstruction")
	for path in ["res://scripts/james_water_player.gd.uid","res://scripts/james_water_phase_player.gd.uid","res://scripts/james_water_clearance.gd.uid","res://character/james-west-carry-walk-keys-v1/water-install-review-v347/install_probe.gd.uid"]:
		if not FileAccess.file_exists(path):FileAccess.open(path,FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	FileAccess.open(OUT+"install-review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"rows":rows,"completionCases":completions,"scope":"Actual selected banks cloned to candidate runtime player; all 288 reorientation rows, latest-heading/stop completion, actual James subclass flooded collision and open-sea swept registered blocker checks. Headless geometry/playback; no native route or normal selection yet."},"\t"))
	grid.free();print("JAMES WATER INSTALL checks=",checks," failures=",failures," rows=",rows," completionCases=",completions);quit(0 if failures==0 else 1)

