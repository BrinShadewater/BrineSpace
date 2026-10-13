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
	var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-walk-north-master-head-v1/manifest.json"));var state:Dictionary=m.states[0];var row:Array=player.frames["walk-north"]
	check(row.size()==30,"All thirty north walk poses")
	check(m.status=="selected_runtime","Current selected status")
	check(grid.human_animations["walk"]["north"][0]==row[0],"Normal grid selects master-head layer")
	check(player.strides["walk-north"]==.1796875,"Original distance stride")
	var board:=Image.create(1536,1536,false,Image.FORMAT_RGBA8);board.fill(Color("22343e"));var idle:=Image.new()
	check(SAFE.load_png(idle,"res://character/bill-seated-north-coherent-v1/frames/sit-down-north/000.png")==OK,"Native master available");board.blend_rect(idle,Rect2i(0,0,256,256),Vector2i.ZERO)
	player.frame("walk","north",0,Vector2.ZERO)
	for i in row.size():
		var raw:=Image.new();check(SAFE.load_png(raw,state.frameFiles[i])==OK,"Selected literal source available")
		check(raw.get_data()==row[i].get_image().get_data(),"Exact normal-loader pixels")
		check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Master density and pivot")
		var mid:float=(i+.5)*.05
		check(player.frame_at_elapsed("walk-north",mid)==row[i],"Original elapsed gait phase")
		check(player.frame("walk","north",mid,Vector2(.1796875*mid/1.5,0))==row[i],"Original movement-distance gait phase")
		var index:=i+1;board.blend_rect(raw,Rect2i(0,0,256,256),Vector2i(index%6*256,index/6*256))
	check(player.frame("walk","north",1.501,Vector2(.1796875*1.501/1.5,0))==row[0],"Distance loop wrap")
	check(player.frame("walk","north",2,Vector2(.1796875*1.501/1.5,0))==row[0],"Stationary gait holds")
	# Native equipment stays at its existing literal selection and source canvas.
	var audit:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-selected-source-audit-2026-10-01-locomotion-v4/source-inventory.json"));var hs:Dictionary=audit.selectedStateSources.helmet["walk-north"];var hr:Array=player.equipment_frames["diving-helmet"]["walk-north"]
	check(hr.size()==30,"Paired original equipment poses retained")
	for i in hr.size():
		var raw:=Image.new();check(SAFE.load_png(raw,hs.sourceFiles[i])==OK,"Original equipment literal source")
		check(raw.get_data()==hr[i].get_image().get_data(),"Unchanged normal-loader equipped pixels")
		check(hr[i].get_meta("crew_pivot")==Vector2(92,172) and hr[i].get_meta("crew_standing_height")==148.0,"Original equipment registration")
		check(player.frame_at_elapsed("walk-north",(i+.5)*.05,"diving-helmet")==hr[i],"Paired original gear clock")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1536,1536);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(board);sprite.centered=false;view.add_child(sprite);await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/bill-walk-north-master-head-selected-native-v1/loaded-water-carry.png")==OK,"Fresh all-pose native capture");view.queue_free()
	grid.free();print("BILL WALK NORTH MASTER HEAD SELECTED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
