extends SceneTree
const PACKS=[["res://character/bill-seated-east-coherent-v1/manifest.json",""],["res://character/bill-seated-helmet-east-coherent-v1/manifest.json","diving-helmet"]]
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
	for spec in PACKS:
		var existing: Texture2D=player.frames["idle-east"][0] if spec[1].is_empty() else player.equipment_frames[spec[1]]["idle-east"][0]
		var original: Image=existing.get_image();var padded:=Image.create(256,256,false,Image.FORMAT_RGBA8)
		padded.blit_rect(original,Rect2i(0,0,original.get_width(),original.get_height()),Vector2i(36,52))
		var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(spec[0]))
		check(padded.get_data()==Image.load_from_file(spec[0].get_base_dir().path_join(m.states[0].frameFiles[0])).get_data(),"Exact currently loaded standing entry")
	player.load_manifest(PACKS[0][0],true);check(player.load_equipment_manifest(PACKS[1][1],PACKS[1][0]),"Paired candidate injection")
	var reviews:=[]
	for spec in PACKS:
		var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(spec[0]))
		for state in m.states:
			var row: Array=player.frames[state.id] if spec[1].is_empty() else player.equipment_frames[spec[1]][state.id]
			var actor=load("res://scripts/bill_npc.gd").new();actor.active=true;actor.goal="fatigue";actor.state="idle";actor.direction="east";actor.movement_medium="dry";actor.helmet_equipped=not spec[1].is_empty();actor.stage="life_sit" if state.id=="sit-down-east" else "life_rise"
			var elapsed:=0.0
			for i in 6:
				var im:=Image.load_from_file(spec[0].get_base_dir().path_join(state.frameFiles[i]))
				check(row[i].get_image().get_data()==im.get_data(),"Loaded source pixels")
				check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Dry sitting plane")
				check(not row[i].get_meta("crew_water_pose"),"Dry sitting metadata")
				var midpoint: float=elapsed+float(state.frameDurationsMs[i])/2000.0
				actor.timer=.8-midpoint
				check(actor.animation_state()+"-east"==state.id,"Actual Bill life-stage chooser")
				check(is_equal_approx(actor.action_elapsed(),midpoint),"Retained800ms life timer")
				check(player.frame_at_elapsed(state.id,actor.action_elapsed(),spec[1])==row[i],"Actual stage elapsed pose")
				check(player.frame_at_elapsed(state.id,actor.action_elapsed(),spec[1])==row[i],"Paused simulation pose")
				elapsed+=float(state.frameDurationsMs[i])/1000.0
			check(is_equal_approx(elapsed,.8) and player.frame_at_elapsed(state.id,9,spec[1])==row[-1],"Finite800ms terminal hold")
			check(actor.valid_snapshot(actor.snapshot()),"Intermediate life snapshot remains valid")
			reviews.append(row)
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1200,840);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(1200,840);bg.color=Color("22343e");view.add_child(bg)
		for j in reviews.size():
			for i in 6:
				var sprite:=Sprite2D.new();sprite.texture=reviews[j][i];sprite.centered=false;sprite.scale=Vector2.ONE*82/148;sprite.position=Vector2(100+i*200,190+j*210)-Vector2(128,224)*82/148;view.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/bill-seated-east-candidate-native-v1/loaded-water-carry.png")==OK,"Fresh native82 paired transition contact")
		view.queue_free()
	grid.free();print("BILL SEATED CANDIDATE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
