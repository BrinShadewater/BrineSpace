extends SceneTree
const PACK="res://character/bill-rest-west-coherent-v1/manifest.json"
const SAFE=preload("res://scripts/safe_image.gd")
var checks:=0
var failures:=0
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	print("BILL REST WEST profile: "+OS.get_user_data_dir())
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(2);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player
	var prior: Array=player.equipment_frames["diving-helmet"]["sleep-west"].duplicate()
	player.load_manifest(PACK,true);var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACK))
	check(m.status=="staged_candidate" and m.states.size()==3,"Explicit bare rest candidate")
	check(player.equipment_frames["diving-helmet"]["sleep-west"]==prior,"Bare candidate preserves existing gear")
	for state in m.states:
		var row: Array=player.frames[state.id];var elapsed:=0.0
		for i in row.size():
			var raw:=Image.new();check(SAFE.load_png(raw,state.frameFiles[i])==OK,"Literal candidate available")
			check(row[i].get_image().get_data()==raw.get_data(),"Exact loaded pixels")
			check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Master plane/density")
			check(not row[i].get_meta("crew_water_pose") and row[i].get_meta("crew_depth_offset")==0.0,"Dry rest metadata")
			check(player.frame_at_elapsed(state.id,elapsed+float(state.frameDurationsMs[i])/2000)==row[i],"Authored finite/loop pacing")
			elapsed+=float(state.frameDurationsMs[i])/1000
		if state.loop:
			check(player.frame("sleep","west",0.0,Vector2.ZERO)==row[0] and player.frame("sleep","west",elapsed+.001,Vector2.ZERO)==row[0],"Loop player returns to exact rest endpoint")
			check(row[0].has_meta("crew_rest_head_offset"),"Rest head anchor exposed")
			check(row[0].get_meta("crew_rest_head_offset")==Vector2(state.restHeadOffset[0],state.restHeadOffset[1]),"Exact west resting head anchor including render lift")
		else:
			check(is_equal_approx(elapsed,.8) and player.frame_at_elapsed(state.id,99)==row[-1],"Finite800ms terminal hold")
	var lie: Array=player.frames["lie-down-west"];var wake: Array=player.frames["get-up-west"];var sleep: Array=player.frames["sleep-west"]
	check(lie[-1].get_image().get_data()==sleep[0].get_image().get_data() and sleep[0].get_image().get_data()==wake[0].get_image().get_data(),"Exact lie/sleep/wake endpoint")
	for i in lie.size():check(lie[i].get_image().get_data()==wake[lie.size()-1-i].get_image().get_data(),"Exact reverse wake choreography")
	if DisplayServer.get_name()!="headless":
		var idle:=Image.new();check(SAFE.load_png(idle,"res://character/bill-seated-west-coherent-v1/frames/sit-down-west/000.png")==OK,"Selected master")
		var view:=SubViewport.new();view.size=Vector2i(2048,768);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(2048,768);bg.color=Color("22343e");view.add_child(bg)
		for i in 8:
			for j in 3:
				var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(idle) if j==2 else lie[i];sprite.centered=false;sprite.scale=Vector2.ONE*(82.0/148.0 if j==1 else 1.0);sprite.position=Vector2(128+i*256,224+j*256)-Vector2(128,224)*sprite.scale;view.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/bill-rest-west-candidate-native-v1/loaded-water-carry.png")==OK,"Native148/82 rest and master review")
		view.queue_free()
	grid.free();print("BILL REST WEST: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
