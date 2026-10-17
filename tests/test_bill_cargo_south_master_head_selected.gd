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
	var board:=Image.create(2048,2048,false,Image.FORMAT_RGBA8);board.fill(Color("22343e"));var slot:=0
	for gear in ["","diving-helmet"]:
		var path:String="res://character/bill-cargo-south-master-head-v1/manifest.json" if gear.is_empty() else "res://character/bill-cargo-south-master-head-v1/helmet-manifest.json"
		var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path));check(m.status=="selected_runtime","Current selected status")
		var master:=Image.new();var mp:String="res://character/bill-seated-south-coherent-v1/frames/sit-down-south/000.png" if gear.is_empty() else "res://character/bill-seated-helmet-south-coherent-v1/frames/sit-down-south/000.png"
		check(SAFE.load_png(master,mp)==OK,"Native master available");board.blend_rect(master,Rect2i(0,0,256,256),Vector2i(slot%8*256,slot/8*256));slot+=1
		for state in m.states:
			var key:String=state.id;var row:Array=player.frames[key] if gear.is_empty() else player.equipment_frames[gear][key]
			check(row.size()==state.frameFiles.size(),"All selected family phases loaded")
			check(player.strides.carry==.12 if gear.is_empty() else player.equipment_strides[gear].carry==.12,"Original cargo travel stride")
			var elapsed:=0.0
			for i in row.size():
				var raw:=Image.new();check(SAFE.load_png(raw,state.frameFiles[i])==OK,"Literal selected frame available")
				check(raw.get_data()==row[i].get_image().get_data(),"Exact normal-loader pixels")
				check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Master density and foot pivot")
				var mid:float=elapsed+float(state.frameDurationsMs[i])/2000.0;elapsed+=float(state.frameDurationsMs[i])/1000.0
				check(player.frame_at_elapsed(key,mid,gear)==row[i],"Original action source clock")
				board.blend_rect(raw,Rect2i(0,0,256,256),Vector2i(slot%8*256,slot/8*256));slot+=1
			check(player.timing[key].loop==state.loop if gear.is_empty() else player.equipment_timing[gear][key].loop==state.loop,"Original action loop mode")
			check(player.frame_at_elapsed(key,elapsed+.001,gear)==row[-1],"Simulation elapsed accessor clamps to terminal phase")
			if state.loop:
				player.frame("carry","south",0,Vector2.ZERO,gear)
				var cycle:float=player.cycle_seconds(key,gear);var cursor:=0.0
				for i in row.size():
					var mid:float=cursor+float(state.frameDurationsMs[i])/2000.0;cursor+=float(state.frameDurationsMs[i])/1000.0
					check(player.frame("carry","south",mid,Vector2(0,.12*mid/cycle),gear)==row[i],"Original carry distance phase")
				check(player.frame("carry","south",cycle+.001,Vector2(0,.12*(cycle+.001)/cycle),gear)==row[0],"Live carry distance loop wraps")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(2048,2048);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
		var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(board);sprite.centered=false;view.add_child(sprite);await RenderingServer.frame_post_draw
		check(view.get_texture().get_image().save_png("res://output/bill-cargo-south-master-head-selected-native-v1/loaded-water-carry.png")==OK,"Fresh all-phase native capture");view.queue_free()
	grid.free();print("BILL CARGO SOUTH MASTER HEAD SELECTED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
