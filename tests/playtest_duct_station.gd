extends SceneTree
const View := preload("res://assets/environment/duct-wreckage-v1/duct_view.gd")
const OUT := "res://output/duct-station-v1/"
var game

class Sheet extends Control:
	var view
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("102a32"))
		var font := ThemeDB.fallback_font
		draw_string(font,Vector2(30,44),"BRINE / DUCT",HORIZONTAL_ALIGNMENT_LEFT,-1,26,Color("b7cec5"))
		draw_string(font,Vector2(30,80),"Original source colors / full transparent canvases",HORIZONTAL_ALIGNMENT_LEFT,-1,19,Color("839f9d"))
		var i := 0
		for id in View.SOURCES:
			var at := Vector2(25+i*525,150)
			var texture: Texture2D = view.textures[id]
			var display := texture.get_size()/texture.get_width()*480.0
			draw_texture_rect(texture,Rect2(at,display),false)
			draw_string(font,at+Vector2(0,520),id,HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color("bdcec6"))
			i += 1
		draw_string(font,Vector2(30,780),"Collapsed duct source sheet. Decorative ground and debris; no resource or clearance mechanics.",HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color("839f9d"))

func _init() -> void:
	call_deferred("run")

func settle() -> void:
	for i in range(6):
		await process_frame
	await RenderingServer.frame_post_draw

func capture(name: String) -> void:
	await settle()
	var frame := root.get_texture().get_image()
	assert(frame.get_size()==root.size,"Actual capture dimensions match requested window")
	frame.save_png(OUT+name+".png")

func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	preload("res://scripts/title_settings.gd").initialized = true
	root.mode = Window.MODE_WINDOWED
	root.content_scale_size = Vector2i.ZERO
	root.size = Vector2i(1600,900)
	var view := View.new()
	view.prepare()
	assert(view.textures.size()==1)
	for texture in view.textures.values():
		assert(not texture.get_image().is_empty())
	var sheet := Sheet.new()
	sheet.view = view
	sheet.size = root.size
	root.add_child(sheet)
	await capture("source-sheet")
	sheet.free()
	root.content_scale_size = Vector2i(1920,1080)
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://duct_wreckage_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://duct_wreckage_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	game._set_paused(true,false)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.wrecks.clear()
	for group in [{"anchor":View.CENTER}]:
		game._place_room("crew_hab",Vector2i(group.anchor.floor())+Vector2i.LEFT,true)
	game.selected_card_id = ""
	game.hovered_card_id = ""
	game.hover_cell = Vector2i(-1,-1)
	game._refresh_all()
	var occupancy: Dictionary = game.occupied.duplicate(true)
	var resources: Dictionary = game.resources.duplicate(true)
	for width in [1280,1600,2560]:
		root.size = Vector2i(width,roundi(width*9.0/16.0))
		await settle()
		game._set_grid_zoom(0.30)
		await settle()
		for index in range([{"anchor":View.CENTER}].size()):
			var scroll_to: Vector2 = [{"anchor":View.CENTER}][index].anchor*game.get_cell_size()-game.grid_scroll.size*0.5
			game.grid_scroll.scroll_horizontal = roundi(scroll_to.x)
			game.grid_scroll.scroll_vertical = roundi(scroll_to.y)
			game.grid_view.queue_redraw()
			await capture("group-%d-%d" % [index+1,width])
	assert(game.occupied==occupancy and game.resources==resources,"Rendering duct_wreckage changes no gameplay state")
	assert(game.grid_view.seabed_background.duct_wreckage.textures.size()==1)
	var paths := [game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		for suffix in ["",".bak",".tmp"]:
			if FileAccess.file_exists(path+suffix):
				DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	print("DUCT STATION PASS: one texture, three verified resolutions, unchanged occupancy and resources")
	quit()
