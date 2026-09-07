extends SceneTree
const View := preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
const OUT := "res://output/sub-biomes-v1/"
var game

class Sheet extends Control:
	var view
	var mesh: ArrayMesh
	var biomes: Array = []
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("0a222c"))
		var font := ThemeDB.fallback_font
		draw_string(font,Vector2(30,38),"BRINE / SUB-BIOME MATERIALS + SCENERY",HORIZONTAL_ALIGNMENT_LEFT,-1,23,Color("93bcb2"))
		var index := 0
		for biome in biomes:
			var at := Vector2(25+index*525,70)
			draw_rect(Rect2(at,Vector2(500,780)),Color("102a32"))
			draw_string(font,at+Vector2(20,35),View.DEFINITIONS[biome].name,HORIZONTAL_ALIGNMENT_LEFT,-1,23,Color("c4d4c7"))
			draw_mesh(mesh,view.textures[biome+"-ground"],Transform2D(0,Vector2.ONE*90,0,at+Vector2(70,100)))
			draw_string(font,at+Vector2(20,520),"Ground + feathered transition",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color("8facaa"))
			for i in range(2):
				var suffix: String = View.DEFINITIONS[biome].props[i]
				var tex: Texture2D = view.textures[biome+"-"+suffix]
				var display := tex.get_size()/maxf(tex.get_width(),tex.get_height())*190.0
				draw_texture_rect(tex,Rect2(at+Vector2(28+i*240,550)+(Vector2(190,190)-display)*0.5,display),false)
				draw_string(font,at+Vector2(28+i*240,762),suffix,HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color("b9c7bd"))
			index += 1

func _init() -> void:
	call_deferred("run")

func settle() -> void:
	for i in range(6):
		await process_frame
	await RenderingServer.frame_post_draw

func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	preload("res://scripts/title_settings.gd").initialized = true
	root.mode = Window.MODE_WINDOWED
	var view := View.new()
	view.prepare()
	assert(view.textures.size()==View.DEFINITIONS.size()*3,"Every habitat material and prop loads")
	var duplicate_view := View.new()
	duplicate_view.prepare()
	assert(view.props==duplicate_view.props,"Habitat decoration is reproducible")
	for region in View.REGIONS:
		assert(View.coverage(region.center,region.center,region.radius)>0.99)
		assert(View.coverage(region.center+region.radius*2,region.center,region.radius)==0)
	var sheet := Sheet.new()
	sheet.view = view
	sheet.mesh = View.ground_mesh(Vector2(2,2),Vector2(2.3,2.3))
	root.content_scale_size = Vector2i.ZERO
	root.size = Vector2i(1600,900)
	sheet.size = root.size
	root.add_child(sheet)
	var keys := View.DEFINITIONS.keys()
	for page in range(ceili(keys.size()/3.0)):
		sheet.biomes = keys.slice(page*3,page*3+3)
		sheet.queue_redraw()
		await settle()
		var sheet_name := "asset-sheet.png" if page==0 else "asset-sheet-%d.png" % (page+1)
		root.get_texture().get_image().save_png(OUT+sheet_name)
	sheet.free()
	root.content_scale_size = Vector2i(1920,1080)
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://biomes_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://biomes_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	game._set_paused(true,false)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.wrecks.clear()
	for region in View.REGIONS:
		var cell := Vector2i(region.center.floor())
		game._place_room("reactor",cell,true)
		game._place_room("crew_hab",cell+Vector2i.RIGHT,true)
	game.selected_card_id = ""
	game.hovered_card_id = ""
	game.hover_cell = Vector2i(-1,-1)
	game._refresh_all()
	for width in [1280,1600,2560]:
		root.size = Vector2i(width,roundi(width*9.0/16.0))
		await settle()
		game._set_grid_zoom(0.085)
		await settle()
		for region in View.REGIONS:
			var scroll_to: Vector2 = region.center*game.get_cell_size()-game.grid_scroll.size*0.5
			game.grid_scroll.scroll_horizontal = roundi(scroll_to.x)
			game.grid_scroll.scroll_vertical = roundi(scroll_to.y)
			game.grid_view.queue_redraw()
			await settle()
			var frame := root.get_texture().get_image()
			assert(frame.get_size()==Vector2i(width,roundi(width*9.0/16.0)),"Actual capture dimensions verified")
			frame.save_png(OUT+"%s-%d.png" % [region.biome,width])
	var live = game.grid_view.seabed_background.sub_biomes
	assert(live.textures.size()==View.DEFINITIONS.size()*3 and live.props==view.props,"Native station consumes complete stable library")
	var positions: Array = live.props.duplicate(true)
	game.grid_view.queue_redraw()
	await settle()
	assert(live.props==positions,"Redraw cannot move habitat props")
	var paths := [game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	print("SUB-BIOMES PASS: %d textures, stable props, blend mask, native asset sheets, %d habitats at three verified resolutions, station layering" % [view.textures.size(),View.DEFINITIONS.size()])
	quit()
