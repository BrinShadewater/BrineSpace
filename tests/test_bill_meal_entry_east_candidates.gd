extends SceneTree
const PACK="res://character/bill-meal-entry-east-v1/manifest.json"
const SAFE=preload("res://scripts/safe_image.gd")
var checks:=0
var failures:=0
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(2);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player
	player.load_manifest("res://character/bill-meal-east-coherent-v1/manifest.json",true);player.load_manifest(PACK,true)
	var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACK));var reviews:=[]
	check(m.status=="staged_candidate" and m.states.size()==2,"Bare finite pickup/return candidate scope")
	for state in m.states:
		var row: Array=player.frames[state.id];var elapsed:=0.0;check(row.size()==7,"Seven finite slots")
		for i in row.size():
			var raw:=Image.new();check(SAFE.load_png(raw,PACK.get_base_dir().path_join(state.frameFiles[i]))==OK,"Raw candidate available")
			check(row[i].get_image().get_data()==raw.get_data(),"Loaded exact candidate pixels")
			check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Master standing plane/density")
			check(not row[i].get_meta("crew_water_pose") and row[i].get_meta("crew_depth_offset")==0.0 and row[i].get_meta("crew_water_kind")==state.id.trim_suffix("-east"),"Directional dry finite action metadata")
			var sample: float=elapsed+float(state.frameDurationsMs[i])/2000
			check(player.frame_at_elapsed(state.id,sample)==row[i],"Authored finite pose pacing");elapsed+=float(state.frameDurationsMs[i])/1000
		check(is_equal_approx(elapsed,.58) and player.frame_at_elapsed(state.id,9)==row[-1],"580ms finite endpoint hold")
		reviews.append(row)
	var enter: Array=player.frames["eat-enter-east"];var exit: Array=player.frames["eat-exit-east"]
	var idle:=Image.new();check(SAFE.load_png(idle,"res://character/bill-seated-east-coherent-v1/frames/sit-down-east/000.png")==OK,"Selected idle source available")
	check(enter[0].get_image().get_data()==idle.get_data() and exit[-1].get_image().get_data()==idle.get_data(),"Exact selected idle endpoint joins")
	check(enter[-1].get_image().get_data()==player.frames["eat-east"][0].get_image().get_data() and exit[0].get_image().get_data()==player.frames["eat-east"][-1].get_image().get_data(),"Exact candidate eating held joins")
	for i in 7:check(enter[i].get_image().get_data()==exit[6-i].get_image().get_data(),"Exact whole-pose reverse return")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1792,1024);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view);var bg:=ColorRect.new();bg.size=Vector2(1792,1024);bg.color=Color("22343e");view.add_child(bg)
		for i in 7:
			for j in 4:
				var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(idle) if j==3 else (exit[i] if j==1 else enter[i]);sprite.centered=false;sprite.scale=Vector2.ONE*(82.0/148.0 if j==2 else 1.0);sprite.position=Vector2(128+i*256,224+j*256)-Vector2(128,224)*sprite.scale;view.add_child(sprite)
		await RenderingServer.frame_post_draw;check(view.get_texture().get_image().save_png("res://output/bill-meal-entry-east-candidate-native-v1/loaded-water-carry.png")==OK,"Native finite pickup/return and master review");view.queue_free()
	grid.free();print("BILL MEAL ENTRY EAST: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
