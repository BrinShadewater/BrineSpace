extends SceneTree
const View := preload("res://assets/environment/ambient-water-v1/ambient_water_view.gd")
const OUT := "res://output/ambient-water-v1/"
var game

class Sheet extends Control:
	var view
	var time_seconds := 0.0
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("102a32"))
		var font := ThemeDB.fallback_font
		draw_string(font,Vector2(30,44),"BRINE / AMBIENT WATER",HORIZONTAL_ALIGNMENT_LEFT,-1,26,Color("b7cec5"))
		draw_string(font,Vector2(30,80),"Original sources above / runtime opacity and drifting crossfade below",HORIZONTAL_ALIGNMENT_LEFT,-1,19,Color("839f9d"))
		for index in range(View.EFFECTS.size()):
			var effect: Dictionary = View.EFFECTS[index]
			var at := Vector2(30+index*525,100)
			var texture: Texture2D = view.textures[effect.id]
			draw_texture_rect(texture,Rect2(at,Vector2.ONE*460),false)
			draw_string(font,at+Vector2(0,480),effect.id,HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color("bdcec6"))
			for sample in View.samples(time_seconds):
				if sample.id!=effect.id:
					continue
				var center: Vector2 = at+Vector2(235,630)+(sample.at-effect.anchor)*130.0
				draw_texture_rect(texture,Rect2(center-Vector2.ONE*160,Vector2.ONE*320),false,Color(0.53,0.65,0.68,sample.opacity))

func _init() -> void:
	call_deferred("run")

func settle() -> void:
	for i in range(6):
		await process_frame
	await RenderingServer.frame_post_draw

func capture(name: String) -> Image:
	await settle()
	var frame := root.get_texture().get_image()
	assert(frame.get_size()==root.size,"Actual capture dimensions match window")
	frame.save_png(OUT+name+".png")
	return frame

func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	preload("res://scripts/title_settings.gd").initialized = true
	root.mode = Window.MODE_WINDOWED
	root.content_scale_size = Vector2i.ZERO
	root.size = Vector2i(1600,900)
	var view := View.new()
	view.prepare()
	assert(view.textures.size()==3)
	for texture in view.textures.values():
		assert(texture.get_image().detect_alpha()!=Image.ALPHA_NONE)
	for time in [0.0,2.0,11.0,18.0,23.0,100000.0]:
		var samples := View.samples(time)
		assert(samples==View.samples(time),"Sampling is deterministic")
		for index in range(View.EFFECTS.size()):
			assert(is_equal_approx(samples[index*2].opacity+samples[index*2+1].opacity,View.EFFECTS[index].opacity),"Crossfade maintains bounded combined opacity")
	# At a wrap the resetting copy is invisible, so it cannot visibly teleport.
	var wrap: float = (1.0-View.EFFECTS[0].offset)*View.EFFECTS[0].period
	assert(View.samples(wrap-0.0001)[0].opacity<0.000001 and View.samples(wrap+0.0001)[0].opacity<0.000001)
	var sheet := Sheet.new()
	sheet.view = view
	sheet.size = root.size
	root.add_child(sheet)
	var first := await capture("source-and-motion-0")
	sheet.time_seconds = 6.0
	sheet.queue_redraw()
	var second := await capture("source-and-motion-6")
	assert(first.get_data()!=second.get_data(),"Motion changes actual rendered pixels")
	sheet.queue_redraw()
	var frozen := await capture("source-and-motion-frozen")
	assert(second.get_data()==frozen.get_data(),"Same time produces pixel-identical water")
	sheet.free()
	root.content_scale_size = Vector2i(1920,1080)
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://ambient_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://ambient_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	game.set_process(false)
	game.tick_timer.stop()
	game._set_paused(true,false)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.wrecks.clear()
	for effect in View.EFFECTS:
		game._place_room("crew_hab",Vector2i(effect.anchor.floor())+Vector2i.LEFT,true)
	game.selected_card_id = ""
	game.hovered_card_id = ""
	game.hover_cell = Vector2i(-1,-1)
	game._refresh_all()
	var initial_time: float = game.get_visual_time_seconds()
	game._process(1.0)
	assert(game.get_visual_time_seconds()==initial_time,"Global pause freezes authoritative visual clock")
	game.paused = false
	game._process(1.0)
	assert(game.get_visual_time_seconds()>initial_time,"Running advances water clock")
	var before_fast: float = game.get_visual_time_seconds()
	game.time_speed_index = 1
	game._process(1.0)
	assert(is_equal_approx(game.get_visual_time_seconds()-before_fast,game.time_speeds[1]),"Water respects selected simulation speed")
	game.time_speed_index = 0
	game.paused = true
	var clock: float = game.get_visual_time_seconds()
	var state := View.samples(clock)
	game._process(2.0)
	assert(View.samples(game.get_visual_time_seconds())==state,"Pause preserves exact water state")
	var occupancy: Dictionary = game.occupied.duplicate(true)
	var resources: Dictionary = game.resources.duplicate(true)
	for width in [1280,1600,2560]:
		root.size = Vector2i(width,roundi(width*9.0/16.0))
		await settle()
		game._set_grid_zoom(0.22)
		await settle()
		for index in range(View.EFFECTS.size()):
			var scroll_to: Vector2 = View.EFFECTS[index].anchor*game.get_cell_size()-game.grid_scroll.size*0.5
			game.grid_scroll.scroll_horizontal = roundi(scroll_to.x)
			game.grid_scroll.scroll_vertical = roundi(scroll_to.y)
			game.grid_view.queue_redraw()
			await capture("effect-%d-%d" % [index+1,width])
	assert(game.occupied==occupancy and game.resources==resources)
	assert(game.grid_view.seabed_background.ambient_water.textures.size()==3)
	# A separate overlap capture verifies the water remains beneath an opaque room.
	game._place_room("crew_hab",Vector2i(View.EFFECTS[0].anchor.floor()),true)
	root.size = Vector2i(1600,900)
	await settle()
	game._set_grid_zoom(0.22)
	await settle()
	var overlap_scroll: Vector2 = View.EFFECTS[0].anchor*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal = roundi(overlap_scroll.x)
	game.grid_scroll.scroll_vertical = roundi(overlap_scroll.y)
	game.grid_view.queue_redraw()
	await capture("room-over-water-1600")
	var paths := [game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		for suffix in ["",".bak",".tmp"]:
			if FileAccess.file_exists(path+suffix):
				DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	print("AMBIENT WATER PASS: three alpha sources, rendered motion/freeze, bounded loop crossfade, authoritative pause clock, three effects at three resolutions, unchanged occupancy/resources")
	quit()
