extends SceneTree
const SAFE=preload("res://scripts/safe_image.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player
	var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-run-head-locked-v1/manifest.json"));var state:Dictionary=m.states.filter(func(s): return s.id=="run-west")[0];var row:Array=player.frames["run-west"]
	check(row.size()==6,"Six authored phases")
	check(m.status=="selected_runtime","Selected bare status");check(grid.human_animations["run"]["west"][0]==row[0],"Normal grid run selection")
	var elapsed:=0.0;var board:=Image.create(1792,1024,false,Image.FORMAT_RGBA8);board.fill(Color("22343e"))
	var idle:=Image.new();check(SAFE.load_png(idle,"res://character/bill-seated-west-coherent-v1/frames/sit-down-west/000.png")==OK,"Selected master available");board.blend_rect(idle,Rect2i(0,0,256,256),Vector2i.ZERO)
	var small=idle.duplicate();small.resize(142,142,Image.INTERPOLATE_LANCZOS);board.blend_rect(small,Rect2i(0,0,142,142),Vector2i(57,320))
	player.frame("run","west",0,Vector2.ZERO)
	for i in row.size():
		var raw:=Image.new();check(SAFE.load_png(raw,state.frameFiles[i])==OK,"Literal source available")
		check(raw.get_data()==row[i].get_image().get_data(),"Loaded pixels exact")
		check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Master density/pivot")
		var mid:float=elapsed+float(state.frameDurationsMs[i])/2000
		check(player.frame_at_elapsed("run-west",mid)==row[i],"Authored clock")
		check(player.frame("run","west",mid,Vector2(.168*mid/.54,0))==row[i],"Movement-distance gait clock")
		elapsed+=float(state.frameDurationsMs[i])/1000
		board.blend_rect(raw,Rect2i(0,0,256,256),Vector2i((i+1)*256,0));small=raw.duplicate();small.resize(142,142,Image.INTERPOLATE_LANCZOS);board.blend_rect(small,Rect2i(0,0,142,142),Vector2i((i+1)*256+57,320))
	check(player.frame("run","west",.541,Vector2(.168*.541/.54,0))==row[0],"Distance loop wrap")
	check(player.frame("run","west",1,Vector2(.168*.541/.54,0))==row[0],"Paused stationary gait holds")
	check(player.equipment_frames.get("diving-helmet",{}).has("run-west"),"Matched candidate equipment profile")
	var hm:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-run-head-locked-v1/helmet-manifest.json"));var hs:Dictionary=hm.states.filter(func(s): return s.id=="run-west")[0];var hr:Array=player.equipment_frames["diving-helmet"]["run-west"]
	check(hm.status=="selected_runtime","Selected equipment status")
	check(SAFE.load_png(idle,"res://character/bill-seated-helmet-west-coherent-v1/frames/sit-down-west/000.png")==OK,"Equipment master available");board.blend_rect(idle,Rect2i(0,0,256,256),Vector2i(0,512));small=idle.duplicate();small.resize(142,142,Image.INTERPOLATE_LANCZOS);board.blend_rect(small,Rect2i(0,0,142,142),Vector2i(57,832))
	elapsed=0;player.frame("run","west",0,Vector2.ZERO,"diving-helmet")
	for i in hr.size():
		var raw:=Image.new();check(SAFE.load_png(raw,hs.frameFiles[i])==OK,"Equipment literal source")
		check(raw.get_data()==hr[i].get_image().get_data(),"Equipment exact loaded pixels")
		check(hr[i].get_meta("crew_pivot")==Vector2(128,224) and hr[i].get_meta("crew_standing_height")==148.0,"Equipment density")
		var mid:float=elapsed+float(hs.frameDurationsMs[i])/2000
		check(player.frame_at_elapsed("run-west",mid,"diving-helmet")==hr[i],"Equipment source clock")
		check(player.frame("run","west",mid,Vector2(.168*mid/.54,0),"diving-helmet")==hr[i],"Equipment movement clock")
		elapsed+=float(hs.frameDurationsMs[i])/1000
		board.blend_rect(raw,Rect2i(0,0,256,256),Vector2i((i+1)*256,512));small=raw.duplicate();small.resize(142,142,Image.INTERPOLATE_LANCZOS);board.blend_rect(small,Rect2i(0,0,142,142),Vector2i((i+1)*256+57,832))
	check(player.frame("run","west",.541,Vector2(.168*.541/.54,0),"diving-helmet")==hr[0],"Equipment loop wrap")
	check(player.frame("run","west",1,Vector2(.168*.541/.54,0),"diving-helmet")==hr[0],"Equipment stationary gait holds")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1792,1024);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(board);sprite.centered=false;view.add_child(sprite);await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/bill-run-west-selected-native-v1/loaded-water-carry.png")==OK,"Fresh native148/82 candidate capture");view.queue_free()
	grid.free();print("BILL RUN WEST SELECTED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
