extends SceneTree

const PACK := "res://character/bill-torch-actions-v1/manifest.json"
var checks := 0
var failures := 0

func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)

func _init() -> void:
	call_deferred("run")

func run() -> void:
	var grid = load("res://scripts/grid_canvas.gd").new()
	grid._load_major_bill_animations()
	var player = grid.human_water_player
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(PACK))
	for state in manifest.states:
		var frames: Array = player.frames[state.id]
		check(frames.size()==6, state.id+" count")
		check(player.timing[state.id].durations==state.frameDurationsMs, state.id+" timing")
		check(player.timing[state.id].loop==state.loop, state.id+" loop")
		for i in range(6):
			var expected := Image.load_from_file(PACK.get_base_dir().path_join(state.frameFiles[i]))
			check(frames[i].get_image().get_data()==expected.get_data(),state.id+" pixels "+str(i))
			check(frames[i].get_meta("crew_pivot")==Vector2(128,224),state.id+" pivot")
			check(frames[i].get_meta("crew_standing_height")==148.0,state.id+" standing scale")
	var actor = load("res://scripts/bill_npc.gd").new()
	actor.movement_medium="dry";actor.state="weld";actor.goal="construction"
	for phase in [[0.2,"torch-draw"],[4.0,"weld"],[9.7,"torch-stow"]]:
		actor.timer=phase[0]
		check(actor.animation_state()==phase[1],"Construction selects "+phase[1])
	actor.goal="hull-repair";check(actor.animation_state()=="weld","Dry repair selects weld")
	var offsets: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-torch-actions-v1/torch-tip-offsets.json"))
	var fake_game := {"bill_npc":actor}
	for direction in ["east","west","south","north"]:
		var idle := Image.create(256,256,false,Image.FORMAT_RGBA8)
		idle.blit_rect(player.frames["idle-"+direction][0].get_image(),Rect2i(0,0,184,184),Vector2i(36,52))
		for y in range(256):
			for x in range(256):
				if idle.get_pixel(x,y).a==0.0:idle.set_pixel(x,y,Color(0,0,0,0))
		check(player.frames["torch-draw-"+direction][0].get_image().get_data()==idle.get_data(),direction+" draw idle endpoint")
		check(player.frames["torch-stow-"+direction][5].get_image().get_data()==idle.get_data(),direction+" stow idle endpoint")
		check(player.frames["torch-draw-"+direction][5].get_image().get_data()==player.frames["weld-"+direction][0].get_image().get_data(),direction+" ignition join")
		check(player.frames["weld-"+direction][5].get_image().get_data()==player.frames["torch-stow-"+direction][0].get_image().get_data(),direction+" stow join")
		actor.direction=direction
		var tip: Vector2 = load("res://scripts/station_effects.gd").torch_tip_offset(fake_game,actor)
		check(tip==Vector2(offsets[direction][0],offsets[direction][1]),direction+" repair spark anchor")
	if DisplayServer.get_name()!="headless":
		root.size=Vector2i(1100,760)
		RenderingServer.set_default_clear_color(Color("#22333c"))
		var directions := ["east","west","south","north"]
		for row in range(4):
			for col in range(6):
				var key: String = ["torch-draw-","weld-","torch-stow-"][col/2]+directions[row]
				var sprite := Sprite2D.new();sprite.texture=player.frames[key][2 if col%2==0 else 4]
				sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;sprite.scale=Vector2.ONE*.68
				sprite.position=Vector2(90+col*183,92+row*185);root.add_child(sprite)
				var label := Label.new();label.text=key;label.position=Vector2(8+col*183,165+row*185);root.add_child(label)
		await RenderingServer.frame_post_draw
		DirAccess.make_dir_recursive_absolute("res://output/bill-torch-native")
		check(root.get_texture().get_image().save_png("res://output/bill-torch-native/loaded-poses.png")==OK,"Native pose capture")
	grid.free()
	print("BILL TORCH: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
