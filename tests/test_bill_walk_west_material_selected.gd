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
	var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-walk-west-material-v1/manifest.json"));var state:Dictionary=m.states[0];var row:Array=player.frames["walk-west"]
	check(row.size()==48,"All forty-eight west walk poses")
	check(m.status=="selected_runtime","Current selected status")
	check(grid.human_animations["walk"]["west"][0]==row[0],"Normal grid selects master-head layer")
	check(player.strides["walk-west"]==.1796875,"Original distance stride")
	var board:=Image.create(1792,1792,false,Image.FORMAT_RGBA8);board.fill(Color("22343e"));var idle:=Image.new()
	check(SAFE.load_png(idle,"res://character/bill-seated-west-coherent-v1/frames/sit-down-west/000.png")==OK,"Native master available");board.blend_rect(idle,Rect2i(0,0,256,256),Vector2i.ZERO)
	var elapsed:=0.0
	player.frame("walk","west",0,Vector2.ZERO)
	for i in row.size():
		var raw:=Image.new();check(SAFE.load_png(raw,state.frameFiles[i])==OK,"Selected literal source available")
		check(raw.get_data()==row[i].get_image().get_data(),"Exact normal-loader pixels")
		check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Master density and pivot")
		var mid:float=elapsed+float(state.frameDurationsMs[i])/2000.0
		elapsed+=float(state.frameDurationsMs[i])/1000.0
		check(player.frame_at_elapsed("walk-west",mid)==row[i],"Original elapsed gait phase")
		check(player.frame("walk","west",mid,Vector2(.1796875*mid/2.0,0))==row[i],"Original movement-distance gait phase")
		var index:=i+1;board.blend_rect(raw,Rect2i(0,0,256,256),Vector2i(index%7*256,index/7*256))
	check(player.frame("walk","west",2.001,Vector2(.1796875*2.001/2.0,0))==row[0],"Distance loop wrap")
	check(player.frame("walk","west",3,Vector2(.1796875*2.001/2.0,0))==row[0],"Stationary gait holds")
	# Native equipment stays at its existing literal selection and source canvas.
	var hm:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-walk-west-material-v1/helmet-manifest.json"));var hs:Dictionary=hm.states[0];var hr:Array=player.equipment_frames["diving-helmet"]["walk-west"]
	elapsed=0
	check(hr.size()==48,"Paired original equipment poses retained")
	for i in hr.size():
		var raw:=Image.new();check(SAFE.load_png(raw,hs.frameFiles[i])==OK,"Original equipment literal source")
		check(raw.get_data()==hr[i].get_image().get_data(),"Unchanged normal-loader equipped pixels")
		check(hr[i].get_meta("crew_pivot")==Vector2(128,224) and hr[i].get_meta("crew_standing_height")==148.0,"Original equipment registration")
		var mid:float=elapsed+float(hs.frameDurationsMs[i])/2000.0
		elapsed+=float(hs.frameDurationsMs[i])/1000.0
		check(player.frame_at_elapsed("walk-west",mid,"diving-helmet")==hr[i],"Paired original gear clock")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1792,1792);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(board);sprite.centered=false;view.add_child(sprite);await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/bill-walk-west-material-selected-native-v1/loaded-water-carry.png")==OK,"Fresh all-pose native capture");view.queue_free()
	grid.free();print("BILL WALK WEST MATERIAL SELECTED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)


