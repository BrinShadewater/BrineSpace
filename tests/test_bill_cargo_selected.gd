extends SceneTree
## Actual Bill loader,paired cargo timing,planted turns and playback clock.
const PACKS := [
	["res://character/bill-cargo-east-coherent-v1/manifest.json", ""],
	["res://character/bill-cargo-west-coherent-v1/manifest.json", ""],
	["res://character/bill-cargo-south-coherent-v1/manifest.json", ""],
	["res://character/bill-cargo-north-coherent-v1/manifest.json", ""],
	["res://character/bill-cargo-helmet-east-v1/manifest.json", "diving-helmet"],
	["res://character/bill-cargo-helmet-west-v1/manifest.json", "diving-helmet"],
	["res://character/bill-cargo-helmet-south-v1/manifest.json", "diving-helmet"],
	["res://character/bill-cargo-helmet-north-v1/manifest.json", "diving-helmet"],
	["res://character/bill-carry-turn-matrix-v1/bare-manifest.json", ""],
	["res://character/bill-carry-turn-matrix-v1/helmet-manifest.json", "diving-helmet"]]
var checks:=0
var failures:=0
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:call_deferred("run")
func run() -> void:
	var user_path: String=OS.get_user_data_dir().replace("\\","/").to_lower()
	var scratch_path: String=OS.get_environment("APPDATA").replace("\\","/").to_lower()
	check(user_path.begins_with(scratch_path+"/") and "/output/bill-cargo-native-v1/scratch-appdata/" in user_path,"Resolved user:// stays in fixture scratch APPDATA")
	print("BILL CARGO USER PATH: "+OS.get_user_data_dir())
	if failures:quit(1);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player
	var keys: Array=[]
	for spec in PACKS:
		var path: String=spec[0];var gear: String=spec[1];var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
		for state in pack.states:
			var rows: Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
			var clocks: Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
			check(rows.has(state.id),state.id+" selected "+gear)
			if not rows.has(state.id):continue
			check(rows[state.id].size()==state.frameFiles.size(),state.id+" frame count")
			check(clocks[state.id].durations==state.frameDurationsMs and clocks[state.id].loop==state.loop,state.id+" paired clock")
			if gear.is_empty():keys.append(state.id)
			var elapsed:=0.0
			for i in state.frameFiles.size():
				var frame: Texture2D=rows[state.id][i];var expected:=Image.load_from_file(path.get_base_dir().path_join(state.frameFiles[i]))
				check(frame.get_image().get_data()==expected.get_data(),state.id+" exact selected pixels "+str(i)+gear)
				check(frame.get_meta("crew_pivot")==Vector2(128,224) and frame.get_meta("crew_standing_height")==148.0,state.id+" render registration")
				check(player.frame_at_elapsed(state.id,elapsed+float(state.frameDurationsMs[i])/2000.0,gear)==frame,state.id+" sampled phase")
				elapsed+=float(state.frameDurationsMs[i])/1000.0
	# Compare unrelated gait stride keys to the pre-cargo selected locomotion authority.
	var locomotion: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/crew-runtime-matte-v1/bill/manifest.json"))
	for key in locomotion.get("strideDistanceCells",{}):
		check(is_equal_approx(player.strides[key],locomotion.strideDistanceCells[key]),"Unchanged selected locomotion stride "+key)
	for gear in ["","diving-helmet"]:
		for source in ["east","west","south","north"]:
			for destination in ["east","west","south","north"]:
				if source==destination:continue
				player.current_key="";player.motion.clear();player.last_time=-1;player.phase=0
				player.frame("carry",source,0.0,Vector2.ZERO,gear)
				var key: String="carry-turn-"+source+"-"+destination
				var rows: Array=player.frames[key] if gear.is_empty() else player.equipment_frames[gear][key]
				check(player.frame("carry",destination,0.1,Vector2.ZERO,gear)==rows[0],key+" neutral start "+gear)
				var clock: Dictionary=player.timing[key] if gear.is_empty() else player.equipment_timing[gear][key]
				var elapsed:=0.1
				for i in rows.size():
					check(player.frame("carry",destination,elapsed+float(clock.durations[i])/2000.0,Vector2.ZERO,gear)==rows[i],key+" live phase "+str(i))
					elapsed+=float(clock.durations[i])/1000.0
				var resumed: Texture2D=player.frame("carry",destination,elapsed+0.01,Vector2.ZERO,gear)
				var walking: Array=player.frames["carry-"+destination] if gear.is_empty() else player.equipment_frames[gear]["carry-"+destination]
				check(resumed==walking[0],key+" fresh gait resume")
	var actor=load("res://scripts/major_bill_npc.gd").new();actor.state="idle";actor.movement_medium="dry"
	actor.stage="workshop_pickup";actor.timer=.4;check(actor.animation_state()=="pickup","Workshop pickup selection")
	actor.stage="workshop_carry";check(actor.animation_state()=="carry","Workshop carry selection")
	actor.stage="workshop_unload";check(actor.animation_state()=="unload","Workshop unload selection")
	if DisplayServer.get_name()!="headless":
		var viewport:=SubViewport.new();viewport.size=Vector2i(1200,1500);viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
		var background:=ColorRect.new();background.size=Vector2(1200,1500);background.color=Color("22343e");viewport.add_child(background)
		for row in 8:
			var direction: String=["east","south","west","north"][row%4];var gear: String="" if row<4 else "diving-helmet"
			var next: String={"east":"west","south":"north","west":"east","north":"south"}[direction]
			var key: String="carry-turn-"+direction+"-"+next
			var label:=Label.new();label.text=key+" "+("bare" if gear.is_empty() else "helmet");label.position=Vector2(10,row*185);viewport.add_child(label)
			for column in 6:
				var index: int=[0,1,3,5,7,10][column];var rows: Array=player.frames[key] if gear.is_empty() else player.equipment_frames[gear][key]
				var sprite:=Sprite2D.new();sprite.texture=rows[index];sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;sprite.scale=Vector2.ONE*(82.0/148.0);sprite.position=Vector2(100+column*200,row*185+103);viewport.add_child(sprite)
		await RenderingServer.frame_post_draw
		DirAccess.make_dir_recursive_absolute("res://output/bill-cargo-native-v1")
		check(viewport.get_texture().get_image().save_png("res://output/bill-cargo-native-v1/loaded-turns.png")==OK,"Native selected half-turn contact review")
		viewport.queue_free()
	grid.free();print("BILL CARGO SELECTED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
