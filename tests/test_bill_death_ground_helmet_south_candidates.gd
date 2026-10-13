extends SceneTree
const PACK="res://character/bill-death-ground-helmet-south-coherent-v1/manifest.json"
const SAFE=preload("res://scripts/safe_image.gd")
var checks:=0
var failures:=0
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	print("BILL DEATH GROUND HELMET SOUTH profile: "+OS.get_user_data_dir())
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(2);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player
	player.load_manifest("res://character/bill-death-ground-south-coherent-v1/manifest.json",true)
	var prior: Array=player.frames["death-ground-south"].duplicate()
	check(player.load_equipment_manifest("diving-helmet",PACK),"Compatible paired equipment loaded");if failures:quit(2);return
	var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACK));var state: Dictionary=m.states[0];var row: Array=player.equipment_frames["diving-helmet"][state.id]
	check(row.size()==6 and m.status=="staged_candidate","Explicit six-slot finite candidate")
	check(player.frames[state.id]==prior,"Helmet candidate preserves paired bare candidate")
	var elapsed:=0.0
	for i in row.size():
		var raw:=Image.new();check(SAFE.load_png(raw,PACK.get_base_dir().path_join(state.frameFiles[i]))==OK,"Raw candidate available")
		check(row[i].get_image().get_data()==raw.get_data(),"Loaded exact candidate pixels")
		check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Selected standing plane/density")
		check(not row[i].get_meta("crew_water_pose") and row[i].get_meta("crew_depth_offset")==0.0 and row[i].get_meta("crew_water_kind")=="death-ground","Dry mortality metadata")
		check(player.frame_at_elapsed(state.id,elapsed+float(state.frameDurationsMs[i])/2000,"diving-helmet")==row[i],"Finite authored pacing")
		elapsed+=float(state.frameDurationsMs[i])/1000
	check(is_equal_approx(elapsed,2) and player.frame_at_elapsed(state.id,2,"diving-helmet")==row[-1] and player.frame_at_elapsed(state.id,99,"diving-helmet")==row[-1],"Finite corpse hold")
	check(row[-1]!=row[0],"No loop resurrection")
	if DisplayServer.get_name()!="headless":
		var idle:=Image.new();check(SAFE.load_png(idle,"res://character/bill-seated-helmet-south-coherent-v1/frames/sit-down-south/000.png")==OK,"Idle visual authority")
		var view:=SubViewport.new();view.size=Vector2i(1536,768);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view);var bg:=ColorRect.new();bg.size=Vector2(1536,768);bg.color=Color("22343e");view.add_child(bg)
		for i in 6:
			for j in 3:
				var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(idle) if j==2 else row[i];sprite.centered=false;sprite.scale=Vector2.ONE*(82.0/148.0 if j==1 else 1.0);sprite.position=Vector2(128+i*256,224+j*256)-Vector2(128,224)*sprite.scale;view.add_child(sprite)
		await RenderingServer.frame_post_draw;check(view.get_texture().get_image().save_png("res://output/bill-death-ground-helmet-south-candidate-native-v1/loaded-water-carry.png")==OK,"Native148/82 collapse and master review");view.queue_free()
	grid.free();print("BILL DEATH GROUND HELMET SOUTH: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
