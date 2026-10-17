extends SceneTree
var checks:=0
var failures:=0
func check(ok:bool,why:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init()->void:call_deferred("run")
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Resolved scratch profile")
	if failures:quit(2);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var player=grid.branforth_player
	for gear in ["","diving-helmet"]:
		var mode:String="bare" if gear.is_empty() else "helmet"
		var path:String="res://character/james-death-family-v1/bare-manifest.json" if gear.is_empty() else "res://character/james-death-family-v1/helmet-manifest.json"
		var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
		var frames:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		for state in m.states:
			var key:String=state.id
			var row:Array=frames[key]
			check(row.size()==6,"Selected slots "+key)
			var elapsed:=0.0
			for i in range(row.size()):
				var tex:Texture2D=row[i]
				var disk:=Image.load_from_file(path.get_base_dir().path_join(state.frameFiles[i]))
				check(tex.get_image().get_data()==disk.get_data(),"Exact staged texture "+key+str(i))
				check(tex.get_meta("crew_pivot")==Vector2(128,224),"World pivot "+key)
				check(tex.get_meta("crew_standing_height")==148.0,"Physical scale "+key)
				check(tex.get_meta("crew_water_pose")==state.waterPoses[i],"Water pose "+key)
				check(tex.get_meta("crew_water_kind")==state.waterKinds[i],"Water kind "+key)
				check(tex.get_meta("crew_water_facing")==state.facings[i],"Facing "+key)
				var sample:float=elapsed+float(state.frameDurationsMs[i])/2000.0
				check(player.frame_at_elapsed(key,sample,gear)==tex,"Elapsed slot "+key+str(i))
				check(player.frame_at_elapsed(key,sample,gear)==tex,"Same elapsed preserves slot "+key+str(i))
				elapsed+=float(state.frameDurationsMs[i])/1000.0
			check(absf(player.cycle_seconds(key,gear)-elapsed)<.001,"Retained clock "+key)
			check(player.frame_at_elapsed(key,elapsed+.001,gear)==row.back(),"Simulation sampler clamps to final slot "+key)
			var d:String=key.get_slice("-",key.get_slice_count("-")-1)
			var action:String=key.trim_suffix("-"+d)
			player.motion.clear();player.current_key="";player.current_equipment=gear;player.last_time=-1;player.phase=0
			check(player.frame(action,d,0.0,Vector2.ZERO,gear)==row[0],"Playback begins at neutral "+key)
			var cursor:=0.0
			for i in range(row.size()):
				var t:float=cursor+float(state.frameDurationsMs[i])/2000.0
				var position:=Vector2(.16*t/elapsed,0) if action=="swim-carry" else Vector2.ZERO
				check(player.frame(action,d,t,position,gear)==row[i],"Actual playback slot "+key+str(i))
				check(player.frame(action,d,t,position,gear)==row[i],"Paused playback slot "+key+str(i))
				cursor+=float(state.frameDurationsMs[i])/1000.0
			var final_position:=Vector2(.16*(elapsed+.001)/elapsed,0) if action=="swim-carry" else Vector2.ZERO
			check(player.frame(action,d,elapsed+.001,final_position,gear)==(row[0] if state.loop else row.back()),"Loop or one-shot playback completion "+key)
		if DisplayServer.get_name()!="headless":
			var viewport:=SubViewport.new();viewport.size=Vector2i(1320,m.states.size()*150);viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
			var bg:=ColorRect.new();bg.size=Vector2(viewport.size);bg.color=Color("303b40");viewport.add_child(bg)
			for r in range(m.states.size()):
				var key:String=m.states[r].id
				var label:=Label.new();label.text=key+" "+mode+" / 82px native";label.position=Vector2(8,r*150);viewport.add_child(label)
				for i in range(6):
					var sprite:=Sprite2D.new();sprite.centered=false;sprite.texture=frames[key][i];sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;sprite.scale=Vector2.ONE*82.0/148.0;sprite.position=Vector2(110+i*210,(35 if m.states[r].waterPoses[0] else 135)+r*150)-Vector2(128,224)*82.0/148.0;viewport.add_child(sprite)
			await RenderingServer.frame_post_draw
			var output:String="res://character/james-death-family-v1/native-installed-bare-contact.png" if gear.is_empty() else "res://character/james-death-family-v1/native-installed-helmet-contact.png"
			check(viewport.get_texture().get_image().save_png(output)==OK,"Native contact "+mode)
			viewport.queue_free()
	print("JAMES DEATH INSTALLED: ",checks," checks; ",failures," failures; actual installed normal loader and player/render")
	grid.free()
	quit(1 if failures else 0)
