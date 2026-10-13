extends SceneTree
const SAFE=preload("res://scripts/safe_image.gd")
const IDLES=[{
	"east":"res://character/bill-seated-east-coherent-v1/frames/sit-down-east/000.png",
	"south":"res://character/bill-seated-south-coherent-v1/frames/sit-down-south/000.png",
	"west":"res://character/bill-seated-west-coherent-v1/frames/sit-down-west/000.png",
	"north":"res://character/bill-seated-north-coherent-v1/frames/sit-down-north/000.png"
},{
	"east":"res://character/bill-seated-helmet-east-coherent-v1/frames/sit-down-east/000.png",
	"south":"res://character/bill-seated-helmet-south-coherent-v1/frames/sit-down-south/000.png",
	"west":"res://character/bill-seated-helmet-west-coherent-v1/frames/sit-down-west/000.png",
	"north":"res://character/bill-seated-helmet-north-coherent-v1/frames/sit-down-north/000.png"
}]
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
	var board:=Image.create(2048,2048,false,Image.FORMAT_RGBA8);board.fill(Color("22343e"))
	for g in 2:
		var equipment:String="" if g==0 else "diving-helmet"
		var path:String="res://character/bill-rest-family-v1/manifest.json" if g==0 else "res://character/bill-rest-family-v1/helmet-manifest.json"
		var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path));check(m.status=="selected_runtime" and m.states.size()==12,"Cardinal normal family")
		for d in 4:
			var direction:String=["east","south","west","north"][d]
			var pool:Dictionary=player.frames if g==0 else player.equipment_frames[equipment]
			for action in 3:
				var state:Dictionary=m.states[d*3+action];var row:Array=pool[state.id];var elapsed:=0.0
				for i in row.size():
					var raw:=Image.new();check(SAFE.load_png(raw,state.frameFiles[i])==OK,"Literal source available")
					check(row[i].get_image().get_data()==raw.get_data(),"Normal loader exact authored pixels")
					check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Master density")
					check(not row[i].get_meta("crew_water_pose") and row[i].get_meta("crew_depth_offset")==0.0,"Dry pose metadata")
					check(player.frame_at_elapsed(state.id,elapsed+float(state.frameDurationsMs[i])/2000,equipment)==row[i],"Normal frame pacing")
					elapsed+=float(state.frameDurationsMs[i])/1000
					if action==0:board.blend_rect(raw,Rect2i(0,0,256,256),Vector2i(i*256,(d*2+g)*256))
				if state.loop:
					check(player.frame("sleep",direction,0.0,Vector2.ZERO,equipment)==row[0] and player.frame("sleep",direction,1.201,Vector2.ZERO,equipment)==row[0],"Actual player sleep wrap")
					check(row[0].get_meta("crew_rest_head_offset")==Vector2(state.restHeadOffset[0],state.restHeadOffset[1]),"Exact family head-anchor metadata")
				else:check(is_equal_approx(elapsed,.8) and player.frame_at_elapsed(state.id,99,equipment)==row[-1],"Finite800ms terminal hold")
			var entry:Array=pool["lie-down-"+direction];var wake:Array=pool["get-up-"+direction];var sleep:Array=pool["sleep-"+direction]
			check(entry[-1].get_image().get_data()==sleep[0].get_image().get_data() and sleep[0].get_image().get_data()==wake[0].get_image().get_data(),"Exact resting joins")
			for i in 8:check(entry[i].get_image().get_data()==wake[7-i].get_image().get_data(),"Exact authored wake reverse")
			var idle:=Image.new()
			check(SAFE.load_png(idle,IDLES[g][direction])==OK and idle.get_data()==entry[0].get_image().get_data(),"Exact selected idle endpoint")
			check(grid.human_animations["lie-down"][direction][0]==player.frames["lie-down-"+direction][0],"Grid selects normal generic family")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(2048,2048);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(board);sprite.centered=false;view.add_child(sprite);await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/bill-rest-family-native-v1/loaded-water-carry.png")==OK,"Fresh native cardinal family capture");view.queue_free()
	grid.free();print("BILL REST FAMILY: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
