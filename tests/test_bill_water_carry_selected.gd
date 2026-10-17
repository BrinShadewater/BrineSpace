extends SceneTree
## Actual Bill runtime-selected water cargo; no selected injection; scratch-profile only.
const PACKS := [
 ["res://character/bill-swim-carry-east-coherent-v1/manifest.json", ""],
 ["res://character/bill-swim-carry-west-coherent-v1/manifest.json", ""],
 ["res://character/bill-swim-carry-north-coherent-v1/manifest.json", ""],
 ["res://character/bill-swim-carry-south-coherent-v1/manifest.json", ""],
 ["res://character/bill-swim-carry-helmet-east-coherent-v1/manifest.json", "diving-helmet"],
 ["res://character/bill-swim-carry-helmet-west-coherent-v1/manifest.json", "diving-helmet"],
 ["res://character/bill-swim-carry-helmet-north-coherent-v1/manifest.json", "diving-helmet"],
 ["res://character/bill-swim-carry-helmet-south-coherent-v1/manifest.json", "diving-helmet"],
 ["res://character/bill-swim-carry-turn-matrix-v1/bare-manifest.json", ""],
 ["res://character/bill-swim-carry-turn-matrix-v1/helmet-manifest.json", "diving-helmet"]]
var checks:=0
var failures:=0
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:call_deferred("run")
func run() -> void:
	var user_path: String=OS.get_user_data_dir().replace("\\","/").to_lower()
	var scratch_path: String=OS.get_environment("APPDATA").replace("\\","/").to_lower()
	check(user_path.begins_with(scratch_path+"/") and "/output/bill-water-carry-selected-native-v1/scratch-appdata/" in user_path,"Resolved user:// is isolated")
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
				check(frame.get_meta("crew_water_pose")==true and frame.get_meta("crew_water_kind")==state.waterKinds[i] and frame.get_meta("crew_water_facing")==state.facings[i],state.id+" water metadata")
				check(player.frame_at_elapsed(state.id,elapsed+float(state.frameDurationsMs[i])/2000.0,gear)==frame,state.id+" selected elapsed sampling")
				elapsed+=float(state.frameDurationsMs[i])/1000.0
	check(is_equal_approx(player.strides["swim-carry"],.16),"Preserved water cargo stride")
	check(is_equal_approx(player.strides.swim,.16),"Preserved swim stride")
	var locomotion: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/crew-runtime-matte-v1/bill/manifest.json"))
	for key in locomotion.get("strideDistanceCells",{}):check(is_equal_approx(player.strides[key],locomotion.strideDistanceCells[key]),"Preserved selected gait stride "+key)
	for direction in ["east","west","north","south"]:
		for gear in ["","diving-helmet"]:
			var key: String="swim-carry-"+direction
			var row: Array=player.frames[key] if gear.is_empty() else player.equipment_frames[gear][key]
			var clock: Dictionary=player.timing[key] if gear.is_empty() else player.equipment_timing[gear][key]
			player.current_key="";player.current_equipment=gear;player.motion.clear();player.last_time=-1;player.phase=0
			check(player.frame("swim-carry",direction,0.0,Vector2.ZERO,gear,true)==row[0],"Selected starts frame zero")
			var elapsed:=0.0
			for i in row.size():
				var center: float=elapsed+float(clock.durations[i])/2000.0
				var position: Vector2=Vector2(center/.96*.16,0)
				check(player.frame("swim-carry",direction,center,position,gear,true)==row[i],"Distance-driven selected phase "+str(i)+direction+gear)
				check(player.frame("swim-carry",direction,center,position,gear,true)==row[i],"Repeated-time pause "+str(i)+direction+gear)
				elapsed+=float(clock.durations[i])/1000.0
			check(player.frame("swim-carry",direction,elapsed+.001,Vector2((elapsed+.001)/.96*.16,0),gear,true)==row[0],"Selected loop wrap")
	for route in [["east","south"],["south","east"],["south","west"],["west","south"],["west","north"],["north","west"],["north","east"],["east","north"],["east","west"],["west","east"],["north","south"],["south","north"]]:
		var reviewed_gear: Array=["","diving-helmet"]
		for gear in reviewed_gear:
			var key: String="swim-carry-turn-"+route[0]+"-"+route[1]
			var rows: Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
			var row: Array=rows[key];var destination: Array=rows["swim-carry-"+route[1]]
			player.current_key="";player.current_equipment=gear;player.motion.clear();player.last_time=-1;player.phase=0
			player.frame("swim-carry",route[0],0.0,Vector2.ZERO,gear,true)
			player.frame("swim-carry",route[0],.4,Vector2(.4/.96*.16,0),gear,true)
			check(player.frame("swim-carry",route[1],1.0,Vector2(.1,0),gear,true)==row[0],"Triggered authored turn "+key+gear)
			var elapsed:=0.0
			for i in row.size():
				var duration: float=float(player.timing[key].durations[i])/1000.0;var center: float=1.0+elapsed+duration/2
				check(player.frame("swim-carry",route[1],center,Vector2(.1,0),gear,true)==row[i],"Native turn phase "+str(i)+key+gear)
				check(player.frame("swim-carry",route[1],center,Vector2(.1,0),gear,true)==row[i],"Native turn pause "+str(i)+key+gear)
				elapsed+=duration
			check(player.frame("swim-carry",route[1],1.0+elapsed+.001,Vector2(.1,0),gear,true)==destination[0],"Destination loop resume "+key+gear)
	if DisplayServer.get_name()!="headless":
		var viewport:=SubViewport.new();viewport.size=Vector2i(2200,5600);viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
		var bg:=ColorRect.new();bg.size=Vector2(2200,5600);bg.color=Color("22343e");viewport.add_child(bg)
		for row_index in 32:
			var direction: String=["east","west","north","south"][row_index%4];var key: String="swim-carry-"+direction;var gear: String="" if row_index<4 else "diving-helmet"
			if row_index>=8:
				key="swim-carry-turn-east-south" if row_index%2==0 else "swim-carry-turn-south-east";gear="" if row_index<10 else "diving-helmet"
			if row_index>=12:
				key="swim-carry-turn-south-west" if row_index%2==0 else "swim-carry-turn-west-south";gear="" if row_index<14 else "diving-helmet"
			if row_index>=16:
				key="swim-carry-turn-west-north" if row_index%2==0 else "swim-carry-turn-north-west";gear="" if row_index<18 else "diving-helmet"
			if row_index>=20:
				key="swim-carry-turn-north-east" if row_index%2==0 else "swim-carry-turn-east-north";gear="" if row_index<22 else "diving-helmet"
			if row_index>=24:
				key=["swim-carry-turn-east-west","swim-carry-turn-south-north","swim-carry-turn-west-east","swim-carry-turn-north-south"][(row_index-24)%4];gear="" if row_index<28 else "diving-helmet"
			var rows: Array=player.frames[key] if gear.is_empty() else player.equipment_frames[gear][key]
			var title:=Label.new();title.text=key+" selected "+("bare" if gear.is_empty() else "helmet");title.position=Vector2(10,row_index*175);viewport.add_child(title)
			for column in rows.size():
				var frame: Texture2D=rows[column];var factor:=82.0/148.0;var sprite:=Sprite2D.new();sprite.centered=false;sprite.texture=frame;sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;sprite.scale=Vector2.ONE*factor;sprite.position=Vector2(100+column*200,row_index*175+85)-frame.get_meta("crew_pivot")*factor;viewport.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(viewport.get_texture().get_image().save_png("res://output/bill-water-carry-selected-native-v1/loaded-water-carry.png")==OK,"Fresh native selected contact")
		viewport.queue_free()
	grid.free();print("BILL WATER SELECTED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
