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
	var player=load("res://scripts/crew_sprite_player.gd").new()
	player.load_manifest("res://character/bill-run-east-coherent-v1/manifest.json")
	var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-run-east-coherent-v1/manifest.json"));var state:Dictionary=m.states[0];var row:Array=player.frames["run-east"]
	check(row.size()==6,"Six authored phases")
	var elapsed:=0.0;var board:=Image.create(1792,512,false,Image.FORMAT_RGBA8);board.fill(Color("22343e"))
	var idle:=Image.new();check(SAFE.load_png(idle,"res://character/bill-seated-east-coherent-v1/frames/sit-down-east/000.png")==OK,"Selected master available");board.blend_rect(idle,Rect2i(0,0,256,256),Vector2i.ZERO)
	var small=idle.duplicate();small.resize(142,142,Image.INTERPOLATE_LANCZOS);board.blend_rect(small,Rect2i(0,0,142,142),Vector2i(57,320))
	player.frame("run","east",0,Vector2.ZERO)
	for i in row.size():
		var raw:=Image.new();check(SAFE.load_png(raw,state.frameFiles[i])==OK,"Literal source available")
		check(raw.get_data()==row[i].get_image().get_data(),"Loaded pixels exact")
		check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Master density/pivot")
		var mid:float=elapsed+float(state.frameDurationsMs[i])/2000
		check(player.frame_at_elapsed("run-east",mid)==row[i],"Authored clock")
		check(player.frame("run","east",mid,Vector2(.168*mid/.54,0))==row[i],"Movement-distance gait clock")
		elapsed+=float(state.frameDurationsMs[i])/1000
		board.blend_rect(raw,Rect2i(0,0,256,256),Vector2i((i+1)*256,0));small=raw.duplicate();small.resize(142,142,Image.INTERPOLATE_LANCZOS);board.blend_rect(small,Rect2i(0,0,142,142),Vector2i((i+1)*256+57,320))
	check(player.frame("run","east",.541,Vector2(.168*.541/.54,0))==row[0],"Distance loop wrap")
	check(player.frame("run","east",1,Vector2(.168*.541/.54,0))==row[0],"Paused stationary gait holds")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1792,512);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(board);sprite.centered=false;view.add_child(sprite);await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/bill-run-east-candidate-native-v1/loaded-water-carry.png")==OK,"Fresh native148/82 candidate capture");view.queue_free()
	print("BILL RUN EAST CANDIDATE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
