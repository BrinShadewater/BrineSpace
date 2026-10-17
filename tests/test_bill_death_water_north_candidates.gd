extends SceneTree
## Staged death candidates injected into actual Bill player; scratch-profile only.
const PACKS := [["res://character/bill-death-water-north-coherent-v1/manifest.json", ""],["res://character/bill-death-water-helmet-north-coherent-v1/manifest.json", "diving-helmet"]]
var checks:=0
var failures:=0
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:call_deferred("run")
func run() -> void:
	var user_path: String=OS.get_user_data_dir().replace("\\","/").to_lower()
	var scratch_path: String=OS.get_environment("APPDATA").replace("\\","/").to_lower()
	check(user_path.begins_with(scratch_path+"/") and "/output/bill-death-water-north-candidate-native-v1/scratch-appdata/" in user_path,"Resolved user:// is isolated")
	print("BILL WATER USER PATH: "+OS.get_user_data_dir())
	if failures:quit(1);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player
	for spec in PACKS:
		if spec[1].is_empty():player.load_manifest(spec[0],true)
		else:check(player.load_equipment_manifest(spec[1],spec[0]),"Candidate equipment profile")
	for spec in PACKS:
		var path: String=spec[0];var gear: String=spec[1];var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path));var direction: String="south" if "south-coherent" in path else "north" if "north-coherent" in path else ("north" if "north-coherent" in path else "south")
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
	check(is_equal_approx(player.strides.swim,.16),"Preserved selected swim stride")
	for gear in ["","diving-helmet"]:
		var row: Array=player.frames["death-water-north"] if gear.is_empty() else player.equipment_frames[gear]["death-water-north"]
		player.current_key="";player.current_equipment=gear;player.motion.clear();player.last_time=-1;player.phase=0
		check(player.frame("death-water","north",0.0,Vector2.ZERO,gear,true)==row[0],"Death entry")
		var elapsed:=0.0
		for i in 6:
			var center: float=elapsed+float([180,180,220,220,260,500][i])/2000.0
			check(player.frame("death-water","north",center,Vector2.ZERO,gear,true)==row[i],"Time-driven death pose")
			check(player.frame("death-water","north",center,Vector2.ZERO,gear,true)==row[i],"Paused death pose")
			elapsed+=float([180,180,220,220,260,500][i])/1000.0
		check(player.frame("death-water","north",9.0,Vector2.ZERO,gear,true)==row[-1],"Finite terminal hold")
	var actor=load("res://scripts/bill_npc.gd").new();actor.movement_medium="exterior";actor.direction="north";actor.state="walk"
	for gear in [false,true]:
		actor.dead=false;actor.helmet_equipped=gear;actor.die()
		check(actor.dead and actor.animation_state()=="death-water","Actual Bill mortality chooser")
		check(actor.action_elapsed()<0,"Death uses visual one-shot clock")
		check(actor.path.is_empty() and actor.expedition.is_empty(),"Mortality cancels travel/work")
	if DisplayServer.get_name()!="headless":
		var viewport:=SubViewport.new();viewport.size=Vector2i(1200,350);viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
		var bg:=ColorRect.new();bg.size=Vector2(1200,350);bg.color=Color("22343e");viewport.add_child(bg)
		for row_index in 2:
			var key: String="death-water-north";var gear: String="" if row_index==0 else "diving-helmet"
			var rows: Array=player.frames[key] if gear.is_empty() else player.equipment_frames[gear][key]
			var title:=Label.new();title.text=key+" candidate "+("bare" if gear.is_empty() else "helmet");title.position=Vector2(10,row_index*175);viewport.add_child(title)
			for column in rows.size():
				var frame: Texture2D=rows[column];var factor:=82.0/148.0;var sprite:=Sprite2D.new();sprite.centered=false;sprite.texture=frame;sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;sprite.scale=Vector2.ONE*factor;sprite.position=Vector2(100+column*200,row_index*175+85)-frame.get_meta("crew_pivot")*factor;viewport.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(viewport.get_texture().get_image().save_png("res://output/bill-death-water-north-candidate-native-v1/loaded-water-carry.png")==OK,"Fresh native selected contact")
		viewport.queue_free()
	grid.free();print("BILL DEATH CANDIDATE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
