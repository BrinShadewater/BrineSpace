extends SceneTree
## Actual installed Bill water family; scratch-profile only.
const PACKS := [
	["res://character/bill-swim-east-coherent-v1/manifest.json", ""],
	["res://character/bill-tread-east-coherent-v1/manifest.json", ""],
	["res://character/bill-swim-transitions-east-coherent-v1/manifest.json", ""],
	["res://character/bill-swim-helmet-east-coherent-v1/manifest.json", "diving-helmet"],
	["res://character/bill-tread-helmet-east-coherent-v1/manifest.json", "diving-helmet"],
	["res://character/bill-swim-transitions-helmet-east-coherent-v1/manifest.json", "diving-helmet"],
	["res://character/bill-swim-west-coherent-v1/manifest.json", ""],
	["res://character/bill-tread-west-coherent-v1/manifest.json", ""],
	["res://character/bill-swim-transitions-west-coherent-v1/manifest.json", ""],
	["res://character/bill-swim-helmet-west-coherent-v1/manifest.json", "diving-helmet"],
	["res://character/bill-tread-helmet-west-coherent-v1/manifest.json", "diving-helmet"],
	["res://character/bill-swim-transitions-helmet-west-coherent-v1/manifest.json", "diving-helmet"],
	["res://character/bill-swim-north-coherent-v1/manifest.json", ""],
	["res://character/bill-tread-north-coherent-v1/manifest.json", ""],
	["res://character/bill-swim-transitions-north-coherent-v1/manifest.json", ""],
	["res://character/bill-swim-helmet-north-coherent-v1/manifest.json", "diving-helmet"],
	["res://character/bill-tread-helmet-north-coherent-v1/manifest.json", "diving-helmet"],
	["res://character/bill-swim-transitions-helmet-north-coherent-v1/manifest.json", "diving-helmet"],
	["res://character/bill-swim-south-coherent-v1/manifest.json", ""],
	["res://character/bill-tread-south-coherent-v1/manifest.json", ""],
	["res://character/bill-swim-transitions-south-coherent-v1/manifest.json", ""],
	["res://character/bill-swim-helmet-south-coherent-v1/manifest.json", "diving-helmet"],
	["res://character/bill-tread-helmet-south-coherent-v1/manifest.json", "diving-helmet"],
	["res://character/bill-swim-transitions-helmet-south-coherent-v1/manifest.json", "diving-helmet"]]
var checks:=0
var failures:=0
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:call_deferred("run")
func run() -> void:
	var user_path: String=OS.get_user_data_dir().replace("\\","/").to_lower()
	var scratch_path: String=OS.get_environment("APPDATA").replace("\\","/").to_lower()
	check(user_path.begins_with(scratch_path+"/") and "/output/bill-water-sides-native-v1/scratch-appdata/" in user_path,"Resolved user:// is isolated")
	print("BILL WATER USER PATH: "+OS.get_user_data_dir())
	if failures:quit(1);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player
	for spec in PACKS:
		var path: String=spec[0];var gear: String=spec[1];var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path));var direction: String="south" if "south-coherent" in path else "north" if "north-coherent" in path else ("west" if "west-coherent" in path else "east")
		for state in pack.states:
			var rows: Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
			var clocks: Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
			check(rows.has(state.id),state.id+" selected "+gear)
			if not rows.has(state.id):continue
			check(rows[state.id].size()==state.frameFiles.size(),state.id+" frame count")
			check(clocks[state.id].durations==state.frameDurationsMs and clocks[state.id].loop==state.loop,state.id+" clock")
			var elapsed:=0.0
			for i in state.frameFiles.size():
				var frame: Texture2D=rows[state.id][i];var expected:=Image.load_from_file(path.get_base_dir().path_join(state.frameFiles[i]))
				check(frame.get_image().get_data()==expected.get_data(),state.id+" selected pixels "+str(i)+gear)
				check(frame.get_meta("crew_pivot")==Vector2(pack.pivot[0],pack.pivot[1]) and frame.get_meta("crew_standing_height")==148.0,state.id+" registration")
				check(frame.get_meta("crew_water_pose")==true and frame.get_meta("crew_water_kind")==state.waterKinds[i] and frame.get_meta("crew_water_facing")==direction,state.id+" water metadata")
				check(player.frame_at_elapsed(state.id,elapsed+float(state.frameDurationsMs[i])/2000.0,gear)==frame,state.id+" selected elapsed sampling")
				elapsed+=float(state.frameDurationsMs[i])/1000.0
	check(is_equal_approx(player.strides.swim,.16),"Selected swim stride")
	var locomotion: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/crew-runtime-matte-v1/bill/manifest.json"))
	for key in locomotion.get("strideDistanceCells",{}):check(is_equal_approx(player.strides[key],locomotion.strideDistanceCells[key]),"Preserved selected gait stride "+key)
	for direction in ["east","west","north","south"]:
		for gear in ["","diving-helmet"]:
			for entering in [true,false]:
				var from_state: String="tread" if entering else "swim"
				var to_state: String="swim" if entering else "tread"
				var clip: String="swim-start-"+direction if entering else "swim-stop-"+direction
				var row: Array=player.frames[clip] if gear.is_empty() else player.equipment_frames[gear][clip]
				var clock: Dictionary=player.timing[clip] if gear.is_empty() else player.equipment_timing[gear][clip]
				for initial_phase in [0.0,.17,.49,.83]:
					player.current_key="";player.current_equipment=gear;player.motion.clear();player.last_time=-1;player.phase=0
					player.frame(from_state,direction,0.0,Vector2.ZERO,gear,true)
					player.frame(from_state,direction,initial_phase,Vector2(initial_phase*.16,0),gear,true)
					var started:=1.0
					check(player.frame(to_state,direction,started,Vector2(.16,0),gear,true)==row[0],clip+" start from loop phase "+str(initial_phase)+gear)
					check(player.frame(to_state,direction,started,Vector2(.16,0),gear,true)==row[0],clip+" paused simulation time")
					var elapsed:=started
					for i in row.size():
						check(player.frame(to_state,direction,elapsed+float(clock.durations[i])/2000.0,Vector2(.2,0),gear,true)==row[i],clip+" live phase "+str(i)+gear)
						elapsed+=float(clock.durations[i])/1000.0
					var destination: Array=player.frames[to_state+"-"+direction] if gear.is_empty() else player.equipment_frames[gear][to_state+"-"+direction]
					check(player.frame(to_state,direction,elapsed+.001,Vector2(.21,0),gear,true)==destination[0],clip+" resumes destination frame zero")
					check(player.motion.get("clip","")=="",clip+" completes transition")
	if DisplayServer.get_name()!="headless":
		for direction in ["east","west","north","south"]:
			var viewport:=SubViewport.new();viewport.size=Vector2i(1200,1400);viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
			var bg:=ColorRect.new();bg.size=Vector2(1200,1400);bg.color=Color("22343e");viewport.add_child(bg)
			for row_index in 8:
				var key: String=["tread-","swim-start-","swim-","swim-stop-"][row_index%4]+direction;var gear: String="" if row_index<4 else "diving-helmet"
				var rows: Array=player.frames[key] if gear.is_empty() else player.equipment_frames[gear][key]
				var title:=Label.new();title.text=key+" "+("bare" if gear.is_empty() else "helmet");title.position=Vector2(10,row_index*175);viewport.add_child(title)
				for column in 6:
					var frame: Texture2D=rows[column];var scale_factor:=82.0/148.0;var sprite:=Sprite2D.new();sprite.centered=false;sprite.texture=frame;sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;sprite.scale=Vector2.ONE*scale_factor;sprite.position=Vector2(100+column*200,row_index*175+85)-frame.get_meta("crew_pivot")*scale_factor;viewport.add_child(sprite)
			await RenderingServer.frame_post_draw
			DirAccess.make_dir_recursive_absolute("res://output/bill-water-sides-native-v1")
			check(viewport.get_texture().get_image().save_png("res://output/bill-water-sides-native-v1/loaded-water-"+direction+".png")==OK,"Fresh native selected water contact")
			viewport.queue_free()
	grid.free();print("BILL WATER SELECTED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
