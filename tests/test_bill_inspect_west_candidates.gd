extends SceneTree
const PACKS=[["res://character/bill-inspect-west-coherent-v1/bare-manifest.json",""],["res://character/bill-inspect-west-coherent-v1/helmet-manifest.json","diving-helmet"]]
var checks:=0
var failures:=0
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:call_deferred("run")
func run() -> void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player
	player.load_manifest(PACKS[0][0],true);check(player.load_equipment_manifest(PACKS[1][1],PACKS[1][0]),"Paired candidate injection")
	var reviews:=[]
	for spec in PACKS:
		var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(spec[0]))
		for state in m.states:
			var row: Array=player.frames[state.id] if spec[1].is_empty() else player.equipment_frames[spec[1]][state.id]
			var actor=load("res://scripts/bill_npc.gd").new();actor.active=true;actor.goal="curiosity" if state.id=="read-seated-west" else "fatigue";actor.state="idle";actor.direction="west";actor.movement_medium="dry";actor.helmet_equipped=not spec[1].is_empty();actor.stage="life_inspect";actor.timer=4.0
			check(actor.animation_state()+"-west"==state.id and actor.action_elapsed()==-1,"Actual seated/reading loop chooser")
			for i in 6:
				var im:=Image.load_from_file(spec[0].get_base_dir().path_join(state.frameFiles[i]))
				check(row[i].get_image().get_data()==im.get_data(),"Loaded exact candidate pixels")
				check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Selected density/pivot")
				check(not row[i].get_meta("crew_water_pose") and row[i].get_meta("crew_depth_offset")==0.0,"Dry seated metadata")
				for cycle in [0,1,7]:
					player.current_key="";player.last_time=-1;player.frame(actor.animation_state(),"west",0,Vector2.ZERO,spec[1])
					check(player.frame(actor.animation_state(),"west",(i+.5)*.16+cycle*.96,Vector2.ZERO,spec[1])==row[i],"Actual cosmetic loop repeats")
			if state.id=="sit-idle-west":
				var endpoint: String="res://character/bill-seated-west-coherent-v1/frames/sit-down-west/005.png" if spec[1].is_empty() else "res://character/bill-seated-helmet-west-coherent-v1/frames/sit-down-west/005.png"
				check(row[0].get_image().get_data()==Image.load_from_file(endpoint).get_data() and row[0].get_image().get_data()==row[-1].get_image().get_data(),"Exact seated transition joins/loop closure")
			check(row[0].get_image().get_data()==row[-1].get_image().get_data(),"Exact inspection loop closure")
			check(actor.valid_snapshot(actor.snapshot()),"Inspection stage snapshot valid");reviews.append(row)
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1200,840);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view);var bg:=ColorRect.new();bg.size=Vector2(1200,840);bg.color=Color("22343e");view.add_child(bg)
		for j in reviews.size():
			for i in 6:
				var sprite:=Sprite2D.new();sprite.texture=reviews[j][i];sprite.centered=false;sprite.scale=Vector2.ONE*82/148;sprite.position=Vector2(100+i*200,190+j*210)-Vector2(128,224)*82/148;view.add_child(sprite)
		await RenderingServer.frame_post_draw;check(view.get_texture().get_image().save_png("res://output/bill-inspect-west-candidate-native-v1/loaded-water-carry.png")==OK,"Fresh native82 review");view.queue_free()
	grid.free();print("BILL INSPECT WEST: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
