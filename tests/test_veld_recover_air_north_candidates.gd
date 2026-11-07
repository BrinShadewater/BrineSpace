extends SceneTree
const PACKS=[["res://character/veld-recover-air-north-coherent-v1/manifest.json",""],["res://character/veld-recover-air-north-coherent-v1/helmet-manifest.json","diving-helmet"]]
var checks:=0
var failures:=0
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:call_deferred("run")
func run() -> void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.veld_player
	player.load_manifest(PACKS[0][0],true);check(player.load_equipment_manifest(PACKS[1][1],PACKS[1][0]),"Paired candidate injection")
	for spec in PACKS:
		var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(spec[0]));var row: Array=player.frames["recover-air-north"] if spec[1].is_empty() else player.equipment_frames[spec[1]]["recover-air-north"]
		for i in 6:
			var im:=Image.load_from_file(spec[0].get_base_dir().path_join(m.states[0].frameFiles[i]))
			check(row[i].get_image().get_data()==im.get_data(),"Loaded source pixels")
			check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Dry recovery registration")
			check(not row[i].get_meta("crew_water_pose") and row[i].get_meta("crew_water_kind")=="recover","Dry metadata")
			check(player.frame_at_elapsed("recover-air-north",i*.5+.25,spec[1])==row[i],"Simulation elapsed pose")
		var actor=load("res://scripts/veld_npc.gd").new();actor.state="idle";actor.direction="north";actor.movement_medium="dry";actor.helmet_equipped=not spec[1].is_empty()
		for i in 6:
			actor.air_recovery=3.0-(i*.5+.25)
			check(actor.animation_state()=="recover-air","Actual Veld dry recovery chooser")
			check(player.frame_at_elapsed(actor.animation_state()+"-north",actor.action_elapsed(),spec[1])==row[i],"Actual recovery simulation clock")
			check(player.frame_at_elapsed(actor.animation_state()+"-north",actor.action_elapsed(),spec[1])==row[i],"Paused simulation pose")
		actor.air_recovery=0;check(actor.animation_state()=="idle","Recovery ends in idle")
		actor.air_recovery=2;actor.movement_medium="flooded";actor.tank_oxygen=60;actor.breath_oxygen=15
		check(actor.animation_state()!="recover-air","No dry recovery underwater")
		check(player.frame_at_elapsed("recover-air-north",9,spec[1])==row[-1],"Finite terminal hold")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1200,420);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var bg:=ColorRect.new();bg.size=Vector2(1200,420);bg.color=Color("22343e");view.add_child(bg)
		for gear in 2:
			var row: Array=player.frames["recover-air-north"] if gear==0 else player.equipment_frames["diving-helmet"]["recover-air-north"]
			for i in 6:
				var sprite:=Sprite2D.new();sprite.texture=row[i];sprite.centered=false;sprite.scale=Vector2.ONE*82/148;sprite.position=Vector2(100+i*200,190+gear*210)-Vector2(128,224)*82/148;view.add_child(sprite)
		await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/veld-recover-air-north-candidate-native-v1/loaded-water-carry.png")==OK,"Fresh native82 contact")
		view.queue_free()
	grid.free();print("VELD RECOVERY CANDIDATE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
