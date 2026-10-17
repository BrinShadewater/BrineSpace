extends SceneTree
const PACKS=[["res://character/bill-reading-entry-north-v1/bare-manifest.json",""],["res://character/bill-reading-entry-north-v1/helmet-manifest.json","diving-helmet"]]
var checks:=0
var failures:=0
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player;player.load_manifest(PACKS[0][0],true);check(player.load_equipment_manifest(PACKS[1][1],PACKS[1][0]),"Paired candidate injection");var reviews:=[]
	for spec in PACKS:
		var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(spec[0]))
		for state in m.states:
			var row: Array=player.frames[state.id] if spec[1].is_empty() else player.equipment_frames[spec[1]][state.id];var elapsed:=0.0
			for i in 6:
				check(row[i].get_image().get_data()==Image.load_from_file(spec[0].get_base_dir().path_join(state.frameFiles[i])).get_data(),"Loaded exact pixels")
				check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Selected plane/density")
				check(not row[i].get_meta("crew_water_pose") and row[i].get_meta("crew_depth_offset")==40.0,"Dry seated depth")
				check(player.frame_at_elapsed(state.id,elapsed+state.frameDurationsMs[i]/2000.0,spec[1])==row[i],"Finite transition pose timing");elapsed+=state.frameDurationsMs[i]/1000.0
			check(is_equal_approx(elapsed,.48) and player.frame_at_elapsed(state.id,9,spec[1])==row[-1],"Finite480ms endpoint hold")
			reviews.append(row)
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1200,840);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view);var bg:=ColorRect.new();bg.size=Vector2(1200,840);bg.color=Color("22343e");view.add_child(bg)
		for j in reviews.size():
			for i in 6:
				var sprite:=Sprite2D.new();sprite.texture=reviews[j][i];sprite.centered=false;sprite.scale=Vector2.ONE*82/148;sprite.position=Vector2(100+i*200,190+j*210)-Vector2(128,224)*82/148;view.add_child(sprite)
		await RenderingServer.frame_post_draw;check(view.get_texture().get_image().save_png("res://output/bill-reading-entry-north-candidate-native-v1/loaded-water-carry.png")==OK,"Native82 transition review");view.queue_free()
	grid.free();print("BILL READING ENTRY: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
