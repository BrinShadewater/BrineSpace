extends SceneTree
var failures:=0
var checks:=0
const MANIFEST := "res://character/james-water-family-v1/bare-manifest.json"
func check(ok: bool,why: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init() -> void:call_deferred("run")
func run() -> void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Resolved user profile is isolated")
	if failures:quit(2);return
	var player=preload("res://scripts/crew_sprite_player.gd").new()
	player.load_manifest(MANIFEST)
	var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(MANIFEST))
	for state in manifest.states:
		var key: String=state.id
		check(player.frames[key].size()==6,"Six staged slots "+key)
		var elapsed:=0.0
		for slot in range(6):
			var tex: Texture2D=player.frames[key][slot]
			var disk:=Image.load_from_file(MANIFEST.get_base_dir().path_join(state.frameFiles[slot]))
			check(tex.get_image().get_data()==disk.get_data(),"Exact staged pixels "+key+str(slot))
			check(tex.get_meta("crew_pivot")==Vector2(128,128),"Pivot "+key)
			check(tex.get_meta("crew_standing_height")==148.0,"Scale "+key)
			check(tex.get_meta("crew_water_pose")==true,"Water pose "+key)
			check(tex.get_meta("crew_water_kind")==state.waterKinds[slot],"Water kind "+key)
			check(tex.get_meta("crew_water_facing")==state.facings[slot],"Facing "+key)
			check(player.frame_at_elapsed(key,elapsed+float(state.frameDurationsMs[slot])/2000.0)==tex,"Simulation slot "+key+str(slot))
			elapsed+=float(state.frameDurationsMs[slot])/1000.0
		check(absf(player.cycle_seconds(key)-elapsed)<0.001,"Cycle duration "+key)
	for direction in ["east","south","west","north"]:
		for entering in [true,false]:
			var from_state: String="tread" if entering else "swim"
			var to_state: String="swim" if entering else "tread"
			var clip: String=("swim-start-" if entering else "swim-stop-")+direction
			var row: Array=player.frames[clip]
			var clock: Dictionary=player.timing[clip]
			for phase in [0.0,.17,.49,.83]:
				player.current_key="";player.current_equipment="";player.motion.clear();player.last_time=-1;player.phase=0
				player.frame(from_state,direction,0.0,Vector2.ZERO,"",true)
				player.frame(from_state,direction,phase,Vector2(phase*.16,0),"",true)
				check(player.frame(to_state,direction,1.0,Vector2(.16,0),"",true)==row[0],clip+" start from loop phase")
				check(player.frame(to_state,direction,1.0,Vector2(.16,0),"",true)==row[0],clip+" pause")
				var elapsed:=1.0
				for slot in range(6):
					check(player.frame(to_state,direction,elapsed+float(clock.durations[slot])/2000.0,Vector2(.2,0),"",true)==row[slot],clip+" transition slot "+str(slot))
					elapsed+=float(clock.durations[slot])/1000.0
				check(player.frame(to_state,direction,elapsed+.001,Vector2(.21,0),"",true)==player.frames[to_state+"-"+direction][0],clip+" destination zero")
				check(player.motion.get("clip","")=="",clip+" completes")
	print("JAMES WATER STAGED: ",checks," loader/clock/transition checks; ",failures," failures; no live-route or installation claim")
	quit(1 if failures else 0)
