extends SceneTree
const PACK="res://character/bill-meal-south-family-v1/manifest.json"
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
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player;player.load_manifest(PACK,true)
	var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACK));var reviews:=[]
	check(m.status=="staged_candidate" and m.states.size()==6,"Six assembled bare meal candidate states")
	for state in m.states:
		var row: Array=player.frames[state.id];var elapsed:=0.0;check(row.size()==7,"Seven authored family slots")
		for i in row.size():
			check(state.frameFiles[i].begins_with("res://"),"Whole literal source paths")
			var raw:=Image.new();check(SAFE.load_png(raw,state.frameFiles[i])==OK,"Parent source available")
			check(row[i].get_image().get_data()==raw.get_data(),"Assembled exact parent pixels")
			check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Shared master plane/density")
			check(not row[i].get_meta("crew_water_pose") and row[i].get_meta("crew_depth_offset")==0.0 and row[i].get_meta("crew_water_facing")=="south","Shared dry facing/depth")
			var sample: float=elapsed+float(state.frameDurationsMs[i])/2000
			check(player.frame_at_elapsed(state.id,sample)==row[i],"Authored family pose pacing");elapsed+=float(state.frameDurationsMs[i])/1000
		check(is_equal_approx(elapsed,.96 if state.loop else .58),"Family loop/transition duration")
		if not state.loop:check(player.frame_at_elapsed(state.id,9)==row[-1],"Finite family endpoint hold")
		else:
			check(row[0].get_image().get_data()==row[-1].get_image().get_data(),"Exact loop closure")
			for cycle in [0,1,7]:
				player.current_key="";player.last_time=-1;player.frame(state.id.trim_suffix("-south"),"south",0,Vector2.ZERO)
				check(player.frame(state.id.trim_suffix("-south"),"south",.5+cycle*.96,Vector2.ZERO)==row[3],"Assembled eating/drinking loop repeats")
		reviews.append(row)
	for i in 5:check(reviews[i][-1].get_image().get_data()==reviews[i+1][0].get_image().get_data(),"Exact complete sequence adjacent join")
	check(reviews[-1][-1].get_image().get_data()==reviews[0][0].get_image().get_data(),"Full meal sequence empty-idle closure")
	for pair in [[0,2],[3,5]]:
		for i in 7:check(reviews[pair[0]][i].get_image().get_data()==reviews[pair[1]][6-i].get_image().get_data(),"Whole pickup/return pose reversal")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1792,1536);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view);var bg:=ColorRect.new();bg.size=Vector2(1792,1536);bg.color=Color("22343e");view.add_child(bg)
		for j in reviews.size():
			for i in 7:
				var sprite:=Sprite2D.new();sprite.texture=reviews[j][i];sprite.centered=false;sprite.scale=Vector2.ONE*82/148;sprite.position=Vector2(128+i*256,224+j*256)-Vector2(128,224)*82/148;view.add_child(sprite)
		await RenderingServer.frame_post_draw;check(view.get_texture().get_image().save_png("res://output/bill-meal-south-family-candidate-native-v1/loaded-water-carry.png")==OK,"Native82 full meal family review");view.queue_free()
	grid.free();print("BILL MEAL SOUTH FAMILY: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
