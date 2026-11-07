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
	var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-torch-helmet-family-v1/manifest.json"))
	check(m.states.size()==12,"Cardinal equipment torch family")
	var board:=Image.create(1536,3072,false,Image.FORMAT_RGBA8);board.fill(Color("22343e"))
	for j in m.states.size():
		var s:Dictionary=m.states[j];var row:Array=player.equipment_frames["diving-helmet"][s.id];var elapsed:=0.0
		for i in row.size():
			var raw:=Image.new();check(SAFE.load_png(raw,s.frameFiles[i])==OK,"Literal source available")
			check(raw.get_data()==row[i].get_image().get_data(),"Normal equipment loader exact pixels")
			check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Master density")
			check(not row[i].get_meta("crew_water_pose"),"Dry equipment")
			check(player.frame_at_elapsed(s.id,elapsed+float(s.frameDurationsMs[i])/2000,"diving-helmet")==row[i],"Equipment clock")
			elapsed+=float(s.frameDurationsMs[i])/1000
			board.blend_rect(raw,Rect2i(0,0,256,256),Vector2i(i*256,j*256))
		if s.loop:
			var direction:String=s.id.get_slice("-",1)
			check(player.frame("weld",direction,.961,Vector2.ZERO,"diving-helmet")==row[0],"Weld wrap")
		else:check(is_equal_approx(elapsed,.52) and player.frame_at_elapsed(s.id,99,"diving-helmet")==row[-1],"Finite terminal hold")
		check(grid.human_animations[s.id.rsplit("-",true,1)[0]][s.id.rsplit("-",true,1)[1]][0]==player.frames[s.id][0],"Bare torch remains selected")
	for direction in ["east","west","south","north"]:
		var p:Dictionary=player.equipment_frames["diving-helmet"]
		check(p["torch-draw-"+direction][-1].get_image().get_data()==p["weld-"+direction][0].get_image().get_data(),"Exact draw/work join")
		check(p["weld-"+direction][-1].get_image().get_data()==p["torch-stow-"+direction][0].get_image().get_data(),"Exact work/stow join")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1536,3072);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(board);sprite.centered=false;view.add_child(sprite);await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/bill-torch-helmet-family-native-v1/loaded-water-carry.png")==OK,"Fresh native family capture");view.queue_free()
	grid.free();print("BILL TORCH HELMET FAMILY: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
