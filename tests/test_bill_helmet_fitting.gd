extends SceneTree

const PACK := "res://character/bill-helmet-fitting-east-v1/manifest.json"
var checks := 0
var failures := 0

func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)

func _init() -> void:
	call_deferred("run")

func padded(texture: Texture2D) -> Image:
	var result := Image.create(256,256,false,Image.FORMAT_RGBA8)
	result.blit_rect(texture.get_image(),Rect2i(0,0,184,184),Vector2i(36,52))
	for y in range(256):
		for x in range(256):
			if result.get_pixel(x,y).a==0.0:result.set_pixel(x,y,Color(0,0,0,0))
	return result

func run() -> void:
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations()
	var player=grid.human_water_player
	var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACK))
	for state in manifest.states:
		var frames: Array=player.frames[state.id]
		check(frames.size()==12,state.id+" count")
		check(player.timing[state.id].durations==state.frameDurationsMs,state.id+" timing")
		for i in range(12):
			var expected:=Image.load_from_file(PACK.get_base_dir().path_join(state.frameFiles[i]))
			check(frames[i].get_image().get_data()==expected.get_data(),state.id+" pixels "+str(i))
			check(frames[i].get_meta("crew_pivot")==Vector2(128,224),state.id+" pivot")
			check(frames[i].get_meta("crew_standing_height")==148.0,state.id+" scale")
	var bare:=padded(player.frames["idle-east"][0]);var helmet:=padded(player.equipment_frames["diving-helmet"]["idle-east"][0])
	for pair in [["equip-helmet-east",0,bare],["equip-helmet-east",11,helmet],["remove-helmet-east",0,helmet],["remove-helmet-east",11,bare]]:
		check(player.frames[pair[0]][pair[1]].get_image().get_data()==pair[2].get_data(),"Exact idle endpoint "+pair[0]+str(pair[1]))
	var actor=load("res://scripts/bill_npc.gd").new();actor.active=true;actor.movement_medium="dry"
	check(actor.begin_helmet_action(true),"Begin fitting")
	check(is_equal_approx(actor.timer,player.timing["equip-helmet-east"].seconds),"Fitting controller duration")
	actor.advance_helmet_action(actor.timer+.001)
	check(actor.helmet_equipped and actor.state=="idle","Fitting completes equipped")
	check(actor.begin_helmet_action(false),"Begin removal")
	check(is_equal_approx(actor.timer,player.timing["remove-helmet-east"].seconds),"Removal controller duration")
	actor.advance_helmet_action(actor.timer+.001)
	check(not actor.helmet_equipped and actor.state=="idle","Removal completes bare")
	if DisplayServer.get_name()!="headless":
		root.size=Vector2i(1100,640);RenderingServer.set_default_clear_color(Color("#22333c"))
		for r in range(2):
			var key: String=["equip-helmet-east","remove-helmet-east"][r]
			for col in range(6):
				var sprite:=Sprite2D.new();sprite.texture=player.frames[key][[0,2,4,6,8,11][col]];sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
				sprite.position=Vector2(90+col*183,145+r*300);root.add_child(sprite)
				var label:=Label.new();label.text=key+" "+str([0,2,4,6,8,11][col]);label.position=Vector2(8+col*183,270+r*300);root.add_child(label)
		await RenderingServer.frame_post_draw
		DirAccess.make_dir_recursive_absolute("res://output/bill-fitting-native")
		check(root.get_texture().get_image().save_png("res://output/bill-fitting-native/loaded-poses.png")==OK,"Native loaded poses")
	grid.free()
	print("BILL FITTING: %d checks, %d failures" % [checks,failures]);quit(1 if failures else 0)
