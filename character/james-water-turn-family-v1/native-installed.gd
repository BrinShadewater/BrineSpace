extends SceneTree
var checks:=0
var failures:=0
const FAMILY:="res://character/james-water-turn-family-v1/"
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
		var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(FAMILY+mode+"-manifest.json"))
		var frames:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		for state in m.states:
			var key:String=state.id
			var source:String=key.get_slice("-",2)
			var target:String=key.get_slice("-",3)
			var row:Array=frames[key]
			check(row.size()==state.frameFiles.size(),"Selected slot count "+key)
			var elapsed:=0.0
			for i in range(row.size()):
				var tex:Texture2D=row[i]
				var disk:=Image.load_from_file((FAMILY+mode+"-manifest.json").get_base_dir().path_join(state.frameFiles[i]))
				check(tex.get_image().get_data()==disk.get_data(),"Exact staged texture "+key+str(i))
				check(tex.get_meta("crew_pivot")==Vector2(128,128),"World pivot "+key)
				check(tex.get_meta("crew_standing_height")==148.0,"Physical scale "+key)
				check(tex.get_meta("crew_water_pose")==true,"Water pose "+key)
				check(tex.get_meta("crew_water_kind")==state.waterKinds[i],"Water kind "+key)
				check(tex.get_meta("crew_water_facing")==state.facings[i],"Facing "+key)
				check(player.frame_at_elapsed(key,elapsed+float(state.frameDurationsMs[i])/2000.0,gear)==tex,"Elapsed slot "+key)
				elapsed+=float(state.frameDurationsMs[i])/1000.0
			check(absf(player.cycle_seconds(key,gear)-elapsed)<.001,"Retained turn clock "+key)
			check(row[0].get_image().get_data()==frames["swim-"+source][0].get_image().get_data(),"Exact source swim endpoint "+key)
			check(row.back().get_image().get_data()==frames["swim-"+target][0].get_image().get_data(),"Exact target swim endpoint "+key)
			for phase in [0.0,.19,.73]:
				player.motion.clear();player.current_key="";player.current_equipment=gear;player.last_time=-1;player.phase=0
				player.frame("swim",source,0.0,Vector2.ZERO,gear,true)
				player.frame("swim",source,phase,Vector2(.03,0),gear,true)
				check(player.frame("swim",target,1.0,Vector2(.04,0),gear,true)==row[0],"Turn entry from moving phase "+key)
				check(player.frame("swim",target,1.0,Vector2(.04,0),gear,true)==row[0],"Paused turn entry "+key)
				var clock:=1.0
				for i in range(row.size()):
					var t:float=clock+float(state.frameDurationsMs[i])/2000.0
					check(player.frame("swim",target,t,Vector2(.05,0),gear,true)==row[i],"Actual player turn slot "+key+str(i))
					check(player.frame("swim",target,t,Vector2(.05,0),gear,true)==row[i],"Pause preserves slot "+key+str(i))
					clock+=float(state.frameDurationsMs[i])/1000.0
				check(player.frame("swim",target,clock+.002,Vector2(.06,0),gear,true)==frames["swim-"+target][0],"Destination loop zero "+key)
				check(player.motion.get("clip","")=="","Turn completes "+key)
		if DisplayServer.get_name()!="headless":
			var viewport:=SubViewport.new();viewport.size=Vector2i(1320,650);viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
			var bg:=ColorRect.new();bg.size=Vector2(1320,650);bg.color=Color("303b40");viewport.add_child(bg)
			for r in range(4):
				var pair:String=["east-south","south-west","west-north","north-east"][r]
				var label:=Label.new();label.text=pair+" "+mode+" / 82px native";label.position=Vector2(8,r*160);viewport.add_child(label)
				for i in range(6):
					var tex:Texture2D=frames["swim-turn-"+pair][i]
					var sprite:=Sprite2D.new();sprite.centered=false;sprite.texture=tex;sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;sprite.scale=Vector2.ONE*82.0/148.0;sprite.position=Vector2(110+i*210,80+r*160)-Vector2(128,128)*82.0/148.0;viewport.add_child(sprite)
			await RenderingServer.frame_post_draw
			check(viewport.get_texture().get_image().save_png(FAMILY+"native-installed-"+mode+"-contact.png")==OK,"Native contact "+mode)
			viewport.queue_free()
	print("JAMES WATER TURNS INSTALLED: ",checks," checks; ",failures," failures; actual normal grid loader and turn playback, route proof separate")
	grid.free()
	quit(1 if failures else 0)
