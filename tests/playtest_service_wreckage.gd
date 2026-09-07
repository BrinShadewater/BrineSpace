extends SceneTree
const View := preload("res://assets/environment/service-wreckage-v1/service_wreckage_view.gd")
const OUT := "res://output/service-wreckage-mast-v1/"
var game

class Sheet extends Control:
	var view
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("102a32"))
		var font := ThemeDB.fallback_font
		draw_string(font,Vector2(30,44),"BRINE / EXTERIOR SERVICE WRECKAGE",HORIZONTAL_ALIGNMENT_LEFT,-1,25,Color("b7cec5"))
		draw_string(font,Vector2(30,76),"Original source color / transparent sprites / native Godot review",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color("839f9d"))
		var i := 0
		for id in View.SOURCES:
			var at := Vector2(20+i*315,120)
			var texture: Texture2D = view.textures[id]
			var display := texture.get_size()/texture.get_width()*290.0
			draw_texture_rect(texture,Rect2(at,display),false)
			draw_string(font,at+Vector2(0,405),id,HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color("bdcec6"))
			i += 1
		draw_string(font,Vector2(30,620),"Fixed groups: broken frame (3 props), pressure line (2), detached cover (1), fallen receiver (1)",HORIZONTAL_ALIGNMENT_LEFT,-1,21,Color("b7cec5"))
		draw_string(font,Vector2(30,663),"Decorative debris sits beneath new construction. Room-sized wrecks retain clearance rules.",HORIZONTAL_ALIGNMENT_LEFT,-1,19,Color("839f9d"))

func _init() -> void:
	call_deferred("run")

func settle() -> void:
	for i in range(6):
		await process_frame
	await RenderingServer.frame_post_draw

func capture(name: String) -> void:
	await settle()
	var frame := root.get_texture().get_image()
	assert(frame.get_size()==root.size,"Capture dimensions match actual window")
	frame.save_png(OUT+name+".png")

func center_on(at: Vector2) -> void:
	var scroll_to: Vector2 = at*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal = roundi(scroll_to.x)
	game.grid_scroll.scroll_vertical = roundi(scroll_to.y)
	game.grid_view.queue_redraw()

func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	preload("res://scripts/title_settings.gd").initialized = true
	root.mode = Window.MODE_WINDOWED
	root.content_scale_size = Vector2i.ZERO
	root.size = Vector2i(1600,900)
	var view := View.new()
	view.prepare()
	assert(view.textures.size()==5,"All five selected sources load")
	for texture in view.textures.values():
		assert(texture.get_image().detect_alpha()!=Image.ALPHA_NONE,"Selected sprites have real alpha")
	var sheet := Sheet.new()
	sheet.view = view
	sheet.size = root.size
	root.add_child(sheet)
	await capture("source-sheet")
	sheet.free()
	root.content_scale_size = Vector2i(1920,1080)
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://service_debris_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://service_debris_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	game._set_paused(true,false)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.wrecks.clear()
	# Isolated fixture anchors supply room scale and a connection for paid build-over.
	for group in View.GROUPS:
		game._place_room("crew_hab",Vector2i(group.anchor.floor())+Vector2i.LEFT,true)
	game.selected_card_id = ""
	game.hovered_card_id = ""
	game.hover_cell = Vector2i(-1,-1)
	game._refresh_all()
	var occupancy: Dictionary = game.occupied.duplicate(true)
	for width in [1280,1600,2560]:
		root.size = Vector2i(width,roundi(width*9.0/16.0))
		await settle()
		game._set_grid_zoom(0.20)
		await settle()
		for index in range(View.GROUPS.size()):
			center_on(View.GROUPS[index].anchor)
			await capture("group-%d-%d" % [index+1,width])
	assert(game.occupied==occupancy,"Rendering debris does not add or mutate occupancy")
	assert(game.grid_view.seabed_background.service_wreckage.textures.size()==5,"Station consumes all five selected sprites")
	var cell := Vector2i(24,23)
	game.selected_card_id = "corridor"
	game.selected_rotation = 1
	game.hand.assign(["corridor"])
	assert(game.get_placement_problem("corridor",cell).is_empty(),"Decorative debris permits normal construction")
	var before: int = game.resources.metal
	game._on_grid_clicked(cell)
	assert(game.occupied.has(cell) and game.resources.metal<before,"Building over debris uses normal paid input")
	game.selected_card_id = ""
	root.size = Vector2i(1600,900)
	await settle()
	game._set_grid_zoom(0.20)
	await settle()
	center_on(View.GROUPS[0].anchor)
	await capture("built-over-1600")
	var paths := [game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		for suffix in ["",".bak",".tmp"]:
			if FileAccess.file_exists(path+suffix):
				DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	print("SERVICE WRECKAGE PASS: five alpha sprites, four authored groups at three resolutions, unchanged occupancy, paid build-over")
	quit()
