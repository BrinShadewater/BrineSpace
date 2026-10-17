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
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var player=grid.branforth_player
	for gear in ["", "diving-helmet"]:
		var path: String=MANIFEST if gear.is_empty() else "res://character/james-water-family-v1/helmet-manifest.json"
		var rows: Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		var clocks: Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
		var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
		for state in manifest.states:
			var key: String=state.id
			check(rows[key].size()==6,"Six staged slots "+key)
			var elapsed:=0.0
			for slot in range(6):
				var tex: Texture2D=rows[key][slot]
				var disk:=Image.load_from_file(path.get_base_dir().path_join(state.frameFiles[slot]))
				check(tex.get_image().get_data()==disk.get_data(),"Exact staged pixels "+key+str(slot))
				check(tex.get_meta("crew_pivot")==Vector2(128,128),"Pivot "+key)
				check(tex.get_meta("crew_standing_height")==148.0,"Scale "+key)
				check(tex.get_meta("crew_water_pose")==true,"Water pose "+key)
				check(tex.get_meta("crew_water_kind")==state.waterKinds[slot],"Water kind "+key)
				check(tex.get_meta("crew_water_facing")==state.facings[slot],"Facing "+key)
				check(player.frame_at_elapsed(key,elapsed+float(state.frameDurationsMs[slot])/2000.0,gear)==tex,"Simulation slot "+key+str(slot))
				elapsed+=float(state.frameDurationsMs[slot])/1000.0
			check(absf(player.cycle_seconds(key,gear)-elapsed)<0.001,"Cycle duration "+key)
		for direction in ["east","south","west","north"]:
			for entering in [true,false]:
				var from_state: String="tread" if entering else "swim"
				var to_state: String="swim" if entering else "tread"
				var clip: String=("swim-start-" if entering else "swim-stop-")+direction
				var row: Array=rows[clip]
				var clock: Dictionary=clocks[clip]
				for phase in [0.0,.17,.49,.83]:
					player.current_key="";player.current_equipment=gear;player.motion.clear();player.last_time=-1;player.phase=0
					player.frame(from_state,direction,0.0,Vector2.ZERO,gear,true)
					player.frame(from_state,direction,phase,Vector2(phase*.16,0),gear,true)
					check(player.frame(to_state,direction,1.0,Vector2(.16,0),gear,true)==row[0],clip+" start from loop phase")
					check(player.frame(to_state,direction,1.0,Vector2(.16,0),gear,true)==row[0],clip+" pause")
					var elapsed:=1.0
					for slot in range(6):
						check(player.frame(to_state,direction,elapsed+float(clock.durations[slot])/2000.0,Vector2(.2,0),gear,true)==row[slot],clip+" transition slot "+str(slot))
						elapsed+=float(clock.durations[slot])/1000.0
					check(player.frame(to_state,direction,elapsed+.001,Vector2(.21,0),gear,true)==rows[to_state+"-"+direction][0],clip+" destination zero")
					check(player.motion.get("clip","")=="",clip+" completes")

	if DisplayServer.get_name()!="headless":
		for direction in ["east","south","west","north"]:
			var viewport:=SubViewport.new();viewport.size=Vector2i(1080,1280);viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
			var bg:=ColorRect.new();bg.size=Vector2(1080,1280);bg.color=Color("303b40");viewport.add_child(bg)
			for row_index in range(8):
				var action: String=["tread","swim-start","swim","swim-stop"][row_index%4]
				var gear: String="" if row_index<4 else "diving-helmet"
				var rows: Array=player.frames[action+"-"+direction] if gear.is_empty() else player.equipment_frames[gear][action+"-"+direction]
				var title:=Label.new();title.text=direction+" "+action+" "+("bare" if gear.is_empty() else "helmet")+" / station82px";title.position=Vector2(8,row_index*160);viewport.add_child(title)
				for column in range(6):
					var tex: Texture2D=rows[column];var sprite:=Sprite2D.new();sprite.centered=false;sprite.texture=tex;sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;sprite.scale=Vector2.ONE*82.0/148.0;sprite.position=Vector2(90+column*180,row_index*160+75)-tex.get_meta("crew_pivot")*82.0/148.0;viewport.add_child(sprite)
			await RenderingServer.frame_post_draw
			check(viewport.get_texture().get_image().save_png("res://character/james-water-family-v1/native-installed-"+direction+"-contact.png")==OK,"Native staged contact "+direction)
			viewport.queue_free()
	print("JAMES WATER INSTALLED: ",checks," loader/clock/transition checks; ",failures," failures; actual installed loader, all192 selected slots; route proof separate")
	grid.free()
	quit(1 if failures else 0)
