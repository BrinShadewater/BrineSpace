extends SceneTree
const PACK="res://character/bill-meal-north-coherent-v1/manifest.json"
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
	var prior_helmet: Array=player.equipment_frames["diving-helmet"]["eat-north"].duplicate()
	player.load_manifest(PACK,true);var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACK));var state: Dictionary=m.states[0];var row: Array=player.frames[state.id]
	check(row.size()==7 and m.status=="staged_candidate","Explicit seven-slot candidate injection")
	check(player.equipment_frames["diving-helmet"]["eat-north"]==prior_helmet,"Bare candidate leaves equipment source unchanged")
	var actor=load("res://scripts/bill_npc.gd").new();actor.stage="life_eat";actor.timer=4;actor.direction="north";actor.movement_medium="dry";actor.helmet_equipped=false
	check(actor.animation_state()=="eat" and actor.action_elapsed()<0,"Bare meal loop chooser remains distinct from helmet reader")
	var elapsed:=0.0
	for i in row.size():
		var raw:=Image.new();check(SAFE.load_png(raw,PACK.get_base_dir().path_join(state.frameFiles[i]))==OK,"Raw candidate available")
		check(row[i].get_image().get_data()==raw.get_data(),"Loaded exact candidate pixels")
		check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Master standing plane/density")
		check(not row[i].get_meta("crew_water_pose") and row[i].get_meta("crew_depth_offset")==0.0,"Dry meal metadata")
		var sample: float=elapsed+float(state.frameDurationsMs[i])/2000
		check(player.frame_at_elapsed(state.id,sample)==row[i],"Authored pose pacing")
		for cycle in [0,1,7]:
			player.current_key="";player.last_time=-1;player.frame("eat","north",0,Vector2.ZERO)
			check(player.frame("eat","north",sample+cycle*.96,Vector2.ZERO)==row[i],"Whole eating loop repeats through cosmetic time")
		elapsed+=float(state.frameDurationsMs[i])/1000
	check(is_equal_approx(elapsed,.96),"960ms eating cycle")
	check(row[0].get_image().get_data()==row[-1].get_image().get_data(),"Exact whole eating closure")
	if DisplayServer.get_name()!="headless":
		var idle:=Image.new();check(SAFE.load_png(idle,"res://character/bill-seated-north-coherent-v1/frames/sit-down-north/000.png")==OK,"Idle visual authority")
		var view:=SubViewport.new();view.size=Vector2i(1792,768);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view);var bg:=ColorRect.new();bg.size=Vector2(1792,768);bg.color=Color("22343e");view.add_child(bg)
		for i in 7:
			for j in 3:
				var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(idle) if j==2 else row[i];sprite.centered=false;sprite.scale=Vector2.ONE*(82.0/148.0 if j==1 else 1.0);sprite.position=Vector2(128+i*256,224+j*256)-Vector2(128,224)*sprite.scale;view.add_child(sprite)
		await RenderingServer.frame_post_draw;check(view.get_texture().get_image().save_png("res://output/bill-meal-north-candidate-native-v1/loaded-water-carry.png")==OK,"Native148/82 meal and selected master review");view.queue_free()
	grid.free();print("BILL MEAL NORTH: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
