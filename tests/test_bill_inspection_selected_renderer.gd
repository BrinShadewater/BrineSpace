extends SceneTree
const PACKS=[["res://character/bill-inspect-family-v1/bare-manifest.json",""],["res://character/bill-inspect-family-v1/helmet-manifest.json","diving-helmet"]]
const SAFE=preload("res://scripts/safe_image.gd")
var checks:=0
var failures:=0
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func raw(path: String) -> Image:
	var image:=Image.new();check(SAFE.load_png(image,path)==OK,"Raw source available "+path);return image
func registered(texture: Texture2D) -> Image:
	var source:=texture.get_image();source.convert(Image.FORMAT_RGBA8)
	var plane:=Image.create(256,256,false,Image.FORMAT_RGBA8);plane.fill(Color(0,0,0,0))
	var offset: Vector2=Vector2(128,224)-texture.get_meta("crew_pivot")
	check(texture.get_meta("crew_standing_height")==148.0 and offset==offset.round(),"Idle join has matching density and integral pivot offset")
	plane.blit_rect(source,Rect2i(Vector2i.ZERO,source.get_size()),Vector2i(offset))
	return plane
func _init():call_deferred("run")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player;var reviews:=[]
	for spec in PACKS:
		var m: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(spec[0]));var rows: Dictionary={}
		check(m.states.size()==12 and m.status=="selected_runtime","Twelve normally selected cardinal actions per gear")
		for state in m.states:
			var frames: Dictionary=player.frames if spec[1].is_empty() else player.equipment_frames[spec[1]]
			check(frames.has(state.id),"Normal loader selects "+state.id)
			if not frames.has(state.id):continue
			var row: Array=frames[state.id];rows[state.id]=row;check(row.size()==6,"Six selected frames")
			var elapsed:=0.0
			for i in 6:
				check(state.frameFiles[i].begins_with("res://"),"Whole literal source path")
				check(row[i].get_image().get_data()==raw(state.frameFiles[i]).get_data(),"Selected exact source pixels")
				check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Selected plane/density")
				check(not row[i].get_meta("crew_water_pose") and row[i].get_meta("crew_depth_offset")==0.0,"Dry standing metadata")
				check(player.frame_at_elapsed(state.id,elapsed+state.frameDurationsMs[i]/2000.0,spec[1])==row[i],"Authored elapsed pose")
				elapsed+=state.frameDurationsMs[i]/1000.0
			check(is_equal_approx(player.cycle_seconds(state.id,spec[1]),elapsed),"Selected timing contract")
			if not state.loop:
				check(player.frame_at_elapsed(state.id,9,spec[1])==row[-1],"Finite endpoint hold")
			else:
				check(row[0].get_image().get_data()==row[-1].get_image().get_data(),"Exact inspection loop closure")
				for cycle in [0,1,7]:
					player.current_key="";player.last_time=-1;player.frame("inspect",state.facings[0],0,Vector2.ZERO,spec[1])
					check(player.frame("inspect",state.facings[0],.4+cycle*.96,Vector2.ZERO,spec[1])==row[2],"Normal cosmetic loop repeat")
			reviews.append(row)
		var frames: Dictionary=player.frames if spec[1].is_empty() else player.equipment_frames[spec[1]]
		for direction in ["east","south","west","north"]:
			var enter: Array=rows["inspect-enter-"+direction];var loop: Array=rows["inspect-"+direction];var exit: Array=rows["inspect-exit-"+direction]
			var idle_plane:=registered(frames["idle-"+direction][0])
			check(registered(enter[0]).get_data()==idle_plane.get_data(),"Normal exact selected idle entry join on shared pivot plane")
			check(enter[-1].get_image().get_data()==loop[0].get_image().get_data() and exit[0].get_image().get_data()==loop[-1].get_image().get_data(),"Exact selected held joins")
			check(registered(exit[-1]).get_data()==idle_plane.get_data(),"Normal exact selected idle exit join on shared pivot plane")
	if DisplayServer.get_name()!="headless":
		var view:=SubViewport.new();view.size=Vector2i(1200,2400);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view);var bg:=ColorRect.new();bg.size=Vector2(1200,2400);bg.color=Color("22343e");view.add_child(bg)
		for j in reviews.size():
			for i in 6:
				var sprite:=Sprite2D.new();sprite.texture=reviews[j][i];sprite.centered=false;sprite.scale=Vector2.ONE*82/148;sprite.position=Vector2(100+i*200,95+j*100)-Vector2(128,224)*82/148;view.add_child(sprite)
		await RenderingServer.frame_post_draw;check(view.get_texture().get_image().save_png("res://output/bill-inspection-selected-renderer-v1/loaded-water-carry.png")==OK,"Native82 selected cardinal review");view.queue_free()
	grid.free();print("BILL INSPECTION SELECTED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
